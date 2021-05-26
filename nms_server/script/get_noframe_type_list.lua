local physicalTypeList = redis.call('SMEMBERS', 'p_server:noframetype')
return cjson.encode(physicalTypeList)