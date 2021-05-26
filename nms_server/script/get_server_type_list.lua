local PhysicalTypeList = redis.call('SMEMBERS', 'p_server:type')
local LogicalTypeList = redis.call('SMEMBERS', 'l_server:type')

for i = 1,table.getn(LogicalTypeList) do
	table.insert(PhysicalTypeList,LogicalTypeList[i])
end

return cjson.encode(PhysicalTypeList)