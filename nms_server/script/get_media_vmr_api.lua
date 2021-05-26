local Result = {}

--接入端口数
local Access = {}
Result["access"] = Access
Access['ap_total'] = 0
Access['ap_used'] = 0
--国密接入端口数
Access['g_ap_total'] = 0
Access['g_ap_used'] = 0

--h264媒体端口数
local Media = {}
Result["media"] = Media
Media['total_h264'] = 0
Media['used_h264'] = 0

--国密h264媒体端口数
Media['total_g_h264'] = 0
Media['used_g_h264'] = 0

--h265媒体端口数
Media['total_h265'] = 0
Media['used_h265'] = 0

--国密h265媒体端口数
Media['total_g_h265'] = 0
Media['used_g_h265'] = 0

--dcs数量统计
local Dcs = {}
Result["dcs"] = Dcs
Dcs['max_conf_num'] = 0 --最大会议数
Dcs['conf_num'] = 0     --实时会议数
Dcs['max_mt_num'] = 0   --最大会议终端数
Dcs['mt_num'] = 0       --实时会议终端数

--虚拟会议室
local Vmr = {}
Result["vmr"] = Vmr
Vmr['env_type'] = 0
Vmr['total_192_1080'] = 0
Vmr['used_192_1080'] = 0
Vmr['total_192_720'] = 0
Vmr['used_192_720'] = 0
Vmr['total_64_1080'] = 0
Vmr['used_64_1080'] = 0
Vmr['total_64_720'] = 0
Vmr['used_64_720'] = 0
Vmr['total_32_1080'] = 0
Vmr['used_32_1080'] = 0
Vmr['total_32_720'] = 0
Vmr['used_32_720'] = 0
Vmr['total_8_1080'] = 0
Vmr['used_8_1080'] = 0
Vmr['total_8_720'] = 0
Vmr['used_8_720'] = 0
Vmr['used_large'] = 0
Vmr['total_large'] = 0
Vmr['used_small'] = 0
Vmr['total_small'] = 0

--vrs资源
local Vrs = {}
Result["vrs"] = Vrs
Vrs['recroomocp'] = 0
Vrs['recroomtotal'] = 0
Vrs['html5lcastocp'] = 0
Vrs['html5lcasttotal'] = 0
Vrs['lcastocp'] = 0
Vrs['lcasttotal'] = 0

--媒体资源
Media['total_vmp'] = 0
Media['used_vmp'] = 0
Media['total_mixer'] = 0
Media['used_mixer'] = 0

--传统会议资源
local Tra = {}
Result["tra_meeting"] = Tra
Tra['used'] = 0
Tra['total'] = 0
Tra['other'] = 0
Tra['remainder'] = 0
Tra['port_used'] = 0

--端口会议资源
local Port = {}
Result['port_meeting'] = Port
Port['used'] = 0
Port['total'] = 0
Port['other'] = 0
Port['remainder'] = 0
Port['tra_used'] = 0

--sfu会议资源(根据带宽计算)
local Sfu = {}
Result['sfu_meeting'] = Sfu
Sfu['used'] = 0         --已接入终端数
Sfu['total'] = 0    
Sfu['remainder'] = 0    --剩余可接入终端数

local function secureTransform(numberOrString)
    if (type(numberOrString) == "nil") then
        return 0
    end

    return numberOrString
end

