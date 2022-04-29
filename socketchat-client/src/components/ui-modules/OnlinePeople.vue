<template>
  <div class="people">
    <h1 class="people-header">Online people</h1>
    <div class="people-list-container">
      <ul class="people-list">
        <li class="current-user">
          <div class="user-icon" :style="getStyleIcon(user['color'])"></div>
          <h3 class="user-name">{{ user['name'] }}</h3>
        </li>
        <li  class="people-user" v-for="(val, inx) in userList" :key="val['username']"
          v-on:click="onChatSelected(inx, val['username']); selectedUser = val['username']"
          :title="val['username']"
          v-bind:class="user['name'] === val['username'] ? 'disabled' : selectedUser === val['username'] ? 'active' : ''">
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
  },
  data () {
    return {
      selectedUser: null,
    }
  },
  methods: {
    getStyleIcon(color){
      return 'background-color:' + color
    }
  }
}
</script>

<style scoped>
@import "../../css/people.css";

</style>