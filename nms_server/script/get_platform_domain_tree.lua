local function get_domain_tree(Moid,DomainInfoList)
    local keyInfo = "domain:" .. Moid .. ":info"
    local Type = redis.call("HGET",keyInfo,"type")
    if Type == 'service' or Type == 'kernel'  then
        local domainInfo = {}
        domainInfo['moid'] = redis.call("HGET",keyInfo,"moid") or ""
        domainInfo['name'] = redis.call("HGET",keyInfo,"name") or ""
        domainInfo['type'] = redis.call("HGET",keyInfo,"type") or ""
        domainInfo['parent_moid'] = redis.call("HGET",keyInfo,"parent_moid") or ""
        table.insert(DomainInfoList,domainInfo)
        
        local KeySub = "domain:" .. Moid .. ":sub"
        if redis.call("EXISTS",KeySub) == 1 then
            local MoidList = redis.call("SMEMBERS",KeySub)
            for i,v in ipairs(MoidList) do
                get_domain_tree(v,DomainInfoList)
            end
        end
    elseif Type == 'platform' then
        local domainInfo = {}
        domainInfo['moid'] = redis.call("HGET",keyInfo,"moid") or ""
        domainInfo['name'] = redis.call("HGET",keyInfo,"name") or ""
        domainInfo['type'] = redis.call("HGET",keyInfo,"type") or ""
        domainInfo['parent_moid'] = redis.call("HGET",keyInfo,"parent_moid") or ""
        table.insert(DomainInfoList,domainInfo)
        
        local KeyMachineRoom = "domain:" .. Moid .. ":machine_room"
        if redis.call("EXISTS",KeyMachineRoom) == 1 then
            local machineRoomMoidList = redis.call("SMEMBERS",KeyMachineRoom)
            --获取机房详细信息
            for i = 1, table.getn(machineRoomMoidList) do
                local keyRoomInfo = "machine_room:" .. machineRoomMoidList[i] .. ":info"
                local machineRoomInfo = {}
                machineRoomInfo['moid'] = redis.call("HGET",keyRoomInfo,"moid") or ""
                machineRoomInfo['name'] = redis.call("HGET",keyRoomInfo,"name") or ""
                machineRoomInfo['type'] = "machine_room"
                machineRoomInfo['parent_moid'] = redis.call("HGET",keyRoomInfo,"domain_moid") or ""
                table.insert(DomainInfoList,machineRoomInfo)
            end
        end
    end
end

-- 从用户域moid获取域树信息
local function get_domain_tree_by_leaf(Moid,DomainInfoList)
    local keyInfo = "domain:" .. Moid .. ":info"
    if redis.call("EXISTS",keyInfo) == 1 then
        local Type = redis.call("HGET",keyInfo,"type") or ""
        if Type == 'service' then
            local domainInfo = {}
            domainInfo['moid'] = redis.call("HGET",keyInfo,"moid") or ""
            domainInfo['name'] = redis.call("HGET",keyInfo,"name") or ""
            domainInfo['type'] = redis.call("HGET",keyInfo,"type") or ""
            domainInfo['parent_moid'] = redis.call("HGET",keyInfo,"parent_moid") or ""
            table.insert(DomainInfoList,domainInfo)
        elseif Type == 'platform' then
            local domainInfo = {}
            domainInfo['moid'] = redis.call("HGET",keyInfo,"moid") or ""
            domainInfo['name'] = redis.call("HGET",keyInfo,"name") or ""
            domainInfo['type'] = redis.call("HGET",keyInfo,"type") or ""
            domainInfo['parent_moid'] = redis.call("HGET",keyInfo,"parent_moid") or ""
            table.insert(DomainInfoList,domainInfo)
            get_domain_tree_by_leaf(domainInfo['parent_moid'],DomainInfoList)
        elseif Type == 'user' then
            local machine_room_moid = redis.call("HGET",keyInfo,"machine_room_moid") or ""
            get_domain_tree_by_leaf(machine_room_moid,DomainInfoList)
        end        
    else
        local keyRoomInfo = "machine_room:" .. Moid .. ":info"
        if redis.call("EXISTS",keyRoomInfo) == 1 then
            local machineRoomInfo = {}
            machineRoomInfo['moid'] = redis.call("HGET",keyRoomInfo,"moid") or ""
            machineRoomInfo['name'] = redis.call("HGET",keyRoomInfo,"name") or ""
            machineRoomInfo['type'] = "machine_room"
            machineRoomInfo['parent_moid'] = redis.call("HGET",keyRoomInfo,"domain_moid") or ""
            table.insert(DomainInfoList,machineRoomInfo)     
            get_domain_tree_by_leaf(machineRoomInfo['parent_moid'],DomainInfoList)
        end  
    end
end

local DomainInfoList = {}

local DomainMoid = ARGV[1]
local KeyDomain = 'domain:' .. DomainMoid .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')
if "user" == DomainType then
    get_domain_tree_by_leaf(ARGV[1],DomainInfoList)
elseif "kernel" == DomainType or "service" == DomainType then
   get_domain_tree(ARGV[1],DomainInfoList) 
end

return cjson.encode(DomainInfoList)




