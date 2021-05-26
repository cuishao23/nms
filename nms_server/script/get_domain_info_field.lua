local domain_moid = ARGV[1]
local key_value = ARGV[2]

local domain_key = "domain:" .. domain_moid .. ":info"
local machine_room_key = "machine_room:" .. domain_moid .. ":info"

if 1 == redis.call("EXISTS",domain_key) then
    return redis.call("HGET",domain_key,key_value)
elseif 1 == redis.call("EXISTS",machine_room_key) then
    return redis.call("HGET",machine_room_key,key_value)
else
    return nil
end