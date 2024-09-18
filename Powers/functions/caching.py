from time import perf_counter

from cachetools import TTLCache


class CACHE:
    ani_info = TTLCache(maxsize=10000, ttl=(60 * 10), timer=perf_counter) #will store as dict query: {info: info str, des: description}

    query_id = dict() #{id: query, query: id}

    results = dict() #{query: {page: results}}

    ep_kb = TTLCache(maxsize=10000, ttl=(60 * 10), timer=perf_counter) #{ani_id: {page: ikm}}

    ani_chars = TTLCache(maxsize=10000, ttl=(60 * 10), timer=perf_counter) #{query: char}