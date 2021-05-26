local IPTerminalList = {}
local KeyTerminal = 'meeting:' .. ARGV[1] .. ':ip_e164'
local TerminalList = redis.call('SMEMBERS', KeyTerminal)
	
for i = 1,table.getn(TerminalList) do
	local KeyTerminalInfo = "ip_e164:" .. TerminalList[i] .. ":conf:" .. ARGV[1] .. ":info"
	local Name = redis.call("HGET", KeyTerminalInfo, "name") or ""

    -- 终端名称筛选
	local matchResult = string.match(Name, ARGV[2])
	if ARGV[2] == '' or matchResult ~= nil then
		local TerminalInfo = {}
		TerminalInfo["name"] = Name
		TerminalInfo["ip"] = TerminalList[i]
   		table.insert(IPTerminalList,TerminalInfo)
   	end
 end

local TotalCount = table.getn(IPTerminalList)

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
    table.insert(ResultTerminalList,IPTerminalList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['ip_terminal'] = ResultTerminalList

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result