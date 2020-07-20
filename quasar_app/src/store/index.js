import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    // modules: {
    //   example
    // },
    state:{
      session:{
        user_id:'',
        user_email:'',
        user_name:'',
        first_name:'',
        last_name:'',
        is_logged_in:false,
        app_theme_color:'#0097A7',
        last_login:''
      }
    },
    mutations:{
      setLoginSession(state, data) {
        // debugger
        state.session.is_logged_in=true;
        state.session.user_id = data.userId;
        state.session.user_email = data.userEmail;
        state.session.user_name = data.userName;
        state.session.first_name = data.firstName;
        state.session.last_name = data.lastName;
        state.session.app_theme_color = data.appThemeColor;
        state.session.last_login = data.last_login
      },
      setAppThemeColor(state, data) {
        state.session.app_theme_color = data;
        },
      destroyLoginSession(state){
        state.session.is_logged_in=false;
        state.session.user_id = '';
        state.session.user_email = '';
        state.session.user_name = '';
        state.session.first_name = '';
        state.session.last_name = '';
        state.session.app_theme_color = '#0097A7';
        state.session.last_login = '';
      }
    },
    actions:{
      setLoginSession(context, data) {
      context.commit('setLoginSession', data)
      },
       destroyLoginSession(context){
        context.commit('destroyLoginSession')
      },
      setAppThemeColor(context, data){
        context.commit('setAppThemeColor', data)
      }
    }
  })

export default store
