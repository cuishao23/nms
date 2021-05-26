local TerminalInfo = {}
local Key = "terminal:" .. ARGV[1] .. ":baseinfo"
local Moid = redis.call("HGET", Key, "moid")

TerminalInfo["moid"] = Moid
TerminalInfo['tamper'] = 'no'

local TerminalInfoKey = "terminal:" .. Moid .. ":baseinfo"
if redis.call("HLEN", TerminalInfoKey) ~= 0 then
    
    TerminalInfo["e164"] = redis.call("HGET", TerminalInfoKey, "e164") or ""
    TerminalInfo["name"] = redis.call("HGET", TerminalInfoKey, "name") or ""
    TerminalInfo['operator'] = redis.call("HGET", TerminalInfoKey, "operator_type") or ""

    local MeetingInfoKey = "terminal:" .. Moid .. ":meetingdetail"
    if redis.call("HLEN", MeetingInfoKey) ~= 0 then
        local MtType = redis.call("HGET", MeetingInfoKey, "mt_type") or ""
        TerminalInfo['mt_type'] = MtType
        TerminalInfo['conf_e164'] = redis.call("HGET", MeetingInfoKey, "conf_e164") or ""
        TerminalInfo['conf_bitrate'] = redis.call("HGET", MeetingInfoKey, "conf_bitrate") or ""
        TerminalInfo['encryption'] = redis.call("HGET", MeetingInfoKey, "encryption") or ""
        TerminalInfo['mute'] = redis.call("HGET", MeetingInfoKey, "mute") or ""
        TerminalInfo['dumbness'] = redis.call("HGET", MeetingInfoKey, "dumbness") or ""
 
        local NetInfoKey = "terminal:" .. Moid .. ":" .. string.gsub(MtType, " ", "~") .. ":netinfo"
        TerminalInfo['mt_ip'] = redis.call("HGET", NetInfoKey, "ip") or ""
        TerminalInfo['nat_ip'] = redis.call("HGET", NetInfoKey, "nat_ip") or ""

        --GET terminal runing info -- 
        local RunningInfo = 'terminal:' .. Moid .. ':' .. string.gsub(MtType, " ", "~") .. ':runninginfo'
        TerminalInfo['version']  =  redis.call('HGET',RunningInfo, 'version')  or ""
    end
end

return cjson.encode(TerminalInfo)