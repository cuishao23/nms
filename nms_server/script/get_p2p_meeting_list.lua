local get_user_meeting_list = function(DomainMoid, MeetingName, P2PMeetingList)
	local KeyMeeting = "domain:" .. DomainMoid .. ":p2p_meeting"
	local MeetingList = redis.call('SMEMBERS', KeyMeeting)
	
	for i = 1,table.getn(MeetingList) do
        local MeetingInfoKey = "p2p_meeting:" .. MeetingList[i] .. ":info"
        
        if redis.call("HLEN", MeetingInfoKey) ~= 0 then
            local CallerName = redis.call("HGET", MeetingInfoKey, "caller_name") or ""
            
            -- 会议名称筛选
            local matchResult = string.match(CallerName, MeetingName)
            if MeetingName == '' or matchResult ~= nil then
                local MeetingInfo = {}
                MeetingInfo["meeting_moid"] = redis.call("HGET", MeetingInfoKey, "meeting_moid") or ""
                MeetingInfo["caller_e164"] = redis.call("HGET", MeetingInfoKey, "caller_e164") or ""
                MeetingInfo["callee_e164"] = redis.call("HGET", MeetingInfoKey, "callee_e164") or ""
                MeetingInfo["callee_name"] = redis.call("HGET", MeetingInfoKey, "callee_name") or ""
                MeetingInfo["bandwidth"] = redis.call("HGET", MeetingInfoKey, "bandwidth") or ""
                MeetingInfo["start_time"] = redis.call("HGET", MeetingInfoKey, "start_time") or ""
                MeetingInfo["caller_name"] = CallerName
                table.insert(P2PMeetingList,MeetingInfo)
            end 
        end
    end
end

local get_service_meeting_list
get_service_meeting_list = function(DomainMoid, MeetingName, P2PMeetingList)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

    	local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
    	local DomainType = redis.call('HGET',KeyDomain,'type')

    	if "user" == DomainType then
    		get_user_meeting_list(SubDomainList[i], MeetingName, P2PMeetingList)
    	elseif "service" == DomainType then
		    get_service_meeting_list(SubDomainList[i], MeetingName, P2PMeetingList)
		end
    end
end

local P2PMeetingList = {}
local KeyDomain = 'domain:' .. ARGV[1] .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    get_user_meeting_list(ARGV[1], ARGV[2], P2PMeetingList)
elseif "kernel" == DomainType or "service" == DomainType then
    get_service_meeting_list(ARGV[1], ARGV[2], P2PMeetingList)
end

local TotalCount = table.getn(P2PMeetingList)

local Start = tonumber(ARGV[3])
local Count = tonumber(ARGV[4])

local MaxIndex = 1
if Start + Count >  TotalCount then
    MaxIndex = TotalCount
else
    MaxIndex = Start + Count
end

local ResultMeetingList = {}
for i = Start + 1 ,MaxIndex do
    table.insert(ResultMeetingList,P2PMeetingList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['meeting'] = ResultMeetingList

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result