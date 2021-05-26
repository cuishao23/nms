local DevMoid = ARGV[1]
local DevType = ARGV[2]
local IsTerminal = ARGV[3]
local CollectorInfo = {}

if IsTerminal == 1 or IsTerminal == '1' then
	local KeyInfo = 'terminal:' .. DevMoid .. ':collectorid'
	if redis.call('EXISTS', KeyInfo) == 1 then 
		--Get server info
		local CollectorId = redis.call('HGET',KeyInfo,DevType) or ""
		
		--Get collector info
		local CollectorDevMoid = "collector:"..CollectorId..":info"
		local DevMoid = redis.call("HGET", CollectorDevMoid, "p_server_moid") or ""

	    -- Format collector info object
	    if DevMoid == '' then
	    	CollectorInfo['success'] = 0
		    CollectorInfo['error_code'] = 10400
	    else
			CollectorInfo['success'] = 1
			CollectorInfo['dev_moid'] = DevMoid
		end
	else
		CollectorInfo['success'] = 0
		CollectorInfo['error_code'] = 10500
	end
else
	local KeyInfo = 'p_server:' .. DevMoid .. ':info'
	if redis.call('EXISTS', KeyInfo) == 1 then 
		--Get server info
		local CollectorId = redis.call('HGET',KeyInfo,'collectorid') or ""
		
		--Get collector info
		local CollectorDevMoid = "collector:"..CollectorId..":info"
		local DevMoid = redis.call("HGET", CollectorDevMoid, "p_server_moid") or ""

	    -- Format collector info object
		if DevMoid == '' then
	    	CollectorInfo['success'] = 0
		    CollectorInfo['error_code'] = 20400
	    else
			CollectorInfo['success'] = 1
			CollectorInfo['dev_moid'] = DevMoid
		end
	else
		CollectorInfo['success'] = 0
		CollectorInfo['error_code'] = 20500
	end
end

return cjson.encode(CollectorInfo)
