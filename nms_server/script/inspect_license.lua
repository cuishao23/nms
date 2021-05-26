-- 获取指定用户域下的license
-- domainMoid

local function getLicenseInfo(domainMoid, licenseId)
    local r = {}
    local key = "license:" .. licenseId .. ":info"
    if redis.call("EXISTS", key) == 1 then
        r["auth_id"] = licenseId
        r["service_domain_moid"] = domainMoid
        r["service_domain_name"] = redis.call("HGET", "domain:" .. domainMoid .. ":info", "name") or ""
        r["auth_dead_time"] = redis.call("HGET", key, "mcu_exp_date") or ""
    end
    return r
end

local domainMoidList = cjson.decode(ARGV[1])
local result = {}

-- 取所有域
for i, moid in pairs(domainMoidList) do
    for i, licenseId in pairs(redis.call("SMEMBERS", "domain:" .. moid .. ":license")) do
        local info = getLicenseInfo(moid, licenseId)
        if next(info) ~= nil then
            table.insert(result, info)
        end
    end
end

return string.gsub(cjson.encode(result), "{}", "[]")
