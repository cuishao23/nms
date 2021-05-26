function getTypeListByDevices(devices) {
  if (devices == null || devices.length === 0) {
    return []
  }

  // 获取所有设备类型
  let types = []
  let obj = {}
  for (let i = 0; i < devices.length; i++) {
    if (devices[i].type != null && devices[i].type !== '') {
      if (obj[devices[i].type] == null) {
        obj[devices[i].type] = i
        types.push(devices[i].type)
      }
    }
  }
  let typeArr = [{
    text: '全部设备类型',
    value: 'all'
  }]

  // 构造k-v
  for (let i = 0; i < types.length; i++) {
    typeArr.push({text: types[i], value: types[i]})
  }
  return typeArr
}

/**
 * 从服务器列表中获取服务器类型列表
 * @param physicals
 * @returns {*}
 */
export function getTypeListByPhysicals(physicals) {
  return getTypeListByDevices(physicals)
}

/**
 * 从逻辑服务器列表中获取类型列表
 * @param logicals
 * @returns {*}
 */
export function getTypeListByLogicals(logicals) {
  return getTypeListByDevices(logicals)
}

/**
 * 获取节点服务器(非机框)列表表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function getPhysicalDeviceListFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'type_ser',
      label: '设备类型'
    },
    {
      prop: 'online',
      label: '设备状态',
      flag: 'serverDeviceOnline'
    },
    {
      prop: 'warning_level',
      label: '告警等级'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'belong_slot',
      label: '槽位'
    },
    {
      prop: 'disk',
      label: '磁盘寿命',
      flag: "serverDeviceDisk"
    },
    {
      prop: 'uptime',
      label: '运行时间'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}
/**
 * 获取会议服务器(机框)列表表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function getFrameListFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'type_ser',
      label: '设备类型'
    },
    {
      prop: 'online',
      label: '设备状态',
      flag: 'frameOnline'
    },
    {
      prop: 'ip',
      label: '设备IP',
      flag: 'frameIp'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取逻辑服务器表格属性列表
 * @param detailCallback
 * @returns {*[]}
 */
