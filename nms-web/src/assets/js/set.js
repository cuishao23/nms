export const clearTimeSetTypes = [
  {
    text: '保留一个月',
    value: 'month'
  },
  {
    text: '保留三个月',
    value: 'threemonth'
  },
  {
    text: '保留半年',
    value: 'halfyear'
  },
  {
    text: '保留一年',
    value: 'year'
  }
];

export const backupTimeSetTypes = [
  {
    text: '一个月前',
    value: 'monthbefore'
  },
  {
    text: '三个月前',
    value: 'threemonthbefore'
  },
  {
    text: '半年前',
    value: 'halfyearbefore'
  },
  {
    text: '一年前',
    value: 'yearbefore'
  }
];

export const dataTypes = [
  {
    text: '终端连接',
    value: 'terminalonline'
  },
  {
    text: '终端版本',
    value: 'terminalversion'
  },
  {
    text: '服务器未修复告警',
    value: 'serverwarningunrepaired'
  },
  {
    text: '服务器已修复告警',
    value: 'serverwarningrepaired'
  },
  {
    text: '终端未修复告警',
    value: 'terminalwarningunrepaired'
  },
  {
    text: '终端已修复告警',
    value: 'terminalwarningrepaired'
  },
  {
    text: '修复数量统计',
    value: 'warningrepaircount'
  },
  {
    text: '平均修复时间统计',
    value: 'warningrepairtime'
  },
  {
    text: '多点历史会议统计',
    value: 'multimeeting'
  },
  {
    text: '点对点历史会议统计',
    value: 'p2pmeeting'
  },
  {
    text: '网管日志',
    value: 'logStatistics'
  }
];
/**
 * 获取服务器表格属性
 * @param editCallback
 * @returns {*[]}
 */
export function getServerLimitTableFields(editCallback) {
  return [
    {
      prop: 'name',
      label: '服务器名称'
    },
    {
      prop: 'cpu',
      label: 'CPU阈值'
    },
    {
      prop: 'memory',
      label: '内存阈值'
    },
    {
      prop: 'port',
      label: '网口阈值'
    },
    {
      prop: 'disk',
      label: '硬盘阈值'
    },
    {
      prop: 'diskwritespeed',
      label: '硬盘写入速度阈值'
    },
    {
      prop: 'rateofflow',
      label: '转发阈值'
    },
    {
      prop: 'details',
      label: '操作',
      opts: [
        {
          text: '编辑',
          click: editCallback
        }
      ]
    }
  ]
}

/**
 * 获取告警通知表格属性
 * @param editCallback
 * @returns {*[]}
 */
export function getWarningNotifyTableFields(editCallback, detailCallback, deleteCallback) {
  return [
    {
      prop: 'name',
      label: '通知人员'
    },
    {
      prop: 'phone',
      label: '短信通知'
    },
    {
      prop: 'email',
      label: '邮箱通知'
    },
    {
      prop: 'wechat',
      label: '微信通知'
    },
    {
      prop: 'details',
      label: '操作',
      opts: [
        {
          text: '编辑',
          click: editCallback
        },
        {
          text: '详情',
          click: detailCallback
        },
        {
          text: '删除',
          click: deleteCallback
        }
      ]
    }
  ]
}
/**
 * 获取设备配置表格属性
 * @param editCallback
 * @returns {*[]}
 */
export function getDeviceConfigFields() {
  return [
    {
      prop: 'name',
      label: '设备主型号'
    },
    {
      prop: 'product_name',
      label: '设备子型号'
    },
    {
      prop: 'terminal_type',
      label: '设备类型'
    },
    {
      prop: 'device_tag',
      label: '可登陆设备'
    },
  ]
}
/**
 * 获取权限配置表格属性
 * @param editCallback
 * @returns {*[]}
 */
export function getPermissionConfigFields(editCallback, deleteCallback) {
  return [
    {
      prop: 'e164',
      label: 'E164号'
    },
    {
      prop: 'version',
      label: '版本号'
    },
    {
      prop: 'ip',
      label: 'IP地址'
    },
    {
      prop: 'terminal_type',
      label: '类型'
    },
    {
      prop: 'sn',
      label: 'SN序列号'
    },
    {
      prop: 'main_type',
      label: '主型号'
    },
    {
      prop: 'sub_type',
      label: '子型号'
    },
    {
      prop: 'details',
      label: '操作',
      opts: [
        {
          text: '编辑',
          click: editCallback
        },
        {
          text: '删除',
          click: deleteCallback
        }
      ]
    }
  ]
}
