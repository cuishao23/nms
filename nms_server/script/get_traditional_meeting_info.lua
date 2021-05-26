local TMeetingKey= "domain:" .. ARGV[1] .. ":t_meeting"
local ConfE164List = redis.call('SMEMBERS', TMeetingKey)

local KeyDomainInfo = "domain:" .. ARGV[1] .. ":info"
local DomainName = redis.call("HGET", KeyDomainInfo, "name")

local Result = {}
for i = 1, table.getn(ConfE164List) do
	local MeetingInfoKey = "t_meeting:" .. ConfE164List[i] .. ":info"
	local  DomainMoid = redis.call("HGET", MeetingInfoKey, "domain_moid") or ""

	if redis.call("HLEN", MeetingInfoKey) ~= 0 and DomainMoid == ARGV[1] then
		local E164 = redis.call("HGET", MeetingInfoKey, "e164") or ""
		local Name = redis.call("HGET", MeetingInfoKey, "name") or ""
		local Bandwidth = redis.call("HGET", MeetingInfoKey, "bandwidth") or ""
		local  StartTime = redis.call("HGET", MeetingInfoKey, "start_time") or ""
		local  StopTime = redis.call("HGET", MeetingInfoKey, "stop_time") or ""
		local Scale = redis.call("HGET", MeetingInfoKey, "scale") or "0"
		local Organizer = redis.call("HGET", MeetingInfoKey, "organizer") or ""
		local NotVisible = redis.call("HGET", MeetingInfoKey, "not_visible") or "off"
		local Encryption = redis.call("HGET", MeetingInfoKey, "encryption") or "none"
		local DontDisturb = redis.call("HGET", MeetingInfoKey, "dont_disturb") or "off"
		local GuestMode = redis.call("HGET", MeetingInfoKey, "guest_mode") or "off"
		local Share = redis.call("HGET", MeetingInfoKey, "share") or "speaker"
		local CallType = redis.call("HGET", MeetingInfoKey, "call_type") or "manual"
		local Format = redis.call("HGET", MeetingInfoKey, "format") or ""
		local Resolution = redis.call("HGET", MeetingInfoKey, "resolution") or ""
		local FrameRate = redis.call("HGET", MeetingInfoKey, "frame") or ""
		local BitRate = redis.call("HGET", MeetingInfoKey, "bitrate") or ""
		local LiveState = redis.call("HGET", MeetingInfoKey, "live_state") or "0"

		local DcsInfoKey = "conf:"..ConfE164List[i]..":dcs_info"
		local DcsStartTime = ""
		local DcsMode = "none"
		local DcsModeStartTime = ""
		if redis.call("EXISTS", DcsInfoKey) == 1 then
			DcsMode = redis.call("HGET", DcsInfoKey, "dcs_mode") or "none"
		end

		-- SCARD meeting:0008933:terminal 
		local MeetingTerminal = "meeting:" .. ConfE164List[i] .. ":terminal"
		local TerminalNum = redis.call("SCARD", MeetingTerminal)

		local MeetingTelphone = "meeting:" .. ConfE164List[i] .. ":telphone"
		local TelphoneNum = redis.call("SCARD", MeetingTelphone)

		local MeetingMeeting = "meeting:" .. ConfE164List[i] .. ":meeting"
		local MeetingNum = redis.call("HLEN", MeetingMeeting)

		local MeetingIP_E164 = "meeting:" .. ConfE164List[i] .. ":ip_e164"
		local IP_E164 = redis.call("SCARD", MeetingIP_E164)

		local MeetingMps = "meeting:" .. ConfE164List[i] .. ":mps"
		local MpsList = redis.call("SMEMBERS", MeetingMps)

		local SmuType
		local SmuMoid = redis.call('GET', 'meeting:'..E164..':smu')
		if (not SmuMoid) then
			SmuType = ''
		else
			SmuType = redis.call('HGET', 'p_server:'..SmuMoid..':info', 'type') or ""
		end

		local  MpsNum = 0
		for j=1,table.getn(MpsList) do
			-- HGET meeting:0008990:mps:0021af57-3339-4afd-849d-c8b24aca55d2:ability vmp_count
			local KeyMpsAbility = "meeting:" .. ConfE164List[i] .. ":mps:" .. MpsList[j] .. ":ability"
			MpsNum = MpsNum + tonumber(redis.call("HGET", KeyMpsAbility, "vmp_count") or 0)
			MpsNum = MpsNum + tonumber(redis.call("HGET", KeyMpsAbility, "mixer_count") or 0)
			MpsNum = MpsNum + tonumber(redis.call("HGET", KeyMpsAbility, "abas_count") or 0)
			MpsNum = MpsNum + tonumber(redis.call("HGET", KeyMpsAbility, "vbas_count") or 0)
		end

		local MeetingInfo = {}
		MeetingInfo["e164"] = E164
		MeetingInfo["machineRoomMoid"] = DomainMoid
		MeetingInfo["domainName"] = DomainName
		MeetingInfo["meetingName"] = Name
		MeetingInfo["bandWidth"] = Bandwidth
		MeetingInfo["startTime"] = StartTime
		MeetingInfo["stopTime"] = StopTime
		MeetingInfo["scale"] = Scale
		MeetingInfo["organizer"] = Organizer
		MeetingInfo["not_visible"] = NotVisible
		MeetingInfo["encryption"] = Encryption
		MeetingInfo["dont_disturb"] = DontDisturb
		MeetingInfo["guest_mode"] = GuestMode
		MeetingInfo["share"] = Share
		MeetingInfo["call_type"] = CallType
		MeetingInfo["format"] = Format
		MeetingInfo["resolution"] = Resolution
		MeetingInfo["frame"] = FrameRate
		MeetingInfo["bitrate"] = BitRate
		MeetingInfo["dcs_mode"] = DcsMode
		MeetingInfo["dcs_start_time"] = DcsStartTime
		MeetingInfo["dcs_mode_start_time"] = DcsModeStartTime
		MeetingInfo["live_state"] = LiveState
		MeetingInfo["terminalNum"] = TerminalNum
		MeetingInfo["telphoneNum"] = TelphoneNum
		MeetingInfo["meetingNum"]  = MeetingNum
		MeetingInfo["externalNum"] = MpsNum
		MeetingInfo["ip_e164_num"] = IP_E164
		MeetingInfo["smu_type"] = SmuType
		table.insert(Result,MeetingInfo)
	end
end

return cjson.encode(Result)
