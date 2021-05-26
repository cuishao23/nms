local physicalTypeList = redis.call('SMEMBERS', 'p_server:frametype')
return cjson.encode(physicalTypeList)