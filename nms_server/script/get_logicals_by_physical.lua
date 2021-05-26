local get_logicals = function(p_server_moid, Result)

    local LogicalListKey = "p_server:"..p_server_moid..":l_server"
    local LogicalList = redis.call("SMEMBERS", LogicalListKey)
    for i=1,#LogicalList do
        local KeyInfo = 'l_server:' .. LogicalList[i] .. ':info'
        if redis.call('EXISTS', KeyInfo) == 1 then
            local Type = redis.call('HGET', KeyInfo, 'type') or ""
            -- 由于DCS和VRS逻辑服务器归属的物理服务器的moid为空，顾屏蔽外设逻辑服务器的显示
    
            --Get server info
            local PServerMoid = redis.call('HGET', KeyInfo, 'p_server_moid') or ""
            local MachineRoomMoid = redis.call('HGET', KeyInfo, 'machine_room_moid') or ""
            local Name = redis.call('HGET', KeyInfo, 'name') or ""
            local BackupState = redis.call('HGET', KeyInfo, 'backup_state') or ""
    
            --此处为了兼容老的api, 老api根据mediaresource的moid获取端口资源, 5.2版本mediaresource不存在了,media-worker代替
            if Type == "media-worker" or Type == "mpu_jd2000" or Type == "mpu" then
                Type = 'MEDIARESOURCE'
            end
    
            --Get ip info
            local IP
            if PServerMoid ~= '' then
                local KeyPhysicalServer = 'p_server:' .. PServerMoid .. ':info'
                IP = redis.call('HGET', KeyPhysicalServer, 'ip') or ""
            else
                IP = ''
            end
    
            --Get server online state
            local KeyOnline = 'l_server:' .. LogicalList[i] .. ':online'
            local Online = redis.call('GET', KeyOnline)
            if (not Online) then
                Online = 'offline'
            end
    
            --Get server warning info
            local KeyWarning = 'l_server:' .. LogicalList[i] .. ':warning'
            local WarningList = redis.call('HGETALL', KeyWarning)
            local hasCritical = false
            local hasImportant = false
            local hasNormal = false
            for i = 2, table.getn(WarningList), 2 do
                if WarningList[i] == 'critical' then
                    hasCritical = true
                elseif WarningList[i] == 'important' then
                    hasImportant = true
                elseif WarningList[i] == 'normal' then
                    hasNormal = true
                end
            end
    
            local WarningLevel = ''
            if hasCritical then
                WarningLevel = 'critical'
            elseif hasImportant then
                WarningLevel = 'important'
            elseif hasNormal then
                WarningLevel = 'normal'
            end
    
            -- Format server info object
            local ServerInfo = {}
            ServerInfo['moid'] = LogicalList[i]
            ServerInfo['guid'] = LogicalList[i]
            ServerInfo['p_server_moid'] = PServerMoid
            ServerInfo['domain_moid'] = ARGV[1]
            ServerInfo['machine_room_moid'] = MachineRoomMoid
            ServerInfo['name'] = Name
            ServerInfo['type'] = Type
            ServerInfo['backup_state'] = BackupState
            ServerInfo['ip'] = IP
            ServerInfo['warning_level'] = WarningLevel
            ServerInfo['online'] = Online
    
            table.insert(Result, ServerInfo)
        end
    end
end



local Logicals = {}
get_logicals(ARGV[1], Logicals)
if next(Logicals) == nil then
    local Result = {}
    Result["success"] = 0
    Result["err_str"] = "logicals list empty"
    Result["error_code"] = 123456
    return cjson.encode(Result)
end

local Result = {}
Result["success"] = 1
Result["logicals"] = Logicals

return cjson.encode(Result)