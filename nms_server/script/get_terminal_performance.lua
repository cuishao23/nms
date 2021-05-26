local KeyOnline = 'terminal:' .. ARGV[1] .. ':onlinestate'
local Online = redis.call('HGET',KeyOnline, ARGV[2]) or ""

local KeyBaseInfo = 'terminal:' .. ARGV[1] .. ':baseinfo'
local Name = redis.call('HGET',KeyBaseInfo,'name') or ""
local DomainMoid = redis.call('HGET',KeyBaseInfo,'domain_moid') or ""

local DomainBaseInfo = 'domain:' .. DomainMoid .. ':info'
local DomainMoidName = redis.call('HGET',DomainBaseInfo,'name') or ""

local RunningInfo = 'terminal:' .. ARGV[1] .. ':' .. string.gsub(ARGV[2], " ", "~") .. ':runninginfo'
local Version = redis.call('HGET',RunningInfo, 'version')  or ""
local SN = redis.call('HGET', RunningInfo, 'SN') or ""

local TerminalInfo = {}
TerminalInfo['name'] = Name
TerminalInfo['online_state'] = Online
TerminalInfo['domain_name'] = DomainMoidName
TerminalInfo['version'] = Version
TerminalInfo['SN'] = SN

return cjson.encode(TerminalInfo)