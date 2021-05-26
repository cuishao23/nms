local get_user_domain_live_list = function(Moid, Result)
    if type(Moid) ~= 'string' then
        return
    end
    local UserDomainName = redis.call("HGET", "domain:"..Moid..":info", "name") or ""
    local ApLiveKey = "domain:"..Moid..":aplive"
    local LiveList = redis.call("SMEMBERS", ApLiveKey)
    for i=1,#LiveList do
        local Key = "aplive:".. LiveList[i]..":info"
        if redis.call("EXISTS", Key) == 1 then
            local AliveInfo = {}
            AliveInfo['confe164'] = redis.call("HGET", Key, "conf_e164") or ''
            AliveInfo['live_name'] = redis.call("HGET", Key, "live_name") or ''
            AliveInfo['domain_moid'] = Moid
            AliveInfo['domain_name'] = UserDomainName
            AliveInfo['start_time'] = redis.call("HGET", Key, "live_start_time") or ''
            AliveInfo['encmode'] = tonumber(redis.call("HGET", Key, "encmode") or "1")
            table.insert(Result,AliveInfo)
        end
    end
end

local get_service_user_list = function(Moid)
    local Users = {}
    local Key = "domain:"..Moid..":sub"
    local MoidList = redis.call("SMEMBERS", Key)
    for i = 1,#MoidList do
        local UserInfoKey = "domain:"..MoidList[i]..":info"
        local Type = redis.call("HGET", UserInfoKey, "type")
        if Type == "user" then
            Users[#Users + 1] = MoidList[i]
        end
    end
    return Users
end

local get_all_service = function()
    local Result = redis.call("SCAN", "0", "MATCH", "domain:*:info", "COUNT", "100000")
    local Keys = Result[2]
    local ServiceList = {}
    for i=1,#Keys do
        local Type = redis.call("HGET", Keys[i], "type")
        if Type == "service" then
            local Moid = redis.call("HGET", Keys[i], "moid")
            ServiceList[#ServiceList+1] = Moid
        end
    end
    return ServiceList
end

local DomainMoid = ARGV[1]
local Result = {}
Result['success'] = 1
Result['aplive'] = {}
local DomainInfoKey = "domain:"..DomainMoid..":info"
local Type = redis.call("HGET", DomainInfoKey, "type")
if Type == "user" then
    get_user_domain_live_list(DomainMoid, Result['aplive'])
elseif Type == "service" then
    local UserMoidList = get_service_user_list(DomainMoid)
    for i = 1, #UserMoidList do
        get_user_domain_live_list(UserMoidList[i], Result['aplive'])
    end
elseif Type == "kernel" then
    local ServiceList = get_all_service()
    for i = 1, #ServiceList do
        local UserMoidArr = get_service_user_list(ServiceList[i])
        for j = 1, #UserMoidArr do
            get_user_domain_live_list(UserMoidArr[j], Result['aplive'])
        end
    end
end

return string.gsub(cjson.encode(Result), "{}", "[]")