--获取服务域下召开的传统会议和端口会议数量==>所属用户域加起来
local get_service_domain_tra_meeting_res = function(ServiceDomainMoid)
    if ServiceDomainMoid == nil then
        return
    end
    --获取服务域下所有用户域domain
    local UserDomainList = {}
    local SubDomainKey = 'domain:'..ServiceDomainMoid..':sub'
    if 1 == redis.call('EXISTS', SubDomainKey) then
        local SubDomainList = redis.call('SMEMBERS', SubDomainKey)
        if SubDomainList ~= nil then
            for i = 1, #SubDomainList do
                local SubDomain = SubDomainList[i]
                if SubDomain ~= nil then
                    local SubDomainInfoKey = 'domain:'..SubDomain..':info'
                    local Type = redis.call('HGET', SubDomainInfoKey, 'type')
                    --用户域moid加进列表作为key
                    if Type == 'user' then
                        -- 遍历全部传统会议
                        local TMeetingE164List = redis.call('SMEMBERS', 'domain:'..SubDomain..':t_meeting')
                        if TMeetingE164List ~= nil then
                            for i = 1, #TMeetingE164List do
                                if TMeetingE164List[i] ~= nil then
                                    local TMeetingKey = 'conf_res:'..TMeetingE164List[i]..':info'
                                    if 1 == redis.call('EXISTS', TMeetingKey) then
                                        local TraNum = tonumber(redis.call('HGET', TMeetingKey, 'tra') or 0)
                                        local PortNum = tonumber(redis.call('HGET', TMeetingKey, 'port') or 0)
                                        Tra['used'] = Tra['used'] + TraNum
                                        Port['other'] = Port['other'] + PortNum
                                    end
                                end
                            end
                        end
                        -- 遍历全部端口会议
                        local PMeetingE164List = redis.call('SMEMBERS', 'domain:'..SubDomain..':p_meeting')
                        if PMeetingE164List ~= nil then
                            for i = 1, #PMeetingE164List do
                                if PMeetingE164List[i] ~= nil then
                                    local PMeetingKey = 'conf_res:'..PMeetingE164List[i]..':info'
                                    if 1 == redis.call('EXISTS', PMeetingKey) then
                                        local TraNum = tonumber(redis.call('HGET', PMeetingKey, 'tra') or 0)
                                        local PortNum = tonumber(redis.call('HGET', PMeetingKey, 'port') or 0)
                                        Port['used'] = Port['used'] + PortNum
                                        Tra['other'] = Tra['other'] + TraNum
                                    end
                                end
                            end
                        end

                        -- 遍历全部混合会议
                        local PMeetingE164List = redis.call('SMEMBERS', 'domain:'..SubDomain..':mix_meeting')
                        if PMeetingE164List ~= nil then
                            for i = 1, #PMeetingE164List do
                                if PMeetingE164List[i] ~= nil then
                                    local MixMeetingKey = 'conf_res:'..PMeetingE164List[i]..':info'
                                    if 1 == redis.call('EXISTS', MixMeetingKey) then
                                        local TraNum = tonumber(redis.call('HGET', MixMeetingKey, 'tra') or 0)
                                        local PortNum = tonumber(redis.call('HGET', MixMeetingKey, 'port') or 0)
                                        Port['other'] = Port['other'] + PortNum
                                        Tra['other'] = Tra['other'] + TraNum
                                    end
                                end
                            end
                        end                      
                    end
                end
            end
        end
    end
end

local get_vrs_res = function(MachineRoomMoid)
    local LogicalServerKey = 'machine_room:'..MachineRoomMoid..':l_server'
    local LogicalServerList = redis.call('SMEMBERS', LogicalServerKey)
    if LogicalServerList == nil or table.getn(LogicalServerList) == 0 then
        return
    end
    for i = 1, table.getn(LogicalServerList) do
        local InfoKey = 'l_server:'..LogicalServerList[i]..':info'
        local Type = redis.call('HGET', InfoKey, 'type')
        if Type ~= nil and type(Type) == 'string' then
            Type = string.lower(Type)
            if 'vrs' == string.sub(Type, 1, 3) then
                local VrsAbilityKey = 'vrs:'..LogicalServerList[i]..':ability'
                Vrs['recroomocp'] = Vrs['recroomocp'] + secureTransform(tonumber(redis.call('HGET', VrsAbilityKey, 'recroomocp') or 0))
                Vrs['recroomtotal'] = Vrs['recroomtotal'] + secureTransform(tonumber(redis.call('HGET', VrsAbilityKey, 'recroomtotal') or 0))
                Vrs['html5lcastocp'] = Vrs['html5lcastocp'] + secureTransform(tonumber(redis.call('HGET', VrsAbilityKey, 'html5lcastocp') or 0))
                Vrs['html5lcasttotal'] = Vrs['html5lcasttotal'] + secureTransform(tonumber(redis.call('HGET', VrsAbilityKey, 'html5lcasttotal') or 0))
                Vrs['lcastocp'] = Vrs['lcastocp'] + secureTransform(tonumber(redis.call('HGET', VrsAbilityKey, 'lcastocp') or 0))
                Vrs['lcasttotal'] = Vrs['lcasttotal'] + secureTransform(tonumber(redis.call('HGET', VrsAbilityKey, 'lcasttotal') or 0))
            end
        end
    end
end

