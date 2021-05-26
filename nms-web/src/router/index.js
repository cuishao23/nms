import Vue from 'vue'
import Router from 'vue-router'

// 网站头部
import PersonalSettings from 'pages/personalsettings'
// import Main from 'pages/main'

// 首页
import Home from 'pages/home'

// 基本信息
import BaseInfo from 'pages/baseinfo'
import BaseInfoHome from 'components/baseinfo/home'
import SearchResult from 'components/baseinfo/search-result'

// 设备信息
import PlatformDeviceInfo from 'pages/platformdeviceinfo'
import PlatformDeviceInfoHome from 'components/platformdeviceinfo/platformdevice/home'
import PhysicalDetail from 'components/platformdeviceinfo/platformdevice/physicaldetail'
import DeviceDetail from 'components/platformdeviceinfo/platformdevice/devicedetail'
import TerminalDeviceInfo from 'pages/terminaldeviceinfo'

import TerminalDeviceInfoHome from 'components/platformdeviceinfo/terminaldevice/home'
import CtrlTerminalDetail from 'components/platformdeviceinfo/terminaldevice/ctrlterminaldetail'
import UnctrlTerminalWarning from 'components/platformdeviceinfo/terminaldevice/unctrlterminalwarning'
import UnctrlTerminalEdit from 'components/platformdeviceinfo/terminaldevice/unctrlterminaledit'

// 设备告警
import SubWarningInfo from 'pages/subwarninginfo'
import UnRepairedWarningInfo from 'pages/unrepairedwarninginfo'
import RepairedWarningInfo from 'pages/repairedwarninginfo'

// 会议详情
import RealTimeMeeting from 'pages/realtimemeeting'
import RealTimeMeetingHome from 'components/realtimemeeting/realtimemeetingdevice/home'
import RealTimeMultiPointMeeting from 'components/realtimemeeting/realtimemeetingdevice/realtimemultipointmeeting'
import SoftHardDetail from 'components/realtimemeeting/realtimemeetingdevice/softharddetail'
import RealTimeCascadeMeeting from 'components/realtimemeeting/realtimemeetingdevice/realtimecascademeeting'
import RealTimeP2pMeeting from 'components/realtimemeeting/realtimemeetingdevice/realtimep2pmeeting'
import HistoryMeeting from 'pages/historymeeting'
import HistoryMeetingHome from 'components/realtimemeeting/historymeetingdevice/home'
import MultiPointMeetingDetail from 'components/realtimemeeting/historymeetingdevice/multipointmeetingdetail'
import P2pMeetingDetail from 'components/realtimemeeting/historymeetingdevice/p2pmeetingdetail'
import MSoftHardDetail from 'components/realtimemeeting/historymeetingdevice/msoftharddetail'
import CascadeMeeting from 'components/realtimemeeting/historymeetingdevice/cascademeeting'

// 诊断分析
import DiagnosisInfo from 'pages/diagnosisinfo'
import DiagnosisInfoHome from 'components/diagnosisinfo/diagnosisdevice/home'
import Inspection from 'pages/inspection'
import InspectionHome from 'components/diagnosisinfo/inspection/home'
import InspectionResult from 'components/diagnosisinfo/inspection/inspection-result'
import PhysicsDetail from 'components/diagnosisinfo/inspection/physicsdetail'
import TerminalDetail from 'components/diagnosisinfo/inspection/terminaldetail'
import AddRegularInspection from 'components/diagnosisinfo/inspection/add-regular-inspection'

// 网管日志
import Log from 'pages/log'
import LogHome from 'components/log/home'

// 系统设置
import LimitSet from 'components/systemconfig/limitset'
import WarningSet from 'components/systemconfig/warningset'
import DeviceSet from 'components/systemconfig/deviceset'
import PermissionSet from 'components/systemconfig/permissionset'

// 版本管理
import SusMgrInfo from 'pages/susmgrinfo'
import SusMgr from 'pages/susmgr'
import SusDetail from 'components/sus/susdetail'