export function getLogicalDeviceListFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'type',
      label: '设备类型'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'warning_level',
      label: '告警'
    },
    {
      prop: 'online',
      label: '在线状态'
    },
    {
      prop: 'version',
      label: '版本号'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取平台设备资源使用情况图表字段
 * @param res
 * @returns {*[]}
 */
export function getPlatformResInfo(res) {
  return [
    {
      title: '授权资源',
      children: [
        {
          title: '接入端口数',
          total: res.ap_total ? res.ap_total : 0,
          usedList: [
            {
              text: '已使用',
              used: res.ap_used ? res.ap_used : 0
            }
          ]
        },
        {
          title: '国密接入端口数',
          total: res.g_ap_total ? res.g_ap_total : 0,
          usedList: [
            {
              text: '已使用',
              used: res.g_ap_used ? res.g_ap_used : 0
            }
          ]
        },
        {
          title: 'H.264媒体端口数',
          total: res.total_h264 ? res.total_h264 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_h264 ? res.used_h264 : 0
            }
          ]
        },
        {
          title: 'H.264国密媒体端口数',
          total: res.total_g_h264 ? res.total_g_h264 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_g_h264 ? res.used_g_h264 : 0
            }
          ]
        },
        {
          title: 'H.265媒体端口数',
          total: res.total_h265 ? res.total_h265 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_h265 ? res.used_h265 : 0
            }
          ]
        },
        {
          title: 'H.265国密媒体端口数',
          total: res.total_g_h265 ? res.total_g_h265 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_g_h265 ? res.used_g_h265 : 0
            }
          ]
        },
        {
          title: '录像资源',
          total: res.recroomtotal ? res.recroomtotal : 0,
          usedList: [
            {
              text: '已使用',
              used: res.recroomocp ? res.recroomocp : 0
            }
          ]
        },
        {
          title: 'ASF直播资源',
          total: res.lcasttotal ? res.lcasttotal : 0,
          usedList: [
            {
              text: '已使用',
              used: res.lcastocp ? res.lcastocp : 0
            }
          ]
        },
        {
          title: 'HTML5直播资源',
          total: res.html5lcasttotal ? res.html5lcasttotal : 0,
          usedList: [
            {
              text: '已使用',
              used: res.html5lcastocp ? res.html5lcastocp : 0
            }
          ]
        },
        {
          title: '数据协作人员数',
          total: res.max_mt_num ? res.max_mt_num : 0,
          usedList: [
            {
              text: '已使用',
              used: res.mt_num ? res.mt_num : 0
            }
          ]
        },
        {
          title: '数据协作会议数',
          total: res.max_conf_num ? res.max_conf_num : 0,
          usedList: [
            {
              text: '已使用',
              used: res.conf_num ? res.conf_num : 0
            }
          ]
        }
      ]
    },
    {
      title: '虚拟会议室',
      children: [
        {
          title: '192方1080P虚拟会议',
          total: res.total_192_1080 ? res.total_192_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_192_1080 ? res.used_192_1080 : 0
            }
          ]
        },
        {
          title: '192方720P虚拟会议',
          total: res.total_192_720 ? res.total_192_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_192_720 ? res.used_192_720 : 0
            }
          ]
        },
        {
          title: '64方1080P虚拟会议',
          total: res.total_64_1080 ? res.total_64_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_64_1080 ? res.used_64_1080 : 0
            }
          ]
        },
        {
          title: '64方720虚拟会议',
          total: res.total_64_720 ? res.total_64_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_64_720 ? res.used_64_720 : 0
            }
          ]
        },
        {
          title: '32方1080P虚拟会议',
          total: res.total_32_1080 ? res.total_32_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_32_1080 ? res.used_32_1080 : 0
            }
          ]
        },
        {
          title: '32方720P虚拟会议',
          total: res.total_32_720 ? res.total_32_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_32_720 ? res.used_32_720 : 0
            }
          ]
        },
        {
          title: '8方1080P虚拟会议\n',
          total: res.total_8_1080 ? res.total_8_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_8_1080 ? res.total_8_1080 : 0
            }
          ]
        },
        {
          title: '8方720P虚拟会议',
          total: res.total_8_720 ? res.total_8_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_8_720 ? res.used_8_720 : 0
            }
          ]
        }
      ]
    },
    {
      title: '媒体资源',
      children: [
        {
          title: '合成器',
          total: res.total_vmp ? res.total_vmp : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_vmp ? res.used_vmp : 0
            }
          ]
        },
        {
          title: '混音器',
          total: res.total_mixer ? res.total_mixer : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_mixer ? res.used_mixer : 0
            }
          ]
        }
      ]
    }]
}

