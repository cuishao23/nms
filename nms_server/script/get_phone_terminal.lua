local MeetingTerminalList = {}
local KeyTerminal = 'meeting:' .. ARGV[1] .. ':telphone'
local TerminalList = redis.call('SMEMBERS', KeyTerminal)
	
for i = 1,table.getn(TerminalList) do
    -- 终端名称筛选
	local matchResult = string.match(TerminalList[i], ARGV[2])
	if ARGV[2] == '' or matchResult ~= nil then
   		table.insert(MeetingTerminalList,TerminalList[i])
   	end
 end

local TotalCount = table.getn(MeetingTerminalList)

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
    table.insert(ResultTerminalList,MeetingTerminalList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['phone'] = ResultTerminalList

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result