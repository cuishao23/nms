local Result = {}

local key_terminal_pfm_info = 'terminal:'..ARGV[1]..':'..ARGV[2]..':pfm_info'
local key_terminal_netcards = 'terminal:'..ARGV[1]..':'..ARGV[2]..':netcards'
local key_terminal_video = 'terminal:'..ARGV[1]..':'..ARGV[2]..':video'
local key_terminal_microphone = 'terminal:'..ARGV[1]..':'..ARGV[2]..':microphone'
local key_terminal_loudspeaker = 'terminal:'..ARGV[1]..':'..ARGV[2]..':loudspeaker'

local key_audio_input_sign = 'terminal:'..ARGV[1]..':audio_input_sign'
local key_audio_output_sign = 'terminal:'..ARGV[1]..':audio_output_sign'
local key_video_input_sign = 'terminal:'..ARGV[1]..':video_input_sign'
local key_video_output_sign = 'terminal:'..ARGV[1]..':video_output_sign'

local key_terminal_meetingdetail = 'terminal:'..ARGV[1]..':meetingdetail'

local key_terminal_netinfo = 'terminal:'..ARGV[1]..':'..ARGV[2]..':netinfo'
-- V6.0版本需要增加终端网络丢包率和码流丢包率的字段上报，由于这些字段已定义，为了保证数据的实时性，终端收到EV_PFMINFO_REQ诊断消息后，除了上报EV_PFMINFO_MSG外，需要上报一下EV_BANDWIDTH_MSG（网络丢包率），如果在会的话，就再加一次EV_CONF_INFO（码流丢包率）
-- 因此需通过时间戳判断是否是最新的消息
local Time = redis.call('TIME')
local netInfoTimeStamp = redis.call("HGET",key_terminal_netinfo,'timestamp') or 0

if ( redis.call('EXISTS', key_terminal_pfm_info) == 0 ) and tonumber(Time[1]) - tonumber(netInfoTimeStamp) > 60 then
	local RetData = {}
	RetData['success'] = 1
	RetData['state'] = {}
	return cjson.encode(RetData)
end

Result['cpu_userate'] = tonumber(redis.call('hget', key_terminal_pfm_info, 'cpu_userate') or '0')
Result['mem_userate'] = tonumber(redis.call('hget', key_terminal_pfm_info, 'mem_userate') or '0')
Result['netcardcount'] = tonumber(redis.call('hget', key_terminal_pfm_info, 'netcardcount') or '0')
Result['master_chip_status'] = tonumber(redis.call('hget', key_terminal_pfm_info, 'master_chip_status') or '0')
Result['temperature_status'] = tonumber(redis.call('hget', key_terminal_pfm_info, 'temperature_status') or '0')

Result['netcards'] = {}
for i, netcard_name in ipairs(redis.call('smembers', key_terminal_netcards)) do
	table.insert(Result['netcards'], netcard_name)
	Result[netcard_name..'_sendkbps'] = tonumber(redis.call('hget', key_terminal_pfm_info, netcard_name..'_sendkbps') or '0')
	Result[netcard_name..'_recvkbps'] = tonumber(redis.call('hget', key_terminal_pfm_info, netcard_name..'_recvkbps') or '0')
end

Result['video'] = {}
for i, video_name in ipairs(redis.call('smembers', key_terminal_video)) do
	local video = {}
	video['name'] = video_name
	video['type'] = redis.call('hget', 'terminal:'..ARGV[1]..':'..ARGV[2]..':video:'..video_name..':info', 'type')
	table.insert(Result['video'], video)
end

Result['microphone'] = {}
for i, microphone_name in ipairs(redis.call('smembers', key_terminal_microphone)) do
	local microphone = {}
	microphone['name'] = microphone_name
	microphone['status'] = tonumber(redis.call('hget', 'terminal:'..ARGV[1]..':'..ARGV[2]..':microphone:'..microphone_name..':info', 'status') or '0')
	table.insert(Result['microphone'], microphone)
end

Result['loudspeaker'] = {}
for i, loudspeaker_name in ipairs(redis.call('smembers', key_terminal_loudspeaker)) do
	local loudspeaker = {}
	loudspeaker['name'] = loudspeaker_name
	loudspeaker['status'] = tonumber(redis.call('hget', 'terminal:'..ARGV[1]..':'..ARGV[2]..':loudspeaker:'..loudspeaker_name..':info', 'status') or '0')
	table.insert(Result['loudspeaker'], loudspeaker)
end

Result['audio_input_sign'] = {}
for i, key in ipairs(redis.call('hkeys', key_audio_input_sign)) do
	local audio_input_sign = {}
	audio_input_sign['type'] = key
	audio_input_sign['status'] = tonumber(redis.call('hget', key_audio_input_sign, key) or '0')
	table.insert(Result['audio_input_sign'], audio_input_sign)
end

Result['audio_output_sign'] = {}
for i, key in ipairs(redis.call('hkeys', key_audio_output_sign)) do
	local audio_output_sign = {}
	audio_output_sign['type'] = key
	audio_output_sign['status'] = tonumber(redis.call('hget', key_audio_output_sign, key) or '0')
	table.insert(Result['audio_output_sign'], audio_output_sign)
end

Result['video_input_sign'] = {}
for i, key in ipairs(redis.call('hkeys', key_video_input_sign)) do
	local video_input_sign = {}
	video_input_sign['type'] = key
	video_input_sign['status'] = tonumber(redis.call('hget', key_video_input_sign, key) or '0')
	table.insert(Result['video_input_sign'], video_input_sign)
end

