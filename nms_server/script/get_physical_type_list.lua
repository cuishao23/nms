local physicalTypeList = redis.call('SMEMBERS', 'p_server:type')
return cjson.encode(physicalTypeList)