# Based on lecture6-thuhe :D

Some starter code for React on Flask.

## Upgrade Node version to 6

```$ nvm install 6```

## Installing Webpack

```$ npm install -g webpack```

## Installing `npm` dependencies from `package.json`

```$ npm install```

## Compiling Javascript using Webpack

```$ webpack --watch```

(The program should not stop running. Leave it running.)

## Edit a JS file

Make a change to `scripts/Content.js`. Webpack should detect the change and 
print a bunch of stuff.

**Do not manually edit `static/script.js`!!**

## Add new JS files

Stuff that is added to `scripts/` and referenced somewhere else will 
automatically be packaged into `static/script.js`.

## Running the web server

Click on the green button on `app.py`, or open up a new terminal and type:

```$ python app.py```

## Confused?

I'll explain what all this does in a bit. For now, use it as a starter to
write some React code.