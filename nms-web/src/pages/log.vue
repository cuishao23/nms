<template>
  <transition :name="animation">
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </transition>
</template>

<script>
  export default {
    name: "log",
    data() {
      return {
        animation: ''
      }
    },
    watch: {
      '$route': function (routerTo, routerFrom) {
        if (routerFrom.path.indexOf('search') !== -1) {
          this.animation = 'right'
        } else {
          this.animation = ''
        }
      }
    }
  }
</script>

<style scoped>
</style>
