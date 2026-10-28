import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtemp, mkdir, copyFile, readFile, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { SEARCH_SORT, SEARCH_ORDER, mapSearchSort, mapSearchOrder, buildCoinSearchQuery,
  createCoinSearchPlanner, selectSearchSession } from '../reconstruction/search-planner/planner.mjs';
import { APP_ROOT, ADAPTER, PROOF, verifyPlanner } from '../scripts/verify-search-planner.mjs';

const proof = JSON.parse(await readFile(path.join(APP_ROOT, PROOF), 'utf8'));
const context = { sort: SEARCH_SORT.MARKET_CAP, offset: 0, limit: 48, includeNsfw: false, order: 'DESC', creator: 'creator', sessionId: 'session' };
const identity = () => ({ deviceId: 'device' });

test('all captured sort values preserve their specific request mappings', () => {
  const mapped = new Set(['featured', 'charity', 'custom_pairs', 'live', 'calls', 'trending', 'stocks', 'majors']);
  for (const value of Object.values(SEARCH_SORT)) assert.equal(mapSearchSort(value), mapped.has(value) ? 'market_cap' : value === 'oldest_coins' ? 'created_timestamp' : value);
  for (const value of ['', undefined, null, 'unrecognized']) assert.equal(mapSearchSort(value), value);
  assert.deepEqual(SEARCH_ORDER, { ASC: 'ASC', DESC: 'DESC' });
});

test('only newest preserves a truthy requested order; oldest is always ASC', () => {
  assert.equal(mapSearchOrder('created_timestamp', 'ASC'), 'ASC');
  assert.equal(mapSearchOrder('created_timestamp', 'custom'), 'custom');
  assert.equal(mapSearchOrder('created_timestamp', ''), 'DESC');
  assert.equal(mapSearchOrder('oldest_coins', 'DESC'), 'ASC');
  assert.equal(mapSearchOrder('market_cap', 'ASC'), 'DESC');
});

test('base query preserves raw terms and optional identity/creator values', () => {
  const calls = [];
  const query = buildCoinSearchQuery({ sort: 'oldest_coins', offset: 12, searchTerm: '  cat  ' }, context,
    function (session) { assert.equal(this, undefined); calls.push(session); return { deviceId: 'device' }; });
  assert.deepEqual(query, { offset: 12, limit: 48, sort: 'created_timestamp', includeNsfw: false, order: 'ASC',
    searchTerm: '  cat  ', deviceId: 'device', sessionId: 'session', creator: 'creator' });
  assert.deepEqual(calls, ['session']);
});

test('base query retains falsy offset behavior and own undefined fields without inventing validation', () => {
  for (const offset of [undefined, null, false, NaN, 0]) {
    const query = buildCoinSearchQuery({ offset }, {}, () => { throw Error('must not run'); });
    assert.equal(query.offset, 0);
    assert.equal(Object.hasOwn(query, 'limit'), true);
    assert.equal(Object.hasOwn(query, 'includeNsfw'), true);
    assert.equal(Object.hasOwn(query, 'sort'), false);
  }
  assert.equal(buildCoinSearchQuery({ offset: -1 }, {}, identity).offset, -1);
  assert.equal(buildCoinSearchQuery({ useLocalFilterLimit: true }, {}, identity).limit, 100);
});

test('empty search guard prevents identity calls and descriptor creation', () => {
  let calls = 0;
  const plan = createCoinSearchPlanner(context, () => { calls++; return {}; });
  for (const searchTerm of [undefined, null, '', ' \t\n']) assert.equal(plan({ searchTerm }), undefined);
  assert.equal(calls, 0);
});

test('charity planning, local filtering and restricted-only includePerps match the original prefix', () => {
  const plan = createCoinSearchPlanner({ ...context, sort: 'charity', offset: 96, includePerps: true }, identity);
  const result = plan({ searchTerm: ' cat ', useLocalFiltering: true });
  assert.deepEqual(result, {
    request: { kind: 'client', route: 'GET /coins/search-v2', query: { offset: 0, limit: 100, sort: 'market_cap', includeNsfw: false,
      order: 'DESC', searchTerm: ' cat ', deviceId: 'device', sessionId: 'session', creator: 'creator', isCharity: true, includePerps: true } },
    reportSearchSettled: true, settledSearchTerm: 'cat', useLocalFiltering: true,
  });
  const unrestricted = createCoinSearchPlanner({ ...context, useUnrestrictedSearch: true, includePerps: true }, identity)({ searchTerm: 'cat' });
  assert.equal(unrestricted.request.route, 'GET /coins/search-unrestricted');
  assert.equal(Object.hasOwn(unrestricted.request.query, 'includePerps'), false);
});

test('settled-report condition uses original strict zero rather than the coerced query offset', () => {
  const result = createCoinSearchPlanner({ ...context, offset: undefined }, identity)({ searchTerm: 'cat' });
  assert.equal(result.request.query.offset, 0);
  assert.equal(result.reportSearchSettled, false);
  assert.equal(createCoinSearchPlanner(context, identity)({ searchTerm: 'cat' }).reportSearchSettled, true);
});

