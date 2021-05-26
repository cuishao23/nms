local get_conf_quality = function(MeetingE164)
    local KeyTerminal = 'meeting:' .. MeetingE164 .. ':terminal'
    local TerminalList = redis.call('SMEMBERS', KeyTerminal)

    local allscore = 0
    local count = 0
    for i = 1,table.getn(TerminalList) do
        local score = 0
        local totalscore = 5
        local Key = "terminal:" .. TerminalList[i] .. ":baseinfo"
        local TerminalMoid = redis.call("HGET", Key, "moid") or ""

        if '' ~= TerminalMoid then
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
        end
        totalscore = totalscore - score
        if totalscore < 0 then
            totalscore = 0
        end
        allscore = allscore + totalscore
        count = count + 1
    end
    local quality = 5
    if 0 == count then
        return quality
    else
        quality = allscore / count
        return quality
    end
end

local get_p2p_conf_quality = function(TerminalE164, MeetingE164)
    local totalscore = 5
    local score = 0
    local TerminalMoid = ""
    local KeyE164BaseInfo = 'terminal:' .. TerminalE164 .. ':baseinfo'
	if redis.call('EXISTS', KeyE164BaseInfo) == 1 then
        TerminalMoid  = redis.call('HGET',KeyE164BaseInfo,'moid') or ""
    else
        return totalscore
    end
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
    totalscore = totalscore - score
    if totalscore < 0 then
        totalscore = 0
    end
    return totalscore
end

local get_meeting_detail_info = function(MeetingInfoKey, MeetingList)
    if redis.call("HLEN", MeetingInfoKey) ~= 0 then
        local MeetingInfo = {}
		MeetingInfo["conf_e164"] = redis.call("HGET", MeetingInfoKey, "e164") or ""
		MeetingInfo["quality"] = get_conf_quality(MeetingInfo["conf_e164"]) or 5
		table.insert(MeetingList,MeetingInfo)
	end
end

local get_p2p_meeting_detail_info = function(MeetingInfoKey, MeetingList)
    if redis.call("HLEN", MeetingInfoKey) ~= 0 then
        local MeetingInfo = {}
        local caller_e164 = redis.call("HGET", MeetingInfoKey, "caller_e164") or ""
        local callee_e164 = redis.call("HGET", MeetingInfoKey, "callee_e164") or ""
        local caller_score = get_p2p_conf_quality(caller_e164, caller_e164) or 5
        local callee_score = get_p2p_conf_quality(callee_e164, caller_e164) or 5
        local quality = (caller_score + callee_score) / 2
        MeetingInfo["conf_e164"] = caller_e164
        MeetingInfo["quality"] = quality
        table.insert(MeetingList,MeetingInfo)
    end
end

local get_user_meeting_list = function(DomainMoid, MeetingList)
    --传统会议列表
	local KeyTMeeting = "domain:" .. DomainMoid .. ":t_meeting"
	local TMeetingList = redis.call('SMEMBERS', KeyTMeeting)
	
	for i = 1,table.getn(TMeetingList) do
		local MeetingInfoKey = "t_meeting:" .. TMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingList)
    end

    --端口会议列表
	local KeyPMeeting = "domain:" .. DomainMoid .. ":p_meeting"
	local PMeetingList = redis.call('SMEMBERS', KeyPMeeting)

	for i = 1,table.getn(PMeetingList) do
		local MeetingInfoKey = "p_meeting:" .. PMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingList)
    end

    --混合会议列表
	local KeyMixMeeting = "domain:" .. DomainMoid .. ":mix_meeting"
	local MixMeetingList = redis.call('SMEMBERS', KeyMixMeeting)

	for i = 1,table.getn(MixMeetingList) do
		local MeetingInfoKey = "mix_meeting:" .. MixMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingList)
    end

    --SFU会议列表
	local KeySfuMeeting = "domain:" .. DomainMoid .. ":sfu_meeting"
	local SfuMeetingList = redis.call('SMEMBERS', KeySfuMeeting)

	for i = 1,table.getn(SfuMeetingList) do
		local MeetingInfoKey = "sfu_meeting:" .. SfuMeetingList[i] .. ":info"
		get_meeting_detail_info(MeetingInfoKey, MeetingList)
    end

    --点对点会议列表
    local KeyP2pMeeting = "domain:" .. DomainMoid .. ":p2p_meeting"
	local P2pMeetingList = redis.call('SMEMBERS', KeyP2pMeeting)

	for i = 1,table.getn(P2pMeetingList) do
		local MeetingInfoKey = "p2p_meeting:" .. P2pMeetingList[i] .. ":info"
		get_p2p_meeting_detail_info(MeetingInfoKey, MeetingList)
    end
end

local get_service_meeting_list
get_service_meeting_list = function(DomainMoid, MeetingList)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

    	local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
    	local DomainType = redis.call('HGET',KeyDomain,'type')

    	if "user" == DomainType then
    		get_user_meeting_list(SubDomainList[i], MeetingList)
    	elseif "service" == DomainType then
		    get_service_meeting_list(SubDomainList[i], MeetingList)
		end
    end
end

local MeetingList = {}
local KeyDomain = 'domain:' .. ARGV[1] .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    get_user_meeting_list(ARGV[1], MeetingList)
elseif "kernel" == DomainType or "service" == DomainType then
    get_service_meeting_list(ARGV[1], MeetingList)
end

return cjson.encode(MeetingList)