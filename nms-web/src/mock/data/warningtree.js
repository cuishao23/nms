const warningTree = [
  {
    code: 4,
    name: '其它',
    children: [
      {
        name: '智能插座离线',
        level: 'critical',
        code: 4002
      },
      {
        name: '智能插座已达最大使用寿命',
        level: 'important',
        code: 4001
      }]
  },
  {
    code: 3,
    name: 'MCU告警',
    children: [
      {
        name: '单板媒体芯片故障',
        level: 'critical',
        code: 3014
      },
      {
        name: '单板电压不在正常范围(一般)',
        level: 'normal',
        code: 3013
      },
      {
        name: '单板电压不在正常范围(重要)',
        level: 'important',
        code: 3012
      },
      {
        name: '单板电压不在正常范围(严重)',
        level: 'critical',
        code: 3011
      },
      {
        name: '单板服务器下线',
        level: 'critical',
        code: 3010
      },
      {
        name: '磁盘空间不足',
        level: 'critical',
        code: 3009
      },
      {
        name: '单板内存资源占用率过高',
        level: 'critical',
        code: 3008
      },
      {
        name: '单板CPU资源占用率过高',
        level: 'critical',
        code: 3007
      },
      {
        name: '单板温度过高(一般)',
        level: 'normal',
        code: 3006
      },
      {
        name: '单板温度过高(重要)',
        level: 'important',
        code: 3005
      },
      {
        name: '单板温度过高(严重)',
        level: 'critical',
        code: 3004
      },
      {
        name: '机箱风扇异常',
        level: 'critical',
        code: 3003
      },
      {
        name: '单电源板异常',
        level: 'important',
        code: 3002
      },
      {
        name: '多电源板异常',
        level: 'critical',
        code: 3001
      }]
  },
  {
    code: 2,
    name: '服务器设备告警',
    children: [
      {
        name: "pas进程异常",
        level: "critical",
        code: 2057
      }, {
        name: "ngi进程异常",
        level: "critical",
        code: 2056
      }, {
        name: "h323nadp进程异常",
        level: "critical",
        code: 2055
      }, {
        name: "h323sadp进程异常",
        level: "critical",
        code: 2054
      }, {
        name: "h323n进程异常",
        level: "critical",
        code: 2053
      }, {
        name: "h323s进程异常",
        level: "critical",
        code: 2052
      }, {
        name: "sipagent进程异常",
        level: "critical",
        code: 2051
      }, {
        name: "sipproxy进程异常",
        level: "critical",
        code: 2050
      }, {
        name: "mpcadp进程异常",
        level: "critical",
        code: 2049
      }, {
        name: "callmanager进程异常",
        level: "critical",
        code: 2048
      }, {
        name: "磁盘写入数据超阈值",
        level: "critical",
        code: 2047
      }, {
        name: "转发服务器流量超阈值",
        level: "critical",
        code: 2046
      }, {
        name: "服务器硬盘使用寿命不足",
        level: "critical",
        code: 2045
      }, {
        name: "系统未检测到U盘",
        level: "important",
        code: 2044
      }, {
        name: "U盘备份功能失败",
        level: "important",
        code: 2043
      }, {
        name: "随机数生成失败",
        level: "critical",
        code: 2042
      }, {
        name: "软件完整性自测试失败",
        level: "critical",
        code: 2041
      }, {
        name: "随机数自测试失败",
        level: "critical",
        code: 2040
      }, {
        name: "SM4算法自测试失败",
        level: "critical",
        code: 2039
      }, {
        name: "SM3算法自测试失败",
        level: "critical",
        code: 2038
      }, {
        name: "SM2算法自测试失败",
        level: "critical",
        code: 2037
      }, {
        name: "SM1算法自测试失败",
        level: "critical",
        code: 2036
      }, {
        name: "dataswitch丢包率过高",
        level: "critical",
        code: 2035
      }, {
        name: "dataswitch丢包率过高",
        level: "critical",
        code: 2034
      }, {
        name: "网管收集器进程崩溃",
        level: "critical",
        code: 2033
      }, {
        name: "云平台主备业务锁异常",
        level: "critical",
        code: 2032
      }, {
        name: "DS系统转发优化未配置",
        level: "critical",
        code: 2031
      }, {
        name: "电视墙板卡服务器温度过高",
        level: "critical",
        code: 2030
      }, {
        name: "网络IP地址冲突",
        level: "critical",
        code: 2029
      }, {
        name: "MYSQL主从同步失败",
        level: "critical",
        code: 2028
      }, {
        name: "SA进程异常",
        level: "critical",
        code: 2027
      }, {
        name: "合成器资源使用百分比超过阈值",
        level: "important",
        code: 2026
      }, {
        name: "混音器资源使用百分比超过阈值",
        level: "important",
        code: 2025
      }, {
        name: "备机业务异常",
        level: "critical",
        code: 2024
      }, {
        name: "daemon进程异常",
        level: "critical",
        code: 2023
      }, {
        name: "服务器切换超时",
        level: "critical",
        code: 2022
      }, {
        name: "服务器切换",
        level: "critical",
        code: 2021
      }, {
        name: "MODB同步失败",
        level: "critical",
        code: 2020
      }, {
        name: "网卡流量过载",
        level: "critical",
        code: 2019
      }, {
        name: "磁盘空间不足",
        level: "critical",
        code: 2018
      }, {
        name: "网管收集器接入容量超过阈值",
        level: "critical",
        code: 2016
      }, {
        name: "服务器下线",
        level: "critical",
        code: 2015
      }, {
        name: "接收丢包(10%)",
        level: "normal",
        code: 2014
      }, {
        name: "接收丢包(5%)",
        level: "normal",
        code: 2013
      }, {
        name: "服务器异常",
        level: "critical",
        code: 2011
      }, {
        name: "端口资源使用百分比超过阈值",
        level: "important",
        code: 2007
      }, {
        name: "并发呼叫容量超过阈值",
        level: "important",
        code: 2006
      }, {
        name: "PAS接入容量超过阈值",
        level: "important",
        code: 2005
      }, {
        name: "NTP时间同步失败",
        level: "important",
        code: 2004
      }, {
        name: "内存高于阈值",
        level: "critical",
        code: 2003
      }, {
        name: "cpu高于阈值",
        level: "critical",
        code: 2002
      }]
  },
  {
    code: 1,
    name: '终端设备告警',
    children: [
      {
        name: "终端内存资源占用率过高",
        level: "critical",
        code: 1024
      }, {
        name: "终端CPU资源占用率过高",
        level: "critical",
        code: 1023
      }, {
        name: "E1失载波线路故障",
        level: "normal",
        code: 1022
      }, {
        name: "E1远端告警线路故障",
        level: "critical",
        code: 1021
      }, {
        name: "E1失同步线路故障",
        level: "critical",
        code: 1020
      }, {
        name: "E1全1线路故障",
        level: "critical",
        code: 1019
      }, {
        name: "终端异常重启",
        level: "critical",
        code: 1008
      }, {
        name: "版本过低",
        level: "important",
        code: 1007
      }, {
        name: "注册GK失败",
        level: "critical",
        code: 1006
      }, {
        name: "丢包率过高(10%)",
        level: "important",
        code: 1004
      }, {
        name: "丢包率过高(5%)",
        level: "normal",
        code: 1003
      }]
  }]

export { warningTree }
