-- 终端巡检
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

local function getOnlineType(moid)
    local onlineType = ""
    local onlineKey = "terminal:" .. moid .. ":onlinestate"
    local list = redis.call("HGETALL", onlineKey)
    for i = 1, #list do
        if list[i * 2] == "online" or list[i * 2] == "conference" then
            onlineType = list[i * 2 - 1]
            break
        end
    end
    return onlineType
end

local function getTerminalInfo(domainMoid, moid)
    local r = {}
    local onlineType = getOnlineType(moid)
    if onlineType and onlineType ~= "" then
        local infoKey = "terminal:" .. moid .. ":baseinfo"
        r["device_name"] = redis.call("HGET", infoKey, "name") or ""
        r["device_moid"] = redis.call("HGET", infoKey, "moid") or ""
        r["e164"] = redis.call("HGET", infoKey, "e164") or ""
        r["level"] = getLevel(redis.call("HVALS", "terminal:" .. moid .. ":warning"))
        r["user_domain_moid"] = domainMoid
        r["user_domain_name"] = redis.call("HGET", "domain:" .. domainMoid .. ":info", "name") or ""
        r["device_type"] = onlineType
        local netinfoKey = "terminal:" .. moid .. ":" .. string.gsub(onlineType, " ", "~") .. ":netinfo"
        r["device_ip"] = redis.call("HGET", netinfoKey, "ip") or ""
    end
    return r
end

local domainMoidList = cjson.decode(ARGV[1])
local result = {}

for i, moid in pairs(domainMoidList) do
    for i, terminalMoid in pairs(redis.call("SMEMBERS", "domain:" .. moid .. ":terminal")) do
        local info = getTerminalInfo(moid, terminalMoid)
        if next(info) then
            table.insert(result, info)
        end
    end
end

return string.gsub(cjson.encode(result), "{}", "[]")
