
export const searchMeetingTypeList = [
  {
    text: '实时会议',
    value: 'realtime'
  },
  {
    text: '历史会议',
    value: 'history'
  }
]

export function getServerTypeList() {
  // 服务器类型列表
  return [
    {
      text: '全部设备类型',
      value: 'all'
    },
    {
      text: 'bgm',
      value: 'bgm'
    }
  ]
}

/**
 * 获取首页服务器告警表格字段
 * @returns {*[]}
 */
export function getServerWarningTblFields() {
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
      prop: 'machine_room_name',
      label: '所属虚拟机房'
    },
    {
      prop: 'description',
      label: '告警名称'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '产生时间'
    }
  ]
}

/**
 * 获取首页终端告警表格字段
 * @returns {*[]}
 */
export function getTerminalWarningTblFields() {
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
      prop: 'device_e164',
      label: 'E164号'
    },
    {
      prop: 'domain_name',
      label: '所属用户域'
    },
    {
      prop: 'description',
      label: '告警名称'
    },
    {
      prop: 'level',
      label: '告警级别'
    },
    {
      prop: 'start_time',
      label: '产生时间'
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
  let option = {
    xAxis: {
      type: 'time',
      name: '时间',
      min: 'dataMin',
      max: 'dataMax',
      interval: 60 * 1000 * 10,
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
        rotate: 90,
        formatter: function (value, index) {
          var date = new Date(value);
          return date.toTimeString().substr(0, 8);
        }
      },
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      name: yName,
      min: 0,
      max: 100,
      interval: 50,
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
      splitLine: {
        show: false
      }
    },
    grid: {
      top: 25,
      bottom: 30
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
    },
    series: data
  }
  let myChart = eTool.init(document.getElementById(id));
  myChart.setOption(option, true);
  window.addEventListener("resize", () => {
    myChart.resize();
  })
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
