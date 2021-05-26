local Moid = ARGV[1]
local ConfType = ARGV[2]
local Count = tonumber(ARGV[3]) or -1
local Result = {}
if ConfType ~= "tran" and ConfType ~= "port" and ConfType ~= "sfu" and ConfType ~= "mix"  and ConfType ~= "p2p" and ConfType ~= "entity" then
    Result["success"] = 0
    Result["error_code"] = -1
    Result["error_str"] = "conf type error, the right value: tran,port,p2p"
    return cjson.encode(Result)
end

if Count < 0 then
    Result["success"] = 0
    Result["error_code"] = -1
    Result["error_str"] = "count param is error"
    return cjson.encode(Result)
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

local cmp_meeting_ele = function(E1, E2)
    return E1["start_time"] > E2["start_time"]
end


local function get_terminal_name(dev_e164)
	local KeyE164BaseInfo = 'terminal:' .. dev_e164 .. ':baseinfo'
	
	if redis.call('EXISTS', KeyE164BaseInfo) == 1 then 
        local Moid  = redis.call('HGET',KeyE164BaseInfo,'moid') or ""
        local KeyMoidBaseInfo = 'terminal:' .. Moid .. ':baseinfo'
        local Name = redis.call("HGET",KeyMoidBaseInfo,"name") or ""
        return Name
    else
        return nil
    end
end

local function get_terminal_type_in_conf(dev_e164)
	local KeyE164BaseInfo = 'terminal:' .. dev_e164 .. ':baseinfo'
	
	if redis.call('EXISTS', KeyE164BaseInfo) == 1 then 
        local Moid  = redis.call('HGET',KeyE164BaseInfo,'moid') or ""
        local KeyMoidBaseInfo = 'terminal:' .. Moid .. ':baseinfo'

        local KeyOnline = 'terminal:' .. Moid .. ':onlinestate'
        local type = nil
        if redis.call('EXISTS', KeyOnline) == 1 then 
            local Types = redis.call('HKEYS', KeyOnline)
            local Vals = redis.call('HVALS', KeyOnline)
            for i=1, table.getn(Types) do
                if(Vals[i] == 'conference') then
                    type = redis.call("HGET",'terminal_type_list',Types[i])
                    break 
                end
            end
        else
            type = nil
        end
        return type
    else
        return nil
    end
end


