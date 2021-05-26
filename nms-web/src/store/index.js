import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations.js'
import getters from './getters.js'
import state from './state.js'

Vue.use(Vuex);

const store = new Vuex.Store({
    state,
    mutations,
    getters,
});
export default store
