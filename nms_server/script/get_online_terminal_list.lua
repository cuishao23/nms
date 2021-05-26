local get_user_terminal_list = function(ParentMoid, Result)
	local KeyTermal = 'domain:' .. ParentMoid .. ':terminal'
	local TerminalList = redis.call('SMEMBERS', KeyTermal)

	for i = 1,table.getn(TerminalList) do

		local KeyBaseInfo = 'terminal:' .. TerminalList[i] .. ':baseinfo'
		if redis.call('EXISTS', KeyBaseInfo) == 1 then 
			--Get terminal base info
			local Moid = redis.call('HGET',KeyBaseInfo,'moid') or ""
			local Name = redis.call('HGET',KeyBaseInfo,'name') or ""

			--Get online terminal
			local KeyOnline = 'terminal:' .. Moid .. ':onlinestate'
			if redis.call('HLEN',KeyOnline) ~= 0  then

				local Types = redis.call('HKEYS', KeyOnline)
				local NetCards = {}
				for j = 1, table.getn(Types) do
					-- netcards
					local Type = string.gsub(Types[j], " ", "~")
					local KeyNetInfo = "terminal:" .. Moid .. ":" .. Type .. ":netcards"
					local NetCardList = redis.call('SMEMBERS', KeyNetInfo) or ""
					NetCards[Type] = NetCardList
				end

				-- Format terminal info object
				local TerminalInfo = {}
				TerminalInfo['moid'] = Moid
				TerminalInfo['domain_moid'] = ParentMoid
				TerminalInfo['name'] = Name
				TerminalInfo['type'] = Types
				TerminalInfo['netcards'] = NetCards
				table.insert(Result,TerminalInfo)
			end
		end
	end
end

local get_service_terminal_list
get_service_terminal_list = function(DomainMoid, Result)
    local SubKey = 'domain:'..DomainMoid..':sub'
    local SubDomainList = redis.call('SMEMBERS', SubKey)
    if table.getn(SubDomainList) <= 0 then
        return
    end
    for i = 1, table.getn(SubDomainList) do

    	local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
    	local DomainType = redis.call('HGET',KeyDomain,'type')

    	if "user" == DomainType then
    		get_user_terminal_list(SubDomainList[i], Result)
    	elseif "service" == DomainType then
		    get_service_terminal_list(SubDomainList[i], Result)
		end
    end
end

local Result = {}
local KeyDomain = 'domain:' .. ARGV[1] .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    get_user_terminal_list(ARGV[1], Result)
elseif "kernel" == DomainType or "service" == DomainType then
    get_service_terminal_list(ARGV[1], Result)
end

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result