export function getUserDomainResInfo(res) {
  return [
    {
      title: '授权资源',
      children: [
        {
          title: '接入端口数',
          total: res.ap_total ? res.ap_total : 0,
          usedList: [
            {
              text: '已使用',
              used: res.ap_used ? res.ap_used : 0
            }
          ]
        },
        {
          title: '国密接入端口数',
          total: res.g_ap_total ? res.g_ap_total : 0,
          usedList: [
            {
              text: '已使用',
              used: res.g_ap_used ? res.g_ap_used : 0
            }
          ]
        },
        {
          title: 'H.264媒体端口数',
          total: res.total_h264 ? res.total_h264 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_h264 ? res.used_h264 : 0
            }
          ]
        },
        {
          title: 'H.264国密媒体端口数',
          total: res.total_g_h264 ? res.total_g_h264 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_g_h264 ? res.used_g_h264 : 0
            }
          ]
        },
        {
          title: 'H.265媒体端口数',
          total: res.total_h265 ? res.total_h265 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_h265 ? res.used_h265 : 0
            }
          ]
        },
        {
          title: 'H.265国密媒体端口数',
          total: res.total_g_h265 ? res.total_g_h265 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_g_h265 ? res.used_g_h265 : 0
            }
          ]
        },
        {
          title: '录像资源',
          total: res.recroomtotal ? res.recroomtotal : 0,
          usedList: [
            {
              text: '已使用',
              used: res.recroomocp ? res.recroomocp : 0
            }
          ]
        },
        {
          title: 'ASF直播资源',
          total: res.lcasttotal ? res.lcasttotal : 0,
          usedList: [
            {
              text: '已使用',
              used: res.lcastocp ? res.lcastocp : 0
            }
          ]
        },
        {
          title: 'HTML5直播资源',
          total: res.html5lcasttotal ? res.html5lcasttotal : 0,
          usedList: [
            {
              text: '已使用',
              used: res.html5lcastocp ? res.html5lcastocp : 0
            }
          ]
        }
      ]
    },
    {
      title: '虚拟会议室',
      children: [
        {
          title: '192方1080P虚拟会议',
          total: res.total_192_1080 ? res.total_192_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_192_1080 ? res.used_192_1080 : 0
            }
          ]
        },
        {
          title: '192方720P虚拟会议',
          total: res.total_192_720 ? res.total_192_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_192_720 ? res.used_192_720 : 0
            }
          ]
        },
        {
          title: '64方1080P虚拟会议',
          total: res.total_64_1080 ? res.total_64_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_64_1080 ? res.used_64_1080 : 0
            }
          ]
        },
        {
          title: '64方720虚拟会议',
          total: res.total_64_720 ? res.total_64_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_64_720 ? res.used_64_720 : 0
            }
          ]
        },
        {
          title: '32方1080P虚拟会议',
          total: res.total_32_1080 ? res.total_32_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_32_1080 ? res.used_32_1080 : 0
            }
          ]
        },
        {
          title: '32方720P虚拟会议',
          total: res.total_32_720 ? res.total_32_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_32_720 ? res.used_32_720 : 0
            }
          ]
        },
        {
          title: '8方1080P虚拟会议\n',
          total: res.total_8_1080 ? res.total_8_1080 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_8_1080 ? res.total_8_1080 : 0
            }
          ]
        },
        {
          title: '8方720P虚拟会议',
          total: res.total_8_720 ? res.total_8_720 : 0,
          usedList: [
            {
              text: '已使用',
              used: res.used_8_720 ? res.used_8_720 : 0
            }
          ]
        }
      ]
    }]
}

export function getCtrlDeviceListFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'e164',
      label: 'E164号码'
    },
    {
      prop: 'online',
      label: '在线状态'
    },
    {
      prop: 'version',
      label: '版本号'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

export function getUnCtrlDeviceListFields(editCallback, warningCallback) {
  return [
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'type',
      label: '设备类型'
    },
    {
      prop: 'e164',
      label: 'E164号码'
    },
    {
      prop: 'version',
      label: '版本号'
    },
    {
      prop: 'online',
      label: '在线状态',
      flag: 'unctrl_ter'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '编辑',
          click: editCallback
        },
        {
          text: '告警信息',
          click: warningCallback
        }
      ]
    }
  ]
}

export function getCtrlDeviceTypeListFields() {
  return [
    {
      prop: 'type_ver',
      label: '终端类型'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'version',
      label: '当前版本'
    },
    {
      prop: 'recomand',
      flag: 'version',
      label: '是否推荐版本'
    },
    {
      prop: 'recomand_version',
      label: '最新版本'
    },
    {
      prop: 'online_state',
      flag: 'online',
      label: '在线状态'
    }
  ]
}

/**
 * 获取未修复此终端告警表格字段
 * @returns {*[]}
 */
