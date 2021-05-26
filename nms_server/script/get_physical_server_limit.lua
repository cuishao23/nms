local get_machine_room_p_list = function(Moid, Result)
    local KeyServer = 'machine_room:' .. Moid .. ':p_server'
    local ServerMoidList = redis.call('SMEMBERS', KeyServer)
    for i = 1,table.getn(ServerMoidList) do
        local KeyInfo = 'p_server:' .. ServerMoidList[i] .. ':info'
        if redis.call('EXISTS', KeyInfo) == 1 then
            local IP = redis.call('HGET',KeyInfo,'ip') or ''
            if IP ~= '' then
                --Get server info
                local Name = redis.call('HGET',KeyInfo,'name') or ServerMoidList[i]

                --Get server limit
                local KeyLimit = 'warning:limit:' .. ServerMoidList[i]
                local CPU     = redis.call('HGET',KeyLimit,'cpu') or '80'
                local Disk    = redis.call('HGET',KeyLimit,'disk') or '80'
                local Memory  = redis.call('HGET',KeyLimit,'memory') or '80'
                local Port    = redis.call('HGET',KeyLimit,'port') or '60'
                local WriteSpeed = redis.call('HGET',KeyLimit,'diskwritespeed') or '2'
                local RateOfflow = redis.call('HGET',KeyLimit,'rateofflow') or '500'

                -- Format server info object
                local ServerInfo = {}
                ServerInfo['cpu'] = CPU
                ServerInfo['disk'] = Disk
                ServerInfo['memory'] = Memory
                ServerInfo['port'] = Port
                ServerInfo['diskwritespeed'] = WriteSpeed
                ServerInfo['rateofflow'] = RateOfflow
                ServerInfo['moid'] = ServerMoidList[i]
                ServerInfo['name'] = Name
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
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end

    for i = 1, table.getn(SubDomainList) do
        local KeyInfo = 'domain:' .. SubDomainList[i] .. ':info'
        if redis.call('EXISTS', KeyInfo) == 1 then
            --Get domain info
            local Type = redis.call('HGET',KeyInfo,'type')
            if 'service' == Type then
                get_service_domain_p_list(SubDomainList[i], Result)
            elseif 'platform' == Type then
                get_platform_domain_p_list(SubDomainList[i], Result)
            end
        end

    end
end

local ServerList = {}
local ParentMoid = ARGV[1]

local KeyDomain = 'domain:' .. ParentMoid .. ':info'
if redis.call('EXISTS',KeyDomain) == 1 then 
    local DomainType = redis.call('HGET',KeyDomain,'type')

    if "platform" == DomainType then
        get_platform_domain_p_list(ParentMoid, ServerList)
    elseif "service" == DomainType or 'kernel' == DomainType then
        get_service_domain_p_list(ParentMoid, ServerList)
    end
elseif redis.call('EXISTS','machine_room:' .. ParentMoid .. ':info') then
    get_machine_room_p_list(ParentMoid, ServerList)
end

local TotalCount = table.getn(ServerList)

local Start = tonumber(ARGV[2])
local Count = tonumber(ARGV[3])

local MaxIndex = 1
if Start + Count >  TotalCount then
    MaxIndex = TotalCount
else
    MaxIndex = Start + Count
end

local ResultPServerList = {}
for i = Start + 1 ,MaxIndex do
    table.insert(ResultPServerList,ServerList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['p_servers'] = ResultPServerList

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result