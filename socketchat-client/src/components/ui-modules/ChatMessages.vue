<template>
  <div >
    <div class="chat" v-if="currentUser !== null">
      <div class="chat-current-user" v-if="currentUser !== null" >
        <div class="user-icon" :style="getStyleIcon(currentUser['color'])"></div>
        <div class="current-user-content">
          <p class="current-user-name">{{ currentUser['username'] }}</p>
          <p class="current-user-status"> online </p>
        </div>
        <div class="chat-cross-icon" @click="closeChat()">
          <span class="chat-cross-el" style="transform: rotate(-45deg);"></span>
          <span class="chat-cross-el" style="transform: rotate(45deg);"></span>
        </div>
      </div>
      <div class="chat-message-area">
        <div class="messages-area" v-if="this.messages">
          <div  v-for="(val, inx) in this.messages" :key="inx" class="message">
            <div v-if="val['type'] === 'received'" class="dialog-message">
              <div class="message-text dialog-message-text"> {{val['msg']}} </div>
              <span class="message-tail dialog-tail"></span>
              <span class="message-tail-corrector dialog-tail-corrector"></span>
            </div>
            <div v-else-if="val['type'] === 'sent'" class="user-message">
              <div class="message-text user-message-text">{{val['msg']}}</div>
              <span class="message-tail user-tail"></span>
              <span class="message-tail-corrector user-tail-corrector"></span>
            </div>
          </div>
        </div>
        <div class="chat-empty" v-else>
          <div class="chat-annotation">
            Say Hi!
          </div>
        </div>
        <div class="send-area" >
          <div class="message-input-container">
            <textarea class="message-input"
                    v-model="message" placeholder="Write a message..."></textarea>
          </div>
          <button class="button message-button" v-on:click="sendMessage(message); message=''">Send</button>
        </div>
      </div>
    </div>
    <div class="chat closed" v-else>
      <div class="chat-annotation">
        Select a user to start messaging
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
    closeChat: {
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
  },
  methods: {
    getStyleIcon(color){
      return 'background-color:' + color
    }
  }
}
</script>

<style scoped>
@import "../../css/message.css";
</style>