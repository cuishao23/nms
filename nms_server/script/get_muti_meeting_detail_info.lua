local MeetingInfo = {}
local MeetingInfoKey = ARGV[2] .. ":" .. ARGV[1] .. ":info"

if redis.call("HLEN", MeetingInfoKey) ~= 0 then
    MeetingInfo['conf_name'] = redis.call("HGET", MeetingInfoKey, "name") or ""
    MeetingInfo['format'] = redis.call("HGET", MeetingInfoKey, "format") or ""
    MeetingInfo['resolution'] = redis.call("HGET", MeetingInfoKey, "resolution") or ""
    MeetingInfo['bitrate'] = redis.call("HGET", MeetingInfoKey, "bitrate") or ""
    MeetingInfo['encryption'] = redis.call("HGET", MeetingInfoKey, "encryption") or ""
    MeetingInfo['guest_mode'] = redis.call("HGET", MeetingInfoKey, "guest_mode") or ""
    MeetingInfo['call_type'] = redis.call("HGET", MeetingInfoKey, "call_type") or ""
    MeetingInfo['frame'] = redis.call("HGET", MeetingInfoKey, "frame") or ""
    MeetingInfo['experience'] = ""
end

return cjson.encode(MeetingInfo)