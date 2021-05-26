local ValueType = ARGV[1]
local Value = ARGV[2]
local t_moid = ""

if ValueType == "e164" then
    t_moid = redis.call('hget', 'terminal:' .. Value .. ':baseinfo', 'moid') or ""
elseif ValueType == "ip" or ValueType == "IP-H323" or ValueType == "ip_sip" then
    t_moid = redis.call('get', "ip:" .. Value .. ":terminal") or ""
    local keys = redis.call('keys','terminal:*:*:netinfo')
    for i = 1,#keys do
        local ip = redis.call('hget',keys[i],'ip') or ''
        if string.find(ip,Value) then
            t_moid = redis.call('hget',keys[i],'moid') or ''
            break
        end
    end
end

local Result = {}
Result['success'] = 1
Result['detail'] = {}

if t_moid ~= "" then
    local Terminal = {}
    local Type = ''

    local terminal_moid_onlinestate = 'terminal:' .. t_moid .. ':onlinestate'
    local Keys = redis.call('hkeys', terminal_moid_onlinestate)
    local Vals = redis.call('hvals', terminal_moid_onlinestate)
    for i=1, table.getn(Keys) do
        if(Vals[i] == 'conference') then
            Type = Keys[i]
            break
        end
    end

    -- 主视频的发送一直存在，
    -- 主视频的接收可以没有（作为发言人的情况下）
    -- 辅视频的接收可以单独存在（其他终端发送双流）
    -- 辅视频的发送可以单独存在（自己发送双流）
    Terminal['primary_video'] = {}
    Terminal['dual_video'] = {}
    local terminal_moid_meetingdetail_privideo_chan = 'terminal:' .. t_moid .. ':meetingdetail:privideo_chan'
    local terminal_moid_meetingdetail_assvideo_chan = 'terminal:' .. t_moid .. ':meetingdetail:assvideo_chan'

    local PriSendList = redis.call('SMEMBERS', terminal_moid_meetingdetail_privideo_chan)
    for ii,id in ipairs(PriSendList) do
        local SendRoad = {}
        local RecvRoad = {}
        local terminal_moid_meetingdetail_privideo_chan_id = 'terminal:' .. t_moid .. ':meetingdetail:privideo_chan:' .. id

        SendRoad['chan_id'] = ii
        SendRoad['up_or_down'] = 1
        SendRoad['video_format'] = redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_video_format') or ""
        -- 为了兼容性考虑，部分终端 上报的为枚举值，部分上报为字符串
        SendRoad['res'] = redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_video_res') or ""
        SendRoad['video_framerate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_video_framerate') or 0)
        SendRoad['video_up_bitrate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_video_bitrate') or 0)
        SendRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_video_pkts_lose') or 0)
        SendRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_video_pkts_lose') or 0)
        SendRoad['audio_format'] = redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_audio_format') or ""
        SendRoad['audio_up_bitrate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_audio_bitrate') or 0)
        SendRoad['audio_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_audio_pkts_lose') or 0)
        SendRoad['audio_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'send_audio_pkts_loserate') or 0)

        RecvRoad['chan_id'] = ii
        RecvRoad['up_or_down'] = 0
        RecvRoad['video_format'] = redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_format') or ""
        RecvRoad['res'] = redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_res') or ""
        RecvRoad['video_framerate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_framerate') or 0)
        RecvRoad['video_down_bitrate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_bitrate') or 0)
        RecvRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_pkts_lose') or 0)
        RecvRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_pkts_loserate') or 0)
        RecvRoad['audio_format'] = redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_video_format') or ""
        RecvRoad['audio_down_bitrate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_audio_bitrate') or 0)
        RecvRoad['audio_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_audio_pkts_lose') or 0)
        RecvRoad['audio_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_privideo_chan_id, 'recv_audio_pkts_loserate') or 0)

        if SendRoad['video_format'] ~= "" then
            table.insert(Terminal['primary_video'], SendRoad)        
        end

        if RecvRoad['video_format'] ~= "" then
            table.insert(Terminal['primary_video'], RecvRoad)      
        end
    end

    local AssSendList = redis.call('SMEMBERS', terminal_moid_meetingdetail_assvideo_chan)

    -- print(terminal_moid_meetingdetail_assvideo_chan)
    for ii,id in ipairs(AssSendList) do
        local SendRoad = {}
        local terminal_moid_meetingdetail_assvideo_chan_id = 'terminal:' .. t_moid .. ':meetingdetail:assvideo_chan:' .. id
        SendRoad['chan_id'] = ii
        SendRoad['up_or_down'] = 1
        SendRoad['video_format'] = redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'send_video_format') or ""
        SendRoad['res'] = redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'send_video_res') or ""
        SendRoad['video_framerate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'send_video_framerate') or 0)
        SendRoad['video_up_bitrate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'send_video_bitrate') or 0)
        SendRoad['send_video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'send_video_pkts_lose') or 0)
        SendRoad['send_video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'send_video_pkts_lose') or 0)

        if SendRoad['video_format'] ~= "" then
            table.insert(Terminal['dual_video'], SendRoad)        
        end

        local RecvRoad = {}
        RecvRoad['chan_id'] = ii
        RecvRoad['up_or_down'] = 0
        RecvRoad['video_format'] = redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'recv_video_format') or ""
        RecvRoad['res'] = redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'recv_video_res') or ""
        RecvRoad['video_framerate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'recv_video_framerate') or 0)
        RecvRoad['video_down_bitrate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'recv_video_bitrate') or 0)
        RecvRoad['video_pkts_lose'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'recv_video_pkts_lose') or 0)
        RecvRoad['video_pkts_loserate'] = tonumber(redis.call('hget', terminal_moid_meetingdetail_assvideo_chan_id, 'recv_video_pkts_loserate') or 0)

        if RecvRoad['video_format'] ~= "" then
            table.insert(Terminal['dual_video'], RecvRoad)        
        end
    end

    Result['detail'] = Terminal
    return string.gsub(cjson.encode(Result), "{}", "[]")
else
    return cjson.encode(Result)
end

