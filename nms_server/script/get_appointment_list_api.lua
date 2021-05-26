local Moid = ARGV[1]

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

local get_user_a_meeting_list = function(Moid, Result)
    local UserDomainAppointmentKey = "domain:"..Moid..":a_meeting"
    local AppointmentList = redis.call("SMEMBERS", UserDomainAppointmentKey)
    for i=1,#AppointmentList do
        local InfoKey = "a_meeting:"..AppointmentList[i]..":info"
        local Exist = redis.call("EXISTS", InfoKey)
        if Exist == 1 then
            local ConfInfoStr = redis.call("HGET", InfoKey, "info") or "{}"
            local ConfInfo = cjson.decode(ConfInfoStr)
            -- 参数格式转化 organizerMoid ---> organizer_moid
            ConfInfo["organizer_moid"] = ConfInfo['organizerMoid'] or ""
            ConfInfo['organizerMoid'] = nil
            ConfInfo["start_time"] = string.gsub(ConfInfo['startTime'],'-','/') or ""
            ConfInfo['startTime'] = nil
            ConfInfo["end_time"] = string.gsub(ConfInfo['endTime'],'-','/') or ""
            ConfInfo['endTime'] = nil
            ConfInfo["regular_id"] = ConfInfo['regularId'] or -1
            ConfInfo['regularId'] = nil
            ConfInfo["is_video_meeting"] = ConfInfo['isVideoMeeting'] or nil
            ConfInfo['isVideoMeeting'] = nil
            ConfInfo["is_conflict"] = ConfInfo['isConflict'] or 0
            ConfInfo['isConflict'] = nil
            ConfInfo["meeting_type"] = ConfInfo['meetingType'] or 0
            ConfInfo['meetingType'] = nil
            ConfInfo["last_modify_time"] = string.gsub(ConfInfo['lastModifyTime'],'-','/') or ""
            ConfInfo['lastModifyTime'] = nil

            ConfInfo["meeting_resource_vo"] = ConfInfo['meetingResourceVO'] or {}
            ConfInfo['meetingResourceVO'] = nil
            
            ConfInfo["meeting_resource_vo"]['framerate'] = ConfInfo["meeting_resource_vo"]['frameRate'] or nil
            ConfInfo["meeting_resource_vo"]['frameRate'] = nil

            ConfInfo["meeting_resource_vo"]['bitrate'] = ConfInfo["meeting_resource_vo"]['bitRate'] or nil
            ConfInfo["meeting_resource_vo"]['bitRate'] = nil   

            ConfInfo["meeting_resource_vo"]['call_type'] = ConfInfo["meeting_resource_vo"]['callType'] or nil
            ConfInfo["meeting_resource_vo"]['callType'] = nil  

            ConfInfo["meeting_resource_vo"]['meeting_type'] = ConfInfo["meeting_resource_vo"]['meetingType'] or nil
            ConfInfo["meeting_resource_vo"]['meetingType'] = nil 
            
            ConfInfo["meeting_resource_vo"]['total_count'] = ConfInfo["meeting_resource_vo"]['totalCount'] or nil
            ConfInfo["meeting_resource_vo"]['totalCount'] = nil

            ConfInfo["meeting_resource_vo"]['used_count'] = ConfInfo["meeting_resource_vo"]['usedCount'] or nil
            ConfInfo["meeting_resource_vo"]['usedCount'] = nil
    
            Result[#Result+1] = ConfInfo
        end
    end
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

local Result = {}

local DomainType = redis.call("HGET", "domain:"..Moid..":info", "type")
if DomainType == "kernel" then
    Moid = "all"
end

if Moid == "all" then
    local ServiceList = get_all_service()
    for i=1,#ServiceList do
        local Users = get_service_user_list(ServiceList[i])
        for j=1,#Users do
            get_user_a_meeting_list(Users[j], Result)
        end
    end
else
    local DomainInfoKey = "domain:"..Moid..":info"
    local Type = redis.call("HGET", DomainInfoKey, "type")
    if Type == "user" then
        get_user_a_meeting_list(Moid, Result)
    elseif Type == "service" then
        local Users = get_service_user_list(Moid)
        for i=1,#Users do
            get_user_a_meeting_list(Users[i], Result)
        end
    end
end

local cmp_meeting_ele = function(E1, E2)
    return E1["start_time"] > E2["start_time"]
end

table.sort(Result, cmp_meeting_ele)

local JsonObj = {}
if #Result == 0 then
    JsonObj["success"] = 1
    JsonObj["total"] = 0
    JsonObj["meetings"] = nil
    return "{\"success\":1,\"total\":0,\"meetings\":[]}"
else
    JsonObj["success"] = 1
    JsonObj["total"] = #Result
    JsonObj["meetings"] = Result
end
return string.gsub(cjson.encode(JsonObj), "{}", "[]")