local get_dcs_res = function(MachineRoomMoid)
    local MachineRoomDcsKey = 'machine_room:'..MachineRoomMoid..':dcs'
    local DcsMoidList = redis.call('SMEMBERS', MachineRoomDcsKey)
    if DcsMoidList == nil or table.getn(DcsMoidList) == 0 then
        return
    end
    for i = 1, table.getn(DcsMoidList) do
        local ResKey = 'dcs:'..DcsMoidList[i]..':resource'
        Dcs['max_conf_num'] = Dcs['max_conf_num'] + secureTransform(tonumber(redis.call('HGET', ResKey, 'max_conf_num') or 0))
        Dcs['conf_num'] = Dcs['conf_num'] + secureTransform(tonumber(redis.call('HGET', ResKey, 'conf_num') or 0))
        Dcs['max_mt_num'] = Dcs['max_mt_num'] + secureTransform(tonumber(redis.call('HGET', ResKey, 'max_mt_num') or 0))
        Dcs['mt_num'] = Dcs['mt_num'] + secureTransform(tonumber(redis.call('HGET', ResKey, 'mt_num') or 0))
    end
end

--获取接入资源信息
local get_ap_res = function(DomainMoid)
    --接入端口
    local ApMachineRoomKey = 'domain:'.. DomainMoid ..':ap'
    local ApTotal = secureTransform(tonumber(redis.call('HGET', ApMachineRoomKey, 'total') or 0))
    Access['ap_total'] = Access['ap_total'] + ApTotal
    local ApUsed = secureTransform(tonumber(redis.call('HGET', ApMachineRoomKey, 'used') or 0))
    Access['ap_used'] = Access['ap_used'] + ApUsed
end

--获取国密接入资源信息
local get_g_ap_res = function(DomainMoid)
    --接入端口
    local GApMachineRoomKey = 'domain:'.. DomainMoid ..':g_ap'
    local GApTotal = secureTransform(tonumber(redis.call('HGET', GApMachineRoomKey, 'total') or 0))
    Access['g_ap_total'] = Access['g_ap_total'] + GApTotal
    local GApUsed = secureTransform(tonumber(redis.call('HGET', GApMachineRoomKey, 'used') or 0))
    Access['g_ap_used'] = Access['g_ap_used'] + GApUsed
end

local get_mp_res = function(DomainMoid)
    --媒体资源
    local MpMachineRoomKey = 'domain:'.. DomainMoid ..':mp'
    local H264Total = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'total_h264') or 0))
    Media['total_h264'] = Media['total_h264'] + H264Total
    local H264Used = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'used_h264') or 0))
    Media['used_h264'] = Media['used_h264'] + H264Used
    local H265Total = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'total_h265') or 0))
    Media['total_h265'] = Media['total_h265'] + H265Total
    local H265Used = secureTransform(tonumber(redis.call('HGET', MpMachineRoomKey, 'used_h265') or 0))
    Media['used_h265'] = Media['used_h265'] + H265Used
end
--国密媒体资源
local get_g_mp_res = function(DomainMoid)
    local GMpMachineRoomKey = 'domain:'.. DomainMoid ..':g_mp'
    local H264Total = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'total_h264') or 0))
    Media['total_g_h264'] = Media['total_g_h264'] + H264Total
    local H264Used = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'used_h264') or 0))
    Media['used_g_h264'] = Media['used_g_h264'] + H264Used
    local H265Total = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'total_h265') or 0))
    Media['total_g_h265'] = Media['total_g_h265'] + H265Total
    local H265Used = secureTransform(tonumber(redis.call('HGET', GMpMachineRoomKey, 'used_h265') or 0))
    Media['used_g_h265'] = Media['used_g_h265'] + H265Used
end

