import api from '../axios'


/**
 * vue从后台获取数据，并导出EXCEL文件
 * @param value
 * @returns {*}
 * @constructor 崔鑫 2020.4.15
 */

export function Upexcele(value, name) {
  const url = window.URL.createObjectURL(value)
  const a = document.createElement('a')
  a.href = url
  a.download = name
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}


/*
*
* 抓包 日志 页面保证不会因登录问题退出
*/

export function keepAlive() {
  if (document.location.hash.indexOf("diagnosisinfo") !== -1) {
    api.getServerInfo()
  }
  setTimeout("keepAlive()", 10*60*1000)
}