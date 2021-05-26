local get_user_meeting_list = function(DomainMoid, AppointMeetingList)
	local KeyMeeting = 'domain:' .. DomainMoid .. ':a_meeting'
	local MeetingList = redis.call('SMEMBERS', KeyMeeting)

	for i = 1,table.getn(MeetingList) do
        local KeyInfo = 'a_meeting:' .. MeetingList[i] .. ':info'
		local MeetingInfo = {}
		MeetingInfo['start_time'] = redis.call('HGET', KeyInfo,'start_time') or ''
		MeetingInfo['domain_moid'] = redis.call('HGET', KeyInfo,'domain_moid') or ''
		table.insert(AppointMeetingList,1,MeetingInfo)
	end
end

local get_service_meeting_list
get_service_meeting_list = function(DomainMoid, AppointMeetingList)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

    	local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
    	local DomainType = redis.call('HGET',KeyDomain,'type')

    	if "user" == DomainType then
    		get_user_meeting_list(SubDomainList[i], AppointMeetingList)
    	elseif "service" == DomainType then
		    get_service_meeting_list(SubDomainList[i], AppointMeetingList)
		end
    end
end

local AppointMeetingList = {}
local DomainMoid = ARGV[1]
local KeyDomain = 'domain:' .. DomainMoid .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    get_user_meeting_list(DomainMoid, AppointMeetingList)
elseif "kernel" == DomainType or "service" == DomainType then
    get_service_meeting_list(DomainMoid, AppointMeetingList)
end

return cjson.encode(AppointMeetingList)