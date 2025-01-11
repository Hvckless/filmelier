class SocketHandler {
    constructor() {
        this.socket = new WebSocket("ws://localhost:8081");
    }
    sendMessage(message) {
        if (this.socket.readyState == WebSocket.OPEN) {
            this.socket.send(message);
        }
    }
}
SocketHandler.instance = new SocketHandler();
export default SocketHandler;
