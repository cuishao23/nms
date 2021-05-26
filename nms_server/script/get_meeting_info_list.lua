local format_time = function( Time )
	if type(Time) ~= "string" then
		return ""
	end
	return string.gsub(string.gsub(Time, "-", "/"), " ", "T") .. "+8:00"
end

local function get_user_domain_meetings( UserDomainMoid, meeting_type, Result )
	local domain_moid_meeting = 'domain:' .. UserDomainMoid .. ':' .. meeting_type
	local MeetingList = redis.call('SMEMBERS', domain_moid_meeting)
	for i,v in pairs(MeetingList) do
		local MeetingInfo = {}

		local meeting_e164_info = meeting_type .. ':' .. v .. ':info'
		MeetingInfo['conf_type'] = 0
		MeetingInfo['e164'] = redis.call('HGET', meeting_e164_info, 'e164') or ""
		MeetingInfo['name'] = redis.call('HGET', meeting_e164_info, 'name') or ""
		MeetingInfo['bitrate'] = tonumber(redis.call('HGET', meeting_e164_info, 'bandwidth') or 0)
		MeetingInfo['start_time'] = format_time(redis.call('HGET', meeting_e164_info, 'start_time') or "")
		MeetingInfo['end_time'] = format_time(redis.call('HGET', meeting_e164_info, 'stop_time') or "")
		MeetingInfo['domain_moid'] = redis.call('HGET', meeting_e164_info, 'domain_moid') or ""

		-- 与会软硬终端
		MeetingInfo['meeting_terminals'] = {}
		local meeting_e164_terminal = 'meeting:' .. v .. ':terminal'
		local MeetingTerminalList = redis.call('SMEMBERS', meeting_e164_terminal)
		for ii,vv in pairs(MeetingTerminalList) do
			local MeetingTerminal = {}
			local terminal_e164_baseinfo = 'terminal:' .. vv .. ':baseinfo'
			MeetingTerminal['moid'] = redis.call('HGET', terminal_e164_baseinfo, 'moid') or ""
			MeetingTerminal['domain_moid'] = redis.call('HGET', terminal_e164_baseinfo, 'domain_moid') or ""
			MeetingTerminal['name'] = redis.call('HGET', terminal_e164_baseinfo, 'name') or ""
			MeetingTerminal['e164'] = vv

			-- 获得type值
			local terminal_moid_onlinestate = 'terminal:' .. MeetingTerminal['moid'] .. ':onlinestate'
			local Keys = redis.call('hkeys', terminal_moid_onlinestate)
			local Vals = redis.call('hvals', terminal_moid_onlinestate)
			local Type = ''
			for iii=1, table.getn(Keys) do
				if(Vals[i] == 'conference') then
					Type = Keys[i]
					break
				end
			end
			MeetingTerminal['type'] = Type

			local terminal_moid_type_netinfo = 'terminal:' .. MeetingTerminal['moid'] .. ':' .. Type .. ':netinfo'
			if(0 == redis.call('EXISTS', terminal_moid_type_netinfo)) then
				MeetingTerminal['ip'] = ''
			else
				MeetingTerminal['ip'] = redis.call('HGET', terminal_moid_type_netinfo, 'ip')
			end

			local terminal_moid_type_runninginfo = 'terminal:' .. MeetingTerminal['moid'] .. ':' .. Type .. ':runninginfo'
			if(0 == redis.call('EXISTS', terminal_moid_type_runninginfo)) then
				MeetingTerminal['version'] = ''
			else
				MeetingTerminal['version'] = redis.call('HGET', terminal_moid_type_runninginfo, 'version') or ""
			end

			table.insert(MeetingInfo['meeting_terminals'], MeetingTerminal)
		end

		-- 与会电话终端
		local meeting_e164_telphone = 'meeting:' .. v .. ':telphone'
		MeetingInfo['telephone_terminals'] = redis.call('SMEMBERS', meeting_e164_telphone)

		-- 与会外设信息
		MeetingInfo['meeting_device'] = {}
		local meeting_e164_mps = 'meeting:' .. v .. ':mps'
		local MpsList = redis.call('SMEMBERS', meeting_e164_mps)
		for ii,vv in pairs(MpsList) do
			local MeetingDevice = {}
			local meeting_e164_mps_moid_ability = 'meeting:' .. v .. ':mps:' .. vv .. ':ability'
			MeetingDevice['type'] = redis.call('HGET', meeting_e164_mps_moid_ability, 'device_type') or ""
			MeetingDevice['vmp_count'] = tonumber(redis.call('HGET', meeting_e164_mps_moid_ability, 'vmp_count') or 0)
			MeetingDevice['mixer_count'] = tonumber(redis.call('HGET', meeting_e164_mps_moid_ability, 'mixer_count') or 0)
			MeetingDevice['abas_count'] = tonumber(redis.call('HGET', meeting_e164_mps_moid_ability, 'abas_count') or 0)
			MeetingDevice['vbas_count'] = tonumber(redis.call('HGET', meeting_e164_mps_moid_ability, 'vbas_count') or 0)
			MeetingDevice['ip'] = redis.call('HGET', meeting_e164_mps_moid_ability, 'device_ip') or ""
			table.insert(MeetingInfo['meeting_device'], MeetingDevice)
		end

		-- 级联会议信息
		MeetingInfo['cascades'] = {}
		local meeting_e164_meeting = 'meeting:' .. v .. ':meeting'
		local MeetingMeetingKeys = redis.call('HKEYS', meeting_e164_meeting)
		for ii,vv in ipairs(MeetingMeetingKeys) do
			local MeetingMeeting = {}
			MeetingMeeting['e164'] = vv
			local MeetingMeetingType = redis.call('HGET', meeting_e164_meeting, vv) or ""
			if(MeetingMeetingType == 'up_meeting') then
				MeetingMeeting['type'] = 1
			elseif(MeetingMeetingType == 'down_meeting') then
				MeetingMeeting['type'] = 0
			-- 不存在其他情况，容错处理
			else
				MeetingMeeting['type'] = -1
			end

			local meeting_e164_info = ''
			local t_meeting_e164_info = 't_meeting:' .. vv .. ':info'
			local p_meeting_e164_info = 'p_meeting:' .. vv .. ':info'
			local sfu_meeting_e164_info = 'sfu_meeting:' .. vv .. ':info'
			local mix_meeting_e164_info = 'mix_meeting:' .. vv .. ':info'

			if(1 == redis.call('EXISTS', t_meeting_e164_info)) then
				meeting_e164_info = t_meeting_e164_info
			elseif (1 == redis.call('EXISTS', p_meeting_e164_info)) then
				meeting_e164_info = p_meeting_e164_info
			elseif (1 == redis.call('EXISTS', sfu_meeting_e164_info)) then
				meeting_e164_info = sfu_meeting_e164_info
			elseif (1 == redis.call('EXISTS', mix_meeting_e164_info)) then
				meeting_e164_info = mix_meeting_e164_info
			end

			MeetingMeeting['name'] = redis.call('HGET', meeting_e164_info, 'name') or ""
			table.insert(MeetingInfo['cascades'], MeetingMeeting)
		end

		-- Ip和友商
		local meeting_e164_ipe164 = 'meeting:' .. v .. ':ip_e164'
		MeetingInfo['ip_e164'] = redis.call('SMEMBERS', meeting_e164_ipe164)

		table.insert(Result['meeting'], MeetingInfo)
	end
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