--获取虚拟会议室资源（用户域资源，或者租赁环境的服务域资源）
local get_common_vmr_res = function(DomainMoid)
    --虚拟会议室
    local VmrKey = 'domain:'.. DomainMoid ..':vmr'
    local EnvType = secureTransform(tonumber(redis.call('HGET', VmrKey, 'env_type')))
    local Total8_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_8_1080') or 0))
    local Used8_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_8_1080') or 0))
    local Total8_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_8_720') or 0))
    local Used8_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_8_720') or 0))
    if EnvType == 1 then
        Vmr['env_type'] = EnvType
    end

    if EnvType == 1 or EnvType == 2 then
        Vmr['used_small'] = Vmr['used_small'] + Used8_720 + Used8_1080
        Vmr['total_small'] = Vmr['total_small'] + Total8_720 + Total8_1080
    else
        Vmr['total_8_1080'] = Vmr['total_8_1080'] + Total8_1080
        Vmr['used_8_1080'] = Vmr['used_8_1080'] + Used8_1080
        Vmr['total_8_720'] = Vmr['total_8_720'] + Total8_720
        Vmr['used_8_720'] = Vmr['used_8_720'] + Used8_720
    end
    local Total192_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_192_1080') or 0))
    local Used192_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_192_1080') or 0))
    local Total192_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_192_720') or 0))
    local Used192_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_192_720') or 0))
    if EnvType == 1 then
        Vmr['used_large'] = Vmr['used_large'] + Used192_720 + Used192_1080
        Vmr['total_large'] = Vmr['total_large'] + Total192_720 + Total192_1080
    else
        Vmr['total_192_1080'] = Vmr['total_192_1080'] + Total192_1080
        Vmr['used_192_1080'] = Vmr['used_192_1080'] + Used192_1080
        Vmr['total_192_720'] = Vmr['total_192_720'] + Total192_720
        Vmr['used_192_720'] = Vmr['used_192_720'] + Used192_720
    end

    if EnvType == 0 then
        local Total64_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_64_1080') or 0))
        Vmr['total_64_1080'] = Vmr['total_64_1080'] + Total64_1080
        local Used64_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_64_1080') or 0))
        Vmr['used_64_1080'] = Vmr['used_64_1080'] + Used64_1080
        local Total64_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_64_720') or 0))
        Vmr['total_64_720'] = Vmr['total_64_720'] + Total64_720
        local Used64_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_64_720') or 0))
        Vmr['used_64_720'] = Vmr['used_64_720'] + Used64_720
        local Total32_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_32_1080') or 0))
        Vmr['total_32_1080'] = Vmr['total_32_1080'] + Total32_1080
        local Used32_1080 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_32_1080') or 0))
        Vmr['used_32_1080'] = Vmr['used_32_1080'] + Used32_1080
        local Total32_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'total_32_720') or 0))
        Vmr['total_32_720'] = Vmr['total_32_720'] + Total32_720
        local Used32_720 = secureTransform(tonumber(redis.call('HGET', VmrKey, 'used_32_720') or 0))
        Vmr['used_32_720'] = Vmr['used_32_720'] + Used32_720
    end
end

--env_type = 0  租赁环境
--env_type = 1  自建环境，服务域vmr资源为0，需自行叠加所有用户域下的vmr资源
local get_sevice_vmr_res = function(DomainMoid)
    local VmrKey = 'domain:'.. DomainMoid ..':vmr'
    local EnvType = secureTransform(tonumber(redis.call('HGET', VmrKey, 'env_type')))
    Result['env_type'] = EnvType
    if EnvType == 0 then
        get_common_vmr_res(DomainMoid)
    else
        local SubKey = 'domain:'..DomainMoid..':sub'
        local SubDomainList = redis.call('SMEMBERS', SubKey)
        if table.getn(SubDomainList) <= 0 then
            return
        end
        for i = 1, table.getn(SubDomainList) do
            get_common_vmr_res(SubDomainList[i])
        end
    end
end

local get_user_domain_res = function(DomainMoid)
    get_ap_res(DomainMoid)
    get_g_ap_res(DomainMoid)
    get_mp_res(DomainMoid)
    get_g_mp_res(DomainMoid)
    get_common_vmr_res(DomainMoid)
end

local get_md_res = function(MachineRoomMoid, Type)
    local Key = 'machine_room:'.. MachineRoomMoid ..':'..Type
    local MdList = redis.call('SMEMBERS', Key)
    if table.getn(MdList) == 0 then
        return
    end
    for i = 1, table.getn(MdList) do
        --合成器
        local VmpKey = Type..':'.. MdList[i]..':ability'
        local TotalVmp = secureTransform(tonumber(redis.call('HGET', VmpKey, 'total_vmp') or 0))
        Media['total_vmp'] = Media['total_vmp'] + TotalVmp
        local UsedVmp = secureTransform(tonumber(redis.call('HGET', VmpKey, 'used_vmp') or 0))
        Media['used_vmp'] = Media['used_vmp'] + UsedVmp

        --混音器
        local TotalMixer = secureTransform(tonumber(redis.call('HGET', VmpKey, 'total_mixer') or 0))
        Media['total_mixer'] = Media['total_mixer'] + TotalMixer
        local UsedMixer = secureTransform(tonumber(redis.call('HGET', VmpKey, 'used_mixer') or 0))
        Media['used_mixer'] = Media['used_mixer'] + UsedMixer
    end
end


