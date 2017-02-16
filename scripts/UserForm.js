import * as React from 'react';

import { Socket } from './Socket';

export class UserForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    //alert('A user was submitted: ' + this.state.value);
    event.preventDefault();
    var msg = this.state.value
    
    //emits the messag eto the socket
     console.log('New user: ', msg);
        Socket.emit('new user', {
            'user': msg,
        });
        
        
        console.log('Sent up the user to the server!');
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          User:
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}