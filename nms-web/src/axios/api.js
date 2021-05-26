import axios from 'axios'
import cookie from 'cookie'
import { onOpen, onMessage, onClose } from "../ws/websock"

if (process.env.API_ROOT === '' && process.env.NODE_ENV === 'development') {
  alert('请配置 API_ROOT, 路径:config/dev.env.js')
  console.log("请配置")
}
console.log("API " + process.env.API_ROOT)
axios.defaults.baseURL = process.env.API_ROOT;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed';
axios.defaults.withCredentials = false;
axios.interceptors.request.use((config) => {
  config.headers['X-Requested-With'] = 'XMLHttpRequest';
  config.headers['X-CSRFToken'] = cookie.parse(document.cookie).csrftoken;
  return config
});
axios.interceptors.response.use(
  response => {
    if (response.data.success === 0 && response.data.error_code === 10002) {
      console.error('nginx sso error')
      console.error(document.location)
    }
    return response
  },
  error => {
    if (error.response) {
      console.error(error.response);
      switch (error.response.status) {
        case 401:
          // 返回 401 验证错误
          let portal = cookie.parse(document.cookie).portal
          if (portal === undefined) {
            console.log('cookie error')
            document.location = "/portal/login"
          } else {
            document.location = portal + '/login'
          }
      }
    }
    return Promise.reject(error.response)
  }
);

export default axios;

