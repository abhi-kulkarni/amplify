<template>
  <q-layout class="bg-white q-pa-none">
    <q-header class="bg-grey-2 no-shadow">
      <q-toolbar :inverted="true" class="bg-grey-2">
        <q-toolbar-title class="toolbar-title"></q-toolbar-title>
      </q-toolbar>
    </q-header>

    <div class="row">
      <div :class="$q.platform.is.desktop?'col-7 text-center':'text-center col-5 q-mt-xl'" style="margin-top: 80px;">
        <div class="login_logo q-mr-xl" :style="$q.platform.is.desktop?{'height':'440px', 'width':'330px'}:{'width':'200px', 'height':'440px'}">
        </div>
      </div>
      <div :class="$q.platform.is.desktop?'col-5 login-box':'q-mt-xl col-7 login-box'" :style="$q.platform.is.desktop?'':'padding-right: 30px'">
        <q-card class="sign-in-header">
          <q-card-section>
            <div class="text-h6 bg-grey-2">Sign In</div>
          </q-card-section>


         <q-card-section class="q-mt-xs bg-white">
          <!--Username/Email -->
            <q-item>
                <q-item-section>
                  <q-item-label class="text-subtitle1">E-mail / Username</q-item-label>
                    <q-input v-model.trim="username" v-on:keyup.enter="login" class="text-subtitle1">
                      <q-icon color="grey-6" class="account q-mt-md" name="account_circle"/>
                    </q-input>
                    <q-tooltip>
                      Please enter email address/username
                    </q-tooltip>
                </q-item-section>
            </q-item>

           <!--Password-->
            <q-item>
                <q-item-section>
                  <q-item-label class="text-subtitle1">Password</q-item-label>
                    <q-input v-on:keyup.enter="login" class="text-subtitle1" :type="is_pwd ? 'password' : 'text'"  no-pass-toggle v-model.trim="password">
                      <template v-slot:append>
                        <q-icon
                          color="bg-grey-6"
                          :name="is_pwd ? 'visibility_off' : 'visibility'"
                          class="cursor-pointer"
                          @click="is_pwd = !is_pwd"
                        />
                      </template>
                    </q-input>
                    <q-tooltip>
                      Enter your password
                    </q-tooltip>
                </q-item-section>
            </q-item>
           <div class="row q-mt-sm">
             <div :class="$q.platform.is.desktop?'offset-8 col-4':'offset-7 col-5'">
               <a @click="forgot_password_modal=true;user_email=''" class="cursor-pointer text-primary text-subtitle2">Forgot Password ?
               </a>
             </div>
           </div>

          </q-card-section>

          <q-item v-if="error" class="bg-red text-white q-ma-md">
            <q-item-section>{{error}}</q-item-section>
          </q-item>

          <q-card-actions vertical align="center">
            <q-btn @click="login" icon="send" color="primary" label="Sign In" class="full-width q-mb-sm"></q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
    <q-dialog v-model="forgot_password_modal">
            <q-card class="dialog no-shadow">
              <q-card-section class="bg-grey-8 text-subtitle1 text-white">Reset Password</q-card-section>
              <q-separator/>
              <q-card-section>
                <div class="text-left text-subtitle1">
                  <q-card class="q-pa-none q-ma-none no-shadow">
                    <q-card-section>
                      <q-input :rules="[val => !!val || 'Email is required']" v-model.trim="user_email" label="Enter Email Id"></q-input>
                    </q-card-section>
                    <q-card-actions align="right" class="q-mt-sm bg-white text-teal">
                      <q-btn class="text-capitalize" color="primary" label="Reset Password"
                             @click="forgotPassword(user_email)"></q-btn>
                      <q-btn class="text-capitalize" color="grey-8" label="Cancel" @click="closeResetPasswordModal"></q-btn>
                    </q-card-actions>
                  </q-card>
                </div>
              </q-card-section>
            </q-card>
          </q-dialog>
  </q-layout>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        username: '',
        password: '',
        error: '',
        msg: '',
        user_email:'',
        is_pwd:true,
        forgot_password_modal:false,
      }
    },
    methods:{
      login(){
        let post_data = {};
        post_data['username']=this.username;
        post_data['password']=this.password;
        this.$axios.post('/login',{post_data:post_data}).then(function (response) {
          if (response.data.ok) {
            this.$store.dispatch('setLoginSession',response.data.user_data);
            this.$router.push('/')
          }
          else{
            this.error=response.data.error;
          }
        }.bind(this)).catch(error => {
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
              });
      },
      forgotPassword(user_email) {
          let self = this;
          if (user_email) {
              this.$axios.post('/forgot_password/', {'user_email': user_email}).then(function (response) {
                  if (response.data.ok) {
                      self.user_email = '';
                      self.forgot_password_modal = false;
                      self.$q.notify({
                          message: 'Email has been sent to reset the user password',
                          type: 'positive',
                          color: 'positive',
                          textColor: 'black',
                          icon: 'done'
                      });
                  } else {
                      self.user_email = '';
                      self.forgot_password_modal = false;
                      self.$q.notify({
                          message: 'No Such User Exists',
                          type: 'warning',
                          color: 'warning',
                          textColor: 'black',
                          icon: 'warning'
                      });
                  }
              })
          } else {
              self.$q.notify({
                  message: 'Please Enter Your Email Id',
                  type: 'warning',
                  color: 'warning',
                  textColor: 'black',
                  icon: 'warning'
              });
          }
      },
      closeResetPasswordModal() {
          this.user_email = '';
          this.forgot_password_modal = false;
      },
      clear_session() {
          this.$axios.get('/clear_session/').then(function (response) {
              if (response.data.ok) {
                  //pass
              }
          }.bind(this)).catch(error => {
              this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });
      },
    }
  }
</script>

<style scoped>

</style>
