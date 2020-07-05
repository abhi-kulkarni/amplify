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
        user_privilege:'',
        access_list:[],
        country_list:[],
        period_list:[],
        period:'',
        period_display: '',
        is_logged_in:false,
        country:''
      }
    },
    mutations:{
      setLoginSession(state, data) {
        // debugger
        state.session.is_logged_in=true;
        state.session.user_id = data.userId;
        state.session.user_email = data.userEmail;
        state.session.user_name = data.userName;
      },
      destroyLoginSession(state){
        state.session.is_logged_in=false;
        state.session.user_id = '';
        state.session.user_email = '';
        state.session.user_name = '';

      }
    },
    actions:{
      setLoginSession(context, data) {
      context.commit('setLoginSession', data)
      },
       destroyLoginSession(context){
        context.commit('destroyLoginSession')
      }
    }
  })

export default store