local function get_user_domain_p2p_meetings( UserDomainMoid, Result )
	local domain_moid_p2pmeeting = 'domain:' .. UserDomainMoid .. ':p2p_meeting'
	local MeetingList = redis.call('SMEMBERS', domain_moid_p2pmeeting)
	for i,v in pairs(MeetingList) do
		local P2PMeetingInfo = {}

		local p2pmeeting_e164_info = 'p2p_meeting:' .. v .. ':info'
		P2PMeetingInfo['conf_type'] = 2

		P2PMeetingInfo['caller_e164'] = redis.call('HGET', p2pmeeting_e164_info, 'caller_e164') or ""

		local callerName = redis.call("HGET", p2pmeeting_e164_info, "caller_name") or ""
		P2PMeetingInfo['caller_name'] = get_terminal_name(P2PMeetingInfo['caller_e164'] ) or callerName

		local calleeType = redis.call("HGET", p2pmeeting_e164_info, "callee_type") or ""

		P2PMeetingInfo['caller_type'] = get_terminal_type_in_conf(P2PMeetingInfo['caller_e164'] ) or calleeType

		P2PMeetingInfo['caller_domain_moid'] = redis.call('HGET', p2pmeeting_e164_info, 'caller_domain_moid')

		P2PMeetingInfo['callee_e164'] = redis.call('HGET', p2pmeeting_e164_info, 'callee_e164') or ""

		local calleeName = redis.call("HGET", p2pmeeting_e164_info, "callee_name") or ""
		P2PMeetingInfo['callee_name'] = get_terminal_name(P2PMeetingInfo['callee_e164']) or calleeName

		local callerType = redis.call("HGET", p2pmeeting_e164_info, "caller_type") or ""
		P2PMeetingInfo['callee_type'] =  get_terminal_type_in_conf(P2PMeetingInfo['callee_e164']) or  calleeType
		P2PMeetingInfo['callee_domain_moid'] = redis.call('HGET', p2pmeeting_e164_info, 'callee_domain_moid') or ""
		P2PMeetingInfo['bitrate'] = tonumber(redis.call('HGET', p2pmeeting_e164_info, 'bandwidth') or 0)
		P2PMeetingInfo['start_time'] = format_time(redis.call('HGET', p2pmeeting_e164_info, 'start_time') or "")

		table.insert(Result['meeting'], P2PMeetingInfo)
	end
