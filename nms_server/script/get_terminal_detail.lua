local KeyOnline = 'terminal:' .. ARGV[1] .. ':onlinestate'
local TerminalTypeList = redis.call('HKEYS', KeyOnline)

local KeyBaseInfo = 'terminal:' .. ARGV[1] .. ':baseinfo'
local Name       = redis.call('HGET',KeyBaseInfo,'name') or ""
local E164       = redis.call('HGET',KeyBaseInfo,'e164') or ""
local DomainMoid = redis.call('HGET',KeyBaseInfo,'domain_moid') or ""

local Result = {}
for i = 1, table.getn(TerminalTypeList) do

	local TerminalInfo = {}
	TerminalInfo['moid'] = ARGV[1]
	TerminalInfo['name'] = Name
	TerminalInfo['e164'] = E164
	TerminalInfo['domain_moid'] = DomainMoid

	--GET termianl online state ---
	TerminalInfo['online_state'] = redis.call('HGET',KeyOnline, TerminalTypeList[i])

	--GET terminal runing info -- 
	local RunningInfo = 'terminal:' .. ARGV[1] .. ':' .. string.gsub(TerminalTypeList[i], " ", "~") .. ':runninginfo'
	TerminalInfo['version']  =  redis.call('HGET',RunningInfo, 'version')  or ""
	TerminalInfo['oem']  =  redis.call('HGET',RunningInfo, 'oem')  or ""
	TerminalInfo['type_ver']     = redis.call('HGET', RunningInfo, "type") or TerminalTypeList[i]
	TerminalInfo['os']       = redis.call('HGET', RunningInfo, 'os') or ""
	TerminalInfo['cpu_type'] = redis.call('HGET', RunningInfo, 'cpu_type') or ""
	TerminalInfo['cpu_freq'] = redis.call('HGET', RunningInfo, 'cpu_freq') or ""
	TerminalInfo['cpu_num']  = redis.call('HGET', RunningInfo, 'cpu_num') or ""
	TerminalInfo['memory']   = redis.call('HGET', RunningInfo, 'memory') or ""
	TerminalInfo['SN']       = redis.call('HGET', RunningInfo, 'SN') or ""
	TerminalInfo['state_secret'] = redis.call('HGET', RunningInfo, 'state_secret') or ""
	TerminalInfo['pkt_loss_resend'] = redis.call('HGET', RunningInfo, 'pkt_loss_resend') or ""
	TerminalInfo['audio_first']     = redis.call('HGET', RunningInfo, 'audio_first') or ""
	TerminalInfo['fec']      = redis.call('HGET', RunningInfo, 'fec') or ""
	TerminalInfo['decode_payload_auto'] = redis.call('HGET', RunningInfo, 'decode_payload_auto') or ""
	TerminalInfo['video_format'] = redis.call('HGET', RunningInfo, 'video_format') or ""

	--GET terminal net info --
	local KeyNetInfo = 'terminal:' .. ARGV[1] .. ':' .. string.gsub(TerminalTypeList[i], " ", "~") .. ':netinfo'
	TerminalInfo['ip']             = redis.call('HGET', KeyNetInfo, 'ip') or ""
	TerminalInfo['nat_ip']         = redis.call('HGET', KeyNetInfo, 'nat_ip') or ""
	TerminalInfo['dns']            = redis.call('HGET', KeyNetInfo, 'dns') or ""
	TerminalInfo['sip_link_protocol'] = redis.call('HGET', KeyNetInfo, 'sip_link_protocol') or ""
	TerminalInfo['aps_domain']     = redis.call('HGET', KeyNetInfo, 'aps_domain') or ""
	TerminalInfo['aps_ip']         = redis.call('HGET', KeyNetInfo, 'aps_ip') or ""
	TerminalInfo['send_bandwidth'] = redis.call('HGET', KeyNetInfo, 'send_bandwidth') or ""
	TerminalInfo['send_droprate']  = redis.call('HGET', KeyNetInfo, 'send_droprate') or ""
	TerminalInfo['recv_bandwidth'] = redis.call('HGET', KeyNetInfo, 'recv_bandwidth') or ""
	TerminalInfo['recv_droprate']  = redis.call('HGET', KeyNetInfo, 'recv_droprate') or ""

	-- 由于终端注册pas的时间晚于注册平台的时间
    -- 因此只能从terminal:{dev_moid}:{dev_type}:connection获取pas的地址，即reg_addr的地址
	TerminalInfo['reg_addr'] = redis.call('HGET', "terminal:" .. ARGV[1] .. ":" .. string.gsub(TerminalTypeList[i], " ", "~") .. ":connection", 'PAS') or ""

	Result[i] = TerminalInfo
end

return cjson.encode(Result)