import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';


export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'numbers': [],
            'users': [],
            'messages': [],
        };
    }

    componentDidMount() {
        Socket.on('all numbers', (data) => {
            this.setState({
                'numbers': data['numbers']
            });
        })
        
        //receive socket message
        Socket.on('all messages', (data) => {
            this.setState({
                'messages': data['messages']
            });
            console.log("got stuff from messages");
        })
        
        //receive socket message
        Socket.on('all users', (data) => {
            this.setState({
                'users': data['users']
            });
            console.log("got stuff from users");
        })
    }

    render() {
        let theMessages = this.state.messages.map(
            (n, index) => <p key={index}>{n}</p>
        );
        
        let theUsers = this.state.users.map(
            (n, index) => <p key={index}>{n}</p>
        );
        
        return (
            <div>
                <h1>Messages</h1>
                {theMessages}
                
                <h1>Users</h1>
                {theUsers}
                
                {/*<Button />*/}
            </div>
        );
    }
}