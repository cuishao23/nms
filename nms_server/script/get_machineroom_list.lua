local keyInfo = "domain:" .. ARGV[1] .. ":machine_room"
local Machineroom_List = redis.call('SMEMBERS', keyInfo)
local Result = {}
for i = 1,table.getn(Machineroom_List) do

    local KeyBaseInfo = 'machine_room:' .. Machineroom_List[i] .. ':info'
    if redis.call('EXISTS', KeyBaseInfo) == 1 then
        --Get terminal base info
        local Moid       = redis.call('HGET',KeyBaseInfo,'moid') or ""
        local DomainMoid = redis.call('HGET',KeyBaseInfo,'domain_moid') or ""
        local Name       = redis.call('HGET',KeyBaseInfo,'name') or ""
        local TotalPort  = redis.call('HGET',KeyBaseInfo,'total_port') or 0
        local RemainderPort  = redis.call('HGET',KeyBaseInfo,'remainder_port') or 0
        local RemainderTra  = redis.call('HGET',KeyBaseInfo,'remainder_tra') or 0

        local MachineroomInfo = {}
        MachineroomInfo['moid'] = Moid
        MachineroomInfo['domain_moid'] = DomainMoid
        MachineroomInfo['name'] = Name
        MachineroomInfo['total_port'] = TotalPort
        MachineroomInfo['remainder_port'] = RemainderPort
        MachineroomInfo['remainder_tra'] = RemainderTra
        if Name ~= '' then
            table.insert(Result, MachineroomInfo)
        end
    end
end
return cjson.encode(Result)
