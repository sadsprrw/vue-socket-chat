<template>
<div class="header-container">
  <div class="header-tabs">
    <h1 v-for="tab in tabs" :key="tab" :class="getActiveTabStyle(tab)" v-on:click="onTabSelected(tab)">{{tab}}</h1>
  </div>
  <div class="current-user">
    <div class="user-icon" :style="'background: '+ user['color']"></div>
    <h3 class="user-name">{{ user['name'] }}</h3>
  </div>
</div>
</template>

<script>
export default {
  name: "ChatHeader",
  props: {
    user: {
      require: true
    },
    onTabSelected: {
      require: true,
      type: Function
    },
    currentTab:{
      require: true
    }
  },
  data (){
    return{
      tabs: ['Chat', 'Hybrid', 'Graph']
    }
  },
  methods: {
    getActiveTabStyle(tab){
      if(this.currentTab === tab)
        return 'chat-tab active'
      else
        return 'chat-tab'
    }
  }
}
</script>

<style scoped>
@import "../../css/header.css";
</style>