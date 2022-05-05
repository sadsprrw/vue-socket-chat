<template>
<div class="header-container">
  <div class="header-tabs">
    <h1 v-for="tab in tabs" :key="tab" :class="getActiveTabStyle(tab)" v-on:click="onTabSelected(tab)">{{tab}}</h1>
  </div>
  <div class="current-user" @click="logOut">
    <div class="current-user-icon" :style="'background: '+ user['color']"></div>
    <h3 class="current-username">{{ user['name'] }}</h3>
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
    logOut: {
      require: true,
      type: Function
    },
    currentTab:{
      require: true
    }
  },
  data (){
    return{
      tabs: ['Chat', 'Combined', 'Graph']
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