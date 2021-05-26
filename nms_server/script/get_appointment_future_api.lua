
-- 日期格式必须为 2018/10/03 13:07:12 这种类型
local str2date = function(DateStr)
    if DateStr == nil or DateStr == "" then
        return 0
    end
    local Sep = "/"
    if string.find(DateStr, "/", 1) == nil then
        Sep = "-"
    end
    local Pos1 = string.find(DateStr, Sep, 1)
    if Pos1 == nil then
        return 0
    end
    local Year = string.sub(DateStr, 1, Pos1 - 1)
    local Pos2 = string.find(DateStr, Sep, Pos1 + 1)
    if Pos2 == nil then
        return 0
    end
    local Month = string.sub(DateStr, Pos1 + 1, Pos2 - 1)
    local Pos3 = string.find(DateStr, " ", Pos2 + 1)
    if Pos3 == nil then
        return 0
    end
    local Day = string.sub(DateStr, Pos2 + 1, Pos3 - 1)
    local Pos4 = string.find(DateStr, ":", Pos3 + 1)
    if Pos4 == nil then
        return 0
    end
    local Hour = string.sub(DateStr, Pos3 + 1, Pos4 - 1)
    local Pos5 = string.find(DateStr, ":", Pos4 + 1)
    if Pos5 == nil then
        return 0
    end
    local Min = string.sub(DateStr, Pos4 + 1, Pos5 - 1)
    local Sec = string.sub(DateStr, Pos5 + 1)
    return {year = tonumber(Year, 10), month = tonumber(Month, 10), day = tonumber(Day, 10),
        hour = tonumber(Hour, 10), minute = tonumber(Min, 10), second = tonumber(Sec, 10)}
end

--是否闰年
local is_leap_year = function(Date)
    if(Date.year % 400 == 0 or (Date.year % 4 == 0 and Date.year % 100 ~= 0))then
        return true
    else
        return false
    end
end

-- 下一个小时
local date_next_hour = function(Date)
    local IsLeapYear = is_leap_year(Date)
    if Date.hour < 23 then
        Date.hour = Date.hour + 1
        return Date
    else
        Date.hour = 0
        if Date.month == 2 then
            if IsLeapYear then
                if Date.day == 29 then
                    Date.month = Date.month + 1
                    Date.day = 1
                    return Date
                else
                    Date.day = Date.day + 1
                    return Date
                end
            else
                if Date.day == 28 then
                    Date.month = Date.month + 1
                    Date.day = 1
                    return Date
                else
                    Date.day = Date.day + 1
                    return Date
                end
            end
        elseif Date.month == 1 or Date.month == 3 or Date.month == 5 or Date.month == 7 or Date.month == 8
                or Date.month == 10 or Date.month == 12 then
            if Date.day == 31 then
                Date.day = 1
                if Date.month == 12 then
                    Date.month = 1
                    Date.year = Date.year + 1
                    return Date
                else
                    Date.month = Date.month + 1
                    return Date
                end
            else
                Date.day = Date.day + 1
                return Date
            end
        elseif Date.month == 4 or Date.month == 6 or Date.month == 9 or Date.month == 11 then
            if Date.day == 30 then
                Date.day = 1
                Date.month = Date.month + 1
                return Date
            else
                Date.day = Date.day + 1
                return Date
            end
        end
    end
end

-- 日期大小比较, D1 >= D2返回true,否则返回false
local date_great_than = function(D1, D2)
    if D1 == 0 then
        return true
    end
    if D2 == 0 then
        return false
    end
    if D1.year > D2.year then
        return true
    elseif D1.year < D2.year then
        return false
    else
        if D1.month > D2.month then
            return true
        elseif D1.month < D2.month then
            return false
        else
            if D1.day > D2.day then
                return true
            elseif D1.day < D2.day then
                return false
            else
                if D1.hour > D2.hour then
                    return true
                elseif D1.hour < D2.hour then
                    return false
                else
                    if D1.minute > D2.minute then
                        return true
                    elseif D1.minute < D2.minute then
                        return false
                    else
                        if D1.second > D2.second then
                            return true
                        elseif D1.second < D2.second then
                            return false
                        else
                            return true
                        end
                    end
                end
            end
        end
    end
end

-- 日期数字转字符串
local time_num2str = function(Num)
    if Num < 10 then
        return "0"..tostring(Num)
    else
        return tostring(Num) or ""
    end
end

