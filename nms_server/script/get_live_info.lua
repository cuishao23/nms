local LiveInfo = {}
local LiveInfoKey = "meeting:" .. ARGV[1] .. ":live"
if redis.call("HLEN", LiveInfoKey) ~= 0 then
    LiveInfo['live_name'] = redis.call("HGET", LiveInfoKey, "live_name") or ""
    LiveInfo['start_time'] = redis.call("HGET", LiveInfoKey, "live_start_time") or ""
    LiveInfo['encmode'] = redis.call("HGET", LiveInfoKey, "encmode") or ""
    LiveInfo['authmode'] = redis.call("HGET", LiveInfoKey, "authmode") or ""
    LiveInfo['max_user_time'] = redis.call("HGET", LiveInfoKey, "max_user_time") or ""
    LiveInfo['max_user_count'] = redis.call("HGET", LiveInfoKey, "max_user_count") or ""
    LiveInfo['current_user_count'] = redis.call("HGET", LiveInfoKey, "max_user_count") or ""
end

local LiveUserList = {}
local LiveUserKey = "meeting:" .. ARGV[1] .. ":live_users"
local UserList = redis.call('SMEMBERS', LiveUserKey)

for i = 1,table.getn(UserList) do
    local UserInfoKey = "user:" .. UserList[i] .. ":conf:" .. ARGV[1] .. ":info_for_live"

	if redis.call("HLEN", UserInfoKey) ~= 0 then
        local LiveUserInfo = {}
	    LiveUserInfo['moid'] = redis.call("HGET", UserInfoKey, "moid") or ""
	    LiveUserInfo['e164'] = redis.call("HGET", UserInfoKey, "e164") or ""
	    LiveUserInfo['name'] = redis.call("HGET", UserInfoKey, "name") or ""
	    LiveUserInfo['enter_time'] = redis.call("HGET", UserInfoKey, "enter_time") or ""
	    table.insert(LiveUserList,LiveUserInfo)
	end
end

local TotalCount = table.getn(LiveUserList)

local Start = tonumber(ARGV[2])
local Count = tonumber(ARGV[3])

local MaxIndex = 1
if Start + Count >  TotalCount then
    MaxIndex = TotalCount
else
    MaxIndex = Start + Count
end

local ResultUserList = {}
for i = Start + 1 ,MaxIndex do
    table.insert(ResultUserList,LiveUserList[i])
end

local Result = {}
Result['total_count'] = TotalCount
Result['user'] = ResultUserList
Result['liveinfo'] = LiveInfo

Result = string.gsub(cjson.encode(Result), "{}", "[]")
return Result