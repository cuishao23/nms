-- 删除告警信息
-- 参数: type moid code
local key = ARGV[1] .. ":" .. ARGV[2] .. ":warning"
local code = ARGV[3]
redis.call("HDEL", key, code)
