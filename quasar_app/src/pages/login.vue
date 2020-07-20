<template>
  <q-layout  class="bg-white q-pa-none">
    <q-header class="bg-grey-2 no-shadow">
      <q-toolbar :inverted="true" class="bg-grey-2">
        <q-toolbar-title class="toolbar-title"></q-toolbar-title>
      </q-toolbar>
    </q-header>

    <div class="row">
      <div class="offset-1 col-4" style="margin-top: 80px;">
        <div>
          <q-img src="../assets/ninja.png"/>
        </div>
      </div>
      <div class="q-mt-lg offset-3 col-3">
        <q-card class="sign-in-header">
          <q-card-section>
            <div class="text-h6 text-center bg-grey-2">Log In</div>
          </q-card-section>

         <q-card-section class="q-mt-xs bg-white">
          <!--Username/Email -->
            <q-item>
                <q-item-section>
                  <q-item-label class="text-subtitle1">Email / Username</q-item-label>
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
             <div class="offset-3 col-6">
               <a @click="openResetPasswordModal()" class="q-ml-md cursor-pointer text-primary text-subtitle2">Forgot Password ?
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
          <div class="q-ml-md q-pa-none row login-choice">
            <div class="col">
                <span>Not a member yet ?</span>
            </div>
          </div>
          <q-card-actions vertical align="center">
            <q-btn to="/signup" icon="send" color="positive" label="Sign up" class="full-width q-mb-sm"></q-btn>
          </q-card-actions>
        </q-card>
      </div>
      <div>
        
      </div>
    </div>
    <q-dialog v-model="forgot_password_modal">
            <q-card class="dialog no-shadow" style="width:500px; min-width:500px">
              <q-card-section class="q-pa-none">
                <q-tabs
                    v-model="tab"
                    class="bg-grey-2 text-primary"
                    active-color="primary"
                    indicator-color="primary"
                    align="justify"
                  >
                    <q-tab icon="mail" name="email" />
                    <q-tab icon="security" name="password" />
                  </q-tabs>

                  <q-tab-panels v-model="tab" animated class="text-white">
                    <q-tab-panel name="email">
                      <div class="text-left text-subtitle1">
                        <q-card class="q-pa-none q-ma-none no-shadow">
                          <q-card-section>
                            <q-input :rules="[val => !!val || 'Email is required']" v-model.trim="user_email" label="Enter Email Id"></q-input>
                          </q-card-section>
                          <q-card-actions align="right" class="bg-white">
                            <q-btn class="text-capitalize" color="primary" label="Validate Email"
                                  @click="validateEmail(user_email)"></q-btn>
                            <q-btn class="text-capitalize" color="grey-8" label="Cancel" @click="closeResetPasswordModal"></q-btn>
                          </q-card-actions>
                        </q-card>
                      </div>
                    </q-tab-panel>

                    <q-tab-panel name="password">
                      <q-card class="q-pa-none q-ma-none no-shadow">
                          <q-card-section>
                            <q-input filled :rules="[val => !!val || 'Password is required']" :type="is_reset_pwd ? 'password' : 'text'"  no-pass-toggle v-model.trim="reset_password" label="Enter New Password">
                              <template v-slot:append>
                              <q-icon
                                color="bg-grey-6"
                                :name="is_reset_pwd ? 'visibility_off' : 'visibility'"
                                class="cursor-pointer"
                                @click="is_reset_pwd = !is_reset_pwd"
                              />
                            </template>
                            </q-input>
                            <q-input filled :rules="[val => !!val || 'Confirm Password is required']" :type="is_confirm_reset_pwd ? 'password' : 'text'"  no-pass-toggle v-model.trim="confirm_reset_password" label="Confirm Password">
                              <template v-slot:append>
                              <q-icon
                                color="bg-grey-6"
                                :name="is_confirm_reset_pwd ? 'visibility_off' : 'visibility'"
                                class="cursor-pointer"
                                @click="is_confirm_reset_pwd = !is_confirm_reset_pwd"
                              />
                            </template>
                            </q-input>
                          </q-card-section>
                          <q-card-actions align="right" class="bg-white">
                            <q-btn class="text-capitalize" color="primary" label="Reset Password"
                                  @click="changePassword()"></q-btn>
                            <q-btn class="text-capitalize" color="grey-8" label="Cancel" @click="closeResetPasswordModal"></q-btn>
                          </q-card-actions>
                        </q-card>
                    </q-tab-panel>

                  </q-tab-panels>
                
              </q-card-section>
            </q-card>
          </q-dialog>
  </q-layout>
