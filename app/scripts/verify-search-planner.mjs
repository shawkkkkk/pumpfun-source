import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from '@babel/parser';
import { openCorpus, findNodes, exactlyOne, member, propertyName, literal, objectProperty, sha256 } from './original-contracts/source.mjs';

export const APP_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const ADAPTER = 'reconstruction/search-planner/planner.mjs';
export const PROOF = 'reconstruction/search-planner/PROVENANCE.json';
const HOOK_SOURCES = ['evidence/web/objects/dba17a249156c6ff.js', 'evidence/web/objects/767cc801e3f88f8b.js'];
const ignore = new Set(['start', 'end', 'loc', 'extra', 'leadingComments', 'trailingComments', 'innerComments']);
const expect = (condition, label) => { if (!condition) throw new Error(`unqualified planner structure: ${label}`); };
const functionType = (node) => ['FunctionExpression', 'ArrowFunctionExpression'].includes(node?.type);
const declarations = (node) => findNodes(node, (child) => child.type === 'VariableDeclarator' && child.id.type === 'Identifier');
const declared = (node, name) => exactlyOne(declarations(node).filter((child) => child.id.name === name), `declaration ${name}`).init;
function difference(left, right, location = '') {
  if (left === right) return null;
  if (!left || !right || typeof left !== 'object' || typeof right !== 'object') return `${location}: ${JSON.stringify(left)} != ${JSON.stringify(right)}`;
  for (const key of new Set([...Object.keys(left), ...Object.keys(right)])) {
    const found = difference(left[key], right[key], `${location}.${key}`);
    if (found) return found;
  }
  return null;
}

function patternRoles(pattern, prefix) {
  expect(pattern?.type === 'ObjectPattern', `${prefix} object pattern`);
  const roles = {};
  for (const property of pattern.properties) {
    expect(property.type === 'ObjectProperty' && !property.computed, `${prefix} property`);
    const value = property.value.type === 'AssignmentPattern' ? property.value.left : property.value;
    expect(value.type === 'Identifier', `${prefix} identifier`);
    roles[value.name] = `${prefix}:${propertyName(property.key)}`;
  }
  return roles;
}

// Bounded alpha comparison: retain operators, literal values, calls and order.
// Only lexical names, parentheses metadata, object shorthand and !0/!1 differ.
export function normalizePlanner(node, roles) {
  let counter = 0;
  const unresolved = new Set();
  function bind(pattern, scope) {
    if (pattern.type === 'Identifier') scope.set(pattern.name, `local:${counter++}`);
    else if (pattern.type === 'ObjectPattern') for (const property of pattern.properties) {
      expect(property.type === 'ObjectProperty' && !property.computed, 'local object binding');
      bind(property.value, scope);
    } else if (pattern.type === 'AssignmentPattern') bind(pattern.left, scope);
    else throw new Error(`unsupported local binding: ${pattern.type}`);
  }
  function identifier(name, scopes) {
    for (let i = scopes.length - 1; i >= 0; i--) if (scopes[i].has(name)) return scopes[i].get(name);
    if (!roles[name]) unresolved.add(name);
    return roles[name] ?? `UNRESOLVED:${name}`;
  }
  function visit(value, scopes = [], parent, key) {
    if (!value || typeof value !== 'object') return value;
    if (Array.isArray(value)) return value.map((child) => visit(child, scopes, parent, key));
    if (value.type === 'UnaryExpression' && value.operator === '!' && value.argument.type === 'NumericLiteral' && [0, 1].includes(value.argument.value)) {
      return { type: 'BooleanLiteral', value: !value.argument.value };
    }
    if (value.type === 'MemberExpression' && !value.computed && value.object.type === 'Identifier') {
      const role = identifier(value.object.name, scopes);
      const property = propertyName(value.property);
      if (role === 'import:148269' && property === 'E') return { type: 'Identifier', name: 'enum:sort' };
      if (role === 'import:231824' && property === 'f') return { type: 'Identifier', name: 'identity:request' };
    }
    if (value.type === 'SequenceExpression' && value.expressions.length === 2 && value.expressions[0].type === 'NumericLiteral' && value.expressions[0].value === 0) {
      const target = visit(value.expressions[1], scopes);
      expect(target.type === 'Identifier' && target.name === 'identity:request', 'unbound captured identity call');
      return target;
    }
    let current = scopes;
    if (functionType(value)) {
      const scope = new Map();
      for (const parameter of value.params) bind(parameter, scope);
      current = [...scopes, scope];
    } else if (value.type === 'BlockStatement') {
      const scope = new Map();
      for (const statement of value.body) if (statement.type === 'VariableDeclaration') {
        for (const declaration of statement.declarations) bind(declaration.id, scope);
      }
      current = [...scopes, scope];
    }
    if (value.type === 'Identifier') {
      const property = (key === 'key' && parent?.type === 'ObjectProperty' && !parent.computed) ||
        (key === 'property' && ['MemberExpression', 'OptionalMemberExpression'].includes(parent?.type) && !parent.computed);
      return { type: value.type, name: property ? value.name : identifier(value.name, current) };
    }
    const result = {};
    for (const [childKey, child] of Object.entries(value)) if (!ignore.has(childKey)) {
      result[childKey] = childKey === 'shorthand' && value.type === 'ObjectProperty' ? false : visit(child, current, value, childKey);
    }
    return result;
  }
  const canonical = visit(node);
  if (unresolved.size) throw new Error(`unresolved planner bindings: ${[...unresolved].join(', ')}`);
  return canonical;
}

