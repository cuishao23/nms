local get_machine_room_p_list = function(Moid, Result)
    local KeyServer = 'machine_room:' .. Moid .. ':p_server'
    local ServerMoidList = redis.call('SMEMBERS', KeyServer)
    for i = 1,table.getn(ServerMoidList) do
        local KeyInfo = 'p_server:' .. ServerMoidList[i] .. ':info'
        if redis.call('EXISTS', KeyInfo) == 1 then
            --Get server info
            local Type = redis.call('HGET',KeyInfo,'type') or ""
            local Name = redis.call('HGET',KeyInfo,'name') or ""
            local Version = redis.call('HGET',KeyInfo,'version') or ""

            --Get server online state
            local KeyOnline = 'p_server:' .. ServerMoidList[i] .. ':online'
            local Online = redis.call('GET',KeyOnline)
            if redis.call('GET',KeyOnline) and Version >= '6.1.0.2.0' then
                local KeyResource = 'p_server:' .. ServerMoidList[i] .. ':resource'
                local NetCardCount = redis.call('HGET',KeyResource,'netcard_count') or 0

                -- Get card name
                local NetCards = {}
                for i = 1, tonumber(NetCardCount) do
                    local NameKey = "netcard" .. i .. "_name"
                    local CardName = redis.call('HGET',KeyResource,NameKey)
                    table.insert(NetCards,CardName)
                end

                local ServerInfo = {}
                ServerInfo['moid'] = ServerMoidList[i]
                ServerInfo['machine_room_moid'] = Moid
                ServerInfo['name'] = Name
                ServerInfo['type_ser'] = Type
                ServerInfo['netcards'] = NetCards
                table.insert(Result,ServerInfo)
            end
        end
    end
end

local get_platform_domain_p_list = function(Moid, Result)
    --获取域所属机房列表
    local DomainMachineListKey = 'domain:' .. Moid .. ':machine_room'
    local MachineRoomMoidList = redis.call('SMEMBERS', DomainMachineListKey)
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
    local SubKey = 'domain:'..DomainMoid..':sub'
    local PlatformDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(PlatformDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(PlatformDomainList) do

        local KeyDomain = 'domain:' .. PlatformDomainList[i] .. ':info'
        local DomainType = redis.call('HGET',KeyDomain,'type')

        if "platform" == DomainType then
            get_platform_domain_p_list(PlatformDomainList[i], Result)
        elseif "service" == DomainType then
            get_service_domain_p_list(PlatformDomainList[i], Result)
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