--获取媒体资源
local get_media_res = function(MachineRoomMoid)
    --传统会议资源
    get_md_res(MachineRoomMoid,'mps')

    --端口会议资源
    get_md_res(MachineRoomMoid, 'mediaresource')
end

local get_tra_port_total = function(MachineRoomMoid)
    local Key = 'machine_room:'..MachineRoomMoid..':info'
    if 1 == redis.call('EXISTS', Key) then
        Port['total'] = Port['total'] + tonumber(redis.call('HGET', Key, 'total_port') or '0')
        Port['remainder'] = Port['remainder'] + tonumber(redis.call('HGET', Key, 'remainder_port') or '0')
        Tra['remainder'] = Tra['remainder'] + tonumber(redis.call('HGET', Key, 'remainder_tra') or '0')

        Sfu['remainder'] = Sfu['remainder'] + tonumber(redis.call('HGET', Key, 'remainder_sfu') or '0')
        Sfu['used'] = Sfu['used'] + tonumber(redis.call('HGET', Key, 'used_sfu') or '0')       
    end
end

--获取机房资源列表
local get_machine_room_res = function(MachineRoomMoid)
    --vrs能力
    get_vrs_res(MachineRoomMoid)
    get_dcs_res(MachineRoomMoid)
    get_media_res(MachineRoomMoid)
    get_tra_port_total(MachineRoomMoid)
end

--获取domain资源
local get_platform_domain_res = function(DomainMoid)
    local DomainMachineListKey = 'domain:'..DomainMoid..':machine_room'
    local MachineRoomMoidList = redis.call('SMEMBERS', DomainMachineListKey)
    if table.getn(MachineRoomMoidList) <= 0 then
        return nil
    end
    for i = 1, table.getn(MachineRoomMoidList) do
        get_machine_room_res(MachineRoomMoidList[i])
    end
end

local get_service_domain_res
get_service_domain_res = function(DomainMoid)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    get_ap_res(DomainMoid)
    get_g_ap_res(DomainMoid)
    get_mp_res(DomainMoid)
    get_g_mp_res(DomainMoid)
    get_sevice_vmr_res(DomainMoid)
    for i = 1, table.getn(SubDomainList) do
        local domainKey = "domain:" .. SubDomainList[i] .. ":info"
        local DomainType = redis.call("HGET",domainKey,"type")
        if "service" == DomainType then
            get_service_domain_res(SubDomainList[i])
        elseif "platform" == DomainType then
            get_platform_domain_res(SubDomainList[i])
        end
    end
end

