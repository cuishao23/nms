import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

import {serverUnrepairedWarnings} from "./data/serverunrepairedwarning";
import {terminalUnrepairedWarnings} from "./data/terminalunrepairedwarning";
import {serverRepairedWarnings} from "./data/serverrepairedwarning";
import {terminalRepairedWarnings} from "./data/terminalrepairedwarning";
import {warningTree} from "./data/warningtree";
import {platformDomainTree} from "./data/platformdomaintree";
import {meetingDomainTree} from "./data/meetingdomaintree";
import {physicals} from "./data/physicals";
import {physicalDetail} from "./data/physicaldetail"
import {logicals} from "./data/logicals"
import {logicalDetail} from "./data/logicaldetail"
import {userDomainTree} from "./data/userdomaintree"
import {resInfo} from "./data/resinfo";
import {controledTerminals} from "./data/controledterminals";
import {ctrlTerminalDetail} from "./data/ctrlterminaldetail";
import {uncontroledTerminals} from "./data/uncontroledterminals";
import {users, userprivileges, nmspages} from "./data/users";
import {logs} from "./data/log";
import {traditionalMeetings} from "./data/realtimemeetings";
import {TraditionMeetingDetail} from "./data/traditionmeetingdetail";
import {cascadeMeetings} from "./data/cascadeMeeting";
import {hardAndSoftTerminals} from "./data/hardandsoftterminal";
import {hardSoftTerminalDetail} from "./data/hardsoftTerminaldetail";
import {mainVideo} from "./data/mainvideo";
import {inOutMeeting} from "./data/inoutmeeting";
import {liveStreaming} from "./data/livestreaming";
import {manager} from "./data/manager";
import {serverDiagnostic, serverWarning} from "./data/serverdiagnostic";
import {terminalDiagnostic, hardwareStatus, video, microPhone, camera, outSignal, inSignal} from "./data/terminaldiagnostic";
import {meetingDiagnostic, pictureSynthesizer, mainRadio, audioAdaptation, terminalName, mixer, codec, serverResource} from "./data/meetingdiagnostic";
import {inspectionDomain} from "./data/inspectiondomain";
import {deviceTypes, versionInfo} from "./data/susmgr";
import {limits, servers, services, machinerooms, platforms, stopWarnings} from "./data/limitset"
import {warnings, subwarningcode} from "./data/warningset";

