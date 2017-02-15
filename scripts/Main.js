import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { UserForm } from './UserForm';

import { Content } from './Content';

Socket.on('connect', function() {
 console.log('Connecting to the server!');
})

ReactDOM.render(
    <Content />, 
    document.getElementById('content')
);

ReactDOM.render(
    <MessageForm />, 
    document.getElementById('chatForm')
);

ReactDOM.render(
    <UserForm />, 
    document.getElementById('userForm')
);