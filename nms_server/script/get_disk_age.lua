local get_machine_room_p_list = function(Moid, Result)
    local KeyServer = 'machine_room:' .. Moid .. ':p_server'
    local ServerMoidList = redis.call('SMEMBERS', KeyServer)
    for i = 1,table.getn(ServerMoidList) do
        local KeyInfo = 'p_server:' .. ServerMoidList[i] .. ':info'
        if redis.call('EXISTS', KeyInfo) == 1 then
            --Get server info
            local Name = redis.call('HGET',KeyInfo,'name') or ""

            --Get server resource info
            local KeyResource = 'p_server:' .. ServerMoidList[i] .. ':resource'
            local DiskCount = redis.call('HGET',KeyResource,'disk_count') or 0

            local ServerInfo = {}
            ServerInfo['moid'] = ServerMoidList[i]
            ServerInfo['name'] = Name
            ServerInfo['disk_count'] = DiskCount

            for i = 1, DiskCount do
				local DiskName = redis.call('HGET',KeyResource,'disk' .. i .. '_name') or ''
				local DiskAge = redis.call('HGET',KeyResource,'disk' .. i .. '_age') or ''

				-- Format server resource object
				ServerInfo['disk' .. i .. '_name'] = DiskName
				ServerInfo['disk' .. i .. '_age'] = DiskAge
			end	

            table.insert(Result,ServerInfo)
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
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

        local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
        local DomainType = redis.call('HGET',KeyDomain,'type')

        if "platform" == DomainType then
            get_platform_domain_p_list(SubDomainList[i], Result)
        elseif "service" == DomainType then
            get_service_domain_p_list(SubDomainList[i], Result)
        end
    end
end

local Result = {}
local ParentMoid = ARGV[1]

local KeyDomain = 'domain:' .. ParentMoid .. ':info'
if redis.call('EXISTS',KeyDomain) == 1 then 
    local DomainType = redis.call('HGET',KeyDomain,'type')
    
    if "platform" == DomainType then
        get_platform_domain_p_list(ParentMoid, Result)
    elseif "service" == DomainType or 'kernel' == DomainType then
        get_service_domain_p_list(ParentMoid, Result)
    elseif "user" == DomainType then
        local machineRoomMoid = redis.call('hget',KeyDomain,'machine_room_moid') or ''
        get_machine_room_p_list(machineRoomMoid, Result)
    end
elseif redis.call('EXISTS','machine_room:' .. ParentMoid .. ':info') then
    get_machine_room_p_list(ParentMoid, Result)
end

return cjson.encode(Result)