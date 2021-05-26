
local Result = {}

local meeting_moid_terminal = 'meeting:' .. ARGV[1] .. ':terminal'
if(0 == redis.call('EXISTS', meeting_moid_terminal)) then
	Result['success'] = 0
	Result['error_code'] = 20003
	return cjson.encode(Result)
end

local TerminalList = redis.call('SMEMBERS', meeting_moid_terminal)
if(0 == table.getn(TerminalList)) then
	Result['success'] = 1
	Result['Terminal'] = {}
	return cjson.encode(Result)
end

Result['success'] = 1
Result['terminals'] = {}

for i,t_e164 in ipairs(TerminalList) do
	local Terminal = {}
	-- 有了正确的e164一定有下面这张表，不用做判断
	local terminal_e164_baseinfo = 'terminal:' .. t_e164 .. ':baseinfo'
	local Moid = redis.call('HGET', terminal_e164_baseinfo, 'moid')
	local terminal_moid_baseinfo = 'terminal:' .. Moid .. ':baseinfo'
	local Type = ''

	Terminal['name'] = redis.call('HGET', terminal_e164_baseinfo, 'name') or ""
	Terminal['e164'] = t_e164

	local Isp = tonumber(redis.call('HGET', terminal_moid_baseinfo, 'operator_type'))
	if(not Isp) then
		Terminal['isp'] = 0
	else
		Terminal['isp'] = Isp
	end

	local terminal_moid_onlinestate = 'terminal:' .. Moid .. ':onlinestate'
	local Keys = redis.call('hkeys', terminal_moid_onlinestate)
	local Vals = redis.call('hvals', terminal_moid_onlinestate)
	for i=1, table.getn(Keys) do
		if(Vals[i] == 'conference') then
			Type = Keys[i]
			Terminal['type'] = Type
			break
		end
	end
	
	local terminal_moid_type_netinfo = 'terminal:' .. Moid .. ':' .. Type .. ':netinfo'
	if(0 == redis.call('EXISTS', terminal_moid_type_netinfo)) then
		Terminal['ip'] = ''
		Terminal['nat_ip'] = ''
	else
		Terminal['ip'] = redis.call('HGET', terminal_moid_type_netinfo, 'ip')
		Terminal['nat_ip'] = redis.call('HGET', terminal_moid_type_netinfo, 'nat_ip')
	end

	local terminal_moid_type_runninginfo = 'terminal:' .. Moid .. ':' .. Type .. ':runninginfo'
	if(0 == redis.call('EXISTS', terminal_moid_type_runninginfo)) then
		Terminal['version'] = ''
	else
		Terminal['version'] = redis.call('HGET', terminal_moid_type_runninginfo, 'version')
	end

	local terminal_moid_meetingdetail = 'terminal:' .. Moid .. ':meetingdetail'
	if(0 == redis.call('EXISTS', terminal_moid_meetingdetail)) then
		Terminal['bitrate'] = 0
	else
		Terminal['bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail, 'conf_bitrate'))
	end

	Terminal['primary_video'] = {}
	Terminal['dual_video'] = {}
	local terminal_moid_meetingdetail_privideo_send_chan = 'terminal:' .. Moid .. ':meetingdetail:privideo_send_chan'
	local terminal_moid_meetingdetail_privideo_recv_chan = 'terminal:' .. Moid .. ':meetingdetail:privideo_recv_chan'
	local terminal_moid_meetingdetail_assvideo_send_chan = 'terminal:' .. Moid .. ':meetingdetail:assvideo_send_chan'
	local terminal_moid_meetingdetail_assvideo_recv_chan = 'terminal:' .. Moid .. ':meetingdetail:assvideo_recv_chan'
	local terminal_moid_meetingdetail_audio_send_chan = 'terminal:' .. Moid .. ':meetingdetail:audio_send_chan'
	local terminal_moid_meetingdetail_audio_recv_chan = 'terminal:' .. Moid .. ':meetingdetail:audio_recv_chan'

	local PriSendList = redis.call('SMEMBERS', terminal_moid_meetingdetail_privideo_send_chan)
	for ii,id in ipairs(PriSendList) do
		local SendRoad = {}
		local RecvRoad = {}
		local terminal_moid_meetingdetail_privideo_send_chan_id = 'terminal:' .. Moid .. ':meetingdetail:privideo_send_chan:' .. id
		local terminal_moid_meetingdetail_privideo_recv_chan_id = 'terminal:' .. Moid .. ':meetingdetail:privideo_recv_chan:' .. id
		local terminal_moid_meetingdetail_audio_send_chan_id = 'terminal:' .. Moid .. ':meetingdetail:audio_send_chan:' .. id
		local terminal_moid_meetingdetail_audio_recv_chan_id = 'terminal:' .. Moid .. ':meetingdetail:audio_recv_chan:' .. id
		SendRoad['chan_id'] = ii
		SendRoad['up_or_down'] = 1
		SendRoad['video_format'] = redis.call('HGET', terminal_moid_meetingdetail_privideo_send_chan_id, 'format') or ""
		SendRoad['video_framerate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_privideo_send_chan_id, 'framerate') or 0)
		SendRoad['video_up_bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_privideo_send_chan_id, 'video_up_bitrate') or 0)
		SendRoad['video_packets_lose'] = 0
		SendRoad['video_packets_loserate'] = 0
		SendRoad['audio_format'] = redis.call('HGET', terminal_moid_meetingdetail_audio_send_chan_id, 'format') or ""
		SendRoad['audio_up_bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_audio_send_chan_id, 'audio_up_bitrate') or 0)
		SendRoad['audio_packets_lose'] = 0
		SendRoad['audio_packets_loserate'] = 0

		RecvRoad['chan_id'] = ii
		RecvRoad['up_or_down'] = 0
		RecvRoad['video_format'] = redis.call('HGET', terminal_moid_meetingdetail_privideo_recv_chan_id, 'format') or ""
		RecvRoad['video_framerate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_privideo_recv_chan_id, 'framerate') or 0)
		RecvRoad['video_down_bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_privideo_recv_chan_id, 'video_down_bitrate') or 0)
		RecvRoad['video_packets_lose'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_privideo_recv_chan_id, 'video_pkts_lose') or 0)
		RecvRoad['video_packets_loserate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_privideo_recv_chan_id, 'video_pkts_loserate') or 0)
		RecvRoad['audio_format'] = redis.call('HGET', terminal_moid_meetingdetail_audio_recv_chan_id, 'format') or ""
		RecvRoad['audio_down_bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_audio_recv_chan_id, 'audio_down_bitrate') or 0)
		RecvRoad['audio_packets_lose'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_audio_recv_chan_id, 'audio_pkts_lose') or 0)
		RecvRoad['audio_packets_loserate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_audio_recv_chan_id, 'audio_pkts_loserate') or 0)
		table.insert(Terminal['primary_video'], SendRoad)
		table.insert(Terminal['primary_video'], RecvRoad)
	end

	local AssSendList = redis.call('SMEMBERS', terminal_moid_meetingdetail_assvideo_send_chan)
	local AssRecvList = redis.call('SMEMBERS', terminal_moid_meetingdetail_assvideo_recv_chan)
	-- print(terminal_moid_meetingdetail_assvideo_recv_chan)
	for ii,id in ipairs(AssSendList) do
		local SendRoad = {}
		local terminal_moid_meetingdetail_assvideo_send_chan_id = 'terminal:' .. Moid .. ':meetingdetail:assvideo_send_chan:' .. id
		SendRoad['chan_id'] = ii
		SendRoad['up_or_down'] = 1
		SendRoad['video_format'] = redis.call('HGET', terminal_moid_meetingdetail_assvideo_send_chan_id, 'format') or ""
		SendRoad['video_framerate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_assvideo_send_chan_id, 'framerate') or 0)
		SendRoad['video_up_bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_assvideo_send_chan_id, 'video_up_bitrate') or 0)
		SendRoad['video_pkts_lose'] = 0
		SendRoad['video_pkts_loserate'] = 0
		table.insert(Terminal['dual_video'], SendRoad)
	end

	for ii,id in ipairs(AssRecvList) do
		local RecvRoad = {}
		local terminal_moid_meetingdetail_assvideo_recv_chan_id = 'terminal:' .. Moid .. ':meetingdetail:assvideo_recv_chan:' .. id
		RecvRoad['chan_id'] = ii
		RecvRoad['up_or_down'] = 0
		RecvRoad['video_format'] = redis.call('HGET', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'format') or ""
		RecvRoad['video_framerate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'framerate') or 0)
		RecvRoad['video_down_bitrate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'video_down_bitrate') or 0)
		RecvRoad['video_pkts_lose'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'video_pkts_lose') or 0)
		RecvRoad['video_pkts_loserate'] = tonumber(redis.call('HGET', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'video_pkts_loserate') or 0)
		table.insert(Terminal['dual_video'], RecvRoad)
	end

	table.insert(Result['terminals'], Terminal)
end

-- print(string.gsub(cjson.encode(Result), "{}", "[]"))
Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result