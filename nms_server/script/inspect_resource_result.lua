-- 会议资源巡检
--

local function getResource(machineRoomMoid)
    local r = {
        ["port_used"] = 0,
        ["sfu_used"] = 0,
        ["p2p_used"] = 0,
        ["port_remainder"] = 0,
        ["sfu_remainder"] = 0,
        ["p2p_remainder"] = 0
    }
    local inofKey = "machine_room:" .. machineRoomMoid .. ":info"
    local RemainderPort = tonumber(redis.call("HGET", inofKey, "remainder_port") or 0)
    local RemainderSfu = tonumber(redis.call("HGET", inofKey, "remainder_sfu") or 0)
    local PMeetingCount = tonumber(redis.call('HGET',inofKey,'total_port') or 0)
    local SfuMeetingCount = tonumber(redis.call('HGET',inofKey,'used_sfu') or 0)
    
    if PMeetingCount > RemainderPort then
        r["port_remainder"] = RemainderPort
        r['port_used'] = PMeetingCount - RemainderPort
    end

    r["sfu_remainder"] = RemainderSfu
    r['sfu_used'] = SfuMeetingCount

    local pasKeyInfo = 'machine_room:' .. machineRoomMoid .. ':pas_server'
    local PasServerList = redis.call('SMEMBERS', pasKeyInfo)
    for j = 1,table.getn(PasServerList) do
        local pasOnlineKey = "pas:" .. PasServerList[j] .. ":online"
        if redis.call('EXISTS', pasOnlineKey) == 1 then
            local maxCall = redis.call('HGET',pasOnlineKey,'max_call') or 0
            local curCall = redis.call('HGET',pasOnlineKey,'cur_call') or 0
            if tonumber(maxCall) > tonumber(curCall) then
                r['p2p_used'] = tonumber(curCall)
                r['p2p_remainder'] = tonumber(maxCall) - tonumber(curCall)
            end
        end
    end

    return r
end

local machineRoomMoidList = cjson.decode(ARGV[1])
local result = {
    ["port_used"] = 0,
    ["port_remainder"] = 0,
    ["sfu_used"] = 0,
    ["sfu_remainder"] = 0,
    ["p2p_used"] = 0,
    ["p2p_remainder"] = 0
}

-- 获取所有机房
for i, moid in pairs(machineRoomMoidList) do
    local info = getResource(moid)
    result["port_used"] = result["port_used"] + info["port_used"]
    result["port_remainder"] = result["port_remainder"] + info["port_remainder"]
    result["sfu_used"] = result["sfu_used"] + info["sfu_used"]
    result["sfu_remainder"] = result["sfu_remainder"] + info["sfu_remainder"]
    result["p2p_used"] = result["p2p_used"] + info["p2p_used"]
    result["p2p_remainder"] = result["p2p_remainder"] + info["p2p_remainder"]
end

return string.gsub(cjson.encode(result), "{}", "[]")
