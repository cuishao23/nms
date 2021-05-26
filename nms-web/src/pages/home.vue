<template>
  <div class="mainContainer">
    <div class="menuContainer"><!--菜单栏-->
      <MenuContainer></MenuContainer>
    </div>
    <div class="contentContainer"><!--网站内容部分-->
      <div id="frame_content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
  import MenuContainer from 'components/menucontainer/menucontainer.vue';

  export default {
    name: 'maincontent',
    data() {
      return {
      }
    },
    methods: {},
    components: {
      MenuContainer,
    }
  }
</script>

<style>
  #frame_content {
    /*margin-top: -10px;*/
    padding-left: 10px;
  }
</style>
