local get_service_domain_tree
get_service_domain_tree = function( DomainInfoIndex, DomainInfoList, SubIndex, SubMoidList )
	if SubIndex > table.getn(SubMoidList) then
		return DomainInfoList
	else
		local KeyInfo = 'domain:' .. SubMoidList[SubIndex] .. ':info'
		local Type    = redis.call('HGET',KeyInfo,'type')

		if Type ~= 'user' and Type ~= 'platform' then

			local DomainInfo = {}
			DomainInfo['moid'] = SubMoidList[SubIndex]
			DomainInfo['name'] = redis.call("HGET",KeyInfo,"name") or ""
			DomainInfo['type'] = redis.call("HGET",KeyInfo,"type") or ""
			DomainInfo['parent_moid'] = redis.call("HGET",KeyInfo,"parent_moid") or ""
			DomainInfoList[DomainInfoIndex+1] = DomainInfo
			DomainInfoIndex = DomainInfoIndex+1

			local KeySub = 'domain:' .. SubMoidList[SubIndex] .. ':sub'
			local SubList = redis.call('SMEMBERS', KeySub)

			--新的moid添加到数组末尾
			local MoidListLen = table.getn(SubMoidList)
			for i = 1,table.getn(SubList) do
				SubMoidList[MoidListLen+i] = SubList[i]
			end
		end

		get_service_domain_tree( DomainInfoIndex, DomainInfoList, SubIndex+1, SubMoidList )
	end
end

local DomainInfoList = {}
local KeyInfo = 'domain:' .. ARGV[1] .. ':info'

local DomainInfo = {}
DomainInfo['moid'] = ARGV[1]
DomainInfo['name'] = redis.call("HGET",KeyInfo,"name") or ""
DomainInfo['type'] = redis.call("HGET",KeyInfo,"type") or ""
DomainInfo['parent_moid'] = redis.call("HGET",KeyInfo,"parent_moid") or ""
DomainInfoList[1] = DomainInfo

local Key = 'domain:' .. ARGV[1] .. ':sub'
local SubMoidList = redis.call('SMEMBERS', Key)
get_service_domain_tree(1,DomainInfoList,1,SubMoidList)
return cjson.encode(DomainInfoList)