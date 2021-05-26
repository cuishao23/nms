-- 获取服务器硬件状态巡检结果
-- 参数: machineRoomMoid

local function getMemory(moid)
    local r = {}
    local key = "p_server:" .. moid .. ":resource"
    r["userd"] = redis.call("HGET", key, "memused") or ""
    r["total"] = redis.call("HGET", key, "memtotal") or ""
    r["userate"] = redis.call("HGET", key, "memory") or ""
    return r
end

local function getCpu(moid)
    local r = {}
    local key = "p_server:" .. moid .. ":resource"
    local count = redis.call("HGET", key, "cpu_count") or 0
    for i = 1, tonumber(count) do
        table.insert(r, redis.call("HGET", key, "cpucore" .. i) or 0)
    end
    return r
end

local function getNetcard(moid)
    local r = {}
    local key = "p_server:" .. moid .. ":resource"
    local count = redis.call("HGET", key, "netcard_count") or 0
    for i = 1, tonumber(count) do
        local info = {}
        info["sendkbps"] = redis.call("HGET", key, "netcard" .. i .. "_sendkbps") or 0
        info["recvkbps"] = redis.call("HGET", key, "netcard" .. i .. "_recvkbps") or 0
        info["name"] = redis.call("HGET", key, "netcard" .. i .. "_name") or ""
        table.insert(r, info)
    end
    return r
end

local function getDisk(moid)
    local r = {}
    local key = "p_server:" .. moid .. ":resource"
    local count = redis.call("HGET", key, "disk_count") or 0
    for i = 1, tonumber(count) do
        local info = {}
        info['disk_name'] = redis.call("HGET", key, "disk" .. i .. "_name") or ''
        info["total"] = redis.call("HGET", key, "disk" .. i .. "_total") or 0
        info["used"] = redis.call("HGET", key, "disk" .. i .. "_used") or 0
        info["userate"] = redis.call("HGET", key, "disk" .. i .. "_userate") or 0
        info["age"] = redis.call("HGET", key, "disk" .. i .. "_age") or 0
        table.insert(r, info)
    end
    return r
end

local function getHwReResource(moid)
    local r = {}
    r["meminfo"] = getMemory(moid)
    r["cpuinfo"] = getCpu(moid)
    r["netcardinfo"] = getNetcard(moid)
    r["diskinfo"] = getDisk(moid)
    return r
end

local machineRoomMoidList = cjson.decode(ARGV[1])
local result = {}

-- 获取所有机房
for i, moid in pairs(machineRoomMoidList) do
    for i, serverMoid in pairs(redis.call("SMEMBERS", "machine_room:" .. moid .. ":p_server")) do
        result[serverMoid] = getHwReResource(serverMoid)
    end
end

return string.gsub(cjson.encode(result), "{}", "[]")
