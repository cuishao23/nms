import 'babel-polyfill'
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import echarts from 'echarts'
import qs from 'qs';
import md5 from 'js-md5';
import Element from 'element-ui';
import 'vx-easyui/dist/themes/default/easyui.css';
import 'vx-easyui/dist/themes/icon.css';
import 'vx-easyui/dist/themes/vue.css';
import EasyUI from 'vx-easyui';

// import $ from 'jquery'

import axios from './axios/api';
import './assets/css/common.css';
import './assets/css/messagebox.css';
import './assets/css/reset.css';
import './assets/css/reset-easyui.css';
import 'animate.css';
import store from '@/store'

require('es6-promise').polyfill();
Vue.prototype.axios = axios;
Vue.use(Element);
Vue.use(echarts);
// 引入告警级别参数在系统配置修改并让首页获取变化
Vue.prototype.app = App;
Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false;
Vue.prototype.qs = qs;
Vue.prototype.$md5 = md5;
// Vue.prototype.global = global;
// axios.defaults.baseURL = global.baseURL;
Vue.use(EasyUI);
// Mock.init();
router.beforeEach((to, from, next) => {
  if (to.matched.length ===0) {                                 //如果未匹配到路由
      from.name ? next({ name:from.name }) : next('/');   //如果上级也未匹配到路由则跳转登录页面，如果上级能匹配到则转上级路由
  } else {
      next();                                                                            //如果匹配到正确跳转
  }
});
/* eslint-disable no-new */
new Vue({
  render: h => h(App),
  axios,
  router,
  store
}).$mount('#app')