// 查询订阅服务器告警信息
export const getSubServerWarning = params => {
  return axios.get('/nms/warning/subserverwarning', params).then(res => res.data)
};
// 查询订阅终端告警信息
export const getSubTerminalWarning = params => {
  return axios.get('/nms/warning/subterminalwarning', params).then(res => res.data)
};
// 查询未修复服务器告警信息
export const getLatestServerUnrepairedWarning = params => {
  return axios.get('/nms/warning/latestserverunrepairedwarning', params).then(res => res.data)
};
// 主界面查询未修复服务器告警信息
export const getServerUnrepairedWarning = params => {
  return axios.get('/nms/warning/serverunrepairedwarning', params).then(res => res.data)
};
// 查询未修复终端告警信息
export const getLatestTerminalUnrepairedWarning = params => {
  return axios.get('/nms/warning/latestterminalunrepairedwarning', params).then(res => res.data)
};
// 主界面查询未修复终端告警信息
export const getTerminalUnrepairedWarning = params => {
  return axios.get('/nms/warning/terminalunrepairedwarning', params).then(res => res.data)
};
// 查询已修复服务器告警信息
export const getLatestServerRepairedWarning = params => {
  return axios.get('/nms/warning/latestserverrepairedwarning', params).then(res => res.data)
};
// 查询已修复终端告警信息
export const getLatestTerminalRepairedWarning = params => {
  return axios.get('/nms/warning/latestterminalrepairedwarning', params).then(res => res.data)
};
// 修复服务器告警信息
export const getRepairServerWarning = params => {
  return axios.get('/nms/warning/repairserverwarning', params).then(res => res.data)
};
// 修复终端告警信息
export const getRepairTerminalWarning = params => {
  return axios.get('/nms/warning/repairterminalwarning', params).then(res => res.data)
};
// 导出告警表
export const getWarningDownLoad = params => {
  return axios.get('/nms/warning/downloadwarning', params).then(res => res.data)
};
// 获取所有域树
export const getDomainTree = params => {
  return axios.get('/nms/domain/domaintree', params).then(res => res.data)
};
// 获取平台设备域树
export const getPlatformDomainTree = params => {
  return axios.get('/nms/domain/platformdomaintree', params).then(res => res.data)
};
// 获取用户域树型结构
export const getUserDomainTree = params => {
  return axios.get('/nms/domain/userdomaintree', params).then(res => res.data)
};
// 获取逻辑服务器信息列表
export const getLogicalList = params => {
  return axios.get('/nms/device/logicals', params).then(res => res.data)
}
// 获取服务器设备信息列表
export const getPhysicals = params => {
  return axios.get('/nms/device/physicals', params).then(res => res.data)
};
// 获取服务器设备详情信息列表
export const getPhysicalDetailInfo = params => {
  return axios.get('/nms/device/physicaldetailinfo', params).then(res => res.data)
};
// 获取所有服务器设备类型列表
export const getServerTypeList = params => {
  return axios.get('/nms/device/servertypelist', params).then(res => res.data)
};
// 获取所有机框设备类型列表
export const getFrameInfo = params => {
  return axios.get('/nms/device/frameinfo', params).then(res => res.data)
};
// 获取机框中设备类型列表
export const getDeviceNameDetail = params => {
  return axios.get('/nms/device/devicenamedetail', params).then(res => res.data)
};
// 获取节点服务器设备信息
export const getNodeServerInfo = params => {
  return axios.get('/nms/device/serverinfo', params).then(res => res.data)
};
// 获取机框设备类型列表
export const getFrameTypeList = params => {
  return axios.get('/nms/device/frametypelist', params).then(res => res.data)
};
// 获取非机框设备类型列表
export const getNoframeTypeList = params => {
  return axios.get('/nms/device/noframetypelist', params).then(res => res.data)
};
// 获取physical设备类型列表
export const getPhysicalTypeList = params => {
  return axios.get('/nms/device/physicaltypelist', params).then(res => res.data)
};
// 获取磁盘信息
export const getDiskInfo = params => {
  return axios.get('/nms/device/diskinfo', params).then(res => res.data)
};
// 获取服务器名称、网口名称（服务器抓包参数）
export const getOnlineServer = params => {
  return axios.get('/nms/device/onlineserver', params).then(res => res.data);
};
// 获取终端名称、类型、网口名称（终端抓包参数）
export const getOnlineTerminal = params => {
  return axios.get('/nms/device/onlineterminal', params).then(res => res.data);
};
// 获取terminal设备类型列表
export const getTerminalTypeList = params => {
  return axios.get('/nms/device/terminaltypelist', params).then(res => res.data)
}
// 获取受管终端数据列表
export const getControledTerminals = params => {
  return axios.get('/nms/device/terminals', params).then(res => res.data)
};
// 导出受管终端数据列表
export const getTerminalsDownLoad = params => {
  return axios.get('/nms/device/terminalinfodownload', params).then(res => res.data)
};
// 获取非受管终端数据列表
export const getUncontroledTerminals = params => {
  return axios.get('/nms/device/uncontroledterminal', params).then(res => res.data)
};
// 获取非受管终端告警
export const getUncontroledTerminalWarnings = params => {
  return axios.get('/nms/warning/uncontroledterminalwarning', params).then(res => res.data)
};
// 获取受管终端详情信息
export const getCtrledTerminalDetail = params => {
  return axios.get('/nms/device/terminaldetail', params).then(res => res.data)
};
// 获取终端性能信息
export const getTerminalPerformance = params => {
  return axios.get('/nms/device/terminalperformance', params).then(res => res.data)
};
// 获取受管终端详情此终端未修复告警列表
export const getCtrlTerminalUnrepairedWarning = params => {
  return axios.get('/nms/warning/terminaldetailwarning', params).then(res => res.data)
};
// 获取受管终端详情外设信息列表
export const getCtrledTerminalPeripherals = params => {
  return axios.get('/nms/device/terminalperipherals', params).then(res => res.data)
};
// 重启服务器
export const rebootServer = params => {
  return axios.post('/nms/device/rebootserver', params).then(res => res.data)
};
// 服务器关机
export const shutdownServer = params => {
  return axios.post('/nms/device/shutdownserver', params).then(res => res.data)
};
// 重启终端
export const rebootTerminal = params => {
  return axios.post('/nms/device/rebootterminal', params).then(res => res.data)
};
// 配置终端注册地址
export const configTerminalRegAddr = params => {
  return axios.post('/nms/device/configterminalregaddr', params).then(res => res.data)
};
// 配置终端网络参数
export const configTerminalNetwork = params => {
  return axios.post('/nms/device/configterminalnetwork', params).then(res => res.data)
};
// 配置终端视频格式
export const configTerminalVideoFormat = params => {
  return axios.post('/nms/device/configterminalvideoformat', params).then(res => res.data)
};
//  获取网管日志信息
export const getLogInfo = params => {
  return axios.get('/nms/opr_log/loginfo', params).then(res => res.data);
};
//  添加网管日志信息
export const addLogInfo = params => {
  return axios.get('/nms/opr_log/loginfolist', params).then(res => res.data);
};
// 导出网管日志
export const getLogDownLoad = params => {
  return axios.get('/nms/opr_log/downloadlog', params).then(res => res.data)
};
// 获取历史多点会议列表
export const getHistoryMultiMeeting = params => {
  return axios.get('/nms/meeting/history/multimeeting', params).then(res => res.data)
};
// 获取历史多点会议详细信息
export const getHistoryMultiMeetingDetail = params => {
  return axios.get('/nms/meeting/history/multimeetingdetail', params).then(res => res.data)
};
// 获取历史多点会议软硬终端列表
export const getHistorySoftHardTerminal = params => {
  return axios.get('/nms/meeting/history/softhardterminal', params).then(res => res.data)
};
// 获取历史多点会议软硬终端详细信息
export const getHistorySoftHardTerminalDetail = params => {
  return axios.get('/nms/meeting/history/softhardterminaldetail', params).then(res => res.data)
};
// 获取历史多点会议终端入离会详情
export const getHistoryTerminalLeaveReason = params => {
  return axios.get('/nms/meeting/history/terminalleavereason', params).then(res => res.data)
};
// 获取历史多点会议终端参会概况
export const getHistoryTerminalMeetingScore = params => {
  return axios.get('/nms/meeting/history/terminalmeetingscore', params).then(res => res.data)
};
// 获取历史多点会议电话终端列表
export const getHistoryPhoneTerminal = params => {
  return axios.get('/nms/meeting/history/phoneterminal', params).then(res => res.data)
};
// 获取历史多点会议级联会议列表
export const getHistoryCascadeMeeting = params => {
  return axios.get('/nms/meeting/history/cascademeeting', params).then(res => res.data)
};
// 获取历史多点会议IP和友商列表
export const getHistoryIPTerminal = params => {
  return axios.get('/nms/meeting/history/ipterminal', params).then(res => res.data)
};
// 获取历史多点会议直播列表
export const getHistoryLiveInfo = params => {
  return axios.get('/nms/meeting/history/liveinfo', params).then(res => res.data)
};
// 获取历史多点会议直播用户列表
export const getHistoryLiveUserInfo = params => {
  return axios.get('/nms/meeting/history/liveuserinfo', params).then(res => res.data)
};
// 获取历史会议数据会议列表
export const getHistoryMeetingDcsInfo = params => {
  return axios.get('/nms/meeting/history/meetingdcsinfo', params).then(res => res.data)
};
// 获取历史会议数据会议模式更改列表
export const getHistoryDcsModeChangeInfo = params => {
  return axios.get('/nms/meeting/history/dcsmodechangeinfo', params).then(res => res.data)
};
// 获取历史会议数据会议终端列表
export const getHistoryDcsMeetingTerminal = params => {
  return axios.get('/nms/meeting/history/dcsmeetingterminal', params).then(res => res.data)
};
// 获取历史点对点会议列表
export const getHistoryP2pMeeting = params => {
  return axios.get('/nms/meeting/history/p2pmeeting', params).then(res => res.data)
};
// 获取历史点对点会议详细信息(主叫终端信息)
export const getHistoryP2pMeetingDetail = params => {
  return axios.get('/nms/meeting/history/p2pmeetingdetail', params).then(res => res.data)
};
// 获取历史点对点会议详细信息(被叫终端信息)
export const getHistoryP2pMeetingCallee = params => {
  return axios.get('/nms/meeting/history/p2pmeetingcallee', params).then(res => res.data)
};
// 获取历史点对点会议详细信息(主辅视屏信息)
export const getHistoryP2pMeetingVideo = params => {
  return axios.get('/nms/meeting/history/p2pmeetingvideo', params).then(res => res.data)
};
// 获取实时多点会议列表
export const getRealTimeMultiMeeting = params => {
  return axios.get('/nms/meeting/realtime/multimeeting', params).then(res => res.data)
};
// 获取实时多点会议详细信息
export const getRealTimeMultiMeetingDetail = params => {
  return axios.get('/nms/meeting/realtime/multimeetingdetail', params).then(res => res.data)
};
// 获取实时多点会议软硬终端列表
export const getRealTimeSoftHardTerminal = params => {
  return axios.get('/nms/meeting/realtime/softhardterminal', params).then(res => res.data)
};
// 获取实时多点会议终端入离会详情
export const getRealTimeTerminalLeaveReason = params => {
  return axios.get('/nms/meeting/realtime/terminalleavereason', params).then(res => res.data)
};
// 获取实时多点会议终端参会概况
export const getRealTimeTerminalMeetingScore = params => {
  return axios.get('/nms/meeting/realtime/terminalmeetingscore', params).then(res => res.data)
};
// 获取实时多点会议电话终端列表
export const getRealTimePhoneTerminal = params => {
  return axios.get('/nms/meeting/realtime/phoneterminal', params).then(res => res.data)
};
// 获取实时多点会议级联会议列表
export const getRealTimeCascadeMeeting = params => {
  return axios.get('/nms/meeting/realtime/cascademeeting', params).then(res => res.data)
};
// 获取实时多点会议IP和友商列表
export const getRealTimeIPTerminal = params => {
  return axios.get('/nms/meeting/realtime/ipterminal', params).then(res => res.data)
};
// 获取实时多点会议直播列表
export const getRealTimeLiveInfo = params => {
  return axios.get('/nms/meeting/realtime/liveinfo', params).then(res => res.data)
};
// 获取实时会议数据信息
export const getRealTimeDcsInfo = params => {
  return axios.get('/nms/meeting/realtime/dcsinfo', params).then(res => res.data)
};
// 获取实时点对点会议列表
export const getRealTimeP2pMeeting = params => {
  return axios.get('/nms/meeting/realtime/p2pmeeting', params).then(res => res.data)
};
// 获取实时点对点会议详细信息
export const getRealTimeTerminalDetail = params => {
  return axios.get('/nms/meeting/realtime/terminaldetail', params).then(res => res.data)
};
// 获取实时点对点会议详细信息(主辅视屏信息)
export const getRealTimeTerminalVideoDetail = params => {
  return axios.get('/nms/meeting/realtime/terminalvideodetail', params).then(res => res.data)
};
// 服务器诊断
export const diagnoseServer = params => {
  return axios.get('/nms/diagnosis/serverdiagnose/', params).then(res => res.data);
};
// 终端诊断
export const diagnoseTerminal = params => {
  return axios.post('/nms/diagnosis/terminaldiagnose/', params).then(res => res.data);
};
// 获取抓包设备信息
export const getCaptureDevice = params => {
  return axios.get('/nms/diagnosis/capturedevice/', params).then(res => res.data);
};
// 编辑抓包设备信息
export const setCaptureDevice = params => {
  return axios.post('/nms/diagnosis/capturedevice/', params).then(res => res.data);
};
// 添加抓包设备信息
export const addCaptureDevice = params => {
  return axios.post('/nms/diagnosis/addcapturedevice/', params).then(res => res.data);
};
// 删除抓包设备信息
export const deleteCaptureDevice = params => {
  return axios.post('/nms/diagnosis/delcapturedevice/', params).then(res => res.data);
};
// 获取抓包数据信息
export const getCaptureFile = params => {
  return axios.get('/nms/diagnosis/capturefile/', params).then(res => res.data);
};
// 删除抓包数据信息
export const deleteCaptureFile = params => {
  return axios.post('/nms/diagnosis/capturefile/', params).then(res => res.data);
};
// 获取抓包日志信息
export const getCaptureLog = params => {
  return axios.post('/nms/diagnosis/capturelog/', params).then(res => res.data);
};
// 开始抓包
export const startCaptureDevice = params => {
  return axios.post('/nms/diagnosis/startcapturedevice/', params).then(res => res.data);
};
// 结束抓包
export const stopCaptureDevice = params => {
  return axios.post('/nms/diagnosis/stopcapturedevice/', params).then(res => res.data);
};
// 下载抓包、日志文件
export const getDownloadCaptureFile = (deviceMoid, fileName) => {
  let url = `/nms/diagnosis/downloadcapturefile/?deviceMoid=${deviceMoid}&fileName=${fileName}`
  console.log(url)
  let a = document.createElement('a')
  a.href = url;
  document.body.append(a)
  a.click()
  a.remove()
};
// 下载抓包日志
export const getDownloadCaptureLog = params => {
  return axios.post('/nms/diagnosis/downloadcapturelog/', params).then(res => res.data);
};
// 查询告警码
export const getWarningTree = params => {
  return axios.get('/nms/system_set/warningtree', params).then(res => res.data)
};
// 获取所有阈值信息
export const getLimitInfo = params => {
  return axios.get('/nms/system_set/resourcelimit/', params).then(res => res.data);
};
// 修改阈值信息
export const setLimitInfo = params => {
  return axios.post('/nms/system_set/resourcelimit/', params).then(res => res.data);
};
// 获取服务器具体信息
export const getServerLimitInfo = params => {
  return axios.get('/nms/system_set/serverslimit/', params).then(res => res.data);
};
// 修改服务器具体信息
export const setServerLimitInfo = params => {
  return axios.post('/nms/system_set/serverslimit/', params).then(res => res.data);
};
// 告警级别
export const warningLevel = params => {
  return axios.get('/nms/system_set/warninglevel', params).then(res => res.data);
};
// 设置告警级别
export const setWarningLevel = params => {
  return axios.post('/nms/system_set/warninglevel/', params).then(res => res.data);
};
// 告警通知
export const getWarningNotifyInfo = params => {
  return axios.get('/nms/system_set/warningnotify', params).then(res => res.data);
};
// 添加告警通知
export const addWarningNotifyInfo = params => {
  return axios.post('/nms/system_set/warningnotify/', params).then(res => res.data);
};
// 编辑告警通知
export const editWarningNotifyInfo = params => {
  return axios.post('/nms/system_set/editwarningnotify/', params).then(res => res.data);
};
// 删除告警通知
export const deleteWarningNotifyInfo = params => {
  return axios.post('/nms/system_set/delwarningnotify/', params).then(res => res.data);
};
// 暂停告警列表
export const getStopWarningInfo = params => {
  return axios.get('/nms/system_set/stopwarning', params).then(res => res.data);
};
// 设置暂停告警
export const setStopWarning = params => {
  return axios.post('/nms/system_set/stopwarning/', params).then(res => res.data);
};
// 设备配置列表
export const getDeviceConfig = params => {
  return axios.get('/nms/system_set/deviceconfig', params).then(res => res.data);
};
// 设备配置列表
export const addDeviceConfig = params => {
  return axios.post('/nms/system_set/deviceconfig/', params).then(res => res.data);
};
// 删除设备配置
export const deleteDeviceConfig = params => {
  return axios.post('/nms/system_set/deldeviceconfig/', params).then(res => res.data);
};
// 获取订阅告警
export const getSubWarningCode = params => {
  return axios.get('/nms/system_set/subwarningcode', params).then(res => res.data);
};
// 设置订阅告警
export const setSubWarningCode = params => {
  return axios.post('/nms/system_set/subwarningcode/', params).then(res => res.data);
};
// 获取设备限制
export const getDeviceTypeLimit = params => {
  return axios.get('/nms/system_set/devicetypelimit/', params).then(res => res.data);
};
// 编辑设备限制
export const setDeviceTypeLimit = params => {
  return axios.post('/nms/system_set/devicetypelimit/', params).then(res => res.data);
};
// 添加设备限制
export const addDeviceTypeLimit = params => {
  return axios.post('/nms/system_set/adddevicetypelimit/', params).then(res => res.data);
};
// 删除设备限制
export const delDeviceTypeLimit = params => {
  return axios.post('/nms/system_set/deldevicetypelimit/', params).then(res => res.data);
};
// 获取设备限制类型
export const getDeviceTypeLimitCfg = params => {
  return axios.get('/nms/system_set/devicetypelimitcfg/', params).then(res => res.data);
};
// 修改设备限制类型
export const setDeviceTypeLimitCfg = params => {
  return axios.post('/nms/system_set/devicetypelimitcfg/', params).then(res => res.data);
};
// 设备型号数据列表api
export const getDeviceTypes = params => {
  return axios.get('/nms/system_set/terminaltypes/', params).then(res => res.data);
};
// 版本信息数据表api
export const getSusVersionInfo = params => {
  return axios.get('/nms/sus/versions/', params).then(res => res.data).catch(err => { console.log(err) });
};
// 单个版本信息数据
export const getTerminalTypeVersions = params => {
  return axios.get('/nms/sus/versiondetails/' + params + '/', params).then(res => res.data);
}
// 获取用户名和品牌信息
export const getServerInfo = params => {
  return axios.get('/nms/server_info/', params).then(res => res.data);
};
// 用户登出
export const logout = params => {
  return axios.post('/nms/logout/', params).then(res => res.data);
};
// CPU 图片
export const getCpuGraphiteInfo = params => {
  return axios.get('/nms/statistic/cpuchart/', params).then(res => res.data);
};
// 内存 图片
export const getMemGraphiteInfo = params => {
  return axios.get('/nms/statistic/memchart/', params).then(res => res.data);
};
// 网口 图片
export const getGraphiteChartData = params => {
  return axios.get('/nms/statistic/netcardchart/', params).then(res => res.data)
};
// 获取机房列表
export const getMachineRoomData = params => {
  return axios.get('/nms/domain/machineroommoid/', params).then(res => res.data)
};
// 获取会议质量数据
export const getMeetingQualityData = params => {
  return axios.get('/nms/statistic/meetingquality/', params).then(res => res.data)
};
// 获取会议资源数据
export const getMeetingResourceData = params => {
  return axios.get('/nms/statistic/meetingresource/', params).then(res => res.data)
};
// 获取预约会议数据
export const getAppointMeetingData = params => {
  return axios.get('/nms/statistic/appointmeeting/', params).then(res => res.data)
};
// 获取设备告警数据
export const getWarningStatisticData = params => {
  return axios.get('/nms/statistic/warningstatistic/', params).then(res => res.data)
};
// 获取会议统计数据
export const getMeetingStatisticData = params => {
  return axios.get('/nms/statistic/meetingstatistic/', params).then(res => res.data)
};
// 获取服务器统计数据
export const getServerStatisticData = params => {
  return axios.get('/nms/statistic/serverstatistic/', params).then(res => res.data)
};
// 获取终端统计数据
export const getTerminalStatisticData = params => {
  return axios.get('/nms/statistic/terminalstatistic/', params).then(res => res.data)
};
// 获取CPU使用数据
export const getCpuUsageData = params => {
  return axios.get('/nms/statistic/cpuusage/', params).then(res => res.data)
};
// 获取内存使用数据
export const getMemUsageData = params => {
  return axios.get('/nms/statistic/memusage/', params).then(res => res.data)
};
// 获取上行带宽数据
export const getNetcardUpData = params => {
  return axios.get('/nms/statistic/netcardup/', params).then(res => res.data)
};
// 获取下行带宽数据
export const getNetcardDownData = params => {
  return axios.get('/nms/statistic/netcarddown/', params).then(res => res.data)
};
// 获取磁盘寿命数据
export const getDiskAgeStatisticData = params => {
  return axios.get('/nms/statistic/diskagestatistic/', params).then(res => res.data)
};
// 获取磁盘使用数据
export const getDiskUsageStatisticData = params => {
  return axios.get('/nms/statistic/diskusagestatistic/', params).then(res => res.data)
};