end

local function get_user_domain_moid_list(ServiceMoid)
	local Result = {}
	local domain_moid_sub = 'domain:' .. ServiceMoid .. ':sub'

	local IsExistServiceMoid = redis.call('EXISTS', 'domain:' .. ServiceMoid .. ':info')
	local IsExistServiceSub = redis.call('EXISTS', domain_moid_sub)
	if(IsExistServiceMoid == 0) then
		Result['success'] = 0
		Result['error_code'] = 20003
		return cjson.encode(Result)
	else
		Result['meeting'] = {}
	end
	local Type = redis.call('HGET', 'domain:'..ServiceMoid..':info', 'type')
	if Type == 'user' then
		get_user_domain_meetings(ServiceMoid, "t_meeting",Result)
		get_user_domain_meetings(ServiceMoid, "p_meeting",Result)
		get_user_domain_meetings(ServiceMoid, "sfu_meeting",Result)
		get_user_domain_meetings(ServiceMoid, "mix_meeting",Result)
		get_user_domain_p2p_meetings(ServiceMoid, Result)
	else
		local UserAndPlatformDomainList = redis.call('SMEMBERS', domain_moid_sub)
		for i,v in ipairs(UserAndPlatformDomainList) do
			local domain_moid_info = 'domain:' .. v .. ':info'
			local DomainType = redis.call('HGET', domain_moid_info, 'type')
			if(DomainType == 'user') then
				get_user_domain_meetings(v, "t_meeting",Result)
				get_user_domain_meetings(v, "p_meeting",Result)
				get_user_domain_meetings(v, "sfu_meeting",Result)
				get_user_domain_meetings(v, "mix_meeting",Result)
				get_user_domain_p2p_meetings(v, Result)
			end
		end
	end
	if(table.getn(Result['meeting']) == 0) then
		Result['meeting'] = nil
		Result['success'] = 0
		Result['error_code'] = 20404
		return cjson.encode(Result)
	else
		Result['success'] = 1
	end
	
	Result = string.gsub(string.gsub(cjson.encode(Result), "\\/", "/"), "{}", "[]")
	return Result
	-- print("\n\n", Result)
end

return(get_user_domain_moid_list(ARGV[1]))