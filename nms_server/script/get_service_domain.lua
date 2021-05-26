-- 参数: 超管moid(kedacom moid) 或 用户域moid
-- return: 获取当前登录账户的服务域

local serviceMoid = ''

local KeyDomain = 'domain:' .. ARGV[1] .. ':info'
if redis.call("EXISTS",KeyDomain) == 1 then
    local DomainType = redis.call('HGET',KeyDomain,'type') or ''
    if "kernel" == DomainType then
        local SubKey = 'domain:'..ARGV[1]..':sub'
        local SubDomainList = redis.call('SMEMBERS', SubKey)
        if table.getn(SubDomainList) <= 0 then
            return
        end
        for i = 1, table.getn(SubDomainList) do
            local KeyDomain = 'domain:' .. SubDomainList[i] .. ':info'
            local DomainType = redis.call('HGET',KeyDomain,'type')
            if "service" == DomainType then
                serviceMoid = redis.call('HGET',KeyDomain,'moid')
            end
        end
    elseif "service" == DomainType then
        serviceMoid = redis.call('HGET',KeyDomain,'moid') or ''
    elseif "user" == DomainType then
        serviceMoid = redis.call('HGET',KeyDomain,'parent_moid') or ''
    end
end
return serviceMoid