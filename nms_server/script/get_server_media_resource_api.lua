local Result = {}

--h264媒体端口数
Result['total_h264'] = 0
Result['used_h264'] = 0

--国密h264媒体端口数
Result['total_g_h264'] = 0
Result['used_g_h264'] = 0

--h265媒体端口数
Result['total_h265'] = 0
Result['used_h265'] = 0

--国密h265媒体端口数
Result['total_g_h265'] = 0
Result['used_g_h265'] = 0

local function secureTransform(numberOrString)
    if (type(numberOrString) == "nil") then
        return 0
    end

    return numberOrString
end

local get_mp_res = function(domainMoid, Result)
    --媒体资源
    local MpMachineRoomKey = 'domain:'..domainMoid..':mp'
    local H264Total = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'total_h264') or 0))
    Result['total_h264'] = Result['total_h264'] + H264Total

    local H264Used = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'used_h264') or 0))
    Result['used_h264'] = Result['used_h264'] + H264Used
    
    local H265Total = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'total_h265') or 0))
    Result['total_h265'] = Result['total_h265'] + H265Total
   
    local H265Used = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'used_h265') or 0))
    Result['used_h265'] = Result['used_h265'] + H265Used
end

--国密媒体资源
local get_g_mp_res = function(domainMoid, Result)
    local GMpMachineRoomKey = 'domain:'..domainMoid..':g_mp'
    local H264Total = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'total_h264') or 0))
    Result['total_g_h264'] = Result['total_g_h264'] + H264Total

    local H264Used = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'used_h264') or 0))
    Result['used_g_h264'] = Result['used_g_h264'] + H264Used
    
    local H265Total = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'total_h265') or 0))
    Result['total_g_h265'] = Result['total_g_h265'] + H265Total
    
    local H265Used = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'used_h265') or 0))
    Result['used_g_h265'] = Result['used_g_h265'] + H265Used
end

--获取用户域资源列表
local get_user_domain_res = function(domainMoid, Result)
    get_mp_res(domainMoid, Result)
    get_g_mp_res(domainMoid, Result)
end

--获取机房资源列表（用户域下资源叠加）
local get_machine_room_res = function(MachineRoomMoid, Result)
	local DomainMachineListKey = 'machine_room:'..MachineRoomMoid..':domain'
	local UserDomainMoidList = redis.call('SMEMBERS', DomainMachineListKey)
	if table.getn(UserDomainMoidList) <= 0 then
		return
	end
	for i = 1, table.getn(UserDomainMoidList) do
		get_user_domain_res(UserDomainMoidList[i],Result)
    end
end

local LMoid = ARGV[1]

local ServerKey = 'l_server:'..LMoid..':info'
if 1 == redis.call('EXISTS', ServerKey) then
    local MachineRoomMoid = redis.call('HGET', ServerKey, 'machine_room_moid') or ''
    get_machine_room_res(MachineRoomMoid,Result)

    Result['success'] = 1
    Result['total_port'] = math.ceil(Result['total_h264'] + Result['total_h265'] + Result['total_g_h264'] + Result['total_g_h265'])
    Result['used_port'] = math.ceil(Result['used_h264'] + Result['used_h265'] + Result['used_g_h264'] + Result['used_g_h265'])
else
    Result['success'] = 0
    Result['error_code'] = 20401
end

-- 移除无用的字段
Result['total_h264'] = nil
Result['used_h264'] = nil
Result['total_g_h264'] = nil
Result['used_g_h264'] = nil
Result['total_h265'] = nil
Result['used_h265'] = nil
Result['total_g_h265'] = nil
Result['used_g_h265'] = nil

return cjson.encode(Result)