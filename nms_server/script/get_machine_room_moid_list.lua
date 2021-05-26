--获取机房列表
local get_machine_room_moid_list
get_machine_room_moid_list = function (DomainMoid, MachineRoomMoidList)
	--获取域所属机房列表
	local DomainMachineListKey = 'domain:' .. DomainMoid .. ':machine_room'
	local MacMoidList = redis.call('SMEMBERS', DomainMachineListKey)
	for i=1,table.getn(MacMoidList) do
		table.insert(MachineRoomMoidList,MacMoidList[i])
	end
end

local get_tree
get_tree = function(DomainMoid, MachineRoomMoidList)
    if DomainMoid == nil then
        return
    end

    local DomainMoidKey = 'domain:'..DomainMoid..':info'
    local DomainType    = redis.call('HGET',DomainMoidKey,'type')
    if "platform" == DomainType then
    	get_machine_room_moid_list(DomainMoid, MachineRoomMoidList)
    elseif "user" ~= DomainMoid then
	    local SubMoidKey = 'domain:' .. DomainMoid .. ':sub'
	    local SubMoidList = redis.call('SMEMBERS', SubMoidKey)

	    if table.getn(SubMoidList) > 0 then
	        for i = 1, table.getn(SubMoidList) do
	            get_tree(SubMoidList[i], MachineRoomMoidList)
	        end
	    end    	
    end
end

local Moid = ARGV[1]
local Type = ""
local KeyMachineRoomInfo = "machine_room:" .. Moid .. ":info"

-- 获取Moid的类型
if 1 == redis.call('EXISTS', KeyMachineRoomInfo) then
    Type = "machine_room"
else
    Type = redis.call("HGET","domain:" .. Moid .. ":info","type")
    if (not Type) then
        Type = ""
    end
end

local MachineRoomMoidList = {}
if Type == "machine_room" then
	table.insert(MachineRoomMoidList,Moid)
elseif Type == "user" then
	local MachineRoomMoid = redis.call("HGET","domain:" .. Moid .. ":info","machine_room_moid")
	table.insert(MachineRoomMoidList,MachineRoomMoid)
else
	get_tree(Moid, MachineRoomMoidList) 
end

return cjson.encode(MachineRoomMoidList)