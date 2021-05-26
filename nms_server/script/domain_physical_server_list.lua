local get_machine_room_p_list = function(Moid, Result)
    local KeyServer = "machine_room:" .. Moid .. ":p_server"
    local ServerMoidList = redis.call("SMEMBERS", KeyServer)
    for i = 1, table.getn(ServerMoidList) do
        local KeyInfo = "p_server:" .. ServerMoidList[i] .. ":info"
        if redis.call("EXISTS", KeyInfo) == 1 then
            --Get server info
            local Type = redis.call("HGET", KeyInfo, "type") or ""
            local Name = redis.call("HGET", KeyInfo, "name") or ""
            local Location = redis.call("HGET", KeyInfo, "location") or ""
            local IP = redis.call("HGET", KeyInfo, "ip") or ""
            local CardPos = redis.call("HGET", KeyInfo, "card_pos") or ""
            local UpTime = redis.call("HGET", KeyInfo, "uptime") or ""
            local Belong_moid = redis.call("HGET", KeyInfo, "belong_moid") or ""
            local Belong_slot = redis.call("HGET", KeyInfo, "belong_slot") or ""
            local Is_frame = redis.call("HGET", KeyInfo, "is_frame") or ""

            --Get server resource info
            local KeyResource = "p_server:" .. ServerMoidList[i] .. ":resource"
            local CPU = redis.call("HGET", KeyResource, "cpu") or ""
            local Disk = redis.call("HGET", KeyResource, "disk1_age") or ""
            local Memory = redis.call("HGET", KeyResource, "memory") or ""
            local PortIn = redis.call("HGET", KeyResource, "portin") or ""
            local PortOut = redis.call("HGET", KeyResource, "portout") or ""

            --Get server online state
            local KeyOnline = "p_server:" .. ServerMoidList[i] .. ":online"
            local Online = redis.call("GET", KeyOnline)
            if (not Online) then
                Online = "offline"
            end

            --Get server warning info
            local KeyWarning = "p_server:" .. ServerMoidList[i] .. ":warning"
            local WarningList = redis.call("HGETALL", KeyWarning)
            local hasCritical = false
            local hasImportant = false
            local hasNormal = false
            for i = 2, table.getn(WarningList), 2 do
                if WarningList[i] == "critical" then
                    hasCritical = true
                elseif WarningList[i] == "important" then
                    hasImportant = true
                elseif WarningList[i] == "normal" then
                    hasNormal = true
                end
            end

            local WarningLevel = ""
            if hasCritical then
                WarningLevel = "critical"
            elseif hasImportant then
                WarningLevel = "important"
            elseif hasNormal then
                WarningLevel = "normal"
            end

            -- if Online == "offline" then
            --     WarningLevel = ""
            -- end

            -- Format server info object
            local ServerInfo = {}
            ServerInfo["moid"] = ServerMoidList[i]
            ServerInfo["machine_room_moid"] = Moid
            ServerInfo["name"] = Name
            ServerInfo["type_ser"] = Type
            ServerInfo["location"] = Location
            ServerInfo["ip"] = IP
            ServerInfo["card_pos"] = CardPos
            ServerInfo["cpu"] = CPU
            ServerInfo["portin"] = PortIn
            ServerInfo["portout"] = PortOut
            ServerInfo["disk"] = Disk
            ServerInfo["memory"] = Memory
            ServerInfo["warning_level"] = WarningLevel
            ServerInfo["online"] = Online
            ServerInfo["uptime"] = UpTime
            ServerInfo["belong_moid"] = Belong_moid
            ServerInfo["belong_slot"] = Belong_slot
            ServerInfo["is_frame"] = Is_frame

            -- 在线设备排在前面
            if Online == 'online' then
                table.insert(Result,1,ServerInfo)
            else
                table.insert(Result,ServerInfo)
            end
        end
    end
end

local get_platform_domain_p_list = function(Moid, Result)
    --获取域所属机房列表
    local DomainMachineListKey = "domain:" .. Moid .. ":machine_room"
    local MachineRoomMoidList = redis.call("SMEMBERS", DomainMachineListKey)
    if table.getn(MachineRoomMoidList) <= 0 then
        return
    end

    --获取机房详细信息
    for i = 1, table.getn(MachineRoomMoidList) do
        get_machine_room_p_list(MachineRoomMoidList[i], Result)
    end
end

local get_service_domain_p_list
get_service_domain_p_list = function(DomainMoid, Result)
    local SubKey = "domain:" .. DomainMoid .. ":sub"
    local SubDomainList = redis.call("SMEMBERS", SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do
        local KeyDomain = "domain:" .. SubDomainList[i] .. ":info"
        local DomainType = redis.call("HGET", KeyDomain, "type")

        if "platform" == DomainType then
            get_platform_domain_p_list(SubDomainList[i], Result)
        elseif "service" == DomainType then
            get_service_domain_p_list(SubDomainList[i], Result)
        end
    end
end

local Result = {}
local KeyDomain = "domain:" .. ARGV[1] .. ":info"

if redis.call("EXISTS", KeyDomain) == 1 then
    local DomainType = redis.call("HGET", KeyDomain, "type")

    if "platform" == DomainType then
        get_platform_domain_p_list(ARGV[1], Result)
    elseif "kernel" == DomainType or "service" == DomainType then
        get_service_domain_p_list(ARGV[1], Result)
    elseif "user" == DomainType then
        local machine_room_moid = redis.call('HGET',KeyDomain,'machine_room_moid') or ''
        get_machine_room_p_list(machine_room_moid, Result)
    end
elseif redis.call("EXISTS", "machine_room:" .. ARGV[1] .. ":info") == 1 then
    get_machine_room_p_list(ARGV[1], Result)
end

return cjson.encode(Result)
