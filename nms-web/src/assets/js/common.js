/**
 * 日期下拉菜单
 * @returns {*[]}
 */
export function getTimePeriod() {
  return [
    {
      value: 'selfdefine',
      label: '自定义'
    },
    {
      value: 'lasthour',
      label: '最近一小时'
    },
    {
      value: 'lastday',
      label: '最近一天'
    },
    {
      value: 'lastweek',
      label: '最近一周'
    },
    {
      value: 'lastmonth',
      label: '最近一个月'
    }
  ]
}

export function getLongTimePeriod() {
  return [
    {
      value: 'selfdefine',
      label: '自定义'
    },
    {
      value: 'lastday',
      label: '最近一天'
    },
    {
      value: 'lastweek',
      label: '最近一周'
    },
    {
      value: 'lastmonth',
      label: '最近一个月'
    },
    {
      value: 'lasthalfyear',
      label: '最近半年'
    },
    {
      value: 'lastyear',
      label: '最近一年'
    },
  ]
}
/**
 * 格式化当前时间
 * @returns {*[]}
 */
export function CurentTime() {
  var now = new Date();

  var year = now.getFullYear(); // 年
  var month = now.getMonth() + 1; // 月
  var day = now.getDate(); // 日

  var hh = now.getHours(); // 时
  var mm = now.getMinutes(); // 分
  var ss = now.getSeconds(); // 秒

  var clock = year.toString();

  if (month < 10)
    clock += "0";

  clock += month;

  if (day < 10)
    clock += "0";

  clock += day;

  if (hh < 10)
    clock += "0";

  clock += hh;

  if (mm < 10)
    clock += '0';

  clock += mm;

  if (ss < 10)
    clock += '0';

  clock += ss;

  return clock;
}

/**
* description: 获取当前日期，时间，周数
* create_time: 2019-4-19
* function: getDate，getTime，getWeek
*/

class DateTime {
  // 构造方法
  constructor() {
    // 列举Week
    this.weekday = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    // 获取当前时间
    this.Date = new Date();
    // 获取当前年
    this.year = this.Date.getFullYear();
    // 获取当前月
    this.month = this.Date.getMonth() + 1;
    // 获取当前日
    this.date = this.Date.getDate();
    // 获取当前星期几
    this.day = this.Date.getDay();
    // 获取小时
    this.hour = this.Date.getHours();
    // 获取分钟
    this.minute = this.Date.getMinutes();
    // 获取秒
    this.second = this.Date.getSeconds();
    // 自动补零
    this.month = (this.month < 10) ? '0' + this.month : this.month = this.month;
    this.date = (this.date < 10) ? '0' + this.date : this.date = this.date;
    this.hour = (this.hour < 10) ? '0' + this.hour : this.hour = this.hour;
    this.minute = (this.minute < 10) ? '0' + this.minute : this.minute = this.minute;
    this.second = (this.second < 10) ? '0' + this.second : this.second = this.second;
  };
  /**
  * 取当前日期
  * @returns {string}
  */
  getDate() {
    return this.year + '-' + this.month + '-' + this.date + ' ' + ' ';
  };
  /**
  * 获取当前时间
  * @returns {string}
  */
  getTime() {
    return this.hour + ':' + this.minute + ':' + this.second;
  };
  /**
  * 获取当前星期几
  *@returns {string}
  */
  getWeek() {
    return this.weekday[this.day]
  };
}
export { DateTime }

/**
* description: 格式化时间
* create_time: 2020-1-7
* function: FormatTime() p()
* 参数格式: Tue Jan 07 2020 11:20:38 GMT+0800 (中国标准时间)
* 返回值格式: 2020-01-07 11:20:38
*/
export function FormatTime(time) {
  const d = new Date(time)
  const resDate = d.getFullYear() + '-' + p((d.getMonth() + 1)) + '-' + p(d.getDate())
  const resTime = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds())
  return resDate+" "+resTime;
}
export function FormatTerminalTime(time) {
  const d = new Date(time)
  const resDate = d.getFullYear() + '-' + p((d.getMonth() + 1)) + '-' + p(d.getDate())
  const resTime = p(d.getHours()) + ':' + p(d.getMinutes())
  return resDate+" "+resTime;
}
export function FormatDateTime(time) {
  const d = new Date(time)
  const resDate = d.getFullYear() + '-' + p((d.getMonth() + 1)) + '-' + p(d.getDate())
  const resTime = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds())
  return resDate
}
/**
* description: 格式化时间
* create_time: 2020-1-7
* function: FormatTime() p()
* 参数格式: Tue Jan 07 2020 11:20:38 GMT+0800 (中国标准时间)
* 返回值格式: 11:20_20200107
*/
export function FormatChartTime(time) {
  const d = new Date(time)
  const resDate = Number((String(d.getFullYear()) + String(p((d.getMonth() + 1))) + String(p(d.getDate()))))
  const resTime = p(d.getHours()) + ':' + p(d.getMinutes())
  return resTime + "_" + resDate;
}
export function FormatDate(time) {
  const d = new Date(time)
  const resDate = p((d.getMonth() + 1)) + '-' + p(d.getDate())
  return resDate
}
function p(s) {
  return s < 10 ? '0' + s : s
}

