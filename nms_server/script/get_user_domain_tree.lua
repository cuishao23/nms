local function get_domain_tree(Moid,DomainInfoList)
    local keyInfo = "domain:" .. Moid .. ":info"
    local Type = redis.call("HGET",keyInfo,"type")
    if Type ~= "platform" then
        local domainInfo = {}
        domainInfo['moid'] = redis.call("HGET",keyInfo,"moid") or ""
        domainInfo['name'] = redis.call("HGET",keyInfo,"name") or ""
        domainInfo['type'] = redis.call("HGET",keyInfo,"type") or ""
        domainInfo['parent_moid'] = redis.call("HGET",keyInfo,"parent_moid") or ""
        table.insert(DomainInfoList,domainInfo)
        
        local KeySub = "domain:" .. Moid .. ":sub"
        if redis.call("EXISTS",KeySub) == 1 then
            local MoidList = redis.call("SMEMBERS",KeySub)
            for i,v in ipairs(MoidList) do
                get_domain_tree(v,DomainInfoList)
            end
        end
    end
end

local DomainInfoList = {}

local DomainMoid = ARGV[1]
local KeyDomain = 'domain:' .. DomainMoid .. ':info'
local DomainType = redis.call('HGET',KeyDomain,'type')

if "user" == DomainType then
    local domainInfo = {}
    domainInfo['moid'] = redis.call('HGET',KeyDomain,'parent_moid') or ''
    local serviceKey = 'domain:' .. domainInfo['moid'] .. ':info'
    domainInfo['name'] = redis.call("HGET",serviceKey,"name") or ""
    domainInfo['type'] = redis.call("HGET",serviceKey,"type") or ""
    domainInfo['parent_moid'] = redis.call("HGET",serviceKey,"parent_moid") or ""
    table.insert(DomainInfoList,domainInfo)
    get_domain_tree(ARGV[1],DomainInfoList)
elseif "kernel" == DomainType or "service" == DomainType then
    get_domain_tree(ARGV[1],DomainInfoList)    
end

return cjson.encode(DomainInfoList)




