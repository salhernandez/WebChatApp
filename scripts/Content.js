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
            'sources': [],
            'userPictures': [],
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
            
            this.setState({
                'sources': data['sources']
            });
            
            this.setState({
                'userPictures': data['userPictures']
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
        
        let theSources = this.state.sources.map(
            (n, index) => <p key={index}>{n}</p>
        );
        
        let theUserPictures = this.state.userPictures.map(
            (n, index) => <img src={n} alt="boohoo" key={index}/>
        );
        
        return (
            <div>
                <h1>Messages</h1>
                {theMessages}
                
                <h1>Users</h1>
                {theUsers}
                
                <h1>Sources</h1>
                {theSources}
                
                <h1>Images</h1>
                {theUserPictures}
                
                {/*<Button />*/}
            </div>
        );
    }
}