local Moid = ARGV[1]

local Key = "p_server:"..Moid..":info"
local Name = redis.call("HGET", Key, "name") or ""
local Ip = redis.call("HGET", Key, "ip") or ""
local Type = redis.call("HGET", Key, "type") or ""
local MachineRoomMoid = redis.call("HGET", Key, "machine_room_moid") or ""
local MachineRoomInfoKey = "machine_room:"..MachineRoomMoid..":info"
local MachineRoomName = redis.call("HGET", MachineRoomInfoKey, "name") or ""
local Ret = {}
Ret["moid"] = Moid
Ret["name"] = Name
Ret["type"] = Type
Ret["ip"] = Ip
Ret["machine_room_moid"] = MachineRoomMoid
Ret["machine_room_name"] = MachineRoomName
Ret["cpu"] = 0
Ret["memory"] = 0
Ret["memtotal"] = 0
Ret["memused"] = 0

local ResourceKey = "p_server:"..Moid..":resource"
Ret["cpu"] = tonumber(redis.call("HGET", ResourceKey, "cpu") or 0 )
Ret["memory"] = tonumber(redis.call("HGET", ResourceKey, "memory") or 0)
Ret["memtotal"] = tonumber(redis.call("HGET", ResourceKey, "memtotal") or 0)
Ret["memused"] = tonumber(redis.call("HGET", ResourceKey, "memused") or 0)

local FrameMoid = redis.call("HGET", Key, "smu") or ""
if type(FrameMoid) == 'string' and string.len(FrameMoid) > 0 then
    Ret["frame_moid"] = FrameMoid
    local FrameInfoKey = "p_server:"..FrameMoid..":info"
    Ret["frame_name"] = redis.call("HGET", FrameInfoKey, "name") or ""
    Ret["frame_type"] = redis.call("HGET", FrameInfoKey, "type") or ""
end

return cjson.encode(Ret)