-- 日期转字符串
local date2str = function(Date)
    if Date == nil or Date == "" then
        return ""
    end
    return time_num2str(Date.year).."/"..time_num2str(Date.month).."/"..time_num2str(Date.day).." "
    ..time_num2str(Date.hour)..":"..time_num2str(Date.minute)..":"..time_num2str(Date.second)
end

local get_service_user_list = function(Moid)
    local Users = {}
    local Key = "domain:"..Moid..":sub"
    local MoidList = redis.call("SMEMBERS", Key)
    for i = 1,#MoidList do
        local UserInfoKey = "domain:"..MoidList[i]..":info"
        local Type = redis.call("HGET", UserInfoKey, "type")
        if Type == "user" then
            Users[#Users + 1] = MoidList[i]
        end
    end
    return Users
end

local get_user_a_meeting_list = function(Moid, Result)
    local UserDomainAppointmentKey = "domain:"..Moid..":a_meeting"
    local AppointmentList = redis.call("SMEMBERS", UserDomainAppointmentKey)
    for i=1,#AppointmentList do
        local InfoKey = "a_meeting:"..AppointmentList[i]..":info"
        if redis.call("EXISTS", InfoKey) == 1 then
            local StartTime = redis.call("HGET", InfoKey, "start_time") or "1970/01/01 00:00:01"
            local EndTime = redis.call("HGET", InfoKey, "end_time") or "9999/12/31 23:59:59"
            Result[#Result+1] = {StartTime, EndTime}
        end
    end
end

local get_user_appointment_list = function(DomainMoid, Result)
    get_user_a_meeting_list(DomainMoid, Result)

end

local get_all_service = function()
    local Result = redis.call("SCAN", "0", "MATCH", "domain:*:info", "COUNT", "100000")
    local Keys = Result[2]
    local ServiceList = {}
    for i=1,#Keys do
        local Type = redis.call("HGET", Keys[i], "type")
        if Type == "service" then
            local Moid = redis.call("HGET", Keys[i], "moid")
            ServiceList[#ServiceList+1] = Moid
        end
    end
    return ServiceList
end

local Moid = ARGV[1]
local StartTime = ARGV[2]
local EndTime = ARGV[3]
local TimeList = {}
local TmpDate = str2date(StartTime)
TimeList[#TimeList + 1] = {date2str(TmpDate), 0}
for i=2, 24 do
    TimeList[#TimeList + 1] = {date2str(date_next_hour(TmpDate)), 0}
end

local Result = {}

local DomainType = redis.call("HGET", "domain:"..Moid..":info", "type")
if DomainType == "kernel" then
    Moid = "all"
end

if Moid == "all" then
    local ServiceList = get_all_service()
    for i=1,#ServiceList do
        local Users = get_service_user_list(ServiceList[i])
        for j=1,#Users do
            get_user_appointment_list(Users[j], Result)
        end
    end
else
    local DomainInfoKey = "domain:"..Moid..":info"
    local Type = redis.call("HGET", DomainInfoKey, "type")
    if Type == "user" then
        get_user_appointment_list(Moid, Result)
    elseif Type == "service" then
        local Users = get_service_user_list(Moid)
        for i=1,#Users do
            get_user_appointment_list(Users[i], Result)
        end
    end
end

for i=1,#Result do
    local Item = Result[i]
    for j=1,#TimeList do
        local Date1 = str2date(Item[1])
        local Date2 = str2date(Item[2])
        local Time = str2date(TimeList[j][1])
        if date_great_than(Time, Date1) and date_great_than(Date2, Time) then
            TimeList[j][2]= TimeList[j][2] + 1
        end
    end
end

local Time = {}
local Values = {}
local Max = 0
local Min = 0
local Sum = 0
for i=1,#TimeList do
    local Item = TimeList[i]
    if i == 1 then
        Min = Item[2]
    end
    Time[#Time+1] = Item[1]
    Values[#Values+1] = Item[2]
    if Item[2] > Max then
        Max = Item[2]
    end
    if Item[2] < Min then
        Min = Item[2]
    end
    Sum = Sum + Item[2]
end

local JsonObj = {}
JsonObj["success"] = 1
local Statistic = {}
Statistic["max"] = Max
Statistic["min"] = Min
local Average, _ = math.modf(Sum/#Time)
Statistic["average"] = Average
Statistic["time"] = Time
Statistic["values"] = Values
JsonObj["statistic"] = Statistic

return cjson.encode(JsonObj)