test('planner captures input values once rather than following later context mutation', () => {
  const snapshot = { ...context };
  const calls = [];
  const plan = createCoinSearchPlanner(snapshot, (session) => { calls.push(session); return { deviceId: 'device' }; });
  Object.assign(snapshot, { limit: 999, creator: 'other', sessionId: 'other', sort: 'oldest_coins' });
  const result = plan({ searchTerm: 'cat' });
  assert.equal(result.request.query.limit, 48);
  assert.equal(result.request.query.creator, 'creator');
  assert.equal(result.request.query.sort, 'market_cap');
  assert.deepEqual(calls, ['session']);
});

test('identity port stays unbound, runs between trim calls and destructures deviceId before returning', () => {
  const events = [];
  let trimCalls = 0;
  const term = { trim() { events.push('trim'); return ++trimCalls === 1 ? 'present' : 'settled'; } };
  const plan = createCoinSearchPlanner(context, function (session) {
    assert.equal(this, undefined);
    events.push(`identity:${session}`);
    return { get deviceId() { events.push('deviceId'); return 'device'; } };
  });
  const result = plan({ searchTerm: term });
  assert.deepEqual(events, ['trim', 'identity:session', 'deviceId', 'trim']);
  assert.equal(result.request.query.searchTerm, term);
  assert.equal(result.settledSearchTerm, 'settled');
});

test('identity failures and invalid results propagate without a synthetic fallback', () => {
  const failure = new Error('synthetic identity failure');
  assert.throws(() => createCoinSearchPlanner(context, () => { throw failure; })({ searchTerm: 'cat' }), (error) => error === failure);
  assert.throws(() => createCoinSearchPlanner(context, () => null)({ searchTerm: 'cat' }), TypeError);
  assert.throws(() => createCoinSearchPlanner(context, () => ({ get deviceId() { throw failure; } }))({ searchTerm: 'cat' }), (error) => error === failure);
  const query = createCoinSearchPlanner({ ...context, creator: '', sessionId: undefined }, () => ({}))({ searchTerm: 'cat' }).request.query;
  assert.equal(Object.hasOwn(query, 'creator'), false);
  assert.equal(Object.hasOwn(query, 'deviceId'), false);
  assert.equal(Object.hasOwn(query, 'sessionId'), false);
});

test('session selection preserves nullish precedence with no ambient cookie access', () => {
  let reads = 0;
  const provider = { get pump_session_id() { reads++; return 'provider'; } };
  for (const cookie of ['', false, 0, 'cookie']) assert.equal(selectSearchSession(cookie, provider), cookie);
  assert.equal(reads, 0);
  assert.equal(selectSearchSession(undefined, provider), 'provider');
  assert.equal(selectSearchSession(null, provider), 'provider');
  assert.equal(selectSearchSession(undefined, null), undefined);
  assert.equal(reads, 2);
});

test('both physical source candidates reproduce every bounded AST and exact saved proof', async () => {
  assert.deepEqual(await verifyPlanner(), proof);
  for (const label of ['sort', 'order', 'query', 'requestPrefix']) {
    const pair = proof.proofs.filter((entry) => entry.label === label);
    assert.equal(pair.length, 2);
    assert.equal(pair[0].normalizedSha256, pair[1].normalizedSha256);
    assert.notEqual(pair[0].source, pair[1].source);
  }
});

async function changedAdapter(t, edit) {
  const root = await mkdtemp(path.join(os.tmpdir(), 'search-planner-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const files = new Set(['evidence/web/manifest.json', 'recovered/modules.json', ADAPTER, ...proof.proofs.map((entry) => entry.source)]);
  for (const file of files) { await mkdir(path.dirname(path.join(root, file)), { recursive: true }); await copyFile(path.join(APP_ROOT, file), path.join(root, file)); }
  const target = path.join(root, ADAPTER);
  await writeFile(target, edit(await readFile(target, 'utf8')));
  return root;
}

test('source verifier rejects changed numeric behavior, identity receiver and unresolved free inputs', async (t) => {
  for (const edit of [
    (text) => text.replace('useLocalFilterLimit ? 100', 'useLocalFilterLimit ? 101'),
    (text) => text.replace('getRequestIdentity(sessionId)', '({ getRequestIdentity }).getRequestIdentity(sessionId)'),
    (text) => text.replace('creator && (query.creator = creator)', 'unresolvedInput && (query.creator = creator)'),
  ]) await assert.rejects(verifyPlanner(await changedAdapter(t, edit)), /AST differs|unresolved planner/);
});

test('source verifier rejects changed declared constants, defaults and descriptor wiring', async (t) => {
  for (const edit of [
    (text) => text.replace("MARKET_CAP: 'market_cap'", "MARKET_CAP: 'invented'"),
    (text) => text.replace('useLocalFilterLimit = false', 'useLocalFilterLimit = true'),
    (text) => text.replace('return { request, reportSearchSettled, settledSearchTerm, useLocalFiltering }', 'return {}'),
  ]) await assert.rejects(verifyPlanner(await changedAdapter(t, edit)), /declared values|defaults|return wiring/);
});
