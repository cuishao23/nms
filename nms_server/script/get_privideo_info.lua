local PriVideoInfo = {}
local Key = "terminal:" .. ARGV[1] .. ":baseinfo"
local Moid = redis.call("HGET", Key, "moid")

local KeyChannel = "terminal:" .. Moid .. ":meetingdetail:privideo_chan"
local ChannelList = redis.call('SMEMBERS', KeyChannel)

for i = 1,table.getn(ChannelList) do
    local InfoKey = "terminal:" .. Moid .. ":meetingdetail:privideo_chan:" .. ChannelList[i]

    local VideoInfo = {}
    VideoInfo['channel_id'] = ChannelList[i]
    VideoInfo['send_video_format'] = redis.call("HGET", InfoKey, "send_video_format") or "" --发送视屏格式
    VideoInfo['send_video_res'] = redis.call("HGET", InfoKey, "send_video_res") or ""--发送视频分辨率
    VideoInfo['send_video_framerate'] = redis.call("HGET", InfoKey, "send_video_framerate") or ""--发送视屏频率
    VideoInfo['send_video_bitrate'] = redis.call("HGET", InfoKey, "send_video_bitrate") or ""--发送视屏码率
    VideoInfo['send_video_pkts_lose'] = redis.call("HGET", InfoKey, "send_video_pkts_lose") or ""--发送视屏丢包总数
    VideoInfo['send_video_pkts_loserate'] = redis.call("HGET", InfoKey, "send_video_pkts_loserate") or ""--发送视屏丢包率
    VideoInfo['send_video_resource_exist'] = redis.call("HGET", InfoKey, "send_video_resource_exist") or ""--有无视屏源
    VideoInfo['recv_video_format'] = redis.call("HGET", InfoKey, "recv_video_format") or ""--接收视屏格式
    VideoInfo['recv_video_res'] = redis.call("HGET", InfoKey, "recv_video_res") or ""--接收视频分辨率
    VideoInfo['recv_video_framerate'] = redis.call("HGET", InfoKey, "recv_video_framerate") or ""--接收视屏频率
    VideoInfo['recv_video_bitrate'] = redis.call("HGET", InfoKey, "recv_video_bitrate") or ""--接收视屏码率
    VideoInfo['recv_video_pkts_loserate'] = redis.call("HGET", InfoKey, "recv_video_pkts_loserate") or ""--接收视屏丢包率
    VideoInfo['recv_video_pkts_lose'] = redis.call("HGET", InfoKey, "recv_video_pkts_lose") or ""--接收视屏丢包总数
    VideoInfo['send_audio_format'] = redis.call("HGET", InfoKey, "send_audio_format") or ""--发送音频格式
    VideoInfo['send_audio_pkts_lose'] = redis.call("HGET", InfoKey, "send_audio_pkts_lose") or ""--发送音频丢包总数
    VideoInfo['send_audio_pkts_loserate'] = redis.call("HGET", InfoKey, "send_audio_pkts_loserate") or ""--发送音频丢包率
    VideoInfo['send_audio_bitrate'] = redis.call("HGET", InfoKey, "send_audio_bitrate") or ""--发送音频码率
    VideoInfo['recv_audio_format'] = redis.call("HGET", InfoKey, "recv_audio_format") or ""--接收音频格式
    VideoInfo['recv_audio_pkts_lose'] = redis.call("HGET", InfoKey, "recv_audio_pkts_lose") or ""--接收音频丢包总数
    VideoInfo['recv_audio_pkts_loserate'] = redis.call("HGET", InfoKey, "recv_audio_pkts_loserate") or ""--接收音频丢包率
    VideoInfo['recv_audio_bitrate'] = redis.call("HGET", InfoKey, "recv_audio_bitrate") or ""--接收音频码率
    table.insert(PriVideoInfo,VideoInfo)
end

return cjson.encode(PriVideoInfo)