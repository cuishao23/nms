-- 服务器巡检
--

local function getLevel(levelList)
    local r = "none"
    local map = {
        ["critical"] = 3,
        ["important"] = 2,
        ["normal"] = 1,
        ["none"] = 0
    }
    for i, level in pairs(levelList) do
        if map[level] > map[r] then
            r = level
        end
    end
    return r
end

local function getServerInfo(machineRoomMoid, moid, serverType)
    local r = {}
    local prefix = ""
    local infoKey = ""
    if serverType == "physical" then
        prefix = "p_server:"
        infoKey = "p_server:" .. moid .. ":info"
        r["device_ip"] = redis.call("HGET", infoKey, "ip") or ""
    else
        prefix = "l_server:"
        infoKey = "l_server:" .. moid .. ":info"
        local physicalMoid = redis.call("HGET", infoKey, "p_server_moid") or ""
        r["device_ip"] = redis.call("HGET", "p_server:" .. physicalMoid .. ":info", "ip") or ""
    end
    r["device_name"] = redis.call("HGET", infoKey, "name") or ""
    r["device_moid"] = redis.call("HGET", infoKey, "moid") or ""
    r["device_type"] = redis.call("HGET", infoKey, "type") or ""
    r["server_type"] = serverType
    r["machine_room_moid"] = machineRoomMoid
    r["machine_room_name"] = redis.call("HGET", "machine_room:" .. machineRoomMoid .. ":info", "name") or ""
    local online = redis.call("GET", prefix .. moid .. ":online")
    if online and online ~= "offline" then
        online = "online"
    else
        online = "offline"
    end
    r["online"] = online
    r["level"] = getLevel(redis.call("HVALS", prefix .. moid .. ":warning"))
    return r
end

local machineRoomMoidList = cjson.decode(ARGV[1])
local result = {}

-- 获取所有机房
for i, moid in pairs(machineRoomMoidList) do
    for i, serverMoid in pairs(redis.call("SMEMBERS", "machine_room:" .. moid .. ":p_server")) do
        local info = getServerInfo(moid, serverMoid, "physical")
        info["machine_room_moid"] = moid
        table.insert(result, info)
    end
    -- 暂时停止逻辑服务器巡检
    -- for i, serverMoid in pairs(redis.call("SMEMBERS", "machine_room:" .. moid .. ":l_server")) do
    --     local info = getServerInfo(moid, serverMoid, "logical")
    --     info["machine_room_moid"] = moid
    --     table.insert(result, info)
    -- end
end

return string.gsub(cjson.encode(result), "{}", "[]")
