local MoidListStr = ARGV[1]

if string.len(MoidListStr) == 0 then
    local Result = {}
    Result["success"] = 0
    Result["err_str"] = "moid list empty"
    Result["error_code"] = 123456
    return cjson.encode(Result)
end

local split_str = function(Src, Sep)
    local StartIndex = 1
    local SplitIndex = 1
    local SplitArray = {}
    while true do
        local LastIndex = string.find(Src, Sep, StartIndex)
        if not LastIndex then
            SplitArray[SplitIndex] = string.sub(Src, StartIndex, string.len(Src))
            break
        end
        SplitArray[SplitIndex] = string.sub(Src, StartIndex, LastIndex - 1)
        StartIndex = LastIndex + string.len(Sep)
        SplitIndex = SplitIndex + 1
    end
    return SplitArray
end

local MoidList = split_str(MoidListStr, ',')
local PhysicalList = {}
for i=1,#MoidList do
    local PhysicalInfoKey = "p_server:"..MoidList[i]..":info"
    if redis.call("EXISTS", PhysicalInfoKey) == 1 then
        local Item = {}
        Item["moid"] = MoidList[i]
        Item["name"] = redis.call("HGET", PhysicalInfoKey, "name") or ""
        Item["type"] = redis.call("HGET", PhysicalInfoKey, "type") or ""
        Item["ip"] = redis.call("HGET", PhysicalInfoKey, "ip") or ""
        Item["machine_room_moid"] = redis.call("HGET", PhysicalInfoKey, "machine_room_moid") or ""
        
        local MachineRoomInfoKey = "machine_room:"..Item["machine_room_moid"]..":info"
        Item["machine_room_name"] = redis.call("HGET", MachineRoomInfoKey, "name") or ""

        local FrameMoid = redis.call("HGET", PhysicalInfoKey, "smu") or ""
        if type(FrameMoid) == 'string' and string.len(FrameMoid) > 0 then
            local FrameInfoKey = "p_server:"..FrameMoid..":info"
            if redis.call("EXISTS", FrameInfoKey) == 1 then
                Item["frame_moid"] = FrameMoid
                Item["frame_name"] = redis.call("HGET", FrameInfoKey, "name") or ""
                Item["frame_type"] = redis.call("HGET", FrameInfoKey, "type") or ""
            end
        end
        local PhysicalResKey = "p_server:"..MoidList[i]..":resource"
        if redis.call("EXISTS", PhysicalResKey) == 1 then
            Item["cpu"] = tonumber(redis.call("HGET", PhysicalResKey, "cpu") or "0")
            Item["memory"] = tonumber(redis.call("HGET", PhysicalResKey, "memory") or "0")
            Item["memtotal"] = tonumber(redis.call("HGET", PhysicalResKey, "memtotal") or "0")
            Item["memused"] = tonumber(redis.call("HGET", PhysicalResKey, "memused") or "0")
        end
        PhysicalList[#PhysicalList+1] = Item
    end
end

local Result = {}
if next(PhysicalList) == nil then
    Result["success"] = 0
    Result["error_code"] = 123456
    Result["error_str"] = "physicals empty"
else
    Result["success"] = 1
    Result["physicals"] = PhysicalList
end

return cjson.encode(Result)