// 巡检 获取巡检任务列表
export const getInspectTasks = params => {
  return axios.get('/nms/inspect/', params).then(res => res.data)
};
// 巡检 获取巡检子任务
export const getInspectTask = taskid => {
  return axios.get('/nms/inspect/' + taskid + '/').then(res => res.data)
};
// 巡检 创建巡检任务(即时巡检task_flag=0)
export const addInspectTask = data => {
  return axios.post('/nms/inspect/', data).then(res => res.data)
};
// 巡检 更新巡检任务
export const updateInspectTask = (taskid, params) => {
  return axios.put('/nms/inspect/' + taskid + '/', params).then(res => res.data)
};
// 巡检 删除巡检任务
export const delInspectTask = taskid => {
  return axios.delete('/nms/inspect/' + taskid + '/').then(res => res.data)
};
// 巡检 导出
export const downloadInspect = params => {
  return axios.get('/nms/inspect/download/', params).then(res => res.data)
};
// 巡检 获取巡检license
export const getInspectLicense = (taskid, params) => {
  return axios.get('/nms/inspect/' + taskid + '/license/', params).then(res => res.data)
};
// 巡检 获取巡检会议资源
export const getInspectResource = (taskid) => {
  return axios.get('/nms/inspect/' + taskid + '/resource/', taskid).then(res => res.data)
};
// 巡检 获取巡检服务器
export const getInspectServer = (taskid, params) => {
  return axios.get('/nms/inspect/' + taskid + '/server/', params).then(res => res.data)
};
// 巡检 获取巡检服务器资源
export const getInspectServerResource = (taskid, deviceMoid) => {
  return axios.get('/nms/inspect/' + taskid + '/server/' + deviceMoid + '/resource/').then(res => res.data)
};
// 巡检 获取巡检终端
export const getInspectTerminal = (taskid, params) => {
  return axios.get('/nms/inspect/' + taskid + '/terminal/', params).then(res => res.data)
};
// 巡检 获取服务器未修复告警
export const getInspectSWarning = (taskid, deviceMoid, deviceType, params) => {
  return axios.get('/nms/inspect/' + taskid + '/server/' + deviceMoid + '/unrepairwarning/', deviceType, params).then(res => res.data)
};
// 巡检 获取终端未修复告警
export const getInspectTWarning = (taskid, deviceMoid, params) => {
  return axios.get('/nms/inspect/' + taskid + '/terminal/' + deviceMoid + '/unrepairwarning/', { params: params }).then(res => res.data)
};
// 巡检 删除定时巡检子任务
export const delInspectChildTask = params => {
  return axios.post('/nms/inspect/delete/', params).then(res => res.data)
};

// websocket连接
export const getWebSocket = () => {
  let protocol = document.location.protocol === 'https:' ? 'wss://' : 'ws://'
  let url = protocol + document.location.host + '/nms/ws/'
  if (window.ws === undefined){
    window.ws = new WebSocket(url)
  } else if (window.ws.readyState != 1){
    window.ws.onclose = null
    window.ws.close()
    window.ws = new WebSocket(url)
  }
  return window.ws
}
