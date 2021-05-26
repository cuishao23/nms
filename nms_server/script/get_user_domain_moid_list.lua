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

return cjson.encode(UserDomainMoidList)
