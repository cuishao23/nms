export const operateTypes = [
  {
    text: '操作类型',
    value: '.*'
  },
  {
    text: '注销',
    value: 'logout'
  },
  {
    text: '设备诊断',
    value: 'diagnose'
  },
  {
    text: '设备抓包',
    value: 'capture'
  },
  {
    text: '日志获取',
    value: 'log'
  },
  {
    text: '版本管理',
    value: 'sus'
  },
  {
    text: '阈值配置',
    value: 'limitset'
  },
  {
    text: '告警配置',
    value: 'warningset'
  },
  {
    text: '设备配置',
    value: 'terminaltype'
  },
  {
    text: '权限配置',
    value: 'terminallimit'
  },
];

export const operateLevels = [
  {
    text: '操作等级',
    value: '.*'
  },
  {
    text: '严重',
    value: 'critical'
  },
  {
    text: '重要',
    value: 'important'
  },
  {
    text: '一般',
    value: 'normal'
  }
];

export const logPeriods = [
  {
    text: '最近一周',
    value: 'lastweek'
  },
  {
    text: '最近一个月',
    value: 'lastmonth'
  },
  {
    text: '最近三个月',
    value: 'lastthreemonth'
  },
  {
    text: '最近半年',
    value: 'lasthalfyear'
  },
  {
    text: '最近一年',
    value: 'lastyear'
  },
  {
    text: '自定义',
    value: 'selfdefine'
  }
];

/**
 * 获取用户管理表格属性
 * @returns {*[]}
 */
export function getLogsTableFields() {
  return [
    {
      prop: 'user',
      label: '用户名'
    },
    {
      prop: 'time',
      label: '操作时间'
    },
    {
      prop: 'ip',
      label: 'IP地址'
    },
    {
      prop: 'log_type',
      label: '操作类型'
    },
    {
      prop: 'description',
      label: '操作描述'
    },
    {
      prop: 'level',
      label: '操作等级'
    },
    {
      prop: 'result',
      label: '操作结果'
    },
    {
      prop: 'fail_reason',
      label: '失败原因'
    }
  ]
}
