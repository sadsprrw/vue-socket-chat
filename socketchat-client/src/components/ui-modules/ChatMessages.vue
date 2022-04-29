<template>
  <div class="chat">
    <h1 class="chat-header" v-if="currentUser === null" >Select chat</h1>
    <h1 class="chat-header" v-else> {{ currentUser['username'] }} </h1>
    <div class="chat-message-area">
      <div class="messages-area">
        <div  v-for="(val, inx) in this.messages" :key="inx" class="message">
          <div v-if="val['type'] === 'received'" class="dialog-message">
            <div class="dialog-message-text"> {{val['msg']}} </div>
          </div>
          <div v-else-if="val['type'] === 'sent'" class="user-message">
            <div class="user-message-text">{{val['msg']}}</div>
          </div>
        </div>
      </div>
      <div class="send-area" >
        <textarea class="message-input"
                  v-model="message" placeholder="Write a message..."></textarea>
        <button :class="currentUser === null ? 'button disabled' : 'button message-button'"
                :disable="currentUser === null ? 'true' : 'false'"
                v-on:click="sendMessage(message); message=''">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatMessages",
  props: {
    messages: {
      require: true
    },
    sendMessage: {
      require: true,
      type: Function
    },
    currentUser: {
      require: true
    }
  },
  data() {
    return {
      message: ''
    }
  }
}
</script>

<style scoped>
@import "../../css/message.css";
</style>