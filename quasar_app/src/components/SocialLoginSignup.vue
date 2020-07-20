<template>
<div class="row">
    <div class="col signup-buttons">
        <div id="fb-root"></div>
        <a href="#" class="google-signup" @click.prevent="loginWithGoogle">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><title>Google</title><g fill="none" fill-rule="evenodd"><path fill="#4285F4" d="M17.64 9.2045c0-.6381-.0573-1.2518-.1636-1.8409H9v3.4814h4.8436c-.2086 1.125-.8427 2.0782-1.7959 2.7164v2.2581h2.9087c1.7018-1.5668 2.6836-3.874 2.6836-6.615z"></path><path fill="#34A853" d="M9 18c2.43 0 4.4673-.806 5.9564-2.1805l-2.9087-2.2581c-.8059.54-1.8368.859-3.0477.859-2.344 0-4.3282-1.5831-5.036-3.7104H.9574v2.3318C2.4382 15.9832 5.4818 18 9 18z"></path><path fill="#FBBC05" d="M3.964 10.71c-.18-.54-.2822-1.1168-.2822-1.71s.1023-1.17.2823-1.71V4.9582H.9573A8.9965 8.9965 0 0 0 0 9c0 1.4523.3477 2.8268.9573 4.0418L3.964 10.71z"></path><path fill="#EA4335" d="M9 3.5795c1.3214 0 2.5077.4541 3.4405 1.346l2.5813-2.5814C13.4632.8918 11.426 0 9 0 5.4818 0 2.4382 2.0168.9573 4.9582L3.964 7.29C4.6718 5.1627 6.6559 3.5795 9 3.5795z"></path></g></svg>
            <span>Signup with Google</span>
        </a>
        <a href="#" class="facebook-signup" @click.prevent="loginWithFacebook">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>
            <span class="text-white">Signup with Facebook</span>
        </a>
    </div>
</div>
</template>

<script>
import { initFbsdk } from '../auth_config/fbOauth.js'
import GoogleAuth from '../auth_config/googleOauth.js'
import Vue from 'vue'

const gauthOption = {
    clientId: process.env.GOOGLE_CLIENT_ID,
    scope: 'profile email',
    prompt: 'select_account'
}

Vue.use(GoogleAuth, gauthOption);

export default {
  name: 'social_login_signup',
  mounted () {
    let element = document.getElementById('fb-root');
    if(element){
      initFbsdk();
    } 
  },
  methods: {
    loginWithGoogle () {
      let random_str = this.randomId(5);
      let self = this;
      this.$gAuth
        .signIn()
        .then(GoogleUser => {
          console.log('GoogleUser', GoogleUser)
          let googleData = GoogleUser['Rt'];
          let user = {};
          user['email'] = googleData['Bu']
          user['first_name'] = googleData['Bd'].split(' ')[0].charAt(0).toUpperCase() + googleData['Bd'].split(' ')[0].slice(1);
          user['last_name'] = googleData['Bd'].split(' ')[1].charAt(0).toUpperCase() + googleData['Bd'].split(' ')[1].slice(1)
          user['profile_picture'] = googleData['dL']
          user['username'] = (user['first_name'] + user['last_name']).toLowerCase() + random_str
          user['sso'] = true;
          self.signup(user);
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    loginWithFacebook () {
      let self = this;
      let random_str = this.randomId(5);
      window.FB.login(res => {
        FB.api('/me?fields=picture,email,name,gender,location{location}', function (res) {
           let user = {
                email:res.email,
                first_name:res.name.split(" ")[0].charAt(0).toUpperCase() + res.name.split(" ")[0].slice(1),
                last_name:res.name.split(" ")[1].charAt(0).toUpperCase() + res.name.split(" ")[1].slice(1),
                username:res.name.split(" ").join("").toLowerCase()+random_str,
                gender:res.gender,
                profile_picture_url:res.picture.data.url,
                country:res.location.location.country,
                sso:true
            }
            self.signup(user);
        });
      })
    },
    signup(user){
      this.$emit('user', user)
    },
    randomId(length) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
           result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
     }
  }
}
</script>

