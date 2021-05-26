
export function getsServiceDomainMoids() {
  // 服务域类型列表
  return [
    {
      text: '默认服务域',
      value: 'subdefault'
    },
    {
      text: 'kedacom',
      value: 'kedacom'
    }
  ]
}

export const sPlatformDomainMoids = [
  {
    text: '默认平台域',
    value: 'pldefault'
  },
  {
    text: '核心平台域',
    value: 'kernel'
  }
]

export const sMachineRoomMoids = [
  {
    text: '所有虚拟机房',
    value: 'allroom'
  },
  {
    text: '核心域默认机房',
    value: 'defaultroom'
  }
]

export function gettTerminalDomainMoids() {
  // 终端类型列表
  return [
    {
      text: '默认服务域',
      value: 'tdefault'
    },
    {
      text: 'kedacom',
      value: 'kedacom'
    }
  ]
}

export const tUserMoids = [
  {
    text: '所有用户域',
    value: 'alltuser'
  },
  {
    text: '无下级域',
    value: 'not'
  }
]

/**
 * 获取未修复服务器告警表格字段
 * @returns {*[]}
 */
export function getUnrepairedServerWarningTblFields(editCallback, detailCallback) {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '告警时间'
    },
    {
      prop: 'operate',
      label: '操作',
      flag: 'warning',
      opts: [
        {
          text: '修复',
          click: editCallback
        },
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取非受管终端告警表格字段
 * @returns {*[]}
 */
export function getUncontroledTerminalWarningFields() {
  return [
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '产生时间'
    },
    {
      prop: 'resolve_time',
      label: '恢复时间'
    }
  ]
}

/**
 * 获取未修复终端告警表格字段
 * @returns {*[]}
 */
export function getUnrepairedTerminalWarningTblFields(editCallback, detailCallback) {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '告警时间'
    },
    {
      prop: 'operate',
      label: '操作',
      flag: 'warning',
      opts: [
        {
          text: '修复',
          click: editCallback
        },
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取已经修复服务器告警表格字段
 * @returns {*[]}
 */
export function getRepairedServerWarningTblFields() {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '告警时间'
    },
    {
      prop: 'resolve_time',
      label: '修复时间'
    }
  ]
}
/**
 * 获取已经修复终端告警表格字段
 * @returns {*[]}
 */
export function getRepairedTerminalWarningTblFields() {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '告警时间'
    },
    {
      prop: 'resolve_time',
      label: '修复时间'
    }
  ]
}

/**
 * 获取订阅服务器告警表格字段
 * @returns {*[]}
 */
export function getSubServerWarningTblFields(editCallback, detailCallback) {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '告警时间'
    },
    {
      prop: 'resolve_time',
      label: '修复时间'
    },
    {
      prop: 'operate',
      label: '操作',
      flag: 'warning',
      opts: [
        {
          text: '修复',
          click: editCallback
        },
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取订阅终端告警表格字段
 * @returns {*[]}
 */
export function getSubTerminalWarningFields(editCallback, detailCallback) {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'description',
      label: '告警描述'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '告警时间'
    },
    {
      prop: 'resolve_time',
      label: '修复时间'
    },
    {
      prop: 'operate',
      label: '操作',
      flag: 'warning',
      opts: [
        {
          text: '修复',
          click: editCallback
        },
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}
