local ServerInfo = {}
local KeyInfo = 'p_server:' .. ARGV[1] .. ':info'
if redis.call('EXISTS', KeyInfo) == 1 then 
	--Get server info
	local MachineRoomMoid = redis.call('HGET',KeyInfo,'machine_room_moid')
	local Type       = redis.call('HGET',KeyInfo,'type') or ""
	local Name       = redis.call('HGET',KeyInfo,'name') or ""
	local Location   = redis.call('HGET',KeyInfo,'location') or ""
	local IP         = redis.call('HGET',KeyInfo,'ip') or ""
	local CardPos    = redis.call('HGET',KeyInfo,'card_pos') or ""

	--Get server resource info 
	local KeyResource = 'p_server:' .. ARGV[1] .. ':resource'
	local CPU = redis.call('HGET', KeyResource, 'cpu') or 0
	local Disk = redis.call('HGET', KeyResource, 'disk_total_userate') or 0
	local Memory = redis.call('HGET', KeyResource, 'memory') or 0
	local PortIn = redis.call('HGET', KeyResource, 'portin') or 0
	local PortOut = redis.call('HGET', KeyResource, 'portout') or 0
	
	ServerInfo['cpu'] = CPU
	ServerInfo['disk'] = Disk
	ServerInfo['memory'] = Memory
	ServerInfo['portin'] = PortIn
	ServerInfo['portout'] = PortOut

	--Get server online state
	local KeyOnline = 'p_server:' .. ARGV[1] .. ':online'
	local Online = redis.call('GET',KeyOnline)
	if( not Online ) then
		Online = 'offline'
	end

	--Get server warning info
	local KeyWarning = 'p_server:' .. ARGV[1] .. ':warning'
	local WarningList = redis.call('HGETALL',KeyWarning)
	local hasCritical = false
	local hasImportant = false
	local hasNormal = false
	for i = 2,table.getn(WarningList),2 do
		if WarningList[i] == 'critical' then
			hasCritical = true
		elseif WarningList[i] == 'important' then
			hasImportant = true
		elseif WarningList[i] == 'normal' then
			hasNormal = true
		end
	end

	local WarningLevel = ''
	if hasCritical then
		WarningLevel = 'critical'
	elseif hasImportant then 
		WarningLevel = 'important'
	elseif hasNormal then 
		WarningLevel = 'normal'
	end

	local MachineRoomKey = "machine_room:"..MachineRoomMoid..":info"
	local DomainMoid = redis.call("HGET", MachineRoomKey, "domain_moid") or ""
	local MachineRoomName = redis.call("HGET", MachineRoomKey, "name") or ""

	local DomainKey = "domain:"..DomainMoid..":info"
	local DomainName = redis.call("HGET", DomainKey, "name")

    -- Format server info object

	ServerInfo['success'] = 1
	ServerInfo['moid'] = ARGV[1]
	ServerInfo['guid'] = ARGV[1]
	ServerInfo['machine_room_moid'] = MachineRoomMoid
	ServerInfo['domain_moid'] = DomainMoid
	ServerInfo['machine_room_name'] = MachineRoomName
	ServerInfo['domain_name'] = DomainName
	ServerInfo['name'] = Name
	ServerInfo['type'] = Type
	ServerInfo['location'] = Location
	ServerInfo['ip'] = IP
	ServerInfo['card_pos'] = CardPos
	ServerInfo['warning_level'] = WarningLevel
	ServerInfo['online'] = Online
else
	ServerInfo['success'] = 0
	ServerInfo['error_code'] = 20404
end

local KeyPLR = 'p_server:'..ARGV[1]..':packet_loss_rate'
if redis.call('EXISTS', KeyPLR) == 1 then
	ServerInfo['send_loss_rate'] = redis.call('HGET', KeyPLR, 'send_loss_rate') or 0
	ServerInfo['recv_loss_rate'] = redis.call('HGET', KeyPLR, 'recv_loss_rate') or 0
end

return cjson.encode(ServerInfo)
