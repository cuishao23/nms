local CascadeMeetingList = {}
local KeyMeeting = 'meeting:' .. ARGV[1] .. ':meeting'
local MeetingList = redis.call('HKEYS', KeyMeeting)
	
for i = 1,table.getn(MeetingList) do
    -- 确定会议类型
	local KeyPMeeting = 'p_meeting:' .. MeetingList[i] .. ':info'
	local KeyTMeeting = 't_meeting:' .. MeetingList[i] .. ':info'
	local KeySfuMeeting = 'sfu_meeting:' .. MeetingList[i] .. ':info'
	local KeyMixMeeting = 'mix_meeting:' .. MeetingList[i] .. ':info'
 
    local KeyInfo = nil
    local MeetingType = nil
	if redis.call("EXISTS", KeyPMeeting) == 1 then
		KeyInfo = KeyPMeeting
		MeetingType = 'p_meeting'
	end

	if redis.call("EXISTS", KeyTMeeting) == 1 then
		KeyInfo = KeyTMeeting
		MeetingType = 't_meeting'
	end

	if redis.call("EXISTS", KeySfuMeeting) == 1 then
		KeyInfo = KeySfuMeeting
		MeetingType = 'sfu_meeting'
	end

	if redis.call("EXISTS", KeyMixMeeting) == 1 then
		KeyInfo = KeyMixMeeting
		MeetingType = 'mix_meeting'
	end

    -- 获取会议详情
	if KeyInfo ~= nil then
        local Name = redis.call("HGET", KeyInfo, "name") or ""
		-- 终端名称筛选Type
		local matchResult = string.match(Name, ARGV[2])
		if ARGV[2] == '' or matchResult ~= nil then

			local MeetingInfo={}
			MeetingInfo['meetingName'] = Name
			MeetingInfo["meetingE164"] = MeetingList[i]
			MeetingInfo["cascadeType"] = redis.call("HGET", KeyMeeting, MeetingList[i]) or ""
			MeetingInfo["bandWidth"] = redis.call("HGET", KeyInfo, "bandwidth") or ""
			MeetingInfo["startTime"] = redis.call("HGET", KeyInfo, "start_time") or ""
			MeetingInfo["endTime"] = redis.call("HGET", KeyInfo, "end_time") or ""
            if MeetingType ~= nil then
                MeetingInfo['meetingType'] = MeetingType
            else
                MeetingInfo['meetingType'] = ''
            end
	   		table.insert(CascadeMeetingList,MeetingInfo)
	   	end
   	end
 end

local TotalCount = table.getn(CascadeMeetingList)

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
    table.insert(ResultMeetingList,CascadeMeetingList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['meeting'] = ResultMeetingList

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result