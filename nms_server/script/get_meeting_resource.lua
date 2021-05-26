local get_machineroom_meeting_list = function(userMoid, MeetingResource)
    -- 在线软终端数
    local KeyTermal = 'domain:' .. userMoid .. ':terminal'
	local domainList = redis.call('SMEMBERS', KeyTermal)
    MeetingResource['STerOnline'] = 0
    for i, moid in pairs(domainList) do
        --Get online terminal
        local KeyOnline = 'terminal:' .. moid .. ':onlinestate'
        if redis.call("EXISTS", KeyOnline) ~= 0 then
            local Types = redis.call('HKEYS', KeyOnline)
            for j = 1, table.getn(Types) do
                -- Get soft terminal type
                local Key = "soft_terminal_type"
                local softTerminalTypeList = redis.call('SMEMBERS', Key)
                for _, v in ipairs(softTerminalTypeList) do
                    if v == Types[j] then
                        MeetingResource['STerOnline'] = MeetingResource['STerOnline'] + 1
                    end
                end
            end
        end
    end
    -- AP MP
    local domainInfo = "domain:" .. userMoid .. ":info"
    if redis.call('EXISTS', domainInfo) == 1 then
        local domainType  = redis.call('HGET',domainInfo,'type') or ''
        if domainType == "user" then
            -- AP接入端口
            local KeyDomainAp = "domain:" .. userMoid .. ":ap"
            if redis.call('EXISTS', KeyDomainAp) == 1 then
                local APused  = redis.call('HGET',KeyDomainAp,'used') or '0'
                local APtotal = redis.call('HGET',KeyDomainAp,'total') or '0'
                if tonumber(APtotal) >= tonumber(APused) then
                    MeetingResource['APStarted'] = MeetingResource['APStarted'] + tonumber(APused)
                    MeetingResource['APUsable'] = MeetingResource['APUsable']  + tonumber(APtotal) - tonumber(APused)
                end
            end
            local KeyDomainGap = "domain:" .. userMoid .. ":g_ap"
            if redis.call('EXISTS', KeyDomainGap) == 1 then
                local GAPused  = redis.call('HGET',KeyDomainGap,'used') or '0'
                local GAPtotal = redis.call('HGET',KeyDomainGap,'total') or '0'
                if tonumber(GAPtotal) >= tonumber(GAPused) then
                    MeetingResource['GAPStarted'] = MeetingResource['GAPStarted'] + tonumber(GAPused)
                    MeetingResource['GAPUsable'] = MeetingResource['GAPUsable']  + tonumber(GAPtotal) - tonumber(GAPused)
                end
            end
            MeetingResource['APsStarted'] = MeetingResource['APStarted'] + MeetingResource['GAPStarted']
            MeetingResource['APsUsable'] = MeetingResource['APUsable'] + MeetingResource['GAPUsable']
            -- MP媒体端口
            local KeyDomainMp = "domain:" .. userMoid .. ":mp"
            if redis.call('EXISTS', KeyDomainMp) == 1 then
                local MPused  = redis.call('HGET',KeyDomainMp,'used_h264') or '0'
                local MPtotal = redis.call('HGET',KeyDomainMp,'total_h264') or '0'
                if tonumber(MPtotal) >= tonumber(MPused) then
                    MeetingResource['MPStarted'] = MeetingResource['MPStarted'] + tonumber(MPused)
                    MeetingResource['MPUsable'] = MeetingResource['MPUsable']  + tonumber(MPtotal) - tonumber(MPused)
                end
                local HMPused  = redis.call('HGET',KeyDomainMp,'used_h265') or '0'
                local HMPtotal = redis.call('HGET',KeyDomainMp,'total_h265') or '0'
                if tonumber(HMPtotal) >= tonumber(HMPused) then
                    MeetingResource['HMPStarted'] = MeetingResource['HMPStarted'] + tonumber(HMPused)
                    MeetingResource['HMPUsable'] = MeetingResource['HMPUsable']  + tonumber(HMPtotal) - tonumber(HMPused)
                end
            end
            local KeyDomainGmp = "domain:" .. userMoid .. ":g_mp"
            if redis.call('EXISTS', KeyDomainGmp) == 1 then
                local GMPused  = redis.call('HGET',KeyDomainGmp,'used_h264') or '0'
                local GMPtotal = redis.call('HGET',KeyDomainGmp,'total_h264') or '0'
                if tonumber(GMPtotal) >= tonumber(GMPused) then
                    MeetingResource['GMPStarted'] = MeetingResource['GMPStarted'] + tonumber(GMPused)
                    MeetingResource['GMPUsable'] = MeetingResource['GMPUsable']  + tonumber(GMPtotal) - tonumber(GMPused)
                end
                local GHMPused  = redis.call('HGET',KeyDomainGmp,'used_h265') or '0'
                local GHMPtotal = redis.call('HGET',KeyDomainGmp,'total_h265') or '0'
                if tonumber(GHMPtotal) >= tonumber(GHMPused) then
                    MeetingResource['GHMPStarted'] = MeetingResource['GHMPStarted'] + tonumber(GHMPused)
                    MeetingResource['GHMPUsable'] = MeetingResource['GHMPUsable']  + tonumber(GHMPtotal) - tonumber(GHMPused)
                end
            end
            MeetingResource['MPsStarted'] = MeetingResource['MPStarted'] + MeetingResource['HMPStarted'] + MeetingResource['GMPStarted'] + MeetingResource['GHMPStarted']
            MeetingResource['MPsUsable'] = MeetingResource['MPUsable'] + MeetingResource['HMPUsable'] + MeetingResource['GMPUsable'] + MeetingResource['GHMPUsable']
        end
    end
    -- 当前用户域下关联机房
    local machineRoomMoid  = redis.call('HGET',domainInfo,'machine_room_moid') or ''
    -- 软终端
    local KeyBaseInfo = 'machine_room:' .. machineRoomMoid .. ':pt_num'
    if redis.call('EXISTS', KeyBaseInfo) == 1 then
        local Sterused  = redis.call('HGET',KeyBaseInfo,'sum_software_count') or '0'
        MeetingResource['STerStarted']  =  MeetingResource['STerStarted'] + tonumber(Sterused)
    end
    local KeyBaseInfo = 'machine_room:' .. machineRoomMoid .. ':info'
    if redis.call('EXISTS', KeyBaseInfo) == 1 then
        local domain_moid  = redis.call('HGET',KeyBaseInfo,'domain_moid') or ''
        local KeyDomainmoidInfo = 'domain:' .. domain_moid .. ':info'
        if redis.call('EXISTS', KeyDomainmoidInfo) == 1 then
            local server_moid  = redis.call('HGET',KeyDomainmoidInfo,'parent_moid') or ''
            local KeyDomainInfo = 'domain:' .. server_moid .. ':license'
            if redis.call('EXISTS', KeyDomainInfo) == 1 then
                local licenseList = redis.call('SMEMBERS', KeyDomainInfo)
                for j = 1,table.getn(licenseList) do
                    local licenseKey = "license:" .. licenseList[j] .. ":info"
                    if redis.call('EXISTS', licenseKey) == 1 then
                        local regiSoftNum = redis.call('HGET',licenseKey,'register_software_limit') or '0'
                        MeetingResource['STerTotal'] = MeetingResource['STerTotal'] + tonumber(regiSoftNum)
                    end
                end         
            end
        end
    end
    -- 直播会议 录像室
    local vrsKeyInfo = 'machine_room:' .. machineRoomMoid .. ':vrs'
    local VrsList = redis.call('SMEMBERS', vrsKeyInfo)
    for j = 1,table.getn(VrsList) do
        local vrsKey = "vrs:" .. VrsList[j] .. ":ability"
        if redis.call('EXISTS', vrsKey) == 1 then
            local HLSused = redis.call('HGET',vrsKey,'html5lcastocp') or '0'
            local HLStotal = redis.call('HGET',vrsKey,'html5lcasttotal') or '0'
            if tonumber(HLStotal) >= tonumber(HLSused) then
                MeetingResource['HLSStarted'] = MeetingResource['HLSStarted'] + tonumber(HLSused)
                MeetingResource['HLSUsable'] = MeetingResource['HLSUsable'] + tonumber(HLStotal) - tonumber(HLSused)
            end
            local ASFused = redis.call('HGET',vrsKey,'lcastocp') or '0'
            local ASFtotal = redis.call('HGET',vrsKey,'lcasttotal') or '0'
            if tonumber(ASFtotal) >= tonumber(ASFused) then
                MeetingResource['ASFStarted'] = MeetingResource['ASFStarted'] + tonumber(ASFused)
                MeetingResource['ASFUsable'] = MeetingResource['ASFUsable'] + tonumber(ASFtotal) - tonumber(ASFused)
            end
            local VRSused = redis.call('HGET',vrsKey,'recroomocp') or '0'
            local VRStotal = redis.call('HGET',vrsKey,'recroomtotal') or '0'
            if tonumber(VRStotal) >= tonumber(VRSused) then
                MeetingResource['VRStarted'] = MeetingResource['VRStarted'] + tonumber(VRSused)
                MeetingResource['VRUsable'] = MeetingResource['VRUsable'] + tonumber(VRStotal) - tonumber(VRSused)
            end
        end
        MeetingResource['LMStarted'] = MeetingResource['HLSStarted'] + MeetingResource['ASFStarted']
        MeetingResource['LMUsable'] = MeetingResource['HLSUsable'] + MeetingResource['ASFUsable']
    end
    -- 直播人数
    local machineRoomKeyInfo = 'machine_room:' .. machineRoomMoid .. ':info'
    local envType = redis.call('HGET',machineRoomKeyInfo,'env_type') or ''
    if envType == "0" or envType == 0 then
        local userkeyInfo = "machine_room:" .. machineRoomMoid .. ":domain"
        local userList = redis.call('SMEMBERS', userkeyInfo)
        for j = 1,table.getn(userList) do
            local domainInfo = "domain:" .. userList[j] .. ":info"
            if redis.call('EXISTS', domainInfo) == 1 then
                local domainType  = redis.call('HGET',domainInfo,'type') or ''
                if domainType == "user" then
                    local KeyDomainAp = "domain:" .. userList[j] .. ":lv"
                    if redis.call('EXISTS', KeyDomainAp) == 1 then
                        local LVused  = redis.call('HGET',KeyDomainAp,'used_num') or '0'
                        local LVtotal = redis.call('HGET',KeyDomainAp,'total_num') or '0'
                        if tonumber(LVtotal) >= tonumber(LVused) then
                            MeetingResource['ViewersStarted'] = MeetingResource['ViewersStarted'] + tonumber(LVused)
                            MeetingResource['ViewersUsable'] = MeetingResource['ViewersUsable']  + tonumber(LVtotal) - tonumber(LVused)
                        end
                    end
                end
            end
        end
    elseif envType == "1" or envType == 1 then
        local logicalKeyServer = "machine_room:" .. machineRoomMoid .. ":l_server"
        local lserverList = redis.call('SMEMBERS', logicalKeyServer)
        for j = 1,table.getn(lserverList) do
            local logicalServerInfo = "l_server:" .. lserverList[j] .. ":lv"
            if redis.call('EXISTS', logicalServerInfo) == 1 then
                local LVused  = redis.call('HGET',logicalServerInfo,'used_num') or '0'
                local LVtotal = redis.call('HGET',logicalServerInfo,'total_num') or '0'
                if tonumber(LVtotal) >= tonumber(LVused) then
                    MeetingResource['ViewersStarted'] = MeetingResource['ViewersStarted'] + tonumber(LVused)
                    MeetingResource['ViewersUsable'] = MeetingResource['ViewersUsable']  + tonumber(LVtotal) - tonumber(LVused)
                end
            end
        end
    end
    -- 协作资源
    local dcsKeyInfo = 'machine_room:' .. machineRoomMoid .. ':dcs'
    local DcsList = redis.call('SMEMBERS', dcsKeyInfo)
    for j = 1,table.getn(DcsList) do
        local dcsKey = "dcs:" .. DcsList[j] .. ":resource"
        if redis.call('EXISTS', dcsKey) == 1 then
            local CRused = redis.call('HGET',dcsKey,'mtnum') or '0'
            local CRtotal = redis.call('HGET',dcsKey,'maxmtnum') or '0'
            if tonumber(CRtotal) >= tonumber(CRused) then
                MeetingResource['CRStarted'] = MeetingResource['CRStarted'] + tonumber(CRused)
                MeetingResource['CRPUsable'] = MeetingResource['CRPUsable'] + tonumber(CRtotal) - tonumber(CRused)
            end
        end
    end
