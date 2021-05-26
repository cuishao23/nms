local TerminalType = 'terminal:' .. ARGV[1] .. ':onlinestate'
local TerminalTypeList = redis.call('HKEYS', TerminalType)

local Result = {}
Result['moid'] = ARGV[1]
Result['cameras'] = {}
Result['microphones'] = {}
Result['imixes'] = {}
for i = 1, table.getn(TerminalTypeList) do
	
	--GET terminal camera info --
    local CameraListKey = 'terminal:' .. ARGV[1] .. ':' .. string.gsub(TerminalTypeList[i], " ", "~") .. ':peripheral:camera'

    local IdList = redis.call("SMEMBERS", CameraListKey)
    for j = 1, #IdList do
        local cameraInfoKey = 'peripheral:camera:' .. IdList[j] .. ':info'
        local cameraInfo = {}
        cameraInfo['id'] = IdList[j] 
        cameraInfo['type'] = redis.call("HGET", cameraInfoKey,'type') or "" 
        cameraInfo['SN'] = redis.call("HGET", cameraInfoKey,'SN') or "" 
        cameraInfo['version'] = redis.call("HGET", cameraInfoKey,'version') or ""
        cameraInfo['status'] = redis.call("HGET", cameraInfoKey,'status') or ""
        cameraInfo['name'] = redis.call("HGET", cameraInfoKey,'name') or ""

        table.insert(Result['cameras'],cameraInfo)
    end
    
	--GET terminal microphone info --
    local MicrophoneListKey = 'terminal:' .. ARGV[1] .. ':' .. string.gsub(TerminalTypeList[i], " ", "~") .. ':peripheral:microphone'

    IdList = redis.call("SMEMBERS", MicrophoneListKey)
    for j = 1, #IdList do
        local microphoneInfoKey = 'peripheral:microphone:' .. IdList[j] .. ':info'
        local microphoneInfo = {}
        microphoneInfo['id'] = IdList[j] 
        microphoneInfo['type'] = redis.call("HGET", microphoneInfoKey,'type') or "" 
        microphoneInfo['version'] = redis.call("HGET", microphoneInfoKey,'version') or "" 
        microphoneInfo['status'] = redis.call("HGET", microphoneInfoKey,'status') or ""
        microphoneInfo['name'] = redis.call("HGET", microphoneInfoKey,'name') or ""

        table.insert(Result['microphones'],microphoneInfo)
    end

    --Get terminal imix info
    local ImixListKey = 'terminal:'..ARGV[1]..':'..string.gsub(TerminalTypeList[i], " ", "~").. ':peripheral:imix'
    local ImixList = redis.call('SMEMBERS', ImixListKey)
    for j = 1, #ImixList do
        local ImixKey = 'peripheral:imix:'..ImixList[j]..':info'
        local ImixInfo = {}
        ImixInfo['type'] = redis.call('HGET', ImixKey, 'type') or ''
        ImixInfo['sn'] = redis.call('HGET', ImixKey, 'sn') or ''
        ImixInfo['mac'] = redis.call('HGET', ImixKey, 'mac') or ''
        ImixInfo['ip'] = redis.call('HGET', ImixKey, 'ip') or ''
        ImixInfo['version'] = redis.call('HGET', ImixKey, 'version') or ''
        ImixInfo['status'] = redis.call('HGET', ImixKey, 'status') or ''
        ImixInfo['name'] = redis.call('HGET', ImixKey, 'name') or ''

        table.insert(Result['imixes'], ImixInfo)
    end
end

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result