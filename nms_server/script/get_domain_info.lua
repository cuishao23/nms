local KeyDomainInfo = "domain:" .. ARGV[1] .. ":info"
if redis.call("EXISTS", KeyDomainInfo) == 1 then
    local DomainInfo = {}
    DomainInfo["moid"] = redis.call("HGET", KeyDomainInfo, "moid") or ""
    DomainInfo["name"] = redis.call("HGET", KeyDomainInfo, "name") or ""
    DomainInfo["type"] = redis.call("HGET", KeyDomainInfo, "type") or ""
    DomainInfo["machine_room_moid"] = redis.call("HGET", KeyDomainInfo, "machine_room_moid") or ""
    DomainInfo["parent_moid"] = redis.call("HGET", KeyDomainInfo, "parent_moid") or ""
    return cjson.encode(DomainInfo)
else
    local KeyMachineInfo = "machine_room:" .. ARGV[1] .. ":info"
    local MachineInfo = {}
    MachineInfo["moid"] = redis.call("HGET", KeyMachineInfo, "moid") or ""
    MachineInfo["name"] = redis.call("HGET", KeyMachineInfo, "name") or ""
    MachineInfo["type"] = "machine_room"
    MachineInfo["parent_moid"] = redis.call("HGET", KeyMachineInfo, "parent_moid") or ""
    return cjson.encode(MachineInfo)
end