// 无权限页面
import Forbidden from 'pages/forbidden'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/baseinfo'
    },
    {
      path: '/personalsettings/:type',
      name: 'personalsettings',
      component: PersonalSettings
    },
    {
      path: '/',
      name: 'home',
      component: Home,
      redirect: '/baseinfo',
      children: [
        {
          path: 'baseinfo',
          name: 'baseinfo',
          component: BaseInfo,
          redirect: '/baseinfo/home',
          children: [
            {
              path: 'home',
              name: 'baseinfohome',
              component: BaseInfoHome
            },
            {
              path: 'search',
              name: 'baseinfosearch',
              component: SearchResult
            }
          ]
        },
        {
          path: 'platformdeviceinfo',
          name: 'platformdeviceinfo',
          redirect: '/platformdeviceinfo/home',
          component: PlatformDeviceInfo,
          children: [
            {
              path: 'home',
              name: 'platformdeviceinfohome',
              component: PlatformDeviceInfoHome,
              // children: [
              //   {
              //     path: ':moid/type/:type',
              //     name: 'platformdevice',
              //     component: PlatformDevice
              //   }
              // ]
            },
            {
              path: 'physical/:moid/:page/detail',
              name: 'physicaldetail',
              component: PhysicalDetail
            },
            {
              path: 'devicedetail/:name/:moid/:frame',
              name: 'devicedetail',
              component: DeviceDetail,
            }
          ]
        },
        {
          path: 'terminaldeviceinfo',
          name: 'terminaldeviceinfo',
          redirect: '/terminaldeviceinfo/home',
          component: TerminalDeviceInfo,
          children: [
            {
              path: 'home',
              name: 'terminaldeviceinfohome',
              component: TerminalDeviceInfoHome,
              // children: [
              //   {
              //     path: ':moid',
              //     name: 'terminaldevice',
              //     component: TerminalDevice
              //   }
              // ]
            },
            {
              path: 'ctrlterminal/:moid/:name/:e164/detail',
              name: 'ctrlterminaldetail',
              component: CtrlTerminalDetail
            },
            {
              path: 'unctrlterminal/warning/:ip/:name/:type/:moid/:e164/:version/:online',
              name: 'unctrlterminalwarning',
              component: UnctrlTerminalWarning
            },
            {
              path: 'unctrlterminal/edit/:ip/:name/:type/:moid/:e164/:online',
              name: 'unctrlterminaledit',
              component: UnctrlTerminalEdit
            }
          ]
        },
        {
          path: 'subwarninginfo',
          name: 'subwarninginfo',
          component: SubWarningInfo,
          meta: {
            keepAlive: true
          }
        },
        {
          path: 'unrepairedwarninginfo',
          name: 'unrepairedwarninginfo',
          component: UnRepairedWarningInfo,
          meta: {
            keepAlive: true
          }
        },
        {
          path: 'repairedwarninginfo',
          name: 'repairedwarninginfo',
          component: RepairedWarningInfo
        },
        {
          path: 'realtimemeeting',
          name: 'realtimemeeting',
          redirect: '/realtimemeeting/home',
          component: RealTimeMeeting,
          children: [
            {
              path: 'home',
              name: 'realtimemeetinghome',
              component: RealTimeMeetingHome,
            },
            {
              path: 'meeting/:multiType/:meetingE164/detail',
              name: 'realtimemultipointmeeting',
              component: RealTimeMultiPointMeeting,
            },
            {
              path: 'cascademeeting/:multiType/:meetingE164/detail',
              name: 'realtimecascademeeting',
              component: RealTimeCascadeMeeting,
            },
            {
              path: 'p2pmeeting/:meetingE164/:calleeE164/detail',
              name: 'realtimep2pmeeting',
              component: RealTimeP2pMeeting,
            },
            {
              path: 'softhard/:multiType/:meetingE164/:terminalE164/detail',
              name: 'softharddetail',
              component: SoftHardDetail
            }
          ]
        },
        {
          path: 'historymeeting',
          name: 'historymeeting',
          redirect: '/historymeeting/home',
          component: HistoryMeeting,
          children: [
            {
              path: 'home',
              name: 'historymeetinghome',
              component: HistoryMeetingHome,
            },
            {
              path: 'multipointmeeting/:meetingRoom/detail',
              name: 'multipointmeetingdetail',
              component: MultiPointMeetingDetail,
            },
            {
              path: 'p2pmeeting/:meetingRoom/detail',
              name: 'p2pmeetingdetail',
              component: P2pMeetingDetail,
            },
            {
              path: 'msofthard/:meetingRoom/:deviceMoid/detail',
              name: 'msoftharddetail',
              component: MSoftHardDetail
            },
            {
              path: 'cascademeeting/:meetingRoom/detail',
              name: 'cascademeeting',
              component: CascadeMeeting
            },
          ]
        },
        {
          path: 'diagnosisinfo',
          redirect: '/diagnosisinfo/home',
          name: 'diagnosisinfo',
          component: DiagnosisInfo,
          children: [
            {
              path: 'home',
              name: 'diagnosisinfohome',
              component: DiagnosisInfoHome,
            }
          ]
        },
        {
          path: 'inspection',
          redirect: '/inspection/home',
          name: 'inspection',
          component: Inspection,
          children: [
            {
              path: 'home',
              name: 'inspectionhome',
              component: InspectionHome,
            },
            {
              path: 'inspection',
              name: 'inspectionresult',
              component: InspectionResult
            },
            {
              path: 'physics/detail/:taskid/:device_moid',
              name: 'physicsdetail',
              component: PhysicsDetail
            },
            {
              path: 'terminal/detail/:taskid/:device_moid',
              name: 'terminaldetail',
              component: TerminalDetail
            },
            {
              path: 'addregular',
              name: 'addregularinspection',
              component: AddRegularInspection
            }
          ]
        },
        {
          path: 'log',
          name: 'log',
          component: Log,
          redirect: '/log/home',
          children: [
            {
              path: 'home',
              name: 'loghome',
              component: LogHome,
            }
          ]
        },
        {
          path: 'deviceset',
          name: 'deviceset',
          component: DeviceSet
        },
        {
          path: 'limitset',
          name: 'limitset',
          component: LimitSet
        },
        {
          path: 'permissionset',
          name: 'permissionset',
          component: PermissionSet
        },
        {
          path: 'warningset',
          name: 'warningset',
          component: WarningSet
        },
        {
          path: 'susmgrinfo',
          redirect: '/susmgrinfo/susmgr',
          component: SusMgrInfo,
          children: [
            {
              path: 'susmgr',
              name: 'susmgr',
              component: SusMgr
            },
            {
              path: 'detail/:terminal/versions',
              name: 'susdetail',
              component: SusDetail
            }
          ]
        },
        {
          path: 'forbidden',
          name: 'forbidden',
          component: Forbidden
        }
      ]
    }
  ]
})
