local get_user_terminal_list = function(DomainMoid, TerminalName, TerminalList)
	local KeyTermal = 'domain:' .. DomainMoid .. ':terminal_e164'
	local TerminalE164List = redis.call('SMEMBERS', KeyTermal)

	for i = 1,table.getn(TerminalE164List) do
		local KeyBaseInfo = 'terminal:' .. TerminalE164List[i] .. ':baseinfo'
		if redis.call('EXISTS', KeyBaseInfo) == 1 then 
			--Get terminal base info
			local Moid       = redis.call('HGET',KeyBaseInfo,'moid') or ""
			local DomainMoid = redis.call('HGET',KeyBaseInfo,'domain_moid') or ""
			local Name       = redis.call('HGET',KeyBaseInfo,'name') or ""
			local E164       = redis.call('HGET',KeyBaseInfo,'e164') or ""

			local VersionList = ""
			local IpList = ""

			--Get terminal online state and sip_link_protocol
			local Types = {}
			local KeyOnline = 'terminal:' .. Moid .. ':onlinestate'
			local OnlineNumber = redis.call('HLEN',KeyOnline)
			local OnlineState = 'online'
			if OnlineNumber == 0  then
				OnlineState = 'offline'
			else
				Types = redis.call('HKEYS', KeyOnline)
				for j = 1, table.getn(Types) do
					local KeyRunningInfo = "terminal:" .. Moid .. ":" .. string.gsub(Types[j], " ", "~") .. ":runninginfo"
					if redis.call("HLEN", KeyRunningInfo) ~= 0 then
						local Version = redis.call("HGET", KeyRunningInfo, "version") or ""
						
						if Version ~= "" then
						    if j == 1 then
								VersionList = Version
							else
								VersionList = VersionList .. "," .. Version
							end
					    end
					end
					
					-- ip
					local KeyNetInfo = "terminal:" .. Moid .. ":" .. string.gsub(Types[j], " ", "~") .. ":netinfo"
					if redis.call("HLEN", KeyNetInfo) ~= 0 then
						local IP = redis.call('HGET', KeyNetInfo, 'ip') or ""
						
						if IP ~= "" then
						    if j == 1 then
								IpList = IP
							else
								IpList = IpList..','..IP
							end
					    end
					end	
				end
			end

			-- 终端名称和ip筛选
			local NameMatchResult = string.match(Name, TerminalName)
			local IPMatchResult = string.match(IpList, TerminalName)
			local E164MatchResult = string.match(E164, TerminalName)
			if TerminalName == '' or NameMatchResult ~= nil or IPMatchResult ~= nil or E164MatchResult ~= nil then
				local TerminalInfo = {}
				TerminalInfo['moid'] = Moid
				TerminalInfo['domain_moid'] = DomainMoid
				TerminalInfo['name'] = Name
				TerminalInfo['e164'] = E164
				TerminalInfo['online'] = OnlineState
				TerminalInfo['version'] = VersionList
				TerminalInfo['ip'] = IpList
				TerminalInfo['type_ter'] = Types

				-- 在线终端排在前面
				if OnlineState == 'online' then
					table.insert(TerminalList,1,TerminalInfo)
				else
					table.insert(TerminalList,TerminalInfo)
				end
			end
		end
	end
end

local get_service_terminal_list
get_service_terminal_list = function(DomainMoid, TerminalName, TerminalList)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

    	local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
    	local DomainType = redis.call('HGET',KeyDomain,'type')

    	if "user" == DomainType then
    		get_user_terminal_list(SubDomainList[i], TerminalName, TerminalList)
    	elseif "service" == DomainType then
		    get_service_terminal_list(SubDomainList[i], TerminalName, TerminalList)
		end
    end
end

local TerminalList = {}
local DomainMoid = ARGV[1]
local TerminalName = ARGV[2]
local KeyDomain = 'domain:' .. DomainMoid .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    get_user_terminal_list(DomainMoid, TerminalName, TerminalList)
elseif "kernel" == DomainType or "service" == DomainType then
    get_service_terminal_list(DomainMoid, TerminalName, TerminalList)
end


local TotalCount = table.getn(TerminalList)
local Result = {}

if ('' == ARGV[3] and '' == ARGV[4]) then
    Result['terminal'] = TerminalList
else
    local Start = tonumber(ARGV[3])
    local Count = tonumber(ARGV[4])

    local MaxIndex = 1
    if Start + Count >  TotalCount then
        MaxIndex = TotalCount
    else
        MaxIndex = Start + Count
    end

    local ResultTerminalList = {}
    for i = Start + 1 ,MaxIndex do
        table.insert(ResultTerminalList,TerminalList[i])
    end

    Result['total_count'] = TotalCount
    Result['terminal'] = ResultTerminalList

end

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result
