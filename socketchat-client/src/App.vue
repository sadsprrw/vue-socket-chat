<template>
  <ChatLogIn :validate="validate"  :on-login="loginUser" v-if="user === null" />
  <div class="main-container" v-else>
    <div class="online-people-container">
      <OnlinePeople :user-list="onlineUsers" :user="user" :on-chat-selected="chatSelected" />
    </div>
    <div class="chat-container">
      <ChatMessages :send-message="sendMessage" :current-user="currentUserChat" :messages="currentMessages" />
    </div>
    <div class="graph-container">
      <ChatGraph :user-list="onlineUsers" :connection-list="chatConnections" ref="messageAnimation"/>
    </div>
  </div>

</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import io from 'socket.io-client'

import ChatMessages from '@/components/ui-modules/ChatMessages.vue'
import OnlinePeople from "@/components/ui-modules/OnlinePeople.vue";
import ChatGraph from "@/components/ui-modules/ChatGraph.vue";
import ChatLogIn from "@/components/ui-modules/ChatLogIn.vue";

import {ChatMessage, OnlineUsers, NewUserData, UserData, Connection} from '@/types/ChatTypes';
@Options({
  data() {
    return {
      user: null,
      currentUserChat: null,
      allMessages: {} ,
      chatConnections: [] as Connection[],
      currentMessages: null,
      onlineUsers: {} as OnlineUsers,
      socket:io('http://localhost:2345'),
      validate: false
    }
  },
  components: {
    ChatMessages,
    OnlinePeople,
    ChatGraph,
    ChatLogIn
  },
  mounted() {
    this.socket.on('MESSAGE', (socket : ChatMessage) => {
      if (!this.allMessages[socket.from]){
        this.allMessages[socket.from] = [socket.message]
      }
      else this.allMessages[socket.from].push(socket.message);

      console.log(this.allMessages);
    })
    this.socket.on('USER_ONLINE_PUBLIC_DATA', (socket : OnlineUsers) => {
      this.onlineUsers = socket;
      console.log("Online Users:");
      console.log(socket);
    })
    this.socket.on('NEW_USER', (socket : NewUserData) => {
      this.onlineUsers[socket['id']] = {'username': socket['username'], 'color': socket['color']}
    })
    this.socket.on('DELETE_USER', (socket : NewUserData) => {
      delete this.onlineUsers[socket['id']]
      if(this.currentUserChat !== null) {
        if (socket['username'] === this.currentUserChat['username']) {
          this.currentUserChat = null
          this.currentMessages = null
        }
      }
      if (this.allMessages[socket['id']]){
        delete this.allMessages[socket['id']]
      }
    })
    this.socket.on('CONNECTION_DATA', (socket : Connection[]) => {
      this.chatConnections = socket;
      console.log(socket)
    })
    this.socket.on('NEW_CONNECTION', (socket : Connection) => {
      this.chatConnections.push(socket)
    })
    this.socket.on('MESSAGE_ANIMATION', (socket : Connection) => {
      this.$refs.messageAnimation.message(socket['source'], socket['target'])
    })
  },
  methods: {
    loginUser(username : string, color : string){
      if (this.userExists(username)){
        this.validate = true
      }
      else {
        this.user = {'name': username,'color': color}
        this.socket.emit('login', this.user)
      }
    },
    sendMessage(message : string) {
      if (this.currentUserChat != null) {
        if(message !== '') {
          const data = {
            user: this.user['name'],
            msg: message,
            to: this.currentUserChat,
            type: "sent",
          }
          if (!this.currentMessages) {
            this.currentMessages = [data];
          } else this.currentMessages.push(data);
          this.socket.emit('send_message', data);

          this.allMessages[this.currentUserChat['id']] = this.currentMessages;
        }
      }
    },
    chatSelected(index : string, username : string){
      this.currentUserChat = {'id': index, 'username': username}
      this.currentMessages = this.allMessages[this.currentUserChat['id']]
    },
    userExists(username : string){
      let onlineUsersValues : UserData[] = Object.values(this.onlineUsers)
      return onlineUsersValues.find((value : UserData)  => (value['username'] === username));
    }
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
@import "scss/main.scss";
</style>
