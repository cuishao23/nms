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

--获取domain资源
local get_platform_domain_res = function(DomainMoid, Result)
	local DomainMachineListKey = 'domain:'..DomainMoid..':machine_room'
	local MachineRoomMoidList = redis.call('SMEMBERS', DomainMachineListKey)
	if table.getn(MachineRoomMoidList) <= 0 then
		return
	end
	for i = 1, table.getn(MachineRoomMoidList) do
		get_machine_room_res(MachineRoomMoidList[i], Result)
	end
end

local get_service_domain_res 
get_service_domain_res = function(DomainMoid, Result)
    get_mp_res(DomainMoid, Result)
    get_g_mp_res(DomainMoid, Result)
end

--moid
local Moid = ARGV[1]

local Type = ""
local KeyMachineRoomInfo = "machine_room:" .. Moid .. ":info"

-- 获取Moid的类型
if 1 == redis.call('EXISTS', KeyMachineRoomInfo) then
    Type = "machine_room"
else
    Type = redis.call("HGET","domain:" .. Moid .. ":info","type")
    if (not Type) then
        Type = ""
    end
end

if Type == 'kernel' then
    local SubKey = "domain:"..Moid..":sub"
    local ServiceList = redis.call("SMEMBERS", SubKey)
    for i=1, #ServiceList do
        get_service_domain_res(ServiceList[i])
    end
elseif Type == 'service' then
    get_service_domain_res(Moid, Result)   
elseif Type == 'platform' then
    get_platform_domain_res(Moid, Result)
elseif Type == 'machine_room' then
    get_machine_room_res(Moid, Result)
elseif Type == 'user' then
    get_user_domain_res(Moid, Result)
end

Result['success'] = 1
Result['total_port'] = math.ceil(Result['total_h264'] + Result['total_h265'] + Result['total_g_h264'] + Result['total_g_h265'])
Result['used_port'] = math.ceil(Result['used_h264'] + Result['used_h265'] + Result['used_g_h264'] + Result['used_g_h265'])

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
