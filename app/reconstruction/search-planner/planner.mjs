// Original-backed synchronous request planning. No fetch, browser-global access,
// session creation, cookie/storage write, or default identity provider.
export const SEARCH_SORT = Object.freeze({
  CALLS: 'calls', CHARITY: 'charity', CLOSEST_MATCH: 'relevance',
  CUSTOM_PAIRS: 'custom_pairs', FEATURED: 'featured', LIVE: 'live',
  MAJORS: 'majors', MARKET_CAP: 'market_cap', NEWEST: 'created_timestamp',
  OLDEST: 'oldest_coins', STOCKS: 'stocks', TOP: 'top',
  TRADE: 'last_trade_timestamp', TRENDING: 'trending',
});
export const SEARCH_ORDER = Object.freeze({ ASC: 'ASC', DESC: 'DESC' });

export const mapSearchSort = (sort) => sort
  ? sort === SEARCH_SORT.FEATURED || sort === SEARCH_SORT.CHARITY ||
    sort === SEARCH_SORT.CUSTOM_PAIRS || sort === SEARCH_SORT.LIVE ||
    sort === SEARCH_SORT.CALLS || sort === SEARCH_SORT.TRENDING ||
    sort === SEARCH_SORT.STOCKS || sort === SEARCH_SORT.MAJORS
    ? SEARCH_SORT.MARKET_CAP
    : sort === SEARCH_SORT.OLDEST ? SEARCH_SORT.NEWEST : sort
  : sort;

export const mapSearchOrder = (sort, order) =>
  sort === SEARCH_SORT.NEWEST && order ? order :
    sort === SEARCH_SORT.OLDEST ? SEARCH_ORDER.ASC : SEARCH_ORDER.DESC;

export function buildCoinSearchQuery(
  { offset, order, searchTerm, sort, useLocalFilterLimit = false },
  { limit, includeNsfw, creator, sessionId },
  getRequestIdentity,
) {
  let querySort = mapSearchSort(sort),
    queryOrder = mapSearchOrder(sort, order),
    query = {
      offset: offset || 0,
      limit: useLocalFilterLimit ? 100 : limit,
      ...(querySort ? { sort: querySort } : {}),
      includeNsfw,
      order: queryOrder,
    };
  if (searchTerm) {
    query.searchTerm = searchTerm;
    let { deviceId } = getRequestIdentity(sessionId);
    (deviceId && (query.deviceId = deviceId), sessionId && (query.sessionId = sessionId));
  }
  return (
    creator && (query.creator = creator),
    sort === SEARCH_SORT.CHARITY && (query.isCharity = true),
    query
  );
}

// Call this when the caller captures a new render/input snapshot. Planning
// closes over those values; later mutation of the input object does not replace
// them. The identity callback is invoked unbound only for an actual search.
export function createCoinSearchPlanner(
  { sort, offset, limit, includeNsfw, order, creator, sessionId,
    useUnrestrictedSearch = false, includePerps = false },
  getRequestIdentity,
) {
  const querySnapshot = { limit, includeNsfw, creator, sessionId };
  const queryBuilder = (args) => buildCoinSearchQuery(args, querySnapshot, getRequestIdentity);
  return ({ searchTerm, useLocalFiltering = false }) => {
    if (!searchTerm?.trim()) return;
    let isCharity = sort === SEARCH_SORT.CHARITY,
      query = {
        ...queryBuilder({
          searchTerm,
          offset: useLocalFiltering ? 0 : offset,
          sort: isCharity ? SEARCH_SORT.MARKET_CAP : sort,
          order,
          useLocalFilterLimit: useLocalFiltering,
        }),
      };
    isCharity && (query.isCharity = true);
    let request = useUnrestrictedSearch
        ? { kind: 'client', route: 'GET /coins/search-unrestricted', query }
        : { kind: 'client', route: 'GET /coins/search-v2', query: includePerps ? { ...query, includePerps: true } : query },
      reportSearchSettled = useLocalFiltering || 0 === offset,
      settledSearchTerm = searchTerm.trim();
    return { request, reportSearchSettled, settledSearchTerm, useLocalFiltering };
  };
}

// Inputs are already-decoded caller data. Reading the original session cookie
// and obtaining SessionProvider state are deliberately outside this module.
export function selectSearchSession(cookieSessionId, sessionData) {
  return cookieSessionId ?? sessionData?.pump_session_id;
}
