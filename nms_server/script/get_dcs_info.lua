local DcsInfo = {}
local CoopState = ARGV[2]
local DcsInfoKey = "meeting:" .. ARGV[1] .. ":dcs_info"
if redis.call("HLEN", DcsInfoKey) ~= 0 then
	DcsInfo['start_time'] = redis.call("HGET", DcsInfoKey, "start_time") or ""
    DcsInfo['dcs_mode'] = redis.call("HGET", DcsInfoKey, "dcs_mode") or ""
    DcsInfo['mode_start_time'] = redis.call("HGET", DcsInfoKey, "mode_start_time") or ""
end

local DcsUserList = {}
local DcsUserKey = "meeting:" .. ARGV[1] .. ":dcs_terminals"
local UserList = redis.call('SMEMBERS', DcsUserKey)

for i = 1,table.getn(UserList) do
    local UserInfoKey = "terminal:" .. UserList[i] .. ":conf:" .. ARGV[1] .. ":info_for_dcs"

	if redis.call("HLEN", UserInfoKey) ~= 0 then
		local State = redis.call("HGET", UserInfoKey, "coop_state") or ""
		if CoopState == State then
	        local DcsUserInfo = {}
		    DcsUserInfo['e164'] = redis.call("HGET", UserInfoKey, "e164") or ""
		    DcsUserInfo['name'] = redis.call("HGET", UserInfoKey, "name") or ""
		    DcsUserInfo['coop_state'] = redis.call("HGET", UserInfoKey, "coop_state") or ""
		    DcsUserInfo['begin_time'] = redis.call("HGET", UserInfoKey, "begin_time") or ""
		    DcsUserInfo['end_time'] = redis.call("HGET", UserInfoKey, "end_time") or ""
	    	table.insert(DcsUserList,DcsUserInfo)
	    end
	end
end

local TotalCount = table.getn(DcsUserList)

local Start = tonumber(ARGV[3])
local Count = tonumber(ARGV[4])

local MaxIndex = 1
if Start + Count >  TotalCount then
    MaxIndex = TotalCount
else
    MaxIndex = Start + Count
end

local ResultUserList = {}
for i = Start + 1 ,MaxIndex do
    table.insert(ResultUserList,DcsUserList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['user'] = ResultUserList
Result['dcsinfo'] = DcsInfo

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result