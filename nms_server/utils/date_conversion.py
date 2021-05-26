# coding:utf-8
import datetime

# 转换时间格式
def get_time(old_time):
    if old_time == None:
        pass
    else:
        new_time = datetime.datetime.strftime(old_time, "%Y-%m-%d %H:%M:%S")
        return new_time

# graphite时间格式转化,不计算时分秒，如下
# "2020/03/15 14:30:40" -> "00:00_20200315" start_time
# "2020/03/15 14:30:40" -> "23:59_20200315" end_time
# 或
# "2020-03-15 14:30:40" -> "00:00_20200315" start_time
# "2020-03-15 14:30:40" -> "23:59_20200315" end_time

def graphite_time(date_time, types):
    if types not in ['from','to']:
        raise ValueError
    start_time = date_time.split(' ')[0]
    now_date = datetime.date.today() + datetime.timedelta()

    if start_time == str(now_date) and types == 'from':
        from_time = start_time = date_time.split(' ')[1].rsplit(":",1)[0]
        default_time = {
            'from': from_time,
            'to': '23:59'
        }
    else:
        default_time = {
            'from': "00:00",
            'to': '23:59'
        }

    date_str = str()
    date_str = date_time.split(' ')[0].replace('/', '').replace('-', '')    
    return default_time[types] + '_' + date_str


# iso8601时间格式转化为graphite时间格式,不计算时分秒，如下
# "2020-03-15T14:30:40+08:00" -> "00:00_20200315" start_time
# "2020-03-15T14:30:40+08:00" -> "23:59_20200315" end_time
def iso_time_format(data_time):
    try:
        return datetime.datetime.strptime(data_time.replace(" ","+"), "%Y-%m-%dT%H:%M:%S+08:00").strftime("%H:%M_%Y%m%d")
    except:
        return False

'''
时间戳转换iso时间格式
1564588800  ->  "2020-03-15T14:30:40+08:00"
''' 
def timestamp_to_iso_time(time_sj):     #传入参数
    time_array = datetime.datetime.fromtimestamp(time_sj)
    time_str = time_array.strftime("%Y/%m/%dT%H:%M:%S+08:00")            #时间戳转换正常时间
    return time_str       #返回日期，格式为str


def period_transform(period):
    periodArr = {
        'lastweek':'-1w',
        'lastmonth':'-1mon',
        'lastthreemonth':'-3mon',
        'lasthalfyear':'-6mon',
        'lastyear':'-1y'
    } 
    try:
        return periodArr[period]
    except:
        return False



'''
时间戳转换年月日时间格式
1564588800  ->  "2020/03/15 14:30:40"
''' 
def timestamp_to_time(time_sj):     #传入参数
    time_array = datetime.datetime.fromtimestamp(time_sj)
    time_str = time_array.strftime("%Y/%m/%d %H:%M:%S")            #时间戳转换正常时间
    return time_str       #返回日期，格式为str

''' 
@description: 获取指定时间和当前时间的时间差，单位：s
@param {str} "2020/03/15 14:30:40"
@return: {int}
'''
def time_difference(time_str):
    return (datetime.datetime.now() - datetime.datetime.strptime(time_str,"%Y/%m/%d %H:%M:%S")).seconds