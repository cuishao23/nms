local ServerList = {}
local LogicalKey = 'p_server:' .. ARGV[1] .. ':l_server'
local LogicalServerList = redis.call('SMEMBERS', LogicalKey)
for i = 1, table.getn(LogicalServerList) do
	local KeyInfo = 'l_server:' .. LogicalServerList[i] .. ':info'
	local ServerInfo = {}
	ServerInfo['moid'] = redis.call('HGET',KeyInfo,'moid') or ""
	ServerInfo['type'] = redis.call('HGET',KeyInfo,'type') or ""
	ServerInfo['name'] = redis.call('HGET',KeyInfo,'name') or ""
	table.insert(ServerList,ServerInfo)
end

return cjson.encode(ServerList)