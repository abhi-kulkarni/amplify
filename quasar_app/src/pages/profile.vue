<template>
    <div>
      <div class="row q-pa-none" :style="{'height':win_height,'width':win_width}">
        <div class="offset-3 col-6 q-pa-none">
            <q-card class="q-my-md shadow-2" flat bordered>
                <q-item class="bg-grey-2 row">
                    <div class="col">
                        <q-item>
                            <q-item-section avatar>
                                <q-avatar>
                                    <img :src="profile_picture_preview" />
                                </q-avatar>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label class="text-bold text-primary text-capitalize">{{user.first_name}} {{user.last_name}}</q-item-label>
                                <q-item-label caption>
                                    @{{user.username}}
                                </q-item-label>
                            </q-item-section>
                        </q-item>
                    </div>
                    <div class="col">
                        <q-item class="row">
                            <q-item-section class="offset-7 col">
                                <q-btn @click="openResetPasswordModal()" flat dense size="md" class="float-right q-pa-none q-ml-md" color="positive" icon="security">
                                    <q-tooltip>Reset Password</q-tooltip>
                                </q-btn>
                            </q-item-section>
                            <q-item-section class="col">
                                <q-btn @click="editUser()" flat dense size="md" class="q-pa-none" color="primary" icon="save">
                                    <q-tooltip>Save</q-tooltip>
                                </q-btn>
                            </q-item-section>
                        </q-item>
                    </div>
                </q-item>

                <q-separator />

                <q-card-section horizontal class="q-pa-none row">
                    <q-card-section class="q-pa-none col-7">
                        <q-item class="q-mt-sm">
                            <q-item-section>
                                <q-input :rules="[val => !!val || 'First Name is required']" ref="first_name" filled v-model="user.first_name" label="First Name" />
                            </q-item-section>
                        </q-item>
                        <q-item>
                            <q-item-section>
                                <q-input :rules="[val => !!val || 'Last Name is required']" ref="last_name" filled v-model="user.last_name" label="Last Name" />
                            </q-item-section>
                        </q-item>
                         <q-item>
                            <q-item-section>
                                <q-input :rules="[val => !!val || 'Email is required']" ref="email" filled v-model="user.email" label="Email" type="email" />
                            </q-item-section>
                        </q-item>
                        <q-item>
                            <q-item-section>
                                <q-select :rules="[val => !!val || 'Gender is required']" ref="gender" emit-value map-options filled :options="gender_options" v-model="selected_gender" label="Gender" />
                            </q-item-section>
                        </q-item>
                        <q-item>
                            <q-item-section>
                                <q-select :rules="[val => !!val || 'Country is required']" ref="country" filled emit-value map-options v-model="selected_country" :options="country_options" label="Country" />
                            </q-item-section>
                        </q-item>
                        <q-item>
                            <q-item-section>
                                <q-file filled bottom-slots v-model="profile_picture_model" label="Profile Picture" counter max-files="1" accept=".png, .jpg, .jpeg"
                                    class="q-my-sm"
                                    style="max-width: 300px"
                                    >
                                    <template v-slot:before>
                                    <q-icon class="q-mr-sm" color="primary" name="attach_file" />
                                    </template>
                                    <template v-slot:hint>
                                    Size
                                    </template>
                                    <template v-slot:append>
                                    <q-btn color="primary" round dense flat icon="add" @click="selectedProfilePicture()">
                                        <q-tooltip>Upload Profile Picture</q-tooltip>
                                    </q-btn>
                                    </template>
                                </q-file>
                            </q-item-section>
                        </q-item>

                    </q-card-section>

                    <q-separator vertical />

                    <q-card-section class="col">
                        <div class="row">
                            <div class="col-10">
                                <q-img class="q-ml-md" style="width: 95%" :src="profile_picture_preview">
                                    <div class="absolute-top text-center">
                                        Profile Photo
                                    </div>
                                </q-img>
                            </div>
                            <div v-if="user.profile_picture" class="col-1">
                                <q-btn @click="removeProfilePicture()" class="q-ml-md" flat icon="close" dense size="10px" color="negative">
                                    <q-tooltip>Remove Profile Picture</q-tooltip>
                                </q-btn>
                            </div>
                        </div>
                        <div class="row q-mt-sm">
                            <div class="col">
                                <q-badge color="white" text-color="black" class="q-ml-sm text-bold q-my-md">
                                    <!-- <q-icon :style="{'color': selected_app_theme_color}" size="20px" class="q-mr-sm" name="invert_colors"></q-icon> -->
                                    <q-btn class="q-mr-sm" flat dense size="sm" color="primary" icon="undo" @click="resetAppThemeColor()">
                                        <q-tooltip>Reset App Theme</q-tooltip>
                                    </q-btn>
                                    <span class="q-my-xs q-mr-sm">Select App theme 
                                        <span class="q-ml-xs" :style="{'color': selected_app_theme_color}">{{ selected_app_theme_color }}</span>
                                    </span>
                                </q-badge>
                                
                            </div>
                        </div>
                        <div class="row q-mt-sm">
                            <div class="col">
                                <q-color
                                    style="width:75%"
                                    v-model="selected_app_theme_color"
                                    no-header
                                    no-footer
                                    default-view="palette"
                                    class="q-ml-md color_picker"
                                />
                            </div>
                        </div>
                        <div class="row q-mb-sm q-mt-md">
                            <div class="col q-mt-md">
                                <q-item>
                                    <q-item-section>
                                        <q-input :rules="[val => !!val || 'Username is required']" ref="username" filled v-model="user.username" label="Username" />
                                    </q-item-section>
                                </q-item>
                            </div>
                        </div>  
                    </q-card-section>
                </q-card-section>
            </q-card>
          <q-dialog v-model="reset_password_modal">
            <q-card class="dialog no-shadow" style="width:500px; min-width:500px">
              <q-card-section class="q-pa-none">
                <q-tabs
                    v-model="tab"
                    class="bg-grey-2 text-primary"
                    active-color="primary"
                    indicator-color="grey-8"
                    align="justify"
                  >
                    <q-tab :icon="forgot_password?'mails':'lock_open'" name="password_email" />
                    <q-tab icon="security" name="reset_password" />
                  </q-tabs>

                  <q-tab-panels v-model="tab" animated class="text-white">
                    <q-tab-panel name="password_email">
                      <div class="text-left text-subtitle1">
                        <q-card class="q-pa-none q-ma-none no-shadow">
                          <q-card-section class="q-pb-none">
                            <q-input filled v-if="forgot_password" :rules="[val => !!val || 'Email is required']" v-model.trim="reset_email" label="Enter Email Id"></q-input>   
                            <q-input v-if="!forgot_password" filled :rules="[val => !!val || 'Current Password is required']" :type="is_current_pwd ? 'password' : 'text'"  no-pass-toggle v-model.trim="current_password" label="Current Password">
                              <template v-slot:append>
                              <q-icon
                                color="primary"
                                :name="is_current_pwd ? 'visibility_off' : 'visibility'"
                                class="cursor-pointer"
                                @click="is_current_pwd = !is_current_pwd"
                              />
                            </template>
                            </q-input>
                          </q-card-section>
                          <q-card-section v-if="!forgot_password" class="q-py-none">
                            <q-icon size="sm" class="q-mb-xs "  name="lock_open" color="primary"></q-icon>
                            <a @click="forgot_password=true" class="q-ml-sm cursor-pointer text-primary text-subtitle2">Forgot Password ?
                            </a>
                          </q-card-section>
                          <q-card-actions align="right" class="bg-white">
                            <q-btn v-if="!forgot_password" class="text-capitalize" color="primary" label="Validate Password"
                                  @click="validatePassword(current_password)"></q-btn>
                            <q-btn v-if="forgot_password" class="text-capitalize" color="primary" label="Validate Email"
                                  @click="validateEmail(reset_email)"></q-btn>
                            <q-btn class="text-capitalize" color="grey-8" label="Cancel" @click="closeResetPasswordModal"></q-btn>
                          </q-card-actions>
                        </q-card>
                      </div>
                    </q-tab-panel>

                    <q-tab-panel name="reset_password">
                      <q-card class="q-pa-none q-ma-none no-shadow">
                          <q-card-section>
                            <q-input filled :rules="[val => !!val || 'Password is required']" :type="is_new_pwd ? 'password' : 'text'"  no-pass-toggle v-model.trim="new_password" label="Enter New Password">
                              <template v-slot:append>
                              <q-icon
                                color="primary"
                                :name="is_new_pwd ? 'visibility_off' : 'visibility'"
                                class="cursor-pointer"
                                @click="is_new_pwd = !is_new_pwd"
                              />
                            </template>
                            </q-input>  
                            <q-input filled :rules="[val => !!val || 'Confirm Password is required']" :type="is_confirm_reset_pwd ? 'password' : 'text'"  no-pass-toggle v-model.trim="confirm_password" label="Confirm Password">
                              <template v-slot:append>
                              <q-icon
                                color="primary"
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
        </div>
      </div>
      </div>
