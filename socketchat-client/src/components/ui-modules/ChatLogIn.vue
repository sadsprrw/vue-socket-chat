<template>
  <div class="wrapper">
    <div class="login-container">
      <h1 class="login-header">Log in</h1>
      <div class="login-color">
        <h4 class="login-color-text">Choose a color:</h4>
        <div class="color-wrapper">
          <input class="login-color-input" type="color" id="colorPicker" v-model="color">
        </div>
      </div>
      <input class="login-input" v-model="username">
      <div :class="validate ? 'login-error' : 'disabled' ">This username is already taken</div>
      <button class="login-button" v-on:click="login">Go!</button>
    </div>

  </div>

</template>

<script>
export default {
  name: "ChatLogIn",
  props: {
    onLogin: {
      require: true
    },
    validate: {
      require: true
    }
  },
  data() {
    return {
      username: '',
      color: "#ffffff"
    }
  },
  methods:{
    login(){
      this.onLogin(this.username, this.color)
    }
  }
}

</script>

<style scoped>
@import "../../scss/login.scss";

</style>