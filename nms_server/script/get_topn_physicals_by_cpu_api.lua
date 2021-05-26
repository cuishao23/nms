--获取机房列表
local get_machine_room_moid_list
get_machine_room_moid_list = function (DomainMoid, MachineRoomMoidList)
    --获取域所属机房列表
    local DomainMachineListKey = 'domain:' .. DomainMoid .. ':machine_room'
    local MacMoidList = redis.call('SMEMBERS', DomainMachineListKey)
    for i=1,table.getn(MacMoidList) do
        table.insert(MachineRoomMoidList,MacMoidList[i])
    end
end

local get_tree
get_tree = function(DomainMoid, MachineRoomMoidList)
    if DomainMoid == nil then
        return
    end

    local DomainMoidKey = 'domain:'..DomainMoid..':info'
    local DomainType = redis.call('HGET',DomainMoidKey,'type')
    if "platform" == DomainType then
        get_machine_room_moid_list(DomainMoid, MachineRoomMoidList)
    elseif "user" ~= DomainMoid then
        local SubMoidKey = 'domain:' .. DomainMoid .. ':sub'
        local SubMoidList = redis.call('SMEMBERS', SubMoidKey)

        if table.getn(SubMoidList) > 0 then
            for i = 1, table.getn(SubMoidList) do
                get_tree(SubMoidList[i], MachineRoomMoidList)
            end
        end
    end
end

local Moid = ARGV[1]
local Type = ""

-- 获取Moid的类型
Type = redis.call("HGET","domain:" .. Moid .. ":info","type")
if (not Type) then
    Type = ""
end

local MachineRoomMoidList = {}
if Type == "user" then
    local MachineRoomMoid = redis.call("HGET","domain:" .. Moid .. ":info","machine_room_moid")
    if Type then
        MachineRoomMoidList[#MachineRoomMoidList + 1] = MachineRoomMoid
    end
else
    get_tree(Moid, MachineRoomMoidList)
end

local is_in_table = function(value, tbl)
    for k,v in ipairs(tbl) do
        if v == value then
            return true;
        end
    end
    return false;
end

local Result = redis.call("SCAN", "0", "MATCH", "p_server:*:info", "COUNT", "100000")
local Keys = Result[2]
local Ret = {}
local Num = tonumber(ARGV[2]) or 5
for i = 1, #Keys do
    local Item = {}
    local Name = redis.call("HGET", Keys[i], "name") or ""
    local Moid = redis.call("HGET", Keys[i], "moid") or ""
    local Type = redis.call("HGET", Keys[i], "type") or ""
    local Ip = redis.call("HGET", Keys[i], "ip") or ""
    local MachineRoomMoid = redis.call("HGET", Keys[i], "machine_room_moid") or ""
    if is_in_table(MachineRoomMoid, MachineRoomMoidList) then
        local MachineRoomName = redis.call("HGET", "machine_room:"..MachineRoomMoid..":info", "name") or ""
        Item["moid"] = Moid
        Item["name"] = Name
        Item["type"] = Type
        Item["ip"] = Ip
        Item["machine_room_moid"] = MachineRoomMoid
        Item["machine_room_name"] = MachineRoomName
        local FrameMoid = redis.call("HGET", Keys[i], "smu") or ""
        if type(FrameMoid) == 'string' and string.len(FrameMoid) > 0 then
            local FrameInfoKey = "p_server:"..FrameMoid..":info"
            if redis.call("EXISTS", FrameInfoKey) == 1 then
                Item["frame_moid"] = FrameMoid
                Item["frame_name"] = redis.call("HGET", FrameInfoKey, "name") or ""
                Item["frame_type"] = redis.call("HGET", FrameInfoKey, "type") or ""
            end
        end

        local KeyOnline = "p_server:"..Moid..":online"
        local OnlineState = redis.call("GET", KeyOnline)
        if OnlineState ~= nil and OnlineState ~= "offline" and Type ~= "smu" and Type ~= "xmpu" and Type ~= "xmpu5" then
            local ResourceKey = "p_server:"..Moid..":resource"
            local Cpu = redis.call("HGET", ResourceKey, "cpu")
            if Cpu ~= nil then
                Item["cpu"] = tonumber(Cpu) or 0
                Ret[#Ret + 1] = Item
            end
        end
    end
end

local comps = function(A, B)
    return A.cpu > B.cpu
end

--排序
table.sort(Ret, comps)

local Result = {}
if next(Ret) == nil then
    Result["success"] = 0
    Result["error_code"] = 123456
    Result["error_str"] = "physicals empty"
else
    local Tmp = {}
    if #Ret > Num then
        for i = 1, Num do
            if #Tmp < Num then
                Tmp[#Tmp + 1] = Ret[i]
            end
        end
    else
        Tmp = Ret
    end
    Result["success"] = 1
    Result["physicals"] = Tmp
end

return cjson.encode(Result)