end

local get_platform_meeting_list = function(DomainMoid, MeetingResource)
    local keyInfo = "domain:" .. DomainMoid .. ":machine_room"
    local machineRoomList = redis.call('SMEMBERS', keyInfo)
    for i = 1,table.getn(machineRoomList) do
        -- 软终端
        local KeyBaseInfo = 'machine_room:' .. machineRoomList[i] .. ':pt_num'
        if redis.call('EXISTS', KeyBaseInfo) == 1 then
            local Sterused  = redis.call('HGET',KeyBaseInfo,'sum_software_count') or '0'
            MeetingResource['STerStarted']  =  MeetingResource['STerStarted'] + tonumber(Sterused)
        end
        local KeyBaseInfo = 'machine_room:' .. machineRoomList[i] .. ':info'
        if redis.call('EXISTS', KeyBaseInfo) == 1 then
            local domain_moid  = redis.call('HGET',KeyBaseInfo,'domain_moid') or ''
            local KeyDomainmoidInfo = 'domain:' .. domain_moid .. ':info'
            if redis.call('EXISTS', KeyDomainmoidInfo) == 1 then
                local server_moid  = redis.call('HGET',KeyDomainmoidInfo,'parent_moid') or ''
                local KeyDomainInfo = 'domain:' .. server_moid .. ':license'
                if redis.call('EXISTS', KeyDomainInfo) == 1 then
                    local licenseList = redis.call('SMEMBERS', KeyDomainInfo)
                    for j = 1,table.getn(licenseList) do
                        local licenseKey = "license:" .. licenseList[j] .. ":info"
                        if redis.call('EXISTS', licenseKey) == 1 then
                            local regiSoftNum = redis.call('HGET',licenseKey,'register_software_limit') or '0'
                            MeetingResource['STerTotal'] = MeetingResource['STerTotal'] + tonumber(regiSoftNum)
                        end
                    end         
                end
            end
        end
        -- 直播会议 录像室
        local vrsKeyInfo = 'machine_room:' .. machineRoomList[i] .. ':vrs'
        local VrsList = redis.call('SMEMBERS', vrsKeyInfo)
        for j = 1,table.getn(VrsList) do
            local vrsKey = "vrs:" .. VrsList[j] .. ":ability"
            if redis.call('EXISTS', vrsKey) == 1 then
                local HLSused = redis.call('HGET',vrsKey,'html5lcastocp') or '0'
                local HLStotal = redis.call('HGET',vrsKey,'html5lcasttotal') or '0'
                if tonumber(HLStotal) >= tonumber(HLSused) then
                    MeetingResource['HLSStarted'] = MeetingResource['HLSStarted'] + tonumber(HLSused)
                    MeetingResource['HLSUsable'] = MeetingResource['HLSUsable'] + tonumber(HLStotal) - tonumber(HLSused)
                end
                local ASFused = redis.call('HGET',vrsKey,'lcastocp') or '0'
                local ASFtotal = redis.call('HGET',vrsKey,'lcasttotal') or '0'
                if tonumber(ASFtotal) >= tonumber(ASFused) then
                    MeetingResource['ASFStarted'] = MeetingResource['ASFStarted'] + tonumber(ASFused)
                    MeetingResource['ASFUsable'] = MeetingResource['ASFUsable'] + tonumber(ASFtotal) - tonumber(ASFused)
                end
                local VRSused = redis.call('HGET',vrsKey,'recroomocp') or '0'
                local VRStotal = redis.call('HGET',vrsKey,'recroomtotal') or '0'
                if tonumber(VRStotal) >= tonumber(VRSused) then
                    MeetingResource['VRStarted'] = MeetingResource['VRStarted'] + tonumber(VRSused)
                    MeetingResource['VRUsable'] = MeetingResource['VRUsable'] + tonumber(VRStotal) - tonumber(VRSused)
                end
            end
            MeetingResource['LMStarted'] = MeetingResource['HLSStarted'] + MeetingResource['ASFStarted']
            MeetingResource['LMUsable'] = MeetingResource['HLSUsable'] + MeetingResource['ASFUsable']
        end
        -- 直播人数
        local machineRoomKeyInfo = 'machine_room:' .. machineRoomList[i] .. ':info'
        local envType = redis.call('HGET',machineRoomKeyInfo,'env_type') or ''
        if envType == "0" or envType == 0 then
            local userkeyInfo = "machine_room:" .. machineRoomList[i] .. ":domain"
            local userList = redis.call('SMEMBERS', userkeyInfo)
            for j = 1,table.getn(userList) do
                local domainInfo = "domain:" .. userList[j] .. ":info"
                if redis.call('EXISTS', domainInfo) == 1 then
                    local domainType  = redis.call('HGET',domainInfo,'type') or ''
                    if domainType == "user" then
                        local KeyDomainAp = "domain:" .. userList[j] .. ":lv"
                        if redis.call('EXISTS', KeyDomainAp) == 1 then
                            local LVused  = redis.call('HGET',KeyDomainAp,'used_num') or '0'
                            local LVtotal = redis.call('HGET',KeyDomainAp,'total_num') or '0'
                            if tonumber(LVtotal) >= tonumber(LVused) then
                                MeetingResource['ViewersStarted'] = MeetingResource['ViewersStarted'] + tonumber(LVused)
                                MeetingResource['ViewersUsable'] = MeetingResource['ViewersUsable']  + tonumber(LVtotal) - tonumber(LVused)
                            end
                        end
                    end
                end
            end
        elseif envType == "1" or envType == 1 then
            local logicalKeyServer = "machine_room:" .. machineRoomList[i] .. ":l_server"
            local lserverList = redis.call('SMEMBERS', logicalKeyServer)
            for j = 1,table.getn(lserverList) do
                local logicalServerInfo = "l_server:" .. lserverList[j] .. ":lv"
                if redis.call('EXISTS', logicalServerInfo) == 1 then
                    local LVused  = redis.call('HGET',logicalServerInfo,'used_num') or '0'
                    local LVtotal = redis.call('HGET',logicalServerInfo,'total_num') or '0'
                    if tonumber(LVtotal) >= tonumber(LVused) then
                        MeetingResource['ViewersStarted'] = MeetingResource['ViewersStarted'] + tonumber(LVused)
                        MeetingResource['ViewersUsable'] = MeetingResource['ViewersUsable']  + tonumber(LVtotal) - tonumber(LVused)
                    end
                end
            end
        end
        -- 协作资源
        local dcsKeyInfo = 'machine_room:' .. machineRoomList[i] .. ':dcs'
        local DcsList = redis.call('SMEMBERS', dcsKeyInfo)
        for j = 1,table.getn(DcsList) do
            local dcsKey = "dcs:" .. DcsList[j] .. ":resource"
            if redis.call('EXISTS', dcsKey) == 1 then
                local CRused = redis.call('HGET',dcsKey,'mtnum') or '0'
                local CRtotal = redis.call('HGET',dcsKey,'maxmtnum') or '0'
                if tonumber(CRtotal) >= tonumber(CRused) then
                    MeetingResource['CRStarted'] = MeetingResource['CRStarted'] + tonumber(CRused)
                    MeetingResource['CRPUsable'] = MeetingResource['CRPUsable'] + tonumber(CRtotal) - tonumber(CRused)
                end
            end
        end
    end
