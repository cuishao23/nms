local Key = "terminal_type_list"
local TypeList = redis.call("HGETALL",Key)

local ReturnData = {}
for i=1,table.getn(TypeList),2 do
	table.insert(ReturnData,TypeList[i+1])
end

return cjson.encode(ReturnData)