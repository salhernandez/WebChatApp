// scripts/Main.js
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Content } from './Content';
import { Socket } from './Socket';
import { ChatForm } from './ChatForm.js';

 
ReactDOM.render(
 <ChatForm />,
 document.getElementById('chatForm')
);

Socket.on('connect', function() {
 console.log('Connecting to the server!');
})

/*
function broadcastToAll(message){
 Socket.emit('coding event', message);
 console.log(message);
 alert(message);
}

broadcastToAll("lmao bruh");
*/