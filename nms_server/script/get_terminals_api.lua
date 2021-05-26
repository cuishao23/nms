local get_terminal_list = function(user_domain_moid,TerminalList)
	local KeyTermal = 'domain:' .. user_domain_moid .. ':terminal_e164'

	local TerminalE164List = redis.call('SMEMBERS', KeyTermal)

	-- 过滤掉E164号为空的数据
	for i = 1, table.getn(TerminalE164List) do 
		local KeyBaseInfo = 'terminal:' .. TerminalE164List[i] .. ':baseinfo'
		if redis.call('EXISTS', KeyBaseInfo) == 1 then 
			--Get terminal base info
			local Moid       = redis.call('HGET',KeyBaseInfo,'moid') or ""
			local DomainMoid = redis.call('HGET',KeyBaseInfo,'domain_moid') or ""
			local Name       = redis.call('HGET',KeyBaseInfo,'name') or ""
			local E164       = redis.call('HGET',KeyBaseInfo,'e164') or ""

			local IpList = ""

			--Get terminal online state
			local KeyOnline = 'terminal:' .. Moid .. ':onlinestate'
			local OnlineNumber = redis.call('HLEN',KeyOnline)
			local OnlineState = 'online'
			if OnlineNumber == 0  then
					OnlineState = 'offline'
			else
				local Types = redis.call('HKEYS', KeyOnline)
				for j = 1, table.getn(Types) do

					local KeyNetInfo = "terminal:" .. Moid .. ":" .. string.gsub(Types[j], " ", "~") .. ":netinfo"
					local IP = redis.call('HGET', KeyNetInfo, 'ip') or ""
					if string.len(IpList) == 0 then
						if string.len(IP) > 0 then
							IpList = IP
						end
					else
						if string.len(IP) > 0 then
							IpList = IpList..';'..IP
						end
					end	
				end		
			end

			-- Format terminal info object
			local TerminalInfo = {}
			TerminalInfo['moid'] = Moid
			TerminalInfo['domain_moid'] = DomainMoid
			TerminalInfo['name'] = Name
			TerminalInfo['e164'] = E164
			TerminalInfo['ip'] = IpList
			TerminalInfo['online'] = OnlineState
			if E164 ~= '' then
				table.insert(TerminalList,TerminalInfo)
			end
		end	
	end
end

-- 获取指定域下所有的用户域moid
local get_all_user_domain
get_all_user_domain = function( UserDomainMoidList, SubIndex, SubMoidList )
	if SubIndex > table.getn(SubMoidList) then
		return
	else
		local KeyInfo = 'domain:' .. SubMoidList[SubIndex] .. ':info'
		local Type    = redis.call('HGET',KeyInfo,'type')
		if Type == "user" then
			table.insert(UserDomainMoidList,SubMoidList[SubIndex])
		elseif Type == 'service' or Type == 'kernel' then

			local KeySub = 'domain:' .. SubMoidList[SubIndex] .. ':sub'
			local SubList = redis.call('SMEMBERS', KeySub)

			--新的moid添加到数组末尾
			for i = 1,table.getn(SubList) do
				table.insert(SubMoidList,SubList[i])
			end
		end

		get_all_user_domain(UserDomainMoidList, SubIndex+1, SubMoidList )
	end
end


local UserDomainMoidList = {}
local SubMoidList = {}
table.insert(SubMoidList,ARGV[1])
get_all_user_domain(UserDomainMoidList,1,SubMoidList)

local TerminalList = {}
for i=1,#UserDomainMoidList do
	get_terminal_list(UserDomainMoidList[i],TerminalList)
end

local TotalCount = table.getn(TerminalList)

local Start = tonumber(ARGV[2])
local Count = tonumber(ARGV[3])

local ResultTerminalList = {}
local MaxIndex = 1
if Start + Count >  TotalCount then
	MaxIndex = TotalCount
else
	MaxIndex = Start + Count
end

for i = Start + 1, MaxIndex do
	table.insert(ResultTerminalList,TerminalList[i])
end

local Result = {};
Result['success'] = 1
Result['total_count'] = TotalCount
Result['terminals'] = ResultTerminalList

return string.gsub(cjson.encode(Result), "{}", "[]")