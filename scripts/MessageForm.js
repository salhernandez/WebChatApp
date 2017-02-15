import * as React from 'react';

import { Socket } from './Socket';

export class MessageForm extends React.Component {
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
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
    var msg = this.state.value
    
    //emits the messag eto the socket
     console.log('New message: ', msg);
        Socket.emit('new message', {
            'message': msg,
        });
        
        
        console.log('Sent up the message to the server!');
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Message:
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}