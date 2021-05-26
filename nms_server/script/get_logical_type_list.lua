local result = {}

local logicalList = redis.call('keys', 'l_server*:info')
for i,logical in ipairs(logicalList) do
    local type = redis.call('hget', logical, 'type')
    table.insert(result, type)
end

return cjson.encode(result)