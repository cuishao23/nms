local MeetingE164 = ARGV[1]
local TerminalMoid = ARGV[2]
local InfoList = {}

--卡顿
if redis.call("EXISTS", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":blunt") == 1 then
    local info = {}
    info["type"] = "blunt"
    info["time"] = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":blunt", "time")
    info["score"] = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":blunt", "score")
    local count = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":blunt", "count")
    info["note"] = "卡顿数为" .. count .. '次'
    table.insert(InfoList, info)
end

--丢包
if redis.call("EXISTS", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":lossrate") == 1 then
    local info = {}
    info["type"] = "lossrate"
    info["time"] = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":lossrate", "time")
    info["score"] = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":lossrate", "score")
    local lossrate = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":lossrate", "lossrate")
    info["note"] = "丢包率为" .. lossrate .. '%'
    table.insert(InfoList, info)
end

--异常离会
local EnterLeaveInfoKey = "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":enter_leave_info:"
local KeyEnterTime = "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":enter_times"
local EnterTimes = redis.call('GET', KeyEnterTime) or '0'
for i = 1, tonumber(EnterTimes) do
    local info = {}
    local reason = redis.call("HGET", EnterLeaveInfoKey .. i, "leave_reason")
    if reason == "1" or reason == "3" or reason == "28" or reason == "29" or reason == "30" or reason == "31" or reason == "37" or reason == "42" or reason == "255" then
        info["time"] = redis.call("HGET", EnterLeaveInfoKey .. i, "leave_time")
        info["score"] = 0.5
        info["type"] = "leave"
        info["note"] = reason
        table.insert(InfoList, info)
    end
end

return cjson.encode(InfoList)