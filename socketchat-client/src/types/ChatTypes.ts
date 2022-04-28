export interface ChatMessage{
    from: string,
    to: string,
    message: ChatMessageType
}

export interface ChatMessageType{
    user: string,
    msg: string,
    type: string
}

export interface UserData{
    username: string,
    color: string
}

export interface OnlineUsers{
    [id : string]: UserData
}

export interface NewUserData{
    id : string,
    username: string,
    color: string
}

export interface Connection{
    target: {id: string}
    source: {id: string}
}