</template>

<script>
  import backgroundimage from '../assets/background.jpg'
  import SocialSignUp from "../components/SocialLoginSignup"
  import { QSpinnerPie } from 'quasar'
  
  export default {
    name: "login",
    components: { SocialSignUp },
    data() {
      return {
        username: '',
        password: '',
        error: '',
        msg: '',
        reset_password:'',
        confirm_reset_password:'',
        tab:'email',
        user_email:'',
        email_validate:false,
        is_pwd:true,
        is_reset_pwd:true,
        is_confirm_reset_pwd:true,
        forgot_password_modal:false,
        reset_password_modal:true
      }
    },
    methods:{
      login(){
        let post_data = {};
        post_data['username']=this.username;
        post_data['password']=this.password;
        this.$axios.post('/api/login',{post_data:post_data}).then(function (response) {
          if (response.data.ok) {
            this.$store.dispatch('setLoginSession',response.data.user_data);
            this.$router.push('/home')
          }
          else{
            this.error=response.data.error;
          }
        }.bind(this)).catch(error => {
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
        });
      },
      validateEmail(email){
          const emailRegex = RegExp(/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/);
          let self = this;
          if (emailRegex.test(email)) {
            self.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
              this.$axios.post('/api/validate_email', {'email': email}).then(function (response) {
                  if (response.data.ok) {
                    self.$q.loading.hide(); 
                    self.tab = 'password';
                    //pass
                  }else{
                      self.$q.loading.hide(); 
                      self.$q.notify({
                          message: 'No such user found',
                          type: 'warning',
                          color: 'warning',
                          textColor: 'black',
                          icon: 'warning'
                      });
                  }
              });
          }else{
              self.$q.notify({
              message: 'Please enter a valid email',
              type: 'warning',
              color: 'warning',
              textColor: 'black',
              icon: 'done'
            });
          }
      },
      changePassword() {
          let self = this;
          // Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character:
          const passwordRegex = RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$/) 
          
          if (!passwordRegex.test(this.reset_password)) {
            self.$q.notify({
                  message: 'Password must contain Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character',
                  type: 'warning',
                  color: 'warning',
                  textColor: 'black',
                  icon: 'warning'
            });
          
          }else if(this.reset_password != this.confirm_reset_password){
              self.$q.notify({
                  message: 'Password and confirm password should be the same',
                  type: 'warning',
                  color: 'warning',
                  textColor: 'black',
                  icon: 'warning'
            });
          }
          else{
              self.$q.loading.show({
                  spinner: QSpinnerPie,
                  spinnerColor: 'orange-5',
                  spinnerSize: 50
              });
              this.$axios.post('/api/change_password', {'password': this.reset_password, 'email': this.user_email}).then(function (response) {
                  if (response.data.ok) {
                      self.$q.loading.hide(); 
                      self.user_email = '';
                      self.closeResetPasswordModal();
                      self.$q.notify({
                          message: 'Password has been Reset Succesfully',
                          type: 'positive',
                          color: 'positive',
                          textColor: 'black',
                          icon: 'done'
                      });
                  }
              })
          }     
      },
      openResetPasswordModal(){
        this.user_email = '';
        this.reset_password = '';
        this.confirm_reset_password = '';
        this.forgot_password_modal = true;
      },
      closeResetPasswordModal() {
          this.user_email = '';
          this.reset_password = '';
          this.confirm_reset_password = '';
          this.forgot_password_modal = false;
      },
      clear_session() {
          this.$axios.get('/api/clear_session/').then(function (response) {
              if (response.data.ok) {
                  //pass
              }
          }.bind(this)).catch(error => {
              this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });
      },
    },
    created(){
      this.clear_session();
    }
  }
</script>

<style scoped>




</style>