end

local get_service_meeting_list
get_service_meeting_list = function(DomainMoid, MeetingResource)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

        local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
        local DomainType = redis.call('HGET',KeyDomain,'type')

        if "service" == DomainType then
            -- AP MP
            -- AP接入端口
            local KeyDomainAp = "domain:" .. SubDomainList[i] .. ":ap"
            if redis.call('EXISTS', KeyDomainAp) == 1 then
                local APused  = redis.call('HGET',KeyDomainAp,'used') or '0'
                local APtotal = redis.call('HGET',KeyDomainAp,'total') or '0'
                if tonumber(APtotal) >= tonumber(APused) then
                    MeetingResource['APStarted'] = MeetingResource['APStarted'] + tonumber(APused)
                    MeetingResource['APUsable'] = MeetingResource['APUsable']  + tonumber(APtotal) - tonumber(APused)
                end
            end
            local KeyDomainGap = "domain:" .. SubDomainList[i] .. ":g_ap"
            if redis.call('EXISTS', KeyDomainGap) == 1 then
                local GAPused  = redis.call('HGET',KeyDomainGap,'used') or '0'
                local GAPtotal = redis.call('HGET',KeyDomainGap,'total') or '0'
                if tonumber(GAPtotal) >= tonumber(GAPused) then
                    MeetingResource['GAPStarted'] = MeetingResource['GAPStarted'] + tonumber(GAPused)
                    MeetingResource['GAPUsable'] = MeetingResource['GAPUsable']  + tonumber(GAPtotal) - tonumber(GAPused)
                end
            end
            MeetingResource['APsStarted'] = MeetingResource['APStarted'] + MeetingResource['GAPStarted']
            MeetingResource['APsUsable'] = MeetingResource['APUsable'] + MeetingResource['GAPUsable']
            -- MP媒体端口
            local KeyDomainMp = "domain:" .. SubDomainList[i] .. ":mp"
            if redis.call('EXISTS', KeyDomainMp) == 1 then
                local MPused  = redis.call('HGET',KeyDomainMp,'used_h264') or '0'
                local MPtotal = redis.call('HGET',KeyDomainMp,'total_h264') or '0'
                if tonumber(MPtotal) >= tonumber(MPused) then
                    MeetingResource['MPStarted'] = MeetingResource['MPStarted'] + tonumber(MPused)
                    MeetingResource['MPUsable'] = MeetingResource['MPUsable']  + tonumber(MPtotal) - tonumber(MPused)
                end
                local HMPused  = redis.call('HGET',KeyDomainMp,'used_h265') or '0'
                local HMPtotal = redis.call('HGET',KeyDomainMp,'total_h265') or '0'
                if tonumber(HMPtotal) >= tonumber(HMPused) then
                    MeetingResource['HMPStarted'] = MeetingResource['HMPStarted'] + tonumber(HMPused)
                    MeetingResource['HMPUsable'] = MeetingResource['HMPUsable']  + tonumber(HMPtotal) - tonumber(HMPused)
                end
            end
            local KeyDomainGmp = "domain:" .. SubDomainList[i] .. ":g_mp"
            if redis.call('EXISTS', KeyDomainGmp) == 1 then
                local GMPused  = redis.call('HGET',KeyDomainGmp,'used_h264') or '0'
                local GMPtotal = redis.call('HGET',KeyDomainGmp,'total_h264') or '0'
                if tonumber(GMPtotal) >= tonumber(GMPused) then
                    MeetingResource['GMPStarted'] = MeetingResource['GMPStarted'] + tonumber(GMPused)
                    MeetingResource['GMPUsable'] = MeetingResource['GMPUsable']  + tonumber(GMPtotal) - tonumber(GMPused)
                end
                local GHMPused  = redis.call('HGET',KeyDomainGmp,'used_h265') or '0'
                local GHMPtotal = redis.call('HGET',KeyDomainGmp,'total_h265') or '0'
                if tonumber(GHMPtotal) >= tonumber(GHMPused) then
                    MeetingResource['GHMPStarted'] = MeetingResource['GHMPStarted'] + tonumber(GHMPused)
                    MeetingResource['GHMPUsable'] = MeetingResource['GHMPUsable']  + tonumber(GHMPtotal) - tonumber(GHMPused)
                end
            end
            MeetingResource['MPsStarted'] = MeetingResource['MPStarted'] + MeetingResource['HMPStarted'] + MeetingResource['GMPStarted'] + MeetingResource['GHMPStarted']
            MeetingResource['MPsUsable'] = MeetingResource['MPUsable'] + MeetingResource['HMPUsable'] + MeetingResource['GMPUsable'] + MeetingResource['GHMPUsable']
            get_service_meeting_list(SubDomainList[i], MeetingResource)
        elseif "platform" == DomainType then
            get_platform_meeting_list(SubDomainList[i], MeetingResource)
        end
    end
