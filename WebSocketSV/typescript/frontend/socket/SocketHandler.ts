class SocketHandler{
    socket:WebSocket;
    public static instance:SocketHandler = new SocketHandler();
    private constructor(){
        this.socket = new WebSocket("ws://localhost:8081");
    }

    public sendMessage(message:string):void{
        if(this.socket.readyState == WebSocket.OPEN){
            this.socket.send(message);
        }
    }
}

export default SocketHandler;