function hookParts(factory) {
  const search = exactlyOne(findNodes(factory.node, (node) => node.type === 'ArrowFunctionExpression' && node.async &&
    findNodes(node, (child) => child.type === 'ObjectProperty' && propertyName(child.key) === 'route' && child.value.value === 'GET /coins/search-v2').length === 1), 'search callback');
  const call = exactlyOne(findNodes(search, (node) => node.type === 'CallExpression' && node.callee.type === 'Identifier' &&
    node.arguments[0]?.type === 'ObjectExpression' && node.arguments[0].properties.some((property) => propertyName(property.key) === 'useLocalFilterLimit')), 'query call');
  const query = declared(factory.node, call.callee.name).arguments[0];
  const outer = exactlyOne(findNodes(factory.node, (node) => node.type === 'FunctionExpression' &&
    node.body.start < search.start && node.body.end > search.end), 'owning hook');
  const roles = {};
  for (const statement of factory.node.body.body) if (statement.type === 'VariableDeclaration') {
    for (const declaration of statement.declarations) if (declaration.id.type === 'Identifier' && declaration.init?.type === 'CallExpression' &&
      member(declaration.init.callee, factory.runtime, 'i')) roles[declaration.id.name] = `import:${declaration.init.arguments[0].value}`;
  }
  const input = exactlyOne(findNodes(outer.body, (node) => node.type === 'VariableDeclarator' && node.id.type === 'ObjectPattern' &&
    node.init?.type === 'Identifier' && node.init.name === outer.params[0].name), 'hook inputs').id;
  Object.assign(roles, patternRoles(input, 'snapshot'));
  const helpers = query.body.body[0].declarations.filter((node) => node.init?.type === 'CallExpression');
  expect(helpers.length === 2, 'sort/order helper calls');
  const sortName = helpers[0].init.callee.name;
  const orderName = helpers[1].init.callee.name;
  roles[sortName] = 'helper:sort';
  roles[orderName] = 'helper:order';
  roles[call.callee.name] = 'helper:query';
  const sort = declared(outer.body, sortName).arguments[0];
  const order = declared(outer.body, orderName).arguments[0];
  const orderEnum = exactlyOne(findNodes(order, (node) => node.type === 'MemberExpression' && propertyName(node.property) === 'ASC'), 'order enum').object.name;
  roles[orderEnum] = 'enum:order';
  const orderDeclaration = exactlyOne(factory.node.body.body.flatMap((node) => node.type === 'VariableDeclaration' ? node.declarations : [])
    .filter((node) => node.id.type === 'Identifier' && node.id.name === orderEnum), 'top-level order enum').init;
  expect(orderDeclaration.type === 'SequenceExpression', 'order enum initialization');
  const values = orderDeclaration.expressions.filter((node) => node.type === 'AssignmentExpression' && node.left.type === 'MemberExpression');
  expect(JSON.stringify(values.map((node) => [propertyName(node.left.property), literal(node.right)])) === JSON.stringify([['ASC', 'ASC'], ['DESC', 'DESC']]), 'ASC/DESC values');
  const sessionWrite = exactlyOne(findNodes(query, (node) => node.type === 'AssignmentExpression' &&
    node.left.type === 'MemberExpression' && propertyName(node.left.property) === 'sessionId'), 'session query value');
  roles[sessionWrite.right.name] = 'snapshot:sessionId';
  const session = declared(outer.body, sessionWrite.right.name);
  expect(session.type === 'LogicalExpression' && session.operator === '??' && session.left.type === 'CallExpression' &&
    session.right.type === 'OptionalMemberExpression' && propertyName(session.right.property) === 'pump_session_id', 'session snapshot selection');
  const cookieCall = session.left.callee;
  expect(cookieCall.type === 'SequenceExpression' && cookieCall.expressions[0].value === 0 &&
    cookieCall.expressions[1].type === 'MemberExpression' && roles[cookieCall.expressions[1].object.name] === 'import:192' &&
    propertyName(cookieCall.expressions[1].property) === 'd', 'session cookie reader import');
  expect(search.body.body[4]?.type === 'ExpressionStatement' && search.body.body[4].expression.type === 'AwaitExpression', 'synchronous prefix boundary');
  return { search, query, sort, order, input, roles, session, orderDeclaration };
}

