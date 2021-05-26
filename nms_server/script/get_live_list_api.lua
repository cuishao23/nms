
-- MeetingType  t_meeting,p_meeting,sfu_meeting,mix_meeting
local get_user_domain_live_list = function(Moid, Result,MeetingType)
    if type(Moid) ~= 'string' and type(MeetingType) ~= 'string' then
        return
    end
    local UserDomainName = redis.call("HGET", "domain:"..Moid..":info", "name") or ""
    local MeetingKey = "domain:"..Moid..":" .. MeetingType
    local MeetingE164List = redis.call("SMEMBERS", MeetingKey)
    for i=1,#MeetingE164List do
        local Key = "meeting:".. MeetingE164List[i]..":live"
        if redis.call("EXISTS", Key) == 1 then
            local liveInfo = {}
            liveInfo['e164'] = MeetingE164List[i]
            liveInfo['live_name'] = redis.call("HGET", Key, "live_name") or ''
            liveInfo['domain_moid'] = Moid
            liveInfo['domain_name'] = UserDomainName
            liveInfo['start_time'] = redis.call("HGET", Key, "live_start_time") or ''
            liveInfo['livestatnum'] = tonumber(redis.call("HGET", Key, "max_user_count") or "0")
            liveInfo['encmode'] = tonumber(redis.call("HGET", Key, "encmode") or "1")
            liveInfo['authmode'] = tonumber(redis.call("HGET", Key, "authmode") or "1")
            table.insert(Result,liveInfo)
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
Result['live'] = {}
local DomainInfoKey = "domain:"..DomainMoid..":info"
local Type = redis.call("HGET", DomainInfoKey, "type")
if Type == "user" then
    get_user_domain_live_list(DomainMoid, Result['live'],"t_meeting")
    get_user_domain_live_list(DomainMoid, Result['live'],"p_meeting")
    get_user_domain_live_list(DomainMoid, Result['live'],"sfu_meeting")
    get_user_domain_live_list(DomainMoid, Result['live'],"mix_meeting")
elseif Type == "service" then
    local UserMoidList = get_service_user_list(DomainMoid)
    for i = 1, #UserMoidList do
        get_user_domain_live_list(UserMoidList[i], Result['live'],"t_meeting")
        get_user_domain_live_list(UserMoidList[i], Result['live'],"p_meeting")
        get_user_domain_live_list(UserMoidList[i], Result['live'],"sfu_meeting")
        get_user_domain_live_list(UserMoidList[i], Result['live'],"mix_meeting")
    end
elseif Type == "kernel" then
    local ServiceList = get_all_service()
    for i = 1, #ServiceList do
        local UserMoidArr = get_service_user_list(ServiceList[i])
        for j = 1, #UserMoidArr do
            get_user_domain_live_list(UserMoidArr[j], Result['live'],"t_meeting")
            get_user_domain_live_list(UserMoidArr[j], Result['live'],"p_meeting")
            get_user_domain_live_list(UserMoidArr[j], Result['live'],"sfu_meeting")
            get_user_domain_live_list(UserMoidArr[j], Result['live'],"mix_meeting")          
        end
    end
end

return string.gsub(cjson.encode(Result), "{}", "[]")