--获取用户域下召开的传统会议和端口会议数量
local get_user_domain_tra_meeting_res = function(UserDomainMoid)
    if UserDomainMoid == nil then
        return
    end
    local DomainInfoKey = 'domain:'..UserDomainMoid..':info'
    --获取机房moid
    local MachineRoomMoid = redis.call('HGET', DomainInfoKey, 'machine_room_moid')
    if MachineRoomMoid == nil then
        return
    end
    -- 获取服务域moid
    local ServiceDomainMoid = redis.call('HGET', DomainInfoKey, 'parent_moid')
    if ServiceDomainMoid == nil then
        return
    end

    -- 遍历同一机房下其他用户域
    local UserDomainList = redis.call('SMEMBERS', 'domain:'..ServiceDomainMoid..':sub')
    if UserDomainList ~= nil then
        for i = 1, #UserDomainList do
            if UserDomainList[i] ~= nil then
                local UserDomainInfoKey = 'domain:'..UserDomainList[i]..':info'
                -- 过滤用户域
                local Type = redis.call('HGET', UserDomainInfoKey, 'type')
                if Type ~= nil and 'user' == Type then
                    -- 检查机房
                    local RoomMoid = redis.call('HGET', UserDomainInfoKey, 'machine_room_moid')
                    -- 同一机房
                    if MachineRoomMoid == RoomMoid then
                        -- 遍历全部传统会议
                        local TMeetingE164List = redis.call('SMEMBERS', 'domain:'..UserDomainList[i]..':t_meeting')
                        if TMeetingE164List ~= nil then
                            for j = 1, #TMeetingE164List do
                                if TMeetingE164List[j] ~= nil then
                                    local TMeetingKey = 'conf_res:'..TMeetingE164List[j]..':info'
                                    if 1 == redis.call('EXISTS', TMeetingKey) then
                                        local TraNum = tonumber(redis.call('HGET', TMeetingKey, 'tra') or 0)
                                        local PortNum = tonumber(redis.call('HGET', TMeetingKey, 'port') or 0)
                                        if UserDomainMoid == UserDomainList[i] then
                                            Tra['used'] = Tra['used'] + TraNum
                                            Port['tra_used'] = Port['tra_used'] + PortNum
                                        else
                                            -- 其他用户域传统会议加到其他占用数
                                            Tra['other'] = Tra['other'] + TraNum
                                        end
                                        Port['other'] = Port['other'] + PortNum
                                    end
                                end
                            end
                        end
                        -- 遍历全部端口会议
                        local PMeetingE164List = redis.call('SMEMBERS', 'domain:'..UserDomainList[i]..':p_meeting')
                        if PMeetingE164List ~= nil then
                            for j = 1, #PMeetingE164List do
                                if PMeetingE164List[j] ~= nil then
                                    local PMeetingKey = 'conf_res:'..PMeetingE164List[j]..':info'
                                    if 1 == redis.call('EXISTS', PMeetingKey) then
                                        local TraNum = tonumber(redis.call('HGET', PMeetingKey, 'tra') or 0)
                                        local PortNum = tonumber(redis.call('HGET', PMeetingKey, 'port') or 0)
                                        if UserDomainMoid == UserDomainList[i] then
                                            Port['used'] = Port['used'] + PortNum
                                            Tra['port_used'] = Tra['port_used'] + TraNum
                                        else
                                            -- 其他用户域端口加到其他占用数
                                            Port['other'] = Port['other'] + PortNum
                                        end
                                        Tra['other'] = Tra['other'] + TraNum
                                    end
                                end
                            end
                        end

                        -- 遍历全部混合会议
                        local MixMeetingE164List = redis.call('SMEMBERS', 'domain:'..UserDomainList[i]..':mix_meeting')
                        if MixMeetingE164List ~= nil then
                            for j = 1, #MixMeetingE164List do
                                if MixMeetingE164List[j] ~= nil then
                                    local MixMeetingKey = 'conf_res:'..MixMeetingE164List[j]..':info'
                                    if 1 == redis.call('EXISTS', MixMeetingKey) then
                                        local TraNum = tonumber(redis.call('HGET', MixMeetingKey, 'tra') or 0)
                                        local PortNum = tonumber(redis.call('HGET', MixMeetingKey, 'port') or 0)
                                        Tra['other'] = Tra['other'] + TraNum
                                        Port['other'] = Port['other'] + PortNum
                                    end
                                end
                            end
                        end                       
                    end
                end
            end
        end
    end

    -- 获取机房会议资源总数
    if MachineRoomMoid ~= nil then
        get_machine_room_res(MachineRoomMoid)
    end
end

--moid
local Moid = ARGV[1]

local Type = nil
if redis.call("EXISTS", "domain:"..Moid..":info") == 1 then
    Type = redis.call("HGET", "domain:"..Moid..":info", "type")
else
    Type = "machine_room"
end

--类型:domain/machine_room
if Type == 'service' then
    get_service_domain_res(Moid)
    get_service_domain_tra_meeting_res(Moid)
elseif Type == 'user' then
    get_user_domain_res(Moid)
    get_user_domain_tra_meeting_res(Moid)
elseif Type == 'kernel' then
    local SubKey = "domain:"..Moid..":sub"
    local ServiceList = redis.call("SMEMBERS", SubKey)
    for i=1, #ServiceList do
        get_service_domain_res(ServiceList[i])
        get_service_domain_tra_meeting_res(ServiceList[i])
    end
end

local PortResUse = Port['used'] + Port['other'] + Port['remainder']
-- 现在上报以整数来，存在误差
Port['total'] = PortResUse

Tra['total'] = Tra['used'] + Tra['other'] + Tra['remainder']

Sfu['total'] = Sfu['used'] + Sfu['remainder']

-- 向上取整
Media['total_h264'] = math.ceil(Media['total_h264'])
Media['used_h264'] = math.ceil(Media['used_h264'])

--国密h264媒体端口数
Media['total_g_h264'] = math.ceil(Media['total_g_h264'])
Media['used_g_h264'] = math.ceil(Media['used_g_h264'])

--h265媒体端口数
Media['total_h265'] = math.ceil(Media['total_h265'])
Media['used_h265'] = math.ceil(Media['used_h265'])

--国密h265媒体端口数
Media['total_g_h265'] = math.ceil(Media['total_g_h265'])
Media['used_g_h265'] = math.ceil(Media['used_g_h265'])

local Ret = {}
Ret['success'] = 1
Ret['resource'] = Result
return cjson.encode(Ret)