local get_user_meetings = function(Moid, ConfType, MeetingObjList)
    local Suffix = ""
    if ConfType == "tran" then
        Suffix = "t_meeting"
    elseif ConfType == "port" then
        Suffix = "p_meeting"
    elseif ConfType == "sfu" then
        Suffix = "sfu_meeting"
    elseif ConfType == "mix" then
        Suffix = "mix_meeting"
    elseif ConfType == "p2p" then
        Suffix = "p2p_meeting"
    elseif ConfType == "entity" then
        Suffix = "entity"
    end

    local DomainName = redis.call("HGET","domain:" ..Moid .. ":info","name") or ""
    local DomainMeetingKey = "domain:"..Moid..":"..Suffix
    local MeetingE164List = redis.call("SMEMBERS", DomainMeetingKey)
    for i=1,#MeetingE164List do
        local Info = {}
        local MeetingKey = Suffix..":".. MeetingE164List[i]..":info"
        if 1 == redis.call('EXISTS', MeetingKey) then
            if ConfType == "tran" or ConfType == "port" or ConfType == "sfu" or ConfType == "mix"  then
                local Name = redis.call("HGET", MeetingKey, "name") or ""
                local StartTime = redis.call("HGET", MeetingKey, "start_time")
                local StopTime = redis.call("HGET", MeetingKey, "stop_time") or ""
                local Organizer = redis.call("HGET", MeetingKey, "organizer") or ""
                local ConfE164 = redis.call("HGET", MeetingKey, "e164") or ""
                local Format = redis.call("HGET", MeetingKey, "format") or ""
                local Resolution = redis.call("HGET", MeetingKey, "resolution") or ""
                local Encryption = redis.call("HGET", MeetingKey, "encryption") or ""
                local Multi = redis.call("HGET", MeetingKey, "scale") or 8
                local Bandwidth = redis.call("HGET", MeetingKey, "bandwidth") or 0
                Info["name"] = Name
                Info["start_time"] = StartTime
                Info["end_time"] = StopTime
                Info["organizer"] = Organizer
                Info["confe164"] = ConfE164
                Info["format"] = Format
                Info["resolution"] = Resolution
                Info["encryption"] = Encryption
                Info["multi"] = tonumber(Multi) or 8
                Info["bandwidth"] = tonumber(Bandwidth) or 0
                Info["domain_name"] = DomainName
                if StartTime ~= nil and ConfE164 ~= nil then
                    MeetingObjList[#MeetingObjList+1] = Info
                end
            elseif ConfType == "entity" then
                local ConfInfoStr = redis.call("HGET", MeetingKey, "info") or "{}"
                local ConfInfo = cjson.decode(ConfInfoStr)
                -- 转化为api需要的参数格式
                ConfInfo["name"] = ConfInfo['subject'] or ""
                ConfInfo['subject'] = nil
                ConfInfo["start_time"] = string.gsub(ConfInfo['startTime'],'-','/') or ""
                ConfInfo["end_time"] = string.gsub(ConfInfo['endTime'],'-','/') or ""
                ConfInfo["endTime"] = nil
                ConfInfo["regular_id"] = ConfInfo['regularId'] or nil
                ConfInfo['regularId'] = nil

                ConfInfo["organizer"] = ConfInfo['creator'] or nil
                ConfInfo['creator'] = nil
                ConfInfo["organizer_moid"] = ConfInfo['organizerMoid'] or nil
                ConfInfo['organizerMoid'] = nil
                ConfInfo["is_video_meeting"] = ConfInfo['isVideoMeeting'] or nil
                ConfInfo['isVideoMeeting'] = nil
                ConfInfo["meeting_type"] = ConfInfo['meetingType'] or nil
                ConfInfo['meetingType'] = nil
                ConfInfo["last_modify_time"] = string.gsub(ConfInfo['lastModifyTime'],'-','/') or nil
                ConfInfo['lastModifyTime'] = nil
                ConfInfo["domain_name"] = DomainName
                MeetingObjList[#MeetingObjList+1] = ConfInfo
            else
                local CallerName = redis.call("HGET", MeetingKey, "caller_name") or ""
                local CalleeName = redis.call("HGET", MeetingKey, "callee_name") or ""
                local CallerE164 = redis.call("HGET", MeetingKey, "caller_e164") or ""
                local CalleeE164 = redis.call("HGET", MeetingKey, "callee_e164") or ""

                local StartTime = redis.call("HGET", MeetingKey, "start_time")
                Info["caller_name"] = get_terminal_name(CallerE164) or CallerName
                Info["callee_name"] = get_terminal_name(CalleeE164) or CalleeName
                Info["caller_e164"] = CallerE164
                Info["callee_e164"] = CalleeE164
                Info["start_time"] = StartTime
                Info["domain_name"] = DomainName
                if StartTime ~= nil and CallerE164 ~= nil then
                    MeetingObjList[#MeetingObjList+1] = Info
                end
            end
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

local MeetingList = {}

local DomainInfoKey = "domain:"..Moid..":info"
local DomainType = redis.call("HGET", DomainInfoKey, "type")
if DomainType == "user" then
    get_user_meetings(Moid, ConfType, MeetingList)
elseif DomainType == "service" then
    local Users = get_service_user_list(Moid)
    for i=1,#Users do
        get_user_meetings(Users[i], ConfType, MeetingList)
    end
elseif DomainType == "kernel" then
    local ServiceList = get_all_service()
    for i = 1, #ServiceList do
        local UserMoidArr = get_service_user_list(ServiceList[i])
        for j = 1, #UserMoidArr do
            get_user_meetings(UserMoidArr[j], ConfType, MeetingList)
        end
    end
end

local NewMeetingList = {}
if Count > 0 then
    for k=1,#MeetingList do
        if MeetingList[k] ~= nil and MeetingList[k]['start_time'] ~= nil then
            if #NewMeetingList < Count then
                NewMeetingList[#NewMeetingList+1] = MeetingList[k]
            else
                break
            end
        end
    end
else
    for k=1,#MeetingList do
        if MeetingList[k] ~= nil and MeetingList[k]['start_time'] ~= nil then
            NewMeetingList[#NewMeetingList+1] = MeetingList[k]
        end
    end
end

table.sort(NewMeetingList, cmp_meeting_ele)

if #NewMeetingList == 0 then
    return "{\"success\":1,\"meetings\":[]}"
end
Result["success"] = 1
Result["meetings"] = NewMeetingList

return cjson.encode(Result)