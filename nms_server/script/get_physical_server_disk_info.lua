local Result = {}
local KeyInfo = 'p_server:' .. ARGV[1] .. ':resource'
if redis.call('EXISTS', KeyInfo) == 1 then 
	--Get server resource
	local DiskNum = redis.call('HGET',KeyInfo,'disk_count') or 0

	Result['disknum'] = DiskNum

	for i = 1, DiskNum do
		local DiskName = redis.call('HGET',KeyInfo,'disk' .. i .. '_name') or ''
		local DiskTotal = redis.call('HGET',KeyInfo,'disk' .. i .. '_total') or ''
		local DiskAge = redis.call('HGET',KeyInfo,'disk' .. i .. '_age') or ''
		local DiskUserate = redis.call('HGET',KeyInfo,'disk' .. i .. '_userate') or ''
		local DiskUsed = redis.call('HGET',KeyInfo,'disk' .. i .. '_used') or ''

		-- Format server resource object
		Result['disk' .. i .. '_name'] = DiskName
		Result['disk' .. i .. '_total'] = DiskTotal
		Result['disk' .. i .. '_age'] = DiskAge
		Result['disk' .. i .. '_userate'] = DiskUserate
		Result['disk' .. i .. '_used'] = DiskUsed
	end	
end

return cjson.encode(Result)
