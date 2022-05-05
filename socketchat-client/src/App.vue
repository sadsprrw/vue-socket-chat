<template>
  <ChatLogIn :validate="validate"  :on-login="loginUser" v-if="user === null" />
  <div class="main-wrap" v-else>
    <div class="main-container" >
      <ChatHeader :user="user" :on-tab-selected="tabSelected" :log-out="logOut" :current-tab="currentTab"/>
      <div class="main-chat" >
          <div :style="currentTab === 'Graph' || currentTab === 'Combined' ?
           'display:none' : ''" class="online-people-container">
            <OnlinePeople :on-chat-selected="chatSelected" :current-user="currentUserChat"
                          :user-list="onlineUsers" :user="user"  />
          </div>
          <div  :style="currentTab === 'Graph' ? 'display:none;' : ''"  class="chat-container">
            <ChatMessages :close-chat="closeChat" :send-message="sendMessage"
                          :current-user="currentUserChat" :messages="currentMessages" />
          </div>
          <Slide :style="currentTab === 'Chat' ? 'display:none' : ''" width="400" :burgerIcon="!menuIsOpen"
                 :isOpen="menuIsOpen" @closeMenu="menuIsOpen = false" >
            <OnlinePeople  :on-chat-selected="chatSelected" :current-user="currentUserChat"
                           :user-list="onlineUsers" :user="user"/>
          </Slide>
          <transition name="graph-fade">
            <div id="graph-container"  :style="currentTab === 'Chat' ? 'width:0;' :
                  currentTab === 'Combined' ? 'width: 50%' : ''" class="graph-container">
              <ChatGraph :select-user-on-graph="selectUserOnGraph"
                         :user-list="onlineUsers" :connection-list="chatConnections" ref="chatGraph"/>
            </div>
          </transition>
      </div>
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
import ChatHeader from "@/components/ui-modules/ChatHeader.vue";
import { Slide } from 'vue3-burger-menu'

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
      socket:io('http://localhost:8000'),
      validate: false,
      menuIsOpen: false,
      currentTab: 'Chat',
    }
  },
  components: {
    ChatMessages,
    OnlinePeople,
    ChatGraph,
    ChatLogIn,
    ChatHeader,
    Slide
  },
  mounted() {
    this.socket.on('MESSAGE', (socket: ChatMessage) => {
      if (!this.allMessages[socket.from]){
        this.allMessages[socket.from] = [socket.message]
      }
      else this.allMessages[socket.from].push(socket.message);
    })
    this.socket.on('USER_ONLINE_PUBLIC_DATA', (socket: OnlineUsers) => {
      this.onlineUsers = socket;
    })
    this.socket.on('NEW_USER', (socket: NewUserData) => {
      this.onlineUsers[socket['id']] = {'username': socket['username'], 'color': socket['color'], 'id': socket['id']}
    })
    this.socket.on('DELETE_USER', (socket: NewUserData) => {
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
    this.socket.on('CONNECTION_DATA', (socket: Connection[]) => {
      this.chatConnections = socket;
    })
    this.socket.on('NEW_CONNECTION', (socket: Connection) => {
      this.chatConnections.push(socket)
    })
    this.socket.on('MESSAGE_ANIMATION', (socket: Connection) => {
      setTimeout(this.$refs.chatGraph.message, 300, socket['source'], socket['target'])
    })
  },
  methods: {

    loginUser(username: string, color: string){
      if (this.userExists(username) || username.trim() === ''){
        this.validate = true
      }
      else {
        this.user = {'name': username,'color': color}
        this.socket.emit('login', this.user)
      }
    },
    checkMenu(){
      if (!this.menuIsOpen)
        return 'left: 0;'
      else return 'left: -400px;'
    },
    sendMessage(message: string) {
      if (this.currentUserChat != null) {
        if(message.trim() !== '') {
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
    tabSelected(tab: string){
      if (this.currentTab !== tab)  {
        if(tab === 'Combined')
          this.$refs.chatGraph.updateWidth(window.innerWidth/2)
        if(tab === 'Graph')
          this.$refs.chatGraph.updateWidth(window.innerWidth)
        this.currentTab = tab
      }
    },
    chatSelected(index: string, username: string, color: string){
      this.currentUserChat = {'id': index, 'username': username, 'color': color}
      this.currentMessages = this.allMessages[this.currentUserChat['id']]
    },
    userExists(username: string){
      const onlineUsersValues: UserData[] = Object.values(this.onlineUsers)
      return onlineUsersValues.find((value : UserData)  => (value['username'] === username.trim()));
    },
    closeChat(){
      this.currentUserChat = null;
    },
    selectUserOnGraph(username: string){
      if(this.user['name'] !== username){
        if(this.currentTab === 'Graph')
          this.tabSelected('Combined')
        let chosenUser = this.userExists(username)
        if(chosenUser)
          this.chatSelected(chosenUser['id'], chosenUser['username'], chosenUser['color'])
      }
    },
    logOut(){
      // TODO
    },
    peopleStyle(){
      if(this.currentTab === 'Graph' || this.currentTab === 'Combined') return 'display:none'
      return ''
    },
    chatStyle(){
      if(this.currentTab === 'Graph') return 'display:none;'
      return ''
    },
    menuStyle(){
      if(this.currentTab === 'Chat') return 'display:none;'
      return ''
    },
    graphStyle(){
      if(this.currentTab === 'Chat') return 'width:0;'
      if(this.currentTab === 'Combined') return 'width: 50%'
      return ''
    }
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">

@import "css/main.scss";
</style>
