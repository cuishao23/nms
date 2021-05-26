local getmeetingscore = function(MeetingE164, TerminalMoid)
    local score = 0
    local totalscore = 5

    --卡顿
    if redis.call("EXISTS", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":blunt") == 1 then
        local info = {}
        info["score"] = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":blunt", "score")
        score = score + tonumber(info["score"])
    end

    --丢包
    if redis.call("EXISTS", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":lossrate") == 1 then
        local info = {}
        info["score"] = redis.call("HGET", "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":lossrate", "score")
        score = score + tonumber(info["score"])
    end

    --异常离会
    local EnterLeaveInfoKey = "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":enter_leave_info:"
    local KeyEnterTime = "terminal:" .. TerminalMoid .. ":conf:" .. MeetingE164 .. ":enter_times"
    local EnterTimes = redis.call('GET', KeyEnterTime) or '0'
    for i = 1, tonumber(EnterTimes) do
        local info = {}
        local reason = redis.call("HGET", EnterLeaveInfoKey .. i, "leave_reason")
        if reason == "1" or reason == "3" or reason == "28" or reason == "29" or reason == "30" or reason == "31" then
            info["score"] = 0.5
            score = score + tonumber(info["score"])
        end
    end

    totalscore = totalscore - score
    if totalscore < 0 then
        totalscore = 0
    end
    return totalscore
end


local MeetingTerminalList = {}
local TerminalName = ARGV[2]
local KeyTerminal = 'meeting:' .. ARGV[1] .. ':terminal'
local TerminalList = redis.call('SMEMBERS', KeyTerminal)
	
for i = 1,table.getn(TerminalList) do
	local Key = "terminal:" .. TerminalList[i] .. ":baseinfo"
	local Moid = redis.call("HGET", Key, "moid") or ""
	local Name = redis.call("HGET", Key, "name") or ""

	-- 终端名称筛选
	local matchResult = string.match(Name, TerminalName)
	if TerminalName == '' or matchResult ~= nil then

        -- 终端存在meetingdetail这个表，并且conf_e164字段跟当前会议相同，才是本会议里面的终端
		local MeetingInfoKey = "terminal:" .. Moid .. ":meetingdetail"
		if redis.call("EXISTS", MeetingInfoKey) == 1 then
			local ConfE164 = redis.call("HGET", MeetingInfoKey, "conf_e164") or ""
			if ConfE164 == ARGV[1] then
				local TerminalInfo={}
				TerminalInfo['star'] = getmeetingscore(ARGV[1], Moid)
				TerminalInfo["e164"] = TerminalList[i]
				TerminalInfo["moid"] = Moid
				TerminalInfo["name"] = Name
				 
				local MtType = redis.call("HGET", MeetingInfoKey, "mt_type") or ""
		        TerminalInfo['mt_type'] = MtType

		        local RunningInfoKey = "terminal:" .. Moid .. ":" .. string.gsub(MtType, " ", "~") .. ":runninginfo"
		        TerminalInfo['version'] = redis.call("HGET", RunningInfoKey, "version") or ""
		        
		        local NetInfoKey = "terminal:" .. Moid .. ":" .. string.gsub(MtType, " ", "~") .. ":netinfo"
		        TerminalInfo['ip'] = redis.call("HGET", NetInfoKey, "ip") or ""

		   		table.insert(MeetingTerminalList,TerminalInfo)

			end
		end
   	end
 end

local TotalCount = table.getn(MeetingTerminalList)

local Start = tonumber(ARGV[3])
local Count = tonumber(ARGV[4])
-- 返回全部终端列表以便求出平均体验分
if Start == 0 and Count == 0 then
    return cjson.encode(MeetingTerminalList)
else
    local MaxIndex = 1
    if Start + Count >  TotalCount then
        MaxIndex = TotalCount
    else
        MaxIndex = Start + Count
    end

    local ResultTerminalList = {}
    for i = Start + 1 ,MaxIndex do
        table.insert(ResultTerminalList,MeetingTerminalList[i])
    end

    local Result = {}
    Result['total_count'] = TotalCount
    Result['terminal'] = ResultTerminalList

    Result = string.gsub(cjson.encode(Result), "{}", "[]")
    return Result
end