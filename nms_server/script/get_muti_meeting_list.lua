local get_meeting_detail_info = function(MeetingInfoKey, MeetingName, MultiMeetingList)
    if redis.call("HLEN", MeetingInfoKey) ~= 0 then
    	local Name = redis.call("HGET", MeetingInfoKey, "name") or ""
        
        -- 会议名称筛选
		local matchResult = string.match(Name, MeetingName)
		if MeetingName ~= '' and matchResult == nil then
			return
        end

        local MeetingInfo = {}
        MeetingInfo["conf_name"] = Name
    	MeetingInfo["domain_moid"] = redis.call("HGET", MeetingInfoKey, "domain_moid") or ""
		MeetingInfo["meeting_moid"] = redis.call("HGET", MeetingInfoKey, "meeting_moid") or ""
		MeetingInfo["conf_e164"] = redis.call("HGET", MeetingInfoKey, "e164") or ""
		MeetingInfo["start_time"] = redis.call("HGET", MeetingInfoKey, "start_time") or ""
		MeetingInfo["end_time"] = redis.call("HGET", MeetingInfoKey, "stop_time") or ""
		MeetingInfo["scale"] = redis.call("HGET", MeetingInfoKey, "scale") or "0"
		MeetingInfo["organizer"] = redis.call("HGET", MeetingInfoKey, "organizer") or ""
        MeetingInfo["conf_type"] = redis.call("HGET", MeetingInfoKey, "conf_type") or ""
		table.insert(MultiMeetingList,MeetingInfo)
	end
end

local get_user_meeting_list = function(DomainMoid, MeetingName, MultiMeetingList)
    --传统会议列表
	local KeyTMeeting = "domain:" .. DomainMoid .. ":t_meeting"
	local TMeetingList = redis.call('SMEMBERS', KeyTMeeting)
	
	for i = 1,table.getn(TMeetingList) do
		local MeetingInfoKey = "t_meeting:" .. TMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingName, MultiMeetingList)
    end

    --端口会议列表
	local KeyPMeeting = "domain:" .. DomainMoid .. ":p_meeting"
	local PMeetingList = redis.call('SMEMBERS', KeyPMeeting)
	
	for i = 1,table.getn(PMeetingList) do
		local MeetingInfoKey = "p_meeting:" .. PMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingName, MultiMeetingList)
    end

    --混合会议列表
	local KeyMixMeeting = "domain:" .. DomainMoid .. ":mix_meeting"
	local MixMeetingList = redis.call('SMEMBERS', KeyMixMeeting)
	
	for i = 1,table.getn(MixMeetingList) do
		local MeetingInfoKey = "mix_meeting:" .. MixMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingName, MultiMeetingList)
    end

    --SFU会议列表
	local KeySfuMeeting = "domain:" .. DomainMoid .. ":sfu_meeting"
	local SfuMeetingList = redis.call('SMEMBERS', KeySfuMeeting)
	
	for i = 1,table.getn(SfuMeetingList) do
		local MeetingInfoKey = "sfu_meeting:" .. SfuMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingName, MultiMeetingList)
    end
end

local get_service_meeting_list
get_service_meeting_list = function(DomainMoid, MeetingName, MultiMeetingList)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

    	local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
    	local DomainType = redis.call('HGET',KeyDomain,'type')

    	if "user" == DomainType then
    		get_user_meeting_list(SubDomainList[i], MeetingName, MultiMeetingList)
    	elseif "service" == DomainType then
		    get_service_meeting_list(SubDomainList[i], MeetingName, MultiMeetingList)
		end
    end
end

local MultiMeetingList = {}
local KeyDomain = 'domain:' .. ARGV[1] .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    get_user_meeting_list(ARGV[1], ARGV[2], MultiMeetingList)
elseif "kernel" == DomainType or "service" == DomainType then
    get_service_meeting_list(ARGV[1], ARGV[2], MultiMeetingList)
end

local TotalCount = table.getn(MultiMeetingList)

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
    table.insert(ResultMeetingList,MultiMeetingList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['meeting'] = ResultMeetingList

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result