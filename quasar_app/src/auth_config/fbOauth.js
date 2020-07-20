export const initFbsdk = () => {
    return new Promise(resolve => {
        window.fbAsyncInit = function() {
          FB.init({
            appId      : process.env.FACEBOOK_APP_ID,
            cookie     : true,
            xfbml      : true,
            version    : 'v7.0'
          });
          FB.AppEvents.logPageView();   
        };
        (function(d, s, id){
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) {return;}
          js = d.createElement(s); js.id = id;
          js.src = "https://connect.facebook.net/en_US/all.js";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
  })
}