/**
* description: 反格式化时间
* create_time: 2020-11-18
* function: UnFormatTime()
* 参数格式:  2019-03-07 12:00:00
* 返回值格式: Thu Mar 07 2019 12:00:00 GMT+0800 (中国标准时间)
*/
export function UnFormatTime(time) {
  var t = Date.parse(time)
  if (!isNaN(t)) {
    return new Date(Date.parse(time.replace(/-/g, '/')))
  }
}

/**
* description: 常用时间计算器
* create_time: 2020-1-7
* function: get_time()
*/
export function get_time(val) {
  let start = new Date();
  switch (val) {
      case "lasthour":
        return new Date(start.setTime(start.getTime() - 3600 * 1000));
      case "lastday":
        return new Date(start.setTime(start.getTime() - 3600 * 1000 * 24));
      case "lastweek":
        return new Date(start.setTime(start.getTime() - 3600 * 1000 * 24 * 7));
      case "lastmonth":
          return new Date(start.setTime(start.getTime() - 3600 * 1000 * 24 * 30));
      case "lastyear":
        return new Date(start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 12));
      case "lasthalfyear":
        return new Date(start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 6));
      default:
          return "";
  }
}

// 枚举视频分辨率格式
const TERMINAL_RES = {
  0: "ResAuto",
  1: "128*96",
  2: "176*144",
  3: "352*288",
  4: "352*576",
  5: "704*576",
  6: "1408*1152",
  7: "352*240",
  8: "2SIF",
  9: "704*480",
  10: "640*480",
  11: "800*600",
  12: "1024*768",
  13: "512*288",
  14: "112*96",
  15: "96*80",
  16: "1024*576",
  17: "1280*720",
  18: "1280*1024",
  19: "1600*1200",
  20: "1920*1080",
  21: "1920*1080",
  22: "1280*800",
  23: "1440*900",
  24: "1280*960",
  25: "1440*816",
  26: "1280*720",
  27: "960*544",
  28: "640*368",
  29: "480*272",
  30: "384*272",
  31: "640*544",
  32: "320*272",
  33: "960*544",
  34: "864*480",
  35: "640*368",
  36: "432*240",
  37: "320*192",
  38: "480*352",
  39: "720*480",
  40: "720*480",
  41: "720*576",
  42: "720*576",
  43: "1280*768",
  44: "1366*768",
  45: "1280*854",
  46: "1680*1050",
  47: "1920*1200",
  48: "V3840*2160",
  49: "1280*600",
  50: "1360*768",
  51: "3840*2160",
  52: "4096*2048",
  53: "4096*2160",
  54: "4096*2304",
  55: "960*540",
  56: "480*270",
  57: "640*360",
  58: "320*180",
  59: "480x268"
}
export {TERMINAL_RES}

// 枚举视频格式
const TERMINAL_VIDEO_FORMAT = {
  0: 'H261',
  1: 'H262',
  2: 'H263',
  3: 'H263plus',
  4: 'H264',
  5: 'MPEG4',
  6: 'H265'
}
export {TERMINAL_VIDEO_FORMAT}

// 枚举音频格式
const TERMINAL_AUDIO_FORMAT = {
  0: 'G711a',
  1: 'G711u',
  2: 'G722',
  3: 'G7231',
  4: 'G728',
  5: 'G729',
  6: 'MP3',
  7: 'G721',
  8: 'G7221',
  9: 'G719',
  10: 'MpegAACLC',
  11: 'MpegAACLD',
  12: 'Opus'
}
export {TERMINAL_AUDIO_FORMAT}

/**
* description: 保留两位小数
* create_time: 2020-11-26
* function: KeepTwoNum()
* 参数格式:   200.631    100.6   60
* 返回值格式: 200.63     100.6   60
*/
export function KeepTwoNum(num) {
  num = Number(num)
  let y = String(num).indexOf(".") + 1 //获取小数点的位置
  var count = String(num).length - y //获取小数点后的个数
  if(y > 0 && count >2) {
    return Number(num.toFixed(2))
  } else {
    return num
  }
}