export function getCtrlUnrepairedterminalWarningListFields() {
  return [
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'description',
      label: '告警描述'
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
 * 摄像机表格字段
 * @returns {*[]}
 */
export function getCameraListFields() {
  return [
    {
      prop: 'name',
      label: '外设名称'
    },
    {
      prop: 'status',
      label: '状态',
      flag: 'terPers'
    },
    {
      prop: 'type',
      label: '摄像机型号',
      flag: 'per_type'
    },
    {
      prop: 'SN',
      label: '服务序列号'
    },
    {
      prop: 'version',
      label: '软件版本号',
      flag: 'per_version'
    }
  ]
}

/**
 * 麦克风表格字段
 * @returns {*[]}
 */
export function getMicrophoneListFields() {
  return [
    {
      prop: 'name',
      label: '外设名称'
    },
    {
      prop: 'status',
      label: '状态',
      flag: 'terPers'
    },
    {
      prop: 'type',
      label: '麦克风型号',
      flag: 'per_type'
    },
    {
      prop: 'version',
      label: '软件版本号',
      flag: 'per_version'
    }
  ]
}

/**
 * IMIX表格字段
 * @returns {*[]}
 */
export function getImixListFields() {
  return [
    {
      prop: 'name',
      label: '外设名称'
    },
    {
      prop: 'status',
      label: '状态',
      flag: 'terPers'
    },
    {
      prop: 'type',
      label: '型号'
    },
    {
      prop: 'sn',
      label: '型号'
    },
    {
      prop: 'mac',
      label: 'MAC地址'
    },
    {
      prop: 'ip',
      label: 'IP地址'
    },
    {
      prop: 'version',
      label: '软件版本号',
      flag: 'per_version'
    }
  ]
}

export function getOldTerminalTypeList() {
  return [
    "PCMT",
    "8010",
    "8010A",
    "8010A+",
    "8010C",
    "8010C1",
    "IMT",

    "8220A",
    "5210",
    "V5",
    "3210",
    "6610E",
    "6210",
    "8010A-2",
    "8010A-4",
    "8010A-8",

    "7210",
    "7610",
    "5610",
    "6610",
    "7810",
    "7910",
    "7620_4",
    "7620_2",

    "7820_A",
    "7820_B",
    "7920_A",
    "7920_B",
    "KDV1000",
    "7921_L",
    "7921_H",

    "H600_LB",
    "H600_B",
    "H600_C",
    "H700_A",
    "H700_B",
    "H700_C",
    "H900_A",
    "H900_B",
    "H900_C",
    "H600_LC",
    "H800_A",
    "H800_B",
    "H800_C",

    "H850_A",
    "H850_B",
    "H850_C",
    "H600_L_TP",
    "H600_TP",
    "H700_TP",
    "H800_TP",
    "H850_TP",
    "H900_TP",

    "H650-B",
    "H650-C",
    "H650-LB",
    "H650-LC",
    "H650-SD",

    "TS300",
    "TS400",
    "TS500"
  ]
}

export const meetingDomainMoids = [
  {
    text: '传统会议',
    value: 'tradition'
  },
  {
    text: '端口会议',
    value: 'port'
  },
  {
    text: '点对点会议',
    value: 'pointtopoint'
  }
]

/**
 * 绘制echart图表
 * @param yAxisName
 * @param id
 * @param series
 */
export function drawMeetingEcharts(eTool, yAxisName, id, series) {
  let data = []
  let yName = ''
  if (yAxisName) {
    yName = yAxisName
  }
  if (series != null && series.length > 0) {
    data = series
  }
  if (id == null) {
    return
  }

  let option = {
    xAxis: {
      type: 'value',
      name: '',
      min: 0,
      max: 100,
      interval: 20,
      axisLine: {
        symbol: ['none', 'arrow'],
        symbolSize: [8, 12],
        lineStyle: {
          color: '#949799'
        }
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        rotate: 0,
      },
      splitLine: {
        show: true
      }
    },
    yAxis: {
      type: 'value',
      name: yName,
      min: -1,
      max: 1,
      interval: 0.5,
      axisLine: {
        symbol: ['none', 'arrow'],
        symbolSize: [8, 12],
        lineStyle: {
          color: '#949799'
        },
      },
      axisTick: {
        show: false
      },
      splitLine: {
        show: true
      },
    },
    grid: {
      top: 30,
      bottom: 188
    },
    legend: {
      top: 230,
      left: 32,
      orient: 'vertical',
      textStyle: {
        color: '#4e4e4e',
        fontFamily: 'Microsoft YaHei'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    series: data
  }
  let chart = eTool.init(document.getElementById(id));
  chart.setOption(option);
}

// CPU
export function drawCPUusingEcharts(eTool, yAxisName, id, cpuValue_1, cpuValue_2) {
  let data = []
  let yName = '%'
  if (yAxisName) {
    yName = yAxisName
  }
  // if (series.length > 0) {
  //  data = series
  // }
  if (id == null) {
    return
  }
  let option = {
    xAxis: {
      type: 'category',
      name: '时间',
      boundaryGap: false,
      data: ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00", "24:00", "02:00", "04:00", "06:00", "08:00"],
      axisLabel: {
        rotate: 90,
        textStyle: {
          color: 'black',
          fontSize: 13,
          fontStyle: 'normal',
          fontWeight: 500
        }
      },
      axisLine: {
        symbol: ['none', 'arrow'],
        symbolSize: [8, 12],
        lineStyle: {
          // color: '#949799'
        }
      },
    },
    yAxis: {
      name: yName,
      min: 0,
      max: 100,
      interval: 50,
      type: 'value',
      axisTick: {
        show: false
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dotted'
        }
      },
      axisLine: {
        symbol: ['none', 'arrow'],
        symbolSize: [8, 12],
        // symbolOffset: 20,
        lineStyle: {
          // color: '#949799'
        }
      },
    },
    grid: {
      top: 30,
      bottom: 55,
      containLabel: true
    },
    // legend: {
    //   top: 800,
    //   left: 32,
    //   orient: 'vertical',
    //   textStyle: {
    //     color: '#4e4e4e',
    //     fontFamily: 'Microsoft YaHei'
    //   }
    // },
    tooltip: {
      trigger: 'axis',
    },
    series: [
      {
        name: '1_cpu',
        type: 'line',
        symbol: 'none',
        data: cpuValue_1,
        itemStyle: {
          normal: {
            color: '#00aeff', // 改变折线点的颜色
            lineStyle: {
              color: '#00aeff' // 改变折线颜色
            }
          }
        }
      },
      {
        name: '2_cpu',
        type: 'line',
        symbol: 'none',
        data: cpuValue_2,
        itemStyle: {
          normal: {
            color: '#32cd32', // 改变折线点的颜色
            lineStyle: {
              color: '#32cd32' // 改变折线颜色
            }
          }
        }
      },
    ],
    legend: {
      orient: 'horizontal',
      bottom: 5,
      itemGap: 8,
      itemWidth: 10,
      itemHeight: 10,
      data: [
        {
          name: '1_cpu',
          icon: 'rect'
        },
        {
          name: '2_cpu',
          icon: 'rect'
        },
      ]
    },
  }
  let myChart = eTool.init(document.getElementById(id));
  myChart.setOption(option, true);
  window.addEventListener("resize", () => {
    myChart.resize();
  })
}


// NETport
export function drawNETportEcharts(eTool, yAxisName, id, flow_in, flow_out) {
  let data = []
  let yName = 'Mbps'
  if (yAxisName) {
    yName = yAxisName
  }
  // if (series.length > 0) {
  //  data = series
  // }
  if (id == null) {
    return
  }
  let option = {
    xAxis: {
      type: 'category',
      name: '时间',
      boundaryGap: false,
      data: ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00", "24:00", "02:00", "04:00", "06:00", "08:00"],
      axisLabel: {
        rotate: 90,
        textStyle: {
          color: 'black',
          fontSize: 13,
          fontStyle: 'normal',
          fontWeight: 500
        }
      },
      axisLine: {
        symbol: ['none', 'arrow'],
        symbolSize: [8, 12],
        lineStyle: {
          // color: '#949799'
        }
      },
    },
    yAxis: {
      name: yName,
      min: 0,
      max: 1000,
      interval: 500,
      type: 'value',
      axisTick: {
        show: false
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dotted'
        }
      },
      axisLine: {
        symbol: ['none', 'arrow'],
        symbolSize: [8, 12],
        // symbolOffset: 20,
        lineStyle: {
          // color: '#949799'
        }
      },
    },
    grid: {
      top: 30,
      bottom: 55,
      containLabel: true
    },
    // legend: {
    //   top: 800,
    //   left: 32,
    //   orient: 'vertical',
    //   textStyle: {
    //     color: '#4e4e4e',
    //     fontFamily: 'Microsoft YaHei'
    //   }
    // },
    tooltip: {
      trigger: 'axis',
    },
    series: [
      {
        name: '进流量',
        type: 'line',
        symbol: 'none',
        data: flow_in,
        itemStyle: {
          normal: {
            color: '#00aeff', // 改变折线点的颜色
            lineStyle: {
              color: '#00aeff' // 改变折线颜色
            }
          }
        }
      },
      {
        name: '出流量',
        type: 'line',
        symbol: 'none',
        data: flow_out,
        itemStyle: {
          normal: {
            color: '#32cd32', // 改变折线点的颜色
            lineStyle: {
              color: '#32cd32' // 改变折线颜色
            }
          }
        }
      },
    ],
    legend: {
      orient: 'horizontal',
      bottom: 5,
      itemGap: 8,
      itemWidth: 10,
      itemHeight: 10,
      data: [
        {
          name: '进流量',
          icon: 'rect'
        },
        {
          name: '出流量',
          icon: 'rect'
        },
      ]
    },
  }
  let myChart = eTool.init(document.getElementById(id));
  myChart.setOption(option, true);
  window.addEventListener("resize", () => {
    myChart.resize();
  })
}

// 视频格式类型
export const videoTypes = [
  {
    text: '4K(3840x2160)_30fps',
    value: '4K(3840x2160)_30fps'
  },
  {
    text: '1080P_60fps',
    value: '1080P_60fps'
  },
  {
    text: '1080P_24fps',
    value: '1080P_24fps'
  },
  {
    text: '1080P_25fps',
    value: '1080P_25fps'
  },
  {
    text: '1080P_29.97fps',
    value: '1080P_29.97fps'
  },
  {
    text: '1080P_30fps',
    value: '1080P_30fps'
  },
  {
    text: '1080P_50fps',
    value: '1080P_50fps'
  },
  {
    text: '1080P_59.94fps',
    value: '1080P_59.94fps'
  },
  {
    text: '1080i_50Hz',
    value: '1080i_50Hz'
  },
  {
    text: '1080i_60Hz',
    value: '1080i_60Hz'
  },
  {
    text: 'UXGA(1600x1200)_60Hz',
    value: 'UXGA(1600x1200)_60Hz'
  },
  {
    text: 'WSXGA+(1680x1050)_60Hz',
    value: 'WSXGA+(1680x1050)_60Hz'
  },
  {
    text: 'SXGA(1280x1024)_60Hz',
    value: 'SXGA(1280x1024)_60Hz'
  },
  {
    text: 'WSXGA(1440x900)_60Hz',
    value: 'WSXGA(1440x900)_60Hz'
  },
  {
    text: '720P_50fps',
    value: '720P_50fps'
  },
  {
    text: '720P_60fps',
    value: '720P_60fps'
  },
  {
    text: 'XGA(1024x768)_60Hz',
    value: 'XGA(1024x768)_60Hz'
  },
  {
    text: 'XGA(1024x768)_75Hz',
    value: 'XGA(1024x768)_75Hz'
  },
  {
    text: 'WXGA(1366x768)_60Hz',
    value: 'WXGA(1366x768)_60Hz'
  },
  {
    text: 'WXGA(1280x800)_60Hz',
    value: 'WXGA(1280x800)_60Hz'
  },
  {
    text: 'WXGA(1280x800)_75Hz',
    value: 'WXGA(1280x800)_75Hz'
  },
  {
    text: 'WXGA(1280x768)_60Hz',
    value: 'WXGA(1280x768)_60Hz'
  },
  {
    text: 'WXGA(1280x768)_75Hz',
    value: 'WXGA(1280x768)_75Hz'
  },
  {
    text: 'SVGA(800x600)_60Hz',
    value: 'SVGA(800x600)_60Hz'
  },
  {
    text: 'SVGA(800x600)_75Hz',
    value: 'SVGA(800x600)_75Hz'
  },
  {
    text: 'VGA(640x480)_60Hz',
    value: 'VGA(640x480)_60Hz'
  },
  {
    text: 'VGA(640x480)_75Hz',
    value: 'VGA(640x480)_75Hz'
  }
];

