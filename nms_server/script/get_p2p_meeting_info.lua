
local function get_terminal_name(dev_e164)
	local KeyE164BaseInfo = 'terminal:' .. dev_e164 .. ':baseinfo'
	
	if redis.call('EXISTS', KeyE164BaseInfo) == 1 then 
        local Moid  = redis.call('HGET',KeyE164BaseInfo,'moid') or ""
        local KeyMoidBaseInfo = 'terminal:' .. Moid .. ':baseinfo'
        local Name = redis.call("HGET",KeyMoidBaseInfo,"name") or ""
        return Name
    else
        return nil
    end
end

local function get_terminal_type_in_conf(dev_e164)
	local KeyE164BaseInfo = 'terminal:' .. dev_e164 .. ':baseinfo'
	
	if redis.call('EXISTS', KeyE164BaseInfo) == 1 then 
        local Moid  = redis.call('HGET',KeyE164BaseInfo,'moid') or ""
        local KeyMoidBaseInfo = 'terminal:' .. Moid .. ':baseinfo'

        local KeyOnline = 'terminal:' .. Moid .. ':onlinestate'
        local type = nil
        if redis.call('EXISTS', KeyOnline) == 1 then 
            local Types = redis.call('HKEYS', KeyOnline)
            local Vals = redis.call('HVALS', KeyOnline)
            for i=1, table.getn(Types) do
                if(Vals[i] == 'conference') then
                    type = redis.call("HGET",'terminal_type_list',Types[i])
                    break 
                end
            end
        else
            type = nil
        end
        return type
    else
        return nil
    end
end


local KeyMeeting = "p2p_meeting:" .. ARGV[1] .. ":info"
if  1 == redis.call("EXISTS",KeyMeeting) then
    local CallerDomainMoid = redis.call("HGET",KeyMeeting,"caller_domain_moid") or ""
    local CallerE164 = redis.call("HGET",KeyMeeting,"caller_e164") or ""
    
    local CallerNameValue = redis.call("HGET",KeyMeeting,"caller_name") or ""
    local CallerName = CallerNameValue or get_terminal_name(CallerE164)

    local CallerTypeValue = redis.call("HGET",KeyMeeting,"caller_type") or ""
    local CallerType = get_terminal_type_in_conf(CallerE164) or CallerTypeValue

    local CalleeDomainMoid = redis.call("HGET",KeyMeeting,"callee_domain_moid") or ""
    local CalleeE164 = redis.call("HGET",KeyMeeting,"callee_e164") or ""
    
    local CalleeNameValue = redis.call("HGET",KeyMeeting,"callee_name") or ""
    local CalleeName = CalleeNameValue or get_terminal_name(CalleeE164)

    local CalleeTypeValue = redis.call("HGET",KeyMeeting,"callee_type") or ""
    local CalleeType = get_terminal_type_in_conf(CalleeE164) or CalleeTypeValue  

    local Bandwidth = redis.call("HGET",KeyMeeting,"bandwidth") or 0
    local StartTime = redis.call("HGET",KeyMeeting,"start_time") or ""
    return {CallerDomainMoid,CallerE164,CallerName,CallerType,CalleeDomainMoid
        ,CalleeE164,CalleeName,CalleeType,Bandwidth,StartTime}
else
    return  {error,"Key Non-Exist"}
end
