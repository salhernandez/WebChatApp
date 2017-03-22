# ChatApp

## Theme
For this project I went with a technological theme given that it involves a chatbot that learns from the messages entered on the chat.
The theme was implemented by adding a robot picture to a background that lightly resembles tech.

## login page
![TheUnderground](http://res.cloudinary.com/djdt5maoi/image/upload/c_scale,w_700/v1490166905/webchat_login_screen_g9di0d.png)

## chat page
![TheUnderground](http://res.cloudinary.com/djdt5maoi/image/upload/c_scale,w_700/v1490166902/webchat_chat_screen_gqwzco.png)

## Known problems
One of the biggest problems was the inability to properly detect when a user disconnects. The app does not register properly when a client leaves.
Also, the facebook and sign in buttons will retrieve the user's previous login information which can be treated as an auto-login feature after the user signed in once. I incorporate the Dark Sky API to get weather data and the chatbot was inspired by potatoes. The user can also chat with the chatbot by typing '!! bot'.

## How to improve
* Detect the bug that does not allow the server to notice on time when a user disconnects
* show the correct user images when a user logins, the image displayed will be from the person that connected last
* Display the right amount of users that are logged in
* On Circleci sometimes the tests fails because of the nature of the tests. It will throw the error that the port is already in use.

##Improvements from handin 1
* page itself should not scroll
* !! say <something> makes the bot say <something> to the room
