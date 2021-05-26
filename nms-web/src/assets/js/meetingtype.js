export const MeetingTypes = [
  {
    text: '全部类型',
    value: 'alltype'
  },
  {
    text: '传统会议',
    value: 'tradition'
  },
  {
    text: '端口会议',
    value: 'port'
  }
]

/**
 * 获取传统会议列表表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function gettraditionalMeetingDeviceListFields(detailCallback) {
  return [
    {
      prop: 'conf_name',
      label: '会议名称'
    },
    {
      prop: 'conf_e164',
      label: '会议号码'
    },
    {
      prop: 'conf_type',
      label: '会议类型'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    },
    {
      prop: 'scale',
      label: '会议规模'
    },
    {
      prop: 'organizer',
      label: '发起人'
    },
    {
      prop: 'machineRoomMoid',
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
 * 获取点对点会议列表表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function getp2pMeetingDeviceListFields(detailCallback) {
  return [
    {
      prop: 'caller_e164',
      label: '主叫号码'
    },
    {
      prop: 'caller_name',
      label: '主叫名称'
    },
    {
      prop: 'callee_e164',
      label: '被叫号码'
    },
    {
      prop: 'callee_name',
      label: '被叫名称'
    },
    {
      prop: 'bandwidth',
      label: '会议码率'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'machineRoomMoid',
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
 * 获取传统会议-级联会议列表表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function getcascadeMeetingFields(detailCallback) {
  return [
    {
      prop: 'meetingName',
      label: '会议名称'
    },
    {
      prop: 'meetingE164',
      label: '会议号码'
    },
    {
      prop: 'cascadeType',
      label: '会议级联类型'
    },
    {
      prop: 'bandWidth',
      label: '会议码率'
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
 * 获取传统会议-软硬终端列表表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function gethardAndSoftTerminalFields(detailCallback) {
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
      prop: 'mt_type',
      label: '设备型号'
    },
    {
      prop: 'version',
      label: '软件版本'
    },
    {
      prop: 'e164',
      label: '设备号码'
    },
    {
      prop: 'star',
      label: '会议体验'
    },
    {
      prop: 'moid',
      label: '操作',
      opts: [
        {
          text: '与会详情',
          click: detailCallback
        }
      ]
    }
  ]
}

/**
 * 获取传统会议-电话终端列表
 * @param detailCallback
 * @returns {*[]}
 */
export function getPhoneTerminalFields() {
  return [
    {
      prop: 'tel_num',
      label: '电话号码'
    },
  ]
}
/**
 * 获取传统会议-IP和友商列表
 * @param detailCallback
 * @returns {*[]}
 */
export function getIPBusinessFriendFields() {
  return [
    {
      prop: 'name',
      label: '友商名称'
    },
    {
      prop: 'ip',
      label: '设备IP'
    },
  ]
}

/**
 * 获取点对点会议-主视频列表表格属性
 * @returns {*[]}
 */
export function getmainVideoFields() {
  return [
    {
      prop: 'updown',
      label: '上下行'
    },
    {
      prop: 'video_format',
      label: '视频格式'
    },
    {
      prop: 'video_power',
      label: '视频能力'
    },
    /*
    {
      prop: 'p_send_framerate',
      label: '视频帧率'
    },
    {
      prop: 'p_up_bitrate',
      label: '视频码率'
    },
    {
      prop: 'assvideo_detail',
      label: '视频分辨率'
    },
    */
    {
      prop: 'video_lostrate',
      label: '视频丢包率',
      flag: 'video_lostrate_tab'
    },
    {
      prop: 'audio_format',
      label: '音频格式'
    },
    {
      prop: 'audio_lostrate',
      label: '音频丢包率',
      flag: 'audio_lostrate_tab'
    },
  ]
}

/**
 * 获取传统会议-软硬终端-入会离会详情列表表格属性
 * @returns {*[]}
 */
export function getInOutMeetingFields() {
  return [
    {
      prop: 'enter_time',
      label: '入会时间'
    },
    {
      prop: 'leave_time',
      label: '退会时间'
    },
    {
      prop: 'leave_reason',
      label: '原因'
    }
  ]
}
export function getMeetingStateFields() {
  return [
    {
      prop: 'type',
      flag: 'meeting_event',
      label: '事项'
    },
    {
      prop: 'time',
      label: '发生时间'
    },
    {
      prop: 'note',
      flag: 'meeting_event',
      label: '备注'
    },
    {
      prop: 'score',
      label: '扣分数'
    }
  ]
}

/**
 * 获取传统会议-直播列表表格属性
 * @returns {*[]}
 */
export function getLiveStreamingFields(onclickCallback) {
  return [
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    },
    {
      prop: 'id',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: onclickCallback
        }
      ]
    }
  ]
}
/**
 * 获取实时会议-直播列表表格属性
 * @returns {*[]}
 */
export function getRealTimeLiveFields() {
  return [
    {
      prop: 'name',
      label: '观看人员'
    },
    {
      prop: 'enter_time',
      label: '开始时间'
    },
  ]
}
/**
 * 获取传统会议-直播-弹框列表表格属性
 * @returns {*[]}
 */
export function getonclickLiveStreamingFields(onclickCallback) {
  return [
    {
      prop: 'user_name',
      label: '观看人员'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    },
    {
      prop: 'time',
      label: '时长'
    }
  ]
}

/**
 * 获取传统会议-数据协作列表表格属性
 * @returns {*[]}
 */
export function getCollaborationFields(onclickCallback) {
  return [
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    },
    {
      prop: 'id',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: onclickCallback
        }
      ]
    }
  ]
}
/**
 * 获取实时会议-数据协作列表表格属性
 * @returns {*[]}
 */
export function getRealTimeCollaborationFields() {
  return [
    {
      prop: 'name',
      label: '协作方',
    },
    {
      prop: 'e164',
      label: 'E164号'
    },
    {
      prop: 'begin_time',
      label: '开始时间'
    },
  ]
}
/**
 * 获取传统会议-数据协作-协作模式列表表格属性
 * @returns {*[]}
 */
export function getCollaborativeModeFields() {
  return [
    {
      prop: 'collaborate_mode',
      label: '协作模式'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    }
  ]
}

/**
 * 获取传统会议-数据协作-协作方列表表格属性
 * @returns {*[]}
 */
export function getCollaboratorFields() {
  return [
    {
      prop: 'collaboration',
      label: '协作方'
    },
    {
      prop: 'e164',
      label: 'E164号码'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    }
  ]
}

/**
 * 获取传统会议-数据协作-观看方列表表格属性
 * @returns {*[]}
 */
export function getViewerFields() {
  return [
    {
      prop: 'looker',
      label: '观看方'
    },
    {
      prop: 'e164',
      label: 'E164号码'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    }
  ]
}

/**
 * 获取传统会议-会场概况-管理方列表表格属性
 * @returns {*[]}
 */
export function getmanagerFields() {
  return [
    {
      prop: 'terminal_name',
      label: '终端名称'
    },
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    }
  ]
}

/**
 * 获取传统会议-会场概况-会议·录像列表表格属性
 * @returns {*[]}
 */
export function getvideoFields() {
  return [
    {
      prop: 'start_time',
      label: '开始时间'
    },
    {
      prop: 'end_time',
      label: '结束时间'
    },
    {
      prop: 'server_ip',
      label: '服务器IP'
    },
    {
      prop: 'file_name',
      label: '文件名称'
    },
    {
      prop: 'path',
      label: '存储路径'
    }
  ]
}