export async function verifyPlanner(root = APP_ROOT) {
  const corpus = await openCorpus(root);
  const bytes = await readFile(path.join(root, ADAPTER));
  const ast = parse(bytes.toString('utf8'), { sourceType: 'module' });
  const allowedExports = ['SEARCH_SORT', 'SEARCH_ORDER', 'mapSearchSort', 'mapSearchOrder', 'buildCoinSearchQuery', 'createCoinSearchPlanner', 'selectSearchSession'];
  expect(ast.program.body.length === allowedExports.length && ast.program.body.every((node) => node.type === 'ExportNamedDeclaration'), 'only bounded adapter exports, no top-level effects');
  const actualExports = ast.program.body.flatMap((node) => node.declaration.type === 'VariableDeclaration' ?
    node.declaration.declarations.map((entry) => entry.id.name) : [node.declaration.id.name]);
  expect(!difference(actualExports, allowedExports), 'bounded export set');
  const exported = (name) => {
    const entry = exactlyOne(ast.program.body.filter((node) => node.type === 'ExportNamedDeclaration' &&
      (node.declaration?.id?.name === name || node.declaration?.declarations?.some((item) => item.id.name === name))), `adapter export ${name}`).declaration;
    return entry.type === 'FunctionDeclaration' ? entry : exactlyOne(entry.declarations.filter((node) => node.id.name === name), name).init;
  };
  const sort = exported('mapSearchSort'), order = exported('mapSearchOrder'), query = exported('buildCoinSearchQuery');
  const creator = exported('createCoinSearchPlanner');
  expect([sort, order, query, creator, exported('selectSearchSession')].every((node) => !node.async && !node.generator), 'synchronous bounded adapters');
  expect(query.params.length === 3 && query.params[2].type === 'Identifier' &&
    JSON.stringify(query.params[1].properties.map((node) => [propertyName(node.key), node.value.type])) ===
      JSON.stringify(['limit', 'includeNsfw', 'creator', 'sessionId'].map((key) => [key, 'Identifier'])), 'query snapshot/identity parameters');
  expect(creator.body.body.length === 3 && creator.params.length === 2 && creator.params[1]?.type === 'Identifier' &&
    creator.body.body.slice(0, 2).every((node) => node.type === 'VariableDeclaration' && node.declarations.length === 1), 'snapshot factory has no ambient work');
  expect(JSON.stringify(creator.params[0].properties.map((node) => propertyName(node.key))) ===
    JSON.stringify(['sort', 'offset', 'limit', 'includeNsfw', 'order', 'creator', 'sessionId', 'useUnrestrictedSearch', 'includePerps']) &&
    creator.params[0].properties.slice(0, 7).every((node) => node.value.type === 'Identifier'), 'snapshot parameters have no new defaults');
  const snapshot = creator.body.body[0].declarations[0];
  expect(snapshot.init.type === 'ObjectExpression', 'query snapshot object');
  const snapshotRoles = patternRoles(creator.params[0], 'snapshot');
  expect(JSON.stringify(snapshot.init.properties.map((node) => [propertyName(node.key), snapshotRoles[node.value.name]])) ===
    JSON.stringify(['limit', 'includeNsfw', 'creator', 'sessionId'].map((name) => [name, `snapshot:${name}`])), 'snapshot copies captured values');
  const bound = creator.body.body[1].declarations[0];
  expect(bound.init.type === 'ArrowFunctionExpression' && bound.init.body.type === 'CallExpression' && bound.init.body.callee.name === 'buildCoinSearchQuery' &&
    bound.init.body.arguments.length === 3 && bound.init.body.arguments[0].name === bound.init.params[0].name &&
    bound.init.body.arguments[1].name === snapshot.id.name && bound.init.body.arguments[2].name === creator.params[1].name, 'identity capability wiring');
  const plan = creator.body.body[2].argument;
  expect(plan?.type === 'ArrowFunctionExpression' && !plan.async && plan.body.body.length === 5, 'planner prefix/return boundary');
  const returned = plan.body.body[4];
  const resultBindings = plan.body.body[3].declarations.map((entry) => entry.id.name);
  const filterBinding = exactlyOne(plan.params[0].properties.filter((entry) => propertyName(entry.key) === 'useLocalFiltering'), 'local-filter argument').value.left.name;
  expect(returned.type === 'ReturnStatement' && returned.argument.type === 'ObjectExpression' &&
    JSON.stringify(returned.argument.properties.map((entry) => [propertyName(entry.key), entry.value.name])) ===
      JSON.stringify([['request', resultBindings[0]], ['reportSearchSettled', resultBindings[1]], ['settledSearchTerm', resultBindings[2]], ['useLocalFiltering', filterBinding]]), 'descriptor return wiring');
  const roles = { SEARCH_SORT: 'enum:sort', SEARCH_ORDER: 'enum:order', mapSearchSort: 'helper:sort', mapSearchOrder: 'helper:order',
    ...patternRoles(query.params[1], 'snapshot'), [query.params[2].name]: 'identity:request' };
  const proofs = [];
  for (const source of HOOK_SOURCES) {
    const factory = await corpus.factory(379705, { source });
    const original = hookParts(factory);
    const sourceQueryRoles = { ...original.roles, ...patternRoles(original.query.params[0], 'query') };
    const adapterQueryRoles = { ...roles, ...patternRoles(query.params[0], 'query') };
    expect(!difference(normalizePlanner(original.query.params[0], sourceQueryRoles), normalizePlanner(query.params[0], adapterQueryRoles)), 'query argument defaults');
    expect(!difference(normalizePlanner(original.search.params[0], { ...original.roles, ...patternRoles(original.search.params[0], 'request') }),
      normalizePlanner(plan.params[0], { ...roles, ...patternRoles(plan.params[0], 'request') })), 'search argument defaults');
    for (const name of ['useUnrestrictedSearch', 'includePerps']) {
      const sourceInput = exactlyOne(original.input.properties.filter((entry) => propertyName(entry.key) === name), name).value;
      const adapterInput = exactlyOne(creator.params[0].properties.filter((entry) => propertyName(entry.key) === name), name).value;
      expect(sourceInput.type === 'AssignmentPattern' && adapterInput.type === 'AssignmentPattern' &&
        literal(sourceInput.right) === false && literal(adapterInput.right) === false, `${name} defaults false`);
    }
    const comparisons = [
      ['sort', original.sort.body, { ...original.roles, [original.sort.params[0].name]: 'argument:sort' }, sort.body, { ...roles, [sort.params[0].name]: 'argument:sort' }],
      ['order', original.order.body, { ...original.roles, [original.order.params[0].name]: 'argument:sort', [original.order.params[1].name]: 'argument:order' }, order.body,
        { ...roles, [order.params[0].name]: 'argument:sort', [order.params[1].name]: 'argument:order' }],
      ['query', original.query.body, { ...original.roles, ...patternRoles(original.query.params[0], 'query') }, query.body,
        { ...roles, ...patternRoles(query.params[0], 'query') }],
      ['requestPrefix', { type: 'BlockStatement', body: original.search.body.body.slice(0, 4), directives: [] },
        { ...original.roles, ...patternRoles(original.search.params[0], 'request') },
        { type: 'BlockStatement', body: plan.body.body.slice(0, 4), directives: [] },
        { ...roles, ...snapshotRoles, [bound.id.name]: 'helper:query', ...patternRoles(plan.params[0], 'request') }],
    ];
    for (const [label, sourceNode, sourceRoles, adaptedNode, adaptedRoles] of comparisons) {
      const expected = normalizePlanner(sourceNode, sourceRoles);
      const actual = normalizePlanner(adaptedNode, adaptedRoles);
      expect(!difference(expected, actual), `${label} AST differs from ${factory.provenance.sha256}: ${difference(expected, actual)}`);
      const range = label === 'requestPrefix' ? { start: original.search.body.body[0].start, end: original.search.body.body[3].end } : sourceNode;
      proofs.push({ ...factory.witness(range, label), normalizedSha256: sha256(JSON.stringify(expected)),
        bindings: Object.fromEntries(Object.entries(sourceRoles).sort(([a], [b]) => a.localeCompare(b))) });
    }
    proofs.push(factory.witness(original.session, 'render-time cookie/provider session selection'));
    proofs.push(factory.witness(original.orderDeclaration, 'captured ASC/DESC declaration'));
  }
  const helperSources = [[148269, 'evidence/web/objects/11cf0bf8a734ea43.js'], [192, 'evidence/web/objects/1e479323ffe53c14.js'],
    [231824, 'evidence/web/objects/3740fc4e7a24596d.js'], [231824, 'evidence/web/objects/cf2bb278631744da.js'],
    [886813, 'evidence/web/objects/01ad4f413e529b60.js']];
  for (const [id, source] of helperSources) proofs.push((await corpus.factory(id, { source })).provenance);
  const enumFactory = await corpus.factory(148269, { source: helperSources[0][1] });
  const enumDeclaration = exactlyOne(enumFactory.node.body.body.flatMap((node) => node.type === 'VariableDeclaration' ? node.declarations : [])
    .filter((entry) => entry.init?.type === 'SequenceExpression'), 'sort enum declaration');
  const enumValues = Object.fromEntries(enumDeclaration.init.expressions.filter((entry) => entry.type === 'AssignmentExpression')
    .map((entry) => { expect(entry.left.type === 'MemberExpression' && entry.operator === '=', 'sort enum field');
      return [propertyName(entry.left.property), literal(entry.right)]; }));
  const enumExport = exactlyOne(findNodes(enumFactory.node, (node) => node.type === 'CallExpression' && member(node.callee, enumFactory.runtime, 's') &&
    node.arguments[0]?.type === 'ArrayExpression' && node.arguments[0].elements.some((entry) => entry?.value === 'E')), 'sort export registration').arguments[0].elements;
  const getter = enumExport[enumExport.findIndex((entry) => entry?.value === 'E') + 1];
  expect(getter.type === 'ArrowFunctionExpression' && getter.body.name === enumDeclaration.id.name, 'sort import E getter');
  for (const [name, expected] of [['SEARCH_SORT', enumValues], ['SEARCH_ORDER', { ASC: 'ASC', DESC: 'DESC' }]]) {
    const value = exported(name);
    expect(value.type === 'CallExpression' && member(value.callee, 'Object', 'freeze') && value.arguments[0]?.type === 'ObjectExpression', `${name} literal`);
    const actual = Object.fromEntries(value.arguments[0].properties.map((entry) => [propertyName(entry.key), literal(entry.value)]));
    expect(!difference(expected, actual), `${name} declared values`);
  }
  const sessionAdapter = exported('selectSearchSession');
  expect(sessionAdapter.params.length === 2 && sessionAdapter.body.body.length === 1 && sessionAdapter.body.body[0].type === 'ReturnStatement', 'pure session selector');
  const selection = sessionAdapter.body.body[0].argument;
  expect(selection.type === 'LogicalExpression' && selection.operator === '??' && selection.left.name === sessionAdapter.params[0].name &&
    selection.right.type === 'OptionalMemberExpression' && selection.right.object.name === sessionAdapter.params[1].name &&
    propertyName(selection.right.property) === 'pump_session_id', 'nullish cookie/provider selection');
  const provider = await corpus.javascript('evidence/web/objects/b677d332af92b7f5.js');
  const providerNode = exactlyOne(provider.factories.filter((entry) => entry.ids.includes(293205)), 'physical nested session provider').node;
  proofs.push(provider.witness(providerNode, 'session-data boundary, not implemented'));
  return { schemaVersion: 1, manifestSha256: corpus.anchors.manifestSha256, adapterSha256: sha256(bytes), proofs,
    comparison: 'Exact selected ASTs after lexical renaming, resolved import references, object shorthand and !0/!1 normalization; captured JavaScript is never evaluated',
    identityPort: { call: 'unbound getRequestIdentity(sessionId)', when: 'once during a nonempty query, before creator/charity fields and request descriptor',
      result: 'destructure deviceId only; callback must model any original unused-field effects/errors it needs',
      exceptions: 'propagate unchanged; no real cookie/storage provider supplied' },
    limits: ['No active runtime candidate selected.', 'No React hook lifecycle, fetch, filtering, cache, pagination execution or analytics callback implemented.',
      'Session snapshot inputs and identity capability are supplied by the caller; cookie/storage/provider implementations remain outside this unit.'] };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const mode = process.argv[2];
    if (!['--write', '--check'].includes(mode) || process.argv.length !== 3) throw new Error('usage: node scripts/verify-search-planner.mjs --write|--check');
    const proof = JSON.stringify(await verifyPlanner(), null, 2) + '\n';
    if (mode === '--write') { await mkdir(path.dirname(path.join(APP_ROOT, PROOF)), { recursive: true }); await writeFile(path.join(APP_ROOT, PROOF), proof); }
    else expect(await readFile(path.join(APP_ROOT, PROOF), 'utf8') === proof, 'saved provenance differs');
    console.log('Search planner: both physical candidates match the bounded adapter; no captured code executed.');
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
