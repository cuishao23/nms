local Moid = ARGV[1]

local Type = ""
local KeyMachineRoomInfo = "machine_room:" .. Moid .. ":info"

-- 获取Moid的类型
if 1 == redis.call('EXISTS', KeyMachineRoomInfo) then
    Type = "machine_room"
else
    Type = redis.call("HGET","domain:" .. Moid .. ":info","type") or ""
end

local get_machine_room
get_machine_room = function(Moid, Result)
    local KeyInfo = "domain:"..Moid..":info"
    local DomainType = redis.call("HGET", KeyInfo, "type")

    if DomainType == "platform" then
        local MachineRoomKey = "domain:"..Moid..":machine_room"
        local MachineRoomList = redis.call("SMEMBERS", MachineRoomKey)
        for i=1,#MachineRoomList do
            local Item = {}
            Item["domain_moid"] = Moid
            Item["machine_room_moid"] = MachineRoomList[i]
            Result[#Result + 1] = Item
        end
    elseif DomainType == "kernel" or DomainType == "service" then
        local SubKey = "domain:"..Moid..":sub"
        local SubList = redis.call("SMEMBERS", SubKey)
        for i=1,#SubList do
            get_machine_room(SubList[i], Result)
        end
    end
end

local get_physicals = function(MachineRoomList, Result)
    for i=1,#MachineRoomList do
        local PhysicalListKey = "machine_room:"..MachineRoomList[i]["machine_room_moid"]..":p_server"
        local PhysicalList = redis.call("SMEMBERS", PhysicalListKey)
        for j=1,#PhysicalList do
            local KeyInfo = "p_server:"..PhysicalList[j]..":info"

            if redis.call('EXISTS', KeyInfo) == 1 then
                --Get server info
                local MachineRoomMoid = redis.call('HGET',KeyInfo,'machine_room_moid') or ""
                local Type       = redis.call('HGET',KeyInfo,'type') or ""
                local Name       = redis.call('HGET',KeyInfo,'name') or ""
                local Location   = redis.call('HGET',KeyInfo,'location') or ""
                local IP         = redis.call('HGET',KeyInfo,'ip') or ""
                local CardPos    = redis.call('HGET',KeyInfo,'card_pos') or ""

                --Get server resource info 
                local KeyResource = 'p_server:' .. PhysicalList[j] .. ':resource'
                local CPU     = redis.call('HGET',KeyResource,'cpu') or 0
                local Disk    = redis.call('HGET',KeyResource,'disk_total_userate') or 0
                local Memory  = redis.call('HGET',KeyResource,'memory') or 0
                local PortIn  = redis.call('HGET',KeyResource,'portin') or 0
                local PortOut = redis.call('HGET',KeyResource,'portout') or 0

                --Get server online state
                local KeyOnline = 'p_server:' .. PhysicalList[j] .. ':online'
                local Online = redis.call('GET',KeyOnline)
                if( not Online ) then
                    Online = 'offline'
                end

                --Get server warning info
                local KeyWarning = 'p_server:' .. PhysicalList[j] .. ':warning'
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
            
                -- Format server info object
                local ServerInfo = {}
                ServerInfo['moid'] = PhysicalList[j]
                ServerInfo['guid'] = PhysicalList[j]
                ServerInfo['domain_moid'] = ARGV[1]
                ServerInfo['machine_room_moid'] = MachineRoomMoid
                ServerInfo['name'] = Name
                ServerInfo['type'] = Type
                ServerInfo['location'] = Location
                ServerInfo['ip'] = IP
                ServerInfo['card_pos'] = CardPos
                ServerInfo['cpu'] = tostring(CPU)
                ServerInfo['portin'] = tostring(PortIn)
                ServerInfo['portout'] = tostring(PortOut)
                ServerInfo['disk'] = tostring(Disk)
                ServerInfo['memory'] = tostring(Memory)
                ServerInfo['warning_level'] = WarningLevel
                ServerInfo['online'] = Online
                Result[#Result + 1] = ServerInfo
            end
        end
    end
end

local MachineRoomList = {}

if Type == "user" then
    local MachineRoomMoid = redis.call('HGET', KeyInfo, 'machine_room_moid')
    local PlatformMoid = redis.call("HGET", 'machine_room:'..tostring(MachineRoomMoid)..':info', 'domain_moid') or ''
    local Item = {}
    Item["domain_moid"] = PlatformMoid
    Item["machine_room_moid"] = MachineRoomMoid
    MachineRoomList[#MachineRoomList + 1] = Item
elseif Type == "machine_room" then
    local PlatformMoid = redis.call("HGET", 'machine_room:'..tostring(Moid)..':info', 'domain_moid') or ''
    local Item = {}
    Item["domain_moid"] = PlatformMoid
    Item["machine_room_moid"] = Moid
    MachineRoomList[#MachineRoomList + 1] = Item
else
    get_machine_room(Moid, MachineRoomList)
end

-- 机房列表为空,返回错误
if next(MachineRoomList) == nil then
    local Result = {}
    Result["success"] = 0
    Result["err_str"] = "machine_room list empty"
    Result["error_code"] = 123456
    return cjson.encode(Result)
end

local Physicals = {}
get_physicals(MachineRoomList, Physicals)
if next(Physicals) == nil then
    local Result = {}
    Result["success"] = 0
    Result["err_str"] = "physicals list empty"
    Result["error_code"] = 123456
    return cjson.encode(Result)
end

local Result = {}
Result["success"] = 1
Result["physicals"] = Physicals

return cjson.encode(Result)