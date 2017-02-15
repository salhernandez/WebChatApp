import * as SocketIO from 'socket.io-client';
export var Socket = SocketIO.connect();
export var Disconnected = Socket.disconnect();

export function broadcastToAll(message){
    Socket.emit('coding event', message);
    console.log(message);
}