Result['video_output_sign'] = {}
for i, key in ipairs(redis.call('hkeys', key_video_output_sign)) do
	local video_output_sign = {}
	video_output_sign['type'] = key
	video_output_sign['status'] = tonumber(redis.call('hget', key_video_output_sign, key) or '0')
	table.insert(Result['video_output_sign'], video_output_sign)
end

Result['input_volume'] = tonumber(redis.call('hget', key_terminal_meetingdetail, 'input_volume') or '0')
if not(Result['input_volume']) then
	Result['input_volume'] = 0
end

Result['output_volume'] = tonumber(redis.call('hget', key_terminal_meetingdetail, 'output_volume') or '0')
if not(Result['output_volume']) then
	Result['output_volume'] = 0
end

Result['upload_drop_rate'] = tonumber(redis.call('hget', key_terminal_netinfo, 'send_droprate') or '0')
Result['download_drop_rate'] = tonumber(redis.call('hget', key_terminal_netinfo, 'recv_droprate') or '0')

-- 码流丢包率
Result['primary_video'] = {}
Result['dual_video'] = {}
local terminal_moid_meetingdetail_privideo_send_chan = 'terminal:' .. ARGV[1] .. ':meetingdetail:privideo_send_chan'
local terminal_moid_meetingdetail_privideo_recv_chan = 'terminal:' .. ARGV[1] .. ':meetingdetail:privideo_recv_chan'
local terminal_moid_meetingdetail_assvideo_send_chan = 'terminal:' .. ARGV[1] .. ':meetingdetail:assvideo_send_chan'
local terminal_moid_meetingdetail_assvideo_recv_chan = 'terminal:' .. ARGV[1] .. ':meetingdetail:assvideo_recv_chan'
local terminal_moid_meetingdetail_audio_send_chan = 'terminal:' .. ARGV[1] .. ':meetingdetail:audio_send_chan'
local terminal_moid_meetingdetail_audio_recv_chan = 'terminal:' .. ARGV[1] .. ':meetingdetail:audio_recv_chan'

local PriSendList = redis.call('SMEMBERS', terminal_moid_meetingdetail_privideo_send_chan)
for ii,id in ipairs(PriSendList) do
	local DetailInfo = {}
	local SendRoad = {}
	local RecvRoad = {}
	local terminal_moid_meetingdetail_privideo_send_chan_id = 'terminal:' .. ARGV[1] .. ':meetingdetail:privideo_send_chan:' .. id
	local terminal_moid_meetingdetail_privideo_recv_chan_id = 'terminal:' .. ARGV[1] .. ':meetingdetail:privideo_recv_chan:' .. id
	local terminal_moid_meetingdetail_audio_send_chan_id = 'terminal:' .. ARGV[1] .. ':meetingdetail:audio_send_chan:' .. id
	local terminal_moid_meetingdetail_audio_recv_chan_id = 'terminal:' .. ARGV[1] .. ':meetingdetail:audio_recv_chan:' .. id
	DetailInfo['chan_id'] = tonumber(id or '0')
	DetailInfo['video_resource_exist'] = 0

	SendRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_send_chan_id, 'video_pkts_lose') or 0)
	SendRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_send_chan_id, 'video_pkts_loserate')or 0)
	SendRoad['audio_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_audio_send_chan_id, 'audio_pkts_lose') or 0)
	SendRoad['audio_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_audio_send_chan_id, 'audio_pkts_loserate') or 0)

	DetailInfo['video_resource_exist'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_send_chan_id, 'video_resource_exist') or 0)	

	RecvRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_recv_chan_id, 'video_pkts_lose') or 0)
	RecvRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_recv_chan_id, 'video_pkts_loserate') or 0)
	RecvRoad['audio_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_audio_recv_chan_id, 'audio_pkts_lose') or 0)
	RecvRoad['audio_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_audio_recv_chan_id, 'audio_pkts_loserate') or 0)

	DetailInfo['send_info'] = SendRoad
	DetailInfo['recv_info'] = RecvRoad
	table.insert(Result['primary_video'], DetailInfo)
end

local AssSendList = redis.call('SMEMBERS', terminal_moid_meetingdetail_assvideo_send_chan)
local AssRecvList = redis.call('SMEMBERS', terminal_moid_meetingdetail_assvideo_recv_chan)
-- print(terminal_moid_meetingdetail_assvideo_recv_chan)
for ii,id in ipairs(AssRecvList) do
	local DetailInfo = {}
	local SendRoad = {}
	local RecvRoad = {}
	DetailInfo['chan_id'] = tonumber(id or '0')

	local terminal_moid_meetingdetail_assvideo_send_chan_id = 'terminal:' .. ARGV[1] .. ':meetingdetail:assvideo_send_chan:' .. id
	
	SendRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_send_chan_id, 'video_pkts_lose') or 0)
	SendRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_send_chan_id, 'video_pkts_loserate') or 0)
	DetailInfo['video_resource_exist'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_send_chan_id, 'video_resource_exist') or 0)	


	local terminal_moid_meetingdetail_assvideo_recv_chan_id = 'terminal:' .. ARGV[1] .. ':meetingdetail:assvideo_recv_chan:' .. id

	RecvRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'video_pkts_lose'))
	RecvRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_recv_chan_id, 'video_pkts_loserate'))
	
	DetailInfo['send_info'] = SendRoad
	DetailInfo['recv_info'] = RecvRoad
	table.insert(Result['dual_video'], DetailInfo)
end

local RetData = {}
RetData['success'] = 1
RetData['state'] = Result

return string.gsub(cjson.encode(RetData), "{}", "[]")