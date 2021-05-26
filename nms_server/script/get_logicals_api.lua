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

local get_logicals = function(MachineRoomList, Result)
    for i=1,#MachineRoomList do
        local LogicalListKey = "machine_room:"..MachineRoomList[i]["machine_room_moid"]..":l_server"
        local LogicalList = redis.call("SMEMBERS", LogicalListKey)
        for j=1,#LogicalList do
            local KeyInfo = 'l_server:' .. LogicalList[i] .. ':info'
            if redis.call('EXISTS', KeyInfo) == 1 then
                local Type = redis.call('HGET', KeyInfo, 'type') or ""
                -- 由于DCS和VRS逻辑服务器归属的物理服务器的moid为空，顾屏蔽外设逻辑服务器的显示
        
                --Get server info
                local PServerMoid = redis.call('HGET', KeyInfo, 'p_server_moid') or ""
                local MachineRoomMoid = redis.call('HGET', KeyInfo, 'machine_room_moid') or ""
                local Name = redis.call('HGET', KeyInfo, 'name') or ""
                local BackupState = redis.call('HGET', KeyInfo, 'backup_state') or ""
        
                --此处为了兼容老的api, 老api根据mediaresource的moid获取端口资源, 5.2版本mediaresource不存在了,media-worker代替
                if Type == "media-worker" or Type == "mpu_jd2000" or Type == "mpu" then
                    Type = 'MEDIARESOURCE'
                end
        
                --Get ip info
                local IP
                if PServerMoid ~= '' then
                    local KeyPhysicalServer = 'p_server:' .. PServerMoid .. ':info'
                    IP = redis.call('HGET', KeyPhysicalServer, 'ip') or ""
                else
                    IP = ''
                end
        
                --Get server online state
                local KeyOnline = 'l_server:' .. LogicalList[i] .. ':online'
                local Online = redis.call('GET', KeyOnline)
                if (not Online) then
                    Online = 'offline'
                end
        
                --Get server warning info
                local KeyWarning = 'l_server:' .. LogicalList[i] .. ':warning'
                local WarningList = redis.call('HGETALL', KeyWarning)
                local hasCritical = false
                local hasImportant = false
                local hasNormal = false
                for i = 2, table.getn(WarningList), 2 do
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
                ServerInfo['moid'] = LogicalList[i]
                ServerInfo['guid'] = LogicalList[i]
                ServerInfo['p_server_moid'] = PServerMoid
                ServerInfo['domain_moid'] = ARGV[1]
                ServerInfo['machine_room_moid'] = MachineRoomMoid
                ServerInfo['name'] = Name
                ServerInfo['type'] = Type
                ServerInfo['backup_state'] = BackupState
                ServerInfo['ip'] = IP
                ServerInfo['warning_level'] = WarningLevel
                ServerInfo['online'] = Online
        
                table.insert(Result, ServerInfo)
            end
        end
    end
end

local MachineRoomList = {}

if Type == "user" then
    local MachineRoomMoid = redis.call('HGET', "domain:" .. Moid .. ":info", 'machine_room_moid')
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

local Logicals = {}
get_logicals(MachineRoomList, Logicals)
if next(Logicals) == nil then
    local Result = {}
    Result["success"] = 0
    Result["err_str"] = "logicals list empty"
    Result["error_code"] = 123456
    return cjson.encode(Result)
end

local Result = {}
Result["success"] = 1
Result["logicals"] = Logicals

return cjson.encode(Result)