export default {
  init() {
    let Mock = new MockAdapter(axios)

    // 告警
    Mock.onGet('/api/nms/warning/latestserverunrepairedwarning').reply(200, {
      success: 1, warnings: serverUnrepairedWarnings
    })
    Mock.onGet('/api/nms/warning/latestterminalunrepairedwarning').reply(200, {
      success: 1, warnings: terminalUnrepairedWarnings
    })
    // 已修复告警
    Mock.onGet('/api/nms/warning/latestserverrepairedwarning').reply(200, {
      success: 1, warnings: serverRepairedWarnings
    })
    Mock.onGet('/api/nms/warning/latestterminalrepairedwarning').reply(200, {
      success: 1, warnings: terminalRepairedWarnings
    })
    // 告警数据
    Mock.onGet('/api/nms/warning/warningtree').reply(200, {
      success: 1, warnings: warningTree
    })
    // 域数据
    Mock.onGet('/api/nms/domain/platformdomaintree').reply(200, {
      success: 1, domains: platformDomainTree
    })

    // 用户域tree
    Mock.onGet('/api/nms/domain/userdomaintree').reply(200, {
      success: 1, domains: userDomainTree
    })

    // 会议域数据
    Mock.onGet('/api/nms/domain/meetingdomaintree').reply(200, {
      success: 1, domains: meetingDomainTree
    })

    // 物理服务器
    Mock.onGet('/api/nms/device/physicals').reply(200, {
      success: 1, physicals: physicals
    })

    // physical详情
    Mock.onGet('/api/nms/device/physical/detail').reply(200, {
      success: 1, physical: physicalDetail
    })

    // 逻辑服务器
    Mock.onGet('/api/nms/device/logicals').reply(200, {
      success: 1, logicals: logicals
    })

    // logical详情
    Mock.onGet('/api/nms/device/logical/detail').reply(200, {
      success: 1, logical: logicalDetail
    })

    // 获取资源数据
    Mock.onGet('/api/nms/domain/resinfo').reply(200, {
      success: 1, res: resInfo
    })

    // 获取受管终端列表
    Mock.onGet('/api/nms/domain/controledterminals').reply(200, {
      success: 1, terminals: controledTerminals
    })

    Mock.onGet('/api/nms/domain/terminal/detail').reply(200, {
      success: 1, terminal: ctrlTerminalDetail
    })

    // 获取非受管终端列表
    Mock.onGet('/api/nms/domain/uncontroledterminals').reply(200, {
      success: 1, terminals: uncontroledTerminals
    })

    // 获取用户域列表
    Mock.onGet('/api/nms/user/getusers').reply(200, {
      success: 1, users: users
    })

    // 用户管理
    Mock.onGet('/api/nms/user/nmspages').reply(200, {
      success: 1,
      nmspages: nmspages
    })

    Mock.onGet('/api/nms/user/userprivileges').reply(200, {
      success: 1,
      userprivileges: userprivileges
    })

    // 获取日志列表
    Mock.onGet('/api/nms/loginfo/userloginfo').reply(200, {
      success: 1, logs: logs
    })

    // 传统会议列表
    Mock.onGet('/api/nms/device/traditionalMeetings').reply(200, {
      success: 1, traditionalMeetings: traditionalMeetings
    })

    // 传统会议详情
    Mock.onGet('/api/nms/device/traditionMeeting/detail').reply(200, {
      success: 1, traditionMeeting: TraditionMeetingDetail
    })

    // 传统会议-级联会议列表
    Mock.onGet('/api/nms/device/cascadeMeetings').reply(200, {
      success: 1, cascadeMeetings: cascadeMeetings
    })

     // 传统会议-软硬终端列表
    Mock.onGet('/api/nms/device/hardAndSoftTerminals').reply(200, {
      success: 1, hardAndSoftTerminals: hardAndSoftTerminals
    })

    // 传统会议-软硬终端列表-所属会议详情
    Mock.onGet('/api/nms/device/softharddetail/detail').reply(200, {
      success: 1, hardSoftTerminalDetail: hardSoftTerminalDetail
    })

    // 传统会议-软硬终端列表-所属会议详情-主会议
    Mock.onGet('/api/nms/device/mainvideos').reply(200, {
      success: 1, mainvideos: mainVideo
    })

    // 传统会议-软硬终端列表-所属会议详情-入会离会详情
    Mock.onGet('/api/nms/device/inoutmeetings').reply(200, {
      success: 1, inoutmeetings: inOutMeeting
    })

    // 传统会议-直播
    Mock.onGet('/api/nms/device/liveStreamings').reply(200, {
      success: 1, liveStreamings: liveStreaming
    })

    // 传统会议-数据协作
    Mock.onGet('/api/nms/device/cooperations').reply(200, {
      success: 1, cooperations: liveStreaming
    })

    // 传统会议-数据协作-协作模式
    Mock.onGet('/api/nms/device/cooperativemodes').reply(200, {
      success: 1, cooperativemodes: liveStreaming
    })

    // 传统会议-数据协作-协作方
    Mock.onGet('/api/nms/device/collaborations').reply(200, {
      success: 1, collaborations: liveStreaming
    })

    // 传统会议-数据协作-观看方
    Mock.onGet('/api/nms/device/viewers').reply(200, {
      success: 1, viewers: liveStreaming
    })

    // 传统会议-会场概况-管理方
    Mock.onGet('/api/nms/device/managers').reply(200, {
      success: 1, managers: manager
    })

    // 传统会议-会场概况-语音激励
    Mock.onGet('/api/nms/device/voiceincentives').reply(200, {
      success: 1, voiceincentives: manager
    })

    // 传统会议-会场概况-画面合成
    Mock.onGet('/api/nms/device/imagesynthesis').reply(200, {
      success: 1, imagesynthesis: manager
    })

    // 传统会议-会场概况-混音
    Mock.onGet('/api/nms/device/soundmixings').reply(200, {
      success: 1, soundmixings: manager
    })

    // 传统会议-会场概况-点名
    Mock.onGet('/api/nms/device/calls').reply(200, {
      success: 1, calls: manager
    })

    // 传统会议-会场概况-会议轮询
    Mock.onGet('/api/nms/device/turnmeetings').reply(200, {
      success: 1, turnmeetings: manager
    })

    // 传统会议-会场概况-录像
    Mock.onGet('/api/nms/device/videos').reply(200, {
      success: 1, videos: manager
    })

    // 传统会议-会场概况-电视墙
    Mock.onGet('/api/nms/device/tvwalls').reply(200, {
      success: 1, tvwalls: manager
    })

    // 诊断分析-诊断功能-终端诊断
    Mock.onGet('/api/nms/device/terminaldiagnostics').reply(200, {
      success: 1, terminaldiagnostics: terminalDiagnostic
    })

    // 诊断分析-诊断功能-终端诊断-硬件状态
    Mock.onGet('/api/nms/device/HardwareStatuss').reply(200, {
      success: 1, hardwareStatuss: hardwareStatus
    })

    // 诊断分析-诊断功能-终端诊断-硬件状态-视频源
    Mock.onGet('/api/nms/hardwareStatus/videos').reply(200, {
      success: 1, videos: video
    })

    // 诊断分析-诊断功能-终端诊断-硬件状态-麦克风
    Mock.onGet('/api/nms/hardwareStatus/microphones').reply(200, {
      success: 1, microphones: microPhone
    })

    // 诊断分析-诊断功能-终端诊断-硬件状态-摄像头
    Mock.onGet('/api/nms/hardwareStatus/cameras').reply(200, {
      success: 1, cameras: camera
    })

    // 诊断分析-诊断功能-终端诊断-硬件状态-输出信号
    Mock.onGet('/api/nms/hardwareStatus/outsignal').reply(200, {
      success: 1, outsignal: outSignal
    })

    // 诊断分析-诊断功能-终端诊断-硬件状态-输入信号
    Mock.onGet('/api/nms/hardwareStatus/insignal').reply(200, {
      success: 1, insignal: inSignal
    })

    // 诊断分析-诊断功能-会议诊断
    Mock.onGet('/api/nms/device/meeting').reply(200, {
      success: 1, meetings: meetingDiagnostic
    })

    // 诊断分析-诊断功能-会议诊断-画面合成器
    Mock.onGet('/api/nms/meeting/picturesynthesizer').reply(200, {
      success: 1, picturesynthesizers: pictureSynthesizer
    })

    // 诊断分析-诊断功能-会议诊断-画面适配-主流广播
    Mock.onGet('/api/nms/meeting/mainradio').reply(200, {
      success: 1, mainradios: mainRadio
    })

    // 诊断分析-诊断功能-会议诊断-音频适配
    Mock.onGet('/api/nms/meeting/audioadaptation').reply(200, {
      success: 1, audioadaptations: audioAdaptation
    })

    // 诊断分析-诊断功能-会议诊断-混音器-终端名称
    Mock.onGet('/api/nms/meeting/terminalname').reply(200, {
      success: 1, terminalnames: terminalName
    })

    // 诊断分析-诊断功能-会议诊断-混音器
    Mock.onGet('/api/nms/meeting/mixer').reply(200, {
      success: 1, mixers: mixer
    })

    // 诊断分析-诊断功能-会议诊断-编解码器
    Mock.onGet('/api/nms/meeting/codec').reply(200, {
      success: 1, codecs: codec
    })

    // 诊断分析-诊断功能-会议诊断-服务器资源
    Mock.onGet('/api/nms/meeting/serverresource').reply(200, {
      success: 1, serverresources: serverResource
    })

    // 诊断分析-诊断功能-服务器诊断
    Mock.onGet('/api/nms/device/server').reply(200, {
      success: 1, servers: serverDiagnostic
    })

    // 诊断分析-诊断功能-服务器诊断-告警
    Mock.onGet('/api/nms/server/warning').reply(200, {
      success: 1, warnings: serverWarning
    })

    // 巡检功能-License文件
    Mock.onGet('/api/nms/device/licenses').reply(200, {
      success: 1, licenses: inspectionDomain
    })

    // 巡检功能-服务器资源
    Mock.onGet('/api/nms/domain/insresinfo').reply(200, {
      success: 1, res: inspectionDomain
    })

    // 巡检功能-服务器状态-物理服务器/逻辑服务器
    Mock.onGet('/api/nms/inspection/physicss').reply(200, {
      success: 1, physicss: inspectionDomain
    })

    // 巡检功能-服务器状态-终端状态
    Mock.onGet('/api/nms/inspection/terminals').reply(200, {
      success: 1, terminals: inspectionDomain
    })

    // 获取阈值设置
    Mock.onGet('/api/nms/systemset/getlimit').reply(200, {
      success: 1, limits: limits
    })

    // 获取服务器
    Mock.onGet('/api/nms/systemset/getserverslimit').reply(200, {
      success: 1, servers: servers
    })

    // 获取服务域
    Mock.onGet('/api/nms/domain/getservicedomain').reply(200, {
      success: 1, services: services
    })

    // 获取平台域
    Mock.onGet('/api/nms/domain/getplatformdomain').reply(200, {
      success: 1, platforms: platforms
    })

    // 获取机房
    Mock.onGet('/api/nms/domain/getmachineroom').reply(200, {
      success: 1, machinerooms: machinerooms
    })

    // 获取告警通知信息
    Mock.onGet('/api/nms/warning/warningnotify').reply(200, {
      success: 1, warnings: warnings
    })

    // 获取暂停告警信息
    Mock.onGet('/api/nms/domain/stopwarningset').reply(200, {
      success: 1, stopWarnings: stopWarnings
    })

    // 获取设备类型信息
    Mock.onGet('/api/nms/sus/getdevicetypes').reply(200, {
      success: 1, deviceTypes: deviceTypes
    })

    // 获取版本信息
    Mock.onGet('/api/nms/sus/getversioninfo').reply(200, {
      success: 1, versionInfo: versionInfo
    })

    Mock.onGet('/api/nms/sus/terminal/versions').reply(200, {
      success: 1, versionInfo: versionInfo
    })

    // 获取已选告警通知信息
    Mock.onGet('/api/nms/warning/subwarningcode').reply(200, {
      success: 1, subwarningcode: subwarningcode
    })
  }
}
