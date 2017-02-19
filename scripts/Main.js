import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { UserForm } from './UserForm';
import { Content } from './Content';
import { FullChatApp } from './FullChatApp';

import GoogleLogin from 'react-google-login';
import FacebookLogin from 'react-facebook-login';


const responseFacebook = (response) => {
  console.log(response);
  
  var userName = response.name;
  var userPic = response.picture.data.url
  
  console.log(userName);
  console.log(userPic);
  
  //emits the messag eto the socket
     console.log('New user: ', userName);
     
     //emits message to server to join again
     Socket.emit('local:user:login', {
            'user': userName,
            'source': "facebook",
            'src': userPic,
        });
}

const responseGoogle = (response) => {
  console.log("FROM GOOGLE"+response);
  
  var userName = response.w3['ig'];
  var userPic = response.w3['Paa'];
  
  //emits the messag eto the socket
     console.log('New user: ', userName);
    Socket.emit('local:user:login', {
            'user': userName,
            'source': "google",
            'src': userPic,
        });
}



Socket.on('connect', function() {
 console.log('Connecting to the server!');
})

Socket.on('disconnect', function() {
 console.log('bye!');
 Socket.emit('user:disconnect');
})

/*
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

*/

ReactDOM.render(
  <GoogleLogin
    clientId="192807312085-9jk4t8hnf02gcb6bekmsu73h5td0reap.apps.googleusercontent.com"
    buttonText="Login with Google"
    onSuccess={responseGoogle}
    onFailure={responseGoogle}
  />,
  document.getElementById('googleButton')
);

ReactDOM.render(
  <FacebookLogin
    appId="379287432464127"
    autoLoad={true}
    fields="name,email,picture"
    //onClick={componentClicked}
    callback={responseFacebook} />,
  document.getElementById('facebookButton')
);



ReactDOM.render(
  <FullChatApp />,
  document.getElementById('chatApp')
);
