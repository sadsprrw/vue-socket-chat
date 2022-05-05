<template>
  <div class="people">
    <h1 class="people-header">Online people</h1>
    <div class="people-list-container">
      <ul class="people-list">
        <li  class="people-user" v-for="(val, inx) in userList" :key="val['username']"
          v-on:click="onChatSelected(inx, val['username'], val['color'])"
          :title="val['username']"
          v-bind:class="bindUserClass(val['username'])">
          <div class="user-icon" :style="getStyleIcon(val['color'])"></div>
          <h3 class="user-name">{{ val['username'] }}</h3>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "OnlinePeople",
  props: {
    userList: {
      require: true,
    },
    onChatSelected: {
      require: true,
      type: Function,
    },
    user: {
      require: true
    },
    currentUser: {
      require: true
    }
  },
  data () {
    return {

    }
  },
  methods: {
    getStyleIcon(color){
      return 'background-color:' + color
    },
    bindUserClass(username){
      if(username === this.user['name'])
        return 'disabled'
      if(this.currentUser) {
        if (username === this.currentUser['username'])
          return 'active'
      }
      return ''
    }
  },
}
</script>

<style scoped>
@import "../../css/people.css";

</style>