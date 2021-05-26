local MeetingE164 = ARGV[1]
local TerminalMoid = ARGV[2]
local KeyEnterTime = "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":enter_times"
local EnterTimes = redis.call('GET', KeyEnterTime) or '0'

local LeaveInfoList = {}
for i = 1, tonumber(EnterTimes) do
	local KeyEnterLeaveInfo = "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":enter_leave_info:" .. i
    local info = {}
    info["enter_time"] = redis.call("HGET", KeyEnterLeaveInfo, "enter_time")
    info["leave_time"] = redis.call("HGET", KeyEnterLeaveInfo, "leave_time") or ""
    info["leave_reason"] = redis.call("HGET", KeyEnterLeaveInfo, "leave_reason") or ""
    table.insert(LeaveInfoList, info)
end

return cjson.encode(LeaveInfoList)