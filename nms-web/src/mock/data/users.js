const users = [{
  "domainMoid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "userMoid": "mooooooo-oooo-oooo-oooo-defaultadmin",
  "role": 1,
  "name": "administrator",
  "email": "",
  "phone": "",
  "officeLocation": ""
}, {
  "domainMoid": "d9eb314a-1fc4-4b4b-867b-18ee8d9ceeba",
  "userMoid": "mooooooo-oooo-oooo-oooo-serviceadmin",
  "role": 0,
  "name": "admin",
  "email": "",
  "phone": "",
  "officeLocation": ""
}];

const nmspages = [{
  'id': "1",
  "page_name": "基本信息"
}, {
  'id': "2",
  "page_name": "设备管理",
  "children": [{
    'id': "3",
    "page_name": "平台设备"
  }, {
    'id': "4",
    "page_name": "终端设备"
  }, {
    'id': "5",
    "page_name": "终端统计"
  }, {
    'id': "6",
    "page_name": "资源统计"
  }]
}, {
  'id': "7",
  "page_name": "设备告警",
  "children": [{
    'id': "8",
    "page_name": "订阅告警"
  }, {
    'id': "9",
    "page_name": "未修复告警"
  }, {
    'id': "10",
    "page_name": "已修复告警"
  }, {
    'id': "11",
    "page_name": "告警统计"
  }]
}, {
  'id': "12",
  "page_name": "会议详情",
  "children": [{
    'id': "13",
    "page_name": "实时会议"
  }, {
    'id': "14",
    "page_name": "历史会议"
  }, {
    'id': "15",
    "page_name": "预约会议"
  }]
}, {
  'id': "16",
  "page_name": "诊断分析",
  "children": [{
    'id': "17",
    "page_name": "诊断功能"
  }, {
    'id': "18",
    "page_name": "巡检功能"
  }]
}, {
  'id': "19",
  "page_name": "系统设置",
  "children": [{
    'id': "20",
    "page_name": "告警设置"
  }]
}];

const userprivileges = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 151, 161, 17, 18, 19];

export {
  users,
  userprivileges,
  nmspages
}