</template>

<script>
    import { QSpinnerPie } from 'quasar'
    import {mapState} from 'vuex';
    import default_img from "../assets/profile_photo_default.png"
    import default_male_img from "../assets/img_avatar_male.png"
    import default_female_img from "../assets/img_avatar_female.png"

    export default {
    name: "profile",
    data() {
        return {
            selected_app_theme_color: '#0097A7',   
            tab:'password_email', 
            user:{},
            forgot_password:false,
            reset_email:'',
            slide: 1,
            country_options:[],
            gender_options:[{"label":"Male", value:"male"},{"label":"Female", value:"female"}],
            selected_country:"",
            selected_gender:"",
            profile_photo_file:null,
            profile_picture_preview:'',
            profile_picture_model: null,
            selected_default_img:'',
            selected_default_male_img:'',
            selected_default_female_img:'',
            reset_password_modal:false,
            current_password:'',
            new_password:'',
            confirm_password:'',
            is_current_pwd:true,
            is_new_pwd:true,
            is_confirm_reset_pwd:true
        }
    },
    created() {
        this.getUserData();
        this.getAllCountries();    
    },
    methods: {
        resetAppThemeColor(){
            this.selected_app_theme_color = '#0097A7';
        },
        openResetPasswordModal(){
            this.reset_password_modal = true;
            this.reset_email = '';
            this.forgot_password = false;
            this.current_password = '';
            this.new_password = '';
            this.confirm_password = '';
        },
        closeResetPasswordModal(){
            this.reset_password_modal = false;
        },
        validatePassword(password){
          const passwordRegex = RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$/)
          let self = this;
          if (passwordRegex.test(password)) {
            self.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
              this.$axios.post('/api/validate_password', {'password': password}).then(function (response) {
                  if (response.data.ok) {
                    self.$q.loading.hide(); 
                    self.tab = 'reset_password';
                    //pass
                  }else{
                      self.$q.loading.hide(); 
                      self.forgot_password=false;
                      self.$q.notify({
                          message: 'The password you have entered is incorrect, please enter a correct one',
                          type: 'warning',
                          color: 'warning',
                          textColor: 'black',
                          icon: 'warning'
                      });
                  }
              });
          }else{
              self.$q.notify({
              message: 'Password must contain Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character',
              type: 'warning',
              color: 'warning',
              textColor: 'black',
              icon: 'done'
            });
          }
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
                    self.tab = 'reset_password';
                    self.forgot_password=false;
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
        changePassword(){
            let self = this;
          // Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character:
          const passwordRegex = RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$/) 
          
            if(!this.current_password && !this.forgot_password){
                self.$q.notify({
                  message: 'Please enter your current password first..!',
                  type: 'warning',
                  color: 'warning',
                  textColor: 'black',
                  icon: 'warning'
                });
                self.tab = 'password_email';
              }else if(!this.reset_email && this.forgot_password){
                  self.$q.notify({
                  message: 'Please enter your email first..!',
                  type: 'warning',
                  color: 'warning',
                  textColor: 'black',
                  icon: 'warning'
                });
                self.tab = 'password_email';
              }
              else if (!passwordRegex.test(this.new_password)) {
                self.$q.notify({
                  message: 'Password must contain Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character',
                  type: 'warning',
                  color: 'warning',
                  textColor: 'black',
                  icon: 'warning'
                });
              }else if(this.new_password != this.confirm_password){
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
              this.$axios.post('/api/change_password', {'password': this.new_password}).then(function (response) {
                  if (response.data.ok) {
                      self.$q.loading.hide(); 
                      self.current_password = '';
                      self.closeResetPasswordModal();
                      self.$q.notify({
                          message: 'Password has been Reset Succesfully, Please Sign In with your new password',
                          type: 'positive',
                          color: 'positive',
                          textColor: 'black',
                          icon: 'done'
                      });
                      self.logout();
                  }
              })
          }     
        },
        getAllCountries(){
            let self = this;
            self.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
            self.$axios.get('https://restcountries.eu/rest/v2/all').then(response => {
            self.$q.loading.hide(); 
            let country_data = response.data;
            self.country_options = country_data.map(function(item){
                return {"label": item.name, "value": item.name}
            })
            }).catch(error => {
                self.$q.loading.hide();
                console.log(error)
            })
        },
        logout(){
            this.$axios.get('/api/logout').then(function (response) {
            if (response.data.ok)
            {
                this.$store.dispatch('destroyLoginSession');
                this.$router.push('/login');
            }
            }.bind(this));
        },
        getUserData() {
            this.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
            this.$axios.get('/api/get_user_data/' + this.sessionData["user_id"]).then(function (response) {
                if (response.data.ok) {
                    this.$q.loading.hide();
                    this.user= response.data.user_data;
                    this.selected_country = this.user.country;
                    this.selected_gender = this.user.gender;
                    this.profile_picture_preview = this.user.profile_picture;
                    this.selected_app_theme_color = JSON.parse(this.user.extra_data)["app_theme_color"]
                }
            }.bind(this)).catch(error => {
                this.$q.loading.hide();
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
        },
        editUser(){
            this.$refs.first_name.validate();
            this.$refs.last_name.validate();
            this.$refs.gender.validate();
            this.$refs.country.validate();
            this.$refs.email.validate();
            if (this.$refs.email.hasError || this.$refs.first_name.hasError || this.$refs.last_name.hasError || this.$refs.gender.hasError || this.$refs.country.hasError) {
                this.$q.notify({
                        message: 'Some of your fields are incorrect or empty',
                        type: 'warning',
                        color: 'warning',
                        textColor: 'black'
                    });
            }else{
                this.$q.dialog({
                    title: 'Save',
                    message: 'Are you sure you want to save the changes ? ',
                    ok: 'Save',
                    cancel: 'Cancel',
                }).onOk(() => {
                    this.$q.loading.show({
                        spinner: QSpinnerPie,
                        spinnerColor: 'orange-5',
                        spinnerSize: 50
                    });
                    this.user.gender = this.selected_gender;
                    this.user.country = this.selected_country;
                    this.user.profile_picture = this.profile_picture_preview;
                    this.user.app_theme_color = this.selected_app_theme_color;
                    this.$axios.post('/api/edit_user', {"post_data": this.user}).then(function (response) {
                        if (response.data.ok) {
                            this.profile_picture_model = null;
                            this.getUserData();
                            this.$q.loading.hide();
                            this.$q.notify({
                                message: 'User Profile Edited successfully ',
                                type: 'positive',
                                color: 'positive',
                                textColor: 'black'
                            });
                        }else{
                            this.$q.loading.hide(); 
                            this.$q.notify({
                                message: response.data.error,
                                type: 'warning',
                                color: 'warning',
                                textColor: 'black'
                            });
                        }
                    }.bind(this)).catch(error => {
                        this.$q.loading.hide();
                        this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
                    });
                });
            }
        },
        convertToDataURL(img){
            var image = new Image();
            image.src = img;
            var canvas = document.createElement("canvas");
            canvas.width = image.width;
            canvas.height = image.height;
            var ctx = canvas.getContext("2d");
            ctx.drawImage(image, 0, 0);
            var dataURL = canvas.toDataURL("image/jpg");
            let image_url = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
            return dataURL
         },
        selectedProfilePicture(){
            let self = this;
            let reader = new FileReader();
            let file = this.profile_picture_model;
            reader.onloadend = () => {
                self.profile_picture_preview = reader.result;
                self.profile_photo_file = file
            }
            reader.readAsDataURL(file)
            console.log(this.profile_picture_preview)
        },
        removeProfilePicture(){
    
            if(this.selected_gender == "male"){
                this.profile_picture_preview = default_male_img;
            }else if(this.selected_gender == "female"){
                this.profile_picture_preview = default_female_img;
            }else{
                this.profile_photo_file = null;
                this.profile_picture_preview = "";
            }
        }
    },
    watch:{
        'selected_app_theme_color':function(val){
            this.$store.dispatch('setAppThemeColor', val)
        }
    },
    computed: mapState({
        sessionData: (state) => {
            return {
                "user_id":state.session.user_id,
                "app_theme_color": state.session.app_theme_color,
                }
            },
            win_height(){
                return this.$q.screen.height;
            },
            win_width(){
                return this.$q.screen.width;
            }
        })
    }
</script>

<style scoped>

</style>
