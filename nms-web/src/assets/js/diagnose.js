
// ************************************终端诊断**********************************

/**
 * 获取诊断分析-诊断功能-终端诊断列表表格属性
 * @returns {*[]}
 */
export function getTerminalDiagnosticsFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'warning_level',
      label: '告警状态'
    },
    {
      prop: 'e164',
      label: 'E164号码'
    },
    {
      prop: 'type',
      label: '设备型号'
    },
    {
      prop: 'service_domain_name',
      label: '所属服务域'
    },
    {
      prop: 'user_domain_name',
      label: '所属用户域'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '诊断',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-终端诊断-硬件状态-视频源-列表表格属性
 * @returns {*[]}
 */
export function getVideoFields() {
  return [
    {
      prop: 'video_name',
      label: '视频源名称'
    },
    {
      prop: 'video_pattern',
      label: '视频源模式'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-终端诊断-硬件状态-麦克风-列表表格属性
 * @returns {*[]}
 */
export function getMicrophoneFields() {
  return [
    {
      prop: 'microphone_name',
      label: '麦克风名称'
    },
    {
      prop: 'status',
      label: '状态'
    },
    {
      prop: 'ed',
      label: '能量检测'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-终端诊断-硬件状态-摄像头-列表表格属性
 * @returns {*[]}
 */
export function getCameraFields() {
  return [
    {
      prop: 'camera_name',
      label: '摄像头名称'
    },
    {
      prop: 'is_video',
      label: '有无视频源'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-终端诊断-硬件状态-输出信号-列表表格属性
 * @returns {*[]}
 */
export function getSignalFields() {
  return [
    {
      prop: 'type1',
      label: '类型'
    },
    {
      prop: 'status',
      label: '状态'
    }
  ]
}

/**
 * 获取诊断功能-终端诊断-外设状态-列表表格属性
 * @returns {*[]}
 */
export function getPeripheralFields() {
  return [
    {
      prop: 'name',
      label: '外设名称'
    },
    {
      prop: 'type',
      label: '类型',
      flag: 'perType'
    },
    {
      prop: 'version',
      label: '版本'
    },
    {
      prop: 'status',
      label: '状态',
      flag: 'Peripheral'
    }
  ]
}

/**
 * 获取诊断功能-终端诊断-第一路主视频-列表表格属性
 * @returns {*[]}
 */
export function getPrivideosFields() {
  return [
    {
      prop: 'up',
      label: '上下行'
    },
    {
      prop: 'video_format',
      label: '视频格式',
      flag: 'videoFormat'
    },
    {
      prop: 'video_ability',
      label: '视频能力',
      flag: 'videoAbility'
    },
    {
      prop: 'video_pkts_lose',
      label: '视频丢包总数',
    },
    {
      prop: 'video_pkts_loserate',
      label: '视频丢包率',
      flag: 'videoPktsLoserate'
    },
    {
      prop: 'audio_format',
      label: '音频格式',
      flag: 'audioFormat'
    },
    {
      prop: 'audio_up_down_bitrate',
      label: '音频码率'
    },
    {
      prop: 'audio_pkts_lose',
      label: '音频丢包总数',
    },
    {
      prop: 'audio_pkts_loserate',
      label: '音频丢包率',
      flag: 'audioPktsLoserate'
    },
    {
      prop: 'audio_codec_start',
      label: '音频编解码',
      flag: 'audioCodec'
    },
    {
      prop: 'video_codec_start',
      label: '视频编解码',
      flag: 'videoCodec'
    },
    {
      prop: 'hw_codec_status',
      label: '硬件编解码',
      flag: 'hwCodecStatus'
    }
  ]
}

/**
 * 获取诊断功能-终端诊断-第一路辅视频-列表表格属性
 * @returns {*[]}
 */
export function getAssvideosFields() {
  return [
    {
      prop: 'up',
      label: '上下行'
    },
    {
      prop: 'video_format',
      label: '视频格式',
      flag: 'videoFormat'
    },
    {
      prop: 'video_ability',
      label: '视频能力',
      flag: 'videoAbility'
    },
    {
      prop: 'video_pkts_lose',
      label: '视频丢包总数',
    },
    {
      prop: 'video_pkts_loserate',
      label: '视频丢包率'
    },
    {
      prop: 'video_codec_start',
      label: '视频编解码',
      flag: 'videoCodec'
    },
    {
      prop: 'hw_codec_status',
      label: '硬件编解码',
      flag: 'hwCodecStatus'
    }
  ]
}
// *********************************************服务器诊断**************************************************

/**
 * 获取诊断分析-服务器诊断-列表表格属性
 * @returns {*[]}
 */
export function getServerFields(detailCallback) {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'level',
      label: '运行状态',
      flag: 'serverDeviceOnline'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'device_type',
      label: '设备类型'
    },
    {
      prop: 'machine_room_name',
      label: '所属机房'
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
 * 绘制echart图表
 * @param yAxisName
 * @param id
 * @param series
 */
export function drawEcharts(eTool, yAxisName, id, series) {
  let data = []
  let yName = '%'
  if (yAxisName) {
    yName = yAxisName
  }
  if (series != null && series.length > 0) {
    data = series
  }
  if (id == null) {
    return
  }

  var coreKeys = [];
  for (var i = 1; i <= 21; i++) {
      coreKeys.push(i + '_cpu');
  }

  let option = {
    xAxis: {
      type: 'value',
      name: '%',
      min: 0,
      max: 100,
      interval: 10,
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
      type: 'category',
      name: yName,
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
        show: false
      },
      data: coreKeys.reverse()
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

/**
 * 绘制echart图表
 * @param yAxisName
 * @param id
 * @param series
 */
export function drawNetEcharts(eTool, yAxisName, id, series) {
  let data = []
  let yName = '%'
  if (yAxisName) {
    yName = yAxisName
  }
  if (series != null && series.length > 0) {
    data = series
  }
  if (id == null) {
    return
  }

  var coreKeys = [];
  for (var i = 1; i <= 6; i++) {
      coreKeys.push(i + '_网口');
  }

  let option = {
    xAxis: {
      type: 'value',
      name: 'Kbps',
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
      type: 'category',
      name: yName,
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
        show: false
      },
      data: coreKeys.reverse()
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

export const tServiceDomainMoids = [
  {
    value: "网口",
    text: "网口"
  }, {
    value: "eth0",
    text: "eth0"
  }, {
    value: "eth1",
    text: "eth1"
  }, {
    value: "eth2",
    text: "eth2"
  }, {
    value: "eth3",
    text: "eth3"
  }, {
    value: "eth4",
    text: "eth4"
  }, {
    value: "eth5",
    text: "eth5"
  }
]

export const sJournals = [
  {
	  value: "all",
		text: "all"
  },
	{
		value: "business_all",
		text: "business_all"
	},
	{
		value: "business_pas",
		text: "business_pas"
	},
	{
		value: "business_cmu",
		text: "business_cmu"
	},
	{
		value: "business_eqp",
		text: "business_eqp"
	},
	{
		value: "business_css",
		text: "business_css"
	},
	{
		value: "dcs",
		text: "dcs"
	},
	{
		value: "dms",
		text: "dms"
	},
	{
		value: "dss",
		text: "dss"
	},
	{
		value: "guard",
		text: "guard"
	},
	{
		value: "haproxy",
		text: "haproxy"
	},
	{
		value: "kdfs",
		text: "kdfs"
	},
	{
		value: "modb",
		text: "modb"
	},
	{
		value: "modbcore",
		text: "modbcore"
	},
	{
		value: "mo_ejabberd",
		text: "mo_ejabberd"
	},
	{
		value: "monitor",
		text: "monitor"
	},
	{
		value: "mysql",
		text: "mysql"
	},
	{
		value: "nginx",
		text: "nginx"
	},
	{
		value: "pms",
		text: "pms"
	},
	{
		value: "rabbitmq",
		text: "rabbitmq"
	},
	{
		value: "radar-server",
		text: "radar-server"
	},
	{
		value: "redis",
		text: "redis"
	},
	{
		value: "restapi",
		text: "restapi"
	},
	{
		value: "tomcat",
		text: "tomcat"
	},
	{
		value: "zookeeper",
		text: "zookeeper"
  }]

  /**
 * 获取诊断分析-诊断功能-服务器诊断-告警状态-列表表格属性
 * @returns {*[]}
 */
export function getWarningFields() {
  return [
    {
      prop: 'warning_drade',
      label: '告警等级'
    },
    {
      prop: 'warning_describe',
      label: '告警描述'
    },
    {
      prop: 'start_time',
      label: '产生时间'
    }
  ]
}

// *************************************************会议诊断****************************************************************

/**
 * 获取诊断分析-诊断功能-会议诊断-列表表格属性
 * @returns {*[]}
 */
export function getMeetingFields(detailCallback) {
  return [
    {
      prop: 'meetingName',
      label: '会议名称'
    },
    {
      prop: 'meeting_p_num',
      label: '会议号码'
    },
    {
      prop: 'startTime',
      label: '开始时间'
    },
    {
      prop: 'endTime',
      label: '结束时间'
    },
    {
      prop: 'meetingType',
      label: '会议类型'
    },
    {
      prop: 'meetingSize',
      label: '会议规模'
    },
    {
      prop: 'initiator',
      label: '发起人'
    },
    {
      prop: 'meetingMoid',
      label: '操作',
      opts: [
        {
          text: '诊断',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-会议诊断-画面合成器-列表表格属性
 * @returns {*[]}
 */
export function getPictureSynthesizerFieldFields() {
  return [
    {
      prop: 'terminal_name',
      label: '终端名称'
    },
    {
      prop: 'video_format',
      label: '视频格式'
    },
    {
      prop: 'video_resolution',
      label: '视频分辨率'
    },
    {
      prop: 'video_fps',
      label: '视频帧率'
    },
    {
      prop: 'video_bitrate',
      label: '视频码率'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-会议诊断-画面适配-主流广播-列表表格属性
 * @returns {*[]}
 */
export function getMainRadioFieldFields() {
  return [
    {
      prop: 'adapter_name',
      label: '适配器名称'
    },
    {
      prop: 'media_ability',
      label: '媒体能力'
    },
    {
      prop: 'resolution_ratio',
      label: '分辨率'
    },
    {
      prop: 'fps',
      label: '帧率'
    },
    {
      prop: 'code_rate',
      label: '码率'
    },
    {
      prop: 'terminal_num',
      label: '终端数'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-会议诊断-音频适配-列表表格属性
 * @returns {*[]}
 */
export function getAudioAdaptationFields() {
  return [
    {
      prop: 'adapter_name',
      label: '适配器名称'
    },
    {
      prop: 'format',
      label: '格式'
    },
    {
      prop: 'terminal_num',
      label: '终端数'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-会议诊断-混音器-终端名称-列表表格属性
 * @returns {*[]}
 */
export function getTerminalNameFields() {
  return [
    {
      prop: 'terminal_name',
      label: '终端名称'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-会议诊断-编解码器-列表表格属性
 * @returns {*[]}
 */
export function getCodecFieldFields() {
  return [
    {
      prop: 'terminal_codec_format',
      label: '终端编解码格式'
    },
    {
      prop: 'terminal_code_resolution',
      label: '卡板'
    },
    {
      prop: 'terminal_codec_fps',
      label: '所属机框'
    },
    {
      prop: 'terminal_code_code',
      label: '终端数'
    }
  ]
}

/**
 * 获取诊断分析-诊断功能-会议诊断-服务器资源-列表表格属性
 * @returns {*[]}
 */
export function getServerResourceFields() {
  return [
    {
      prop: 'board_card',
      label: '终端编解码格式'
    },
    {
      prop: 'machine_frame',
      label: '终端编解码分辨率'
    },
    {
      prop: 'terminal_num',
      label: '终端编解码帧率'
    }
  ]
}

// *************************************************巡检功能****************************************************************

/**
 * 巡检功能-License文件-列表表格属性
 * @returns {*[]}
 */
export function getLicenseFields() {
  return [
    {
      prop: 'auth_id',
      label: '授权许可ID'
    },
    {
      prop: 'auth_status',
      label: '文件状态',
      flag: 'license_file_status'
    },
    {
      prop: 'service_domain_name',
      label: '所属服务域'
    },
    {
      prop: 'auth_dead_time',
      label: '授权到期时间'
    }
  ]
}

/**
 * 巡检功能-服务器资源属性
 * @returns {*[]}
 */
export function getInspectionResInfo(res) {
  return [
    {
      children: [
        {
          title: '端口资源',
          total: res.port_remainder ? res.port_remainder : 0,
          usedList: [
            {
              text: '已使用资源',
              used: res.port_used ? res.port_used : 0
            }
          ]
        },
        {
          title: 'SFU资源',
          total: res.sfu_remainder ? res.sfu_remainder : 0,
          usedList: [
            {
              text: '已使用资源',
              used: res.sfu_used ? res.sfu_used : 0
            }
          ]
        },
        {
          title: 'Pas资源',
          total: res.p2p_remainder ? res.p2p_remainder : 0,
          usedList: [
            {
              text: '已使用资源',
              used: res.p2p_used ? res.p2p_used : 0
            }
          ]
        }
      ]
    }]
}

/**
 * 巡检功能-服务器状态-物理服务器表格属性
 * @returns {*[]}
 */
export function getPhysicsFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'online',
      label: '设备状态'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'type',
      label: '设备类型'
    },
    {
      prop: 'service_domain_moid',
      label: '所属服务域'
    },
    {
      prop: 'platform_domain_moid',
      label: '所属平台域'
    },
    {
      prop: 'virtual_machine_room_moid',
      label: '所属虚拟机房'
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
 * 巡检功能-服务器状态-物理服务器表格属性
 * @returns {*[]}
 */
export function getLogicFields(detailCallback) {
  return [
    {
      prop: 'name',
      label: '设备名称'
    },
    {
      prop: 'online',
      label: '设备状态'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
    {
      prop: 'type',
      label: '设备类型'
    },
    {
      prop: 'service_domain_moid',
      label: '所属服务域'
    },
    {
      prop: 'platform_domain_moid',
      label: '所属平台域'
    },
    {
      prop: 'virtual_machine_room_moid',
      label: '所属虚拟机房'
    },
    {
      prop: 'moid',
      label: '操作',
    }
  ]
}

/**
 * 巡检功能-服务器状态-物理服务器未修复告警表格属性
 * @returns {*[]}
 */
export function getuServerWarninglListFields() {
  return [
    {
      prop: 'level',
      label: '告警等级',
      flag: 'inspect_server_unrepaires_warning'
    },
    {
      prop: 'description',
      label: '告警描述',
    },
    {
      prop: 'start_time',
      label: '告警时间'
    }
  ]
}

/**
 * 巡检功能-终端状态-表格属性
 * @returns {*[]}
 */
export function getTerminalFields(detailCallback) {
  return [
    {
      prop: 'device_name',
      label: '设备名称'
    },
    {
      prop: 'level',
      label: '运行状态',
      flag: 'terminalSatus'
    },
    {
      prop: 'e164',
      label: 'E164号码'
    },
    {
      prop: 'device_ip',
      label: '设备IP'
    },
    {
      prop: 'user_domain_name',
      label: '所属用户域'
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
 * 巡检功能-终端状态-未修复告警-表格属性
 * @returns {*[]}
 */
export function getuTermminalWarninglListFields() {
  return [
    {
      prop: 'level',
      label: '告警等级',
      flag: 'inspect_server_unrepaires_warning'
    },
    {
      prop: 'description',
      label: '告警描述',
    },
    {
      prop: 'start_time',
      label: '告警时间'
    }
  ]
}
/**
 * 抓包功能-抓包对象-表格属性
 * @returns {*[]}
 */
export function getGrabObjectFields(editCallback, deleteCallback) {
  return [
    {
      prop: 'device_name',
      label: '抓包对象'
    },
    {
      prop: 'device_category',
      label: '设备类型'
    },
    {
      prop: 'device_type',
      label: '设备型号'
    },
    {
      prop: 'netcard',
      label: '网口'
    },
    {
      prop: 'status',
      label: '状态',
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
          text: '删除',
          click: deleteCallback
        }
      ]
    }
  ]
}
/**
 * 抓包功能-抓包文件-表格属性
 * @returns {*[]}
 */
export function getGrabFileFields(download) {
  return [
    {
      prop: 'file_name',
      label: '文件名'
    },
    {
      prop: 'file_size',
      label: '文件大小',
      flag: 'file_tag'
    },
    {
      prop: 'create_time',
      label: '文件生成日期'
    },
    {
      prop: 'device_name',
      label: '归属设备'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '下载',
          click: download
        }
      ]
    }
  ]
}
/**
 * 日志获取-日志文件-表格属性
 * @returns {*[]}
 */
export function getLogFileFields() {
  return [
    {
      prop: 'name',
      label: '文件名'
    },
    {
      prop: 'ctime',
      label: '时间'
    },
    {
      prop: 'dir',
      label: '日志目录'
    }
  ]
}
/**
 * 绘制echart图表
 * @param yAxisName
 * @param id
 * @param series
 */
export function ins_drawEcharts(eTool, yAxisName, id, series) {
  let data = []
  let yName = '%'
  if (yAxisName) {
    yName = yAxisName
  }
  if (series != null && series.length > 0) {
    data = series
  }
  if (id == null) {
    return
  }

  var coreKeys = [];
  for (var i = 0; i <= 7; i++) {
      coreKeys.push(i + '_cpu');
  }

  let option = {
    xAxis: {
      type: 'value',
      name: '%',
      min: 0,
      max: 100,
      interval: 10,
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
      type: 'category',
      name: yName,
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
        show: false
      },
      data: coreKeys
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

/**
 * 绘制echart图表
 * @param yAxisName
 * @param id
 * @param series
 */
export function ins_drawNetEcharts(eTool, yAxisName, id, series) {
  let data = []
  let yName = '%'
  if (yAxisName) {
    yName = yAxisName
  }
  if (series != null && series.length > 0) {
    data = series
  }
  if (id == null) {
    return
  }

  var coreKeys = [];
  for (var i = 0; i <= 2; i++) {
      coreKeys.push(i + '_网口');
  }

  let option = {
    xAxis: {
      type: 'value',
      name: 'M',
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
      type: 'category',
      name: yName,
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
        show: false
      },
      data: coreKeys
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
// ****************************************************定时巡检*******************************************************

/**
 * 巡检功能-定时巡检-巡检任务表格属性
 * @returns {*[]}
 */
export function getInspectTaskListFields(deleteCallback, editCallback, detailCallback) {
  return [
    {
      prop: 'start_time',
      label: '巡检时间'
    },
    {
      prop: 'inspects',
      label: '巡检项',
      flag: 'a1'
    },
    {
      prop: 'status',
      label: '任务状态',
      flag: 'diagnose_status'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '删除',
          click: deleteCallback
        },
        {
          text: '编辑',
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
 * 时间选择器-hours
 * @returns {*[]}
 */
export function getHours() {
  var hours= []
  for(let i=0; i<24; i++) {
    if(i<10){
      i = "0"+i
    }
    let dic = {}
    dic["text"] = i+" "+"时"
    dic["value"] = i
    hours.push(dic)
  }
  return hours
}

/**
 * 时间选择器-minutes
 * @returns {*[]}
 */
export function getMinutes() {
  var minutes= []
  for(let i=0; i<60; i++) {
    if(i<10){
      i = "0"+i
    }
    let dic = {}
    dic["text"] = i+" "+"分"
    dic["value"] = i
    minutes.push(dic)
  }
  return minutes
}
/**
 * 时间选择器-seconds
 * @returns {*[]}
 */
export function getSeconds() {
  var seconds= []
  for(let i=0; i<60; i++) {
    if(i<10){
      i = "0"+i
    }
    let dic = {}
    dic["text"] = i+" "+"秒"
    dic["value"] = i
    seconds.push(dic)
  }
  return seconds
}

export function setMyOption(eTool, id, myOption) {
  if (id == null) {
    return false
  }
  let myChart = eTool.init(document.getElementById(id));
  myChart.setOption(myOption, true);
  window.addEventListener("resize", () => {
    myChart.resize();
  })
}
