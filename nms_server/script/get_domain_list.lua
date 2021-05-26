--获取机房列表
local get_machine_room_list
get_machine_room_list = function (DomainMoid, DomainInfoList)
	--获取域所属机房列表
	local DomainMachineListKey = 'domain:' .. DomainMoid .. ':machine_room'
	local MachineRoomMoidList = redis.call('SMEMBERS', DomainMachineListKey)
	if table.getn(MachineRoomMoidList) <= 0 then
		return
	end

	--获取机房详细信息
	for i = 1, table.getn(MachineRoomMoidList) do
		local MachineRoomKey = "machine_room:" .. MachineRoomMoidList[i] .. ":info"
        local Name = redis.call('HGET', MachineRoomKey, 'name') or ''
        local domain_info = {}
        domain_info['moid'] = MachineRoomMoidList[i]
        domain_info['parent_moid'] = DomainMoid
        domain_info['type'] = 'machine_room'
        domain_info['name'] = Name or ''
        table.insert(DomainInfoList,domain_info)
	end
end

local get_tree
get_tree = function(DomainMoid, DomainInfoList)
    if DomainMoid == nil then
        return
    end

    local DomainKey = 'domain:'..DomainMoid..':info'
    local domain_info = {}
    domain_info['moid'] = DomainMoid
    domain_info['parent_moid'] = redis.call('HGET',DomainKey,'parent_moid') or ''
    domain_info['type'] = redis.call('HGET',DomainKey,'type')
    domain_info['name'] = redis.call('HGET',DomainKey,'name') or ''
    table.insert(DomainInfoList,domain_info)

    if domain_info['type'] == 'platform' then
        get_machine_room_list(DomainMoid, DomainInfoList)
    else
        local SubMoidKey = 'domain:' .. DomainMoid .. ':sub'
        local SubMoidList = redis.call('SMEMBERS', SubMoidKey)

        if table.getn(SubMoidList) > 0 then
            for i = 1, table.getn(SubMoidList) do
                get_tree(SubMoidList[i], DomainInfoList)
            end
        end
    end
end

local DomainInfoList = {}
get_tree(ARGV[1], DomainInfoList) 

return cjson.encode(DomainInfoList)