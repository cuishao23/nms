
local function get_parents_domain_info(DomainMoid, Result,RootMoid)
    local KeyMachineRoomInfo = "machine_room:" .. DomainMoid .. ":info"
    if 1 == redis.call('EXISTS', KeyMachineRoomInfo) then
        local DomainParentMoid = redis.call('HGET',KeyMachineRoomInfo,'domain_moid')
        local DomainName       = redis.call('HGET',KeyMachineRoomInfo,'name') or ''

        local domain_info = {}
        domain_info['moid'] = DomainMoid
        domain_info['parent_moid'] = DomainParentMoid
        domain_info['type'] = 'machine_room'
        domain_info['name'] = DomainName

        table.insert(Result,domain_info)
        get_parents_domain_info(DomainParentMoid,Result,RootMoid)
    else
        local DomainMoidKey = "domain:" .. DomainMoid .. ":info"
        local DomainParentMoid = redis.call('HGET',DomainMoidKey,'parent_moid') or ''
        local DomainName       = redis.call('HGET',DomainMoidKey,'name') or ''
        local DomainType       = redis.call('HGET',DomainMoidKey,'type') or ''
        
        local domain_info = {}
        domain_info['moid'] = DomainMoid
        domain_info['parent_moid'] = DomainParentMoid
        domain_info['type'] = DomainType
        domain_info['name'] = DomainName

        table.insert(Result,domain_info)
        if (not DomainParentMoid) or (RootMoid == "" and "service" == DomainType) or (RootMoid ~= "" and RootMoid == DomainMoid) then
            return
        else
            get_parents_domain_info(DomainParentMoid,Result,RootMoid)
        end
    end
end

local Moid = ARGV[1]
local RootMoid = ARGV[2]
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

local Result = {}
-- 参数仅取用户域或机房moid
if "user" == Type or "machine_room" == Type then
    get_parents_domain_info(Moid, Result,RootMoid)
end

return cjson.encode(Result)    