end

-- 资源获取
local MeetingResource = {
    -- AP接入端口
    ['APsStarted'] = 0,
    ['APsUsable'] = 0,
    ['APStarted'] = 0,
    ['APUsable'] = 0,
    ['GAPStarted'] = 0,
    ['GAPUsable'] = 0,
    -- MP媒体端口
    ['MPsStarted'] = 0,
    ['MPsUsable'] = 0,
    ['MPStarted'] = 0,
    ['MPUsable'] = 0,
    ['HMPStarted'] = 0,
    ['HMPUsable'] = 0,
    ['GMPStarted'] = 0,
    ['GMPUsable'] = 0,
    ['GHMPStarted'] = 0,
    ['GHMPUsable'] = 0,
    -- 软终端
    ['STerStarted'] = 0,
    ['STerTotal'] = 0,
    ['STerOnline'] = 0,
    -- 直播会议
    ['LMStarted'] = 0,
    ['LMUsable'] = 0,
    ['HLSStarted'] = 0,
    ['HLSUsable'] = 0,
    ['ASFStarted'] = 0,
    ['ASFUsable'] = 0,
    -- 录像室
    ['VRStarted'] = 0,
    ['VRUsable'] = 0,
    -- 直播人数
    ['ViewersStarted'] = 0,
    ['ViewersUsable'] = 0,
    -- 协作资源
    ['CRStarted'] = 0,
    ['CRPUsable'] = 0,
}
local KeyDomain = 'domain:' .. ARGV[1] .. ':info'
if redis.call("EXISTS",KeyDomain) == 1 then
    local DomainType = redis.call('HGET',KeyDomain,'type') or ''
    if "kernel" == DomainType or "service" == DomainType then
        get_service_meeting_list(ARGV[1], MeetingResource)
        local domainList = redis.call("SMEMBERS", "domain_moids")
        MeetingResource['STerOnline'] = 0
        for i, domainMoid in pairs(domainList) do
            if redis.call("EXISTS", "domain:" .. domainMoid .. ":info") ~= 0 then
                for i, moid in pairs(redis.call("SMEMBERS", "domain:" .. domainMoid .. ":terminal")) do
                    --Get online terminal
                    local KeyOnline = 'terminal:' .. moid .. ':onlinestate'
                    if redis.call("EXISTS", KeyOnline) ~= 0 then
                        local Types = redis.call('HKEYS', KeyOnline)
                        for j = 1, table.getn(Types) do
                            -- Get soft terminal type
                            local Key = "soft_terminal_type"
                            local softTerminalTypeList = redis.call('SMEMBERS', Key)
                            for _, v in ipairs(softTerminalTypeList) do
                                if v == Types[j] then
                                    MeetingResource['STerOnline'] = MeetingResource['STerOnline'] + 1
                                end
                            end
                        end
                    end
                end
            end
        end
    elseif "user" == DomainType then
        get_machineroom_meeting_list(ARGV[1], MeetingResource)
    end
else
    get_machineroom_meeting_list(ARGV[1], MeetingResource)
end

return cjson.encode(MeetingResource)