const warnings = {
  "warning_notify_list": [{
    "warning_notify_id": "ed355927-6907-452c-862c-86c5313b9136",
    "warning": "智能插座已达最大使用寿命,智能插座离线",
    "email": "",
    "phone": "12332112221",
    "wechat": ""
  }],
  "total_count": 1
};
const subwarningcode = [{
  "type": "其他",
  "code": 4002,
  "name": "智能插座离线",
  "level": "critical",
  "description": "终端会场中的智能插座离线",
  "suggestion": "1.请确认智能中控主机的SSID名称是否修改,如果有改动,则重新初始化智能插座并配对。2.请确认中控主机的无线热点是否稳定,如不稳定则请更换中控主机。3.请重新初始化智能插座,并进行配对;如果此措施无效,请更换智能插座"
}, {
  "type": "其他",
  "code": 4001,
  "name": "智能插座已达最大使用寿命",
  "level": "important",
  "description": "终端会场中的智能插座已达到最大使用寿命，请更换",
  "suggestion": "请更换新的智能插座并重新与中控设备进行配对"
}];
export {warnings, subwarningcode}
