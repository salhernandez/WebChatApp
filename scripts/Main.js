import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { UserForm } from './UserForm';

import { Content } from './Content';

import GoogleLogin from 'react-google-login';

const responseGoogle = (response) => {
  console.log(response);
  
  var msg = response.w3['ig'];
  //emits the messag eto the socket
     console.log('New user: ', msg);
        Socket.emit('new user', {
            'user': msg,
        });
}



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

ReactDOM.render(
  <GoogleLogin
    clientId="192807312085-9jk4t8hnf02gcb6bekmsu73h5td0reap.apps.googleusercontent.com"
    buttonText="Login"
    onSuccess={responseGoogle}
    onFailure={responseGoogle}
  />,
  document.getElementById('googleButton')
);