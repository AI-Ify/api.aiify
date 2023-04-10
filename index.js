require('dotenv').config({ path: './secrets/.env' })
const express = require('express');
const passport = require('passport');
const session = require('express-session');
const SpotifyStrategy = require('passport-spotify').Strategy;

var port = 8000;
var authCallback = '/callback';

passport.serializeUser(function (user, done) {
    done(null, user);
});

passport.deserializeUser(function (obj, done) {
    done(null, obj);
});

passport.use(
    new SpotifyStrategy(
        {
            clientID: process.env.SPOTIFY_CLIENT_ID,
            clientSecret: process.env.SPOTIFY_CLIENT_SECRET,
            callbackURL: 'http://localhost:' + port + authCallback,
            passReqToCallback: true,
        },
        function (req, accessToken, refreshToken, expires_in, profile, done) {
            process.nextTick(function () {
                return done(null, profile);
            });
        }
    )
);

const app = express();

app.use(
    session({
        secret: 'Keyboard cat',
        resave: true,
        saveUninitialized: true,
    })
)

app.use(passport.initialize())
app.use(passport.session())

app.get('/login/failure', (req, res) => {
    res.json({ failure: req.session.messages })
});

app.get('/authorize', passport.authenticate('spotify', {
    scope: ['user-top-read', 'playlist-modify-public'],
    showDialog: true,
}));

// trying to figure out how to get access_token from oauth callback !!!
app.get(authCallback, passport.authenticate('spotify', { failureRedirect: '/login/failure', failureMessage: 'Could not authenticate' }),
    function (req, res) {
        console.log(req.session._json)
        res.json({ key: 'a_new_api_key' })
    })

app.listen(port, () => console.log('server running on port ' + port))

function ensureAuthenticated(res, req, next) {
    if (req.isAuthenticated()) {
        return next();
    }
    res.redirect('/login')
}