<template>
<q-layout class="bg-white q-pa-none">
    <q-header class="bg-grey-2 no-shadow">
    <q-toolbar :inverted="true" class="bg-grey-2">
        <q-toolbar-title class="toolbar-title"></q-toolbar-title>
    </q-toolbar>
    </q-header>
    <div class="row">
        <div class="q-mt-lg offset-3 col-3">
            <q-card style="width:600px;min-width:600px" class="sign-up-header">
            <q-card-section class="q-pa-none">
                <div class="row text-h6 text-center bg-grey-2">
                    <q-img style="border: 1px solid #F5F5F5;border-radius:50%" class="text-center offset-5 col-2" :src="profile_picture_preview" />
                    <div v-if="!default_img && profile_picture_preview" class="col-1">
                        <q-btn class="q-mt-xs float-left" @click="removeProfilePicture()" round icon="close" dense size="6px" color="red">
                            <q-tooltip>Remove Profile Picture</q-tooltip>
                        </q-btn>
                    </div>
                </div>
            </q-card-section>

            <q-card-section class="q-mt-xs bg-white">
                <div class="row">
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>First Name</q-item-label>
                                <q-input :rules="[val => !!val || 'First Name is required']" ref="first_name" v-model="user.first_name">
                                </q-input>
                        </q-item-section>
                        </q-item>
                    </div>
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Last Name</q-item-label>
                                <q-input :rules="[val => !!val || 'Last Name is required']" ref="last_name" v-model="user.last_name">
                                </q-input>
                        </q-item-section>
                        </q-item>
                    </div>
                </div>          
                <div class="row">
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Email</q-item-label>
                                <q-input :rules="[val => !!val || 'Email is required']" ref="email" v-model="user.email">
                                </q-input>
                        </q-item-section>
                        </q-item>
                    </div>
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Username</q-item-label>
                                <q-input :rules="[val => !!val || 'Username is required']" ref="username" v-model="user.username">
                                </q-input>
                        </q-item-section>
                        </q-item>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Gender</q-item-label>
                            <q-select
                                :rules="[val => !!val || 'Gender is required']" ref="gender"
                                v-model="selected_gender"
                                :options="gender_options"
                                map-options
                                emit-value
                            />
                        </q-item-section>
                        </q-item>
                    </div>
                    <div class="col-6">
                      <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Country</q-item-label>
                            <q-select
                                :rules="[val => !!val || 'Country is required']"
                                ref="country"
                                map-options
                                emit-value
                                v-model="selected_country"
                                :options="country_options"
                            />
                        </q-item-section>
                        </q-item>  
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Confirm Password</q-item-label>
                                <q-input :type="is_confirm_pwd ? 'password' : 'text'" no-pass-toggle v-model="user.confirm_password">
                                <template v-slot:append>
                                    <q-icon
                                    color="bg-grey-6"
                                    :name="is_confirm_pwd ? 'visibility_off' : 'visibility'"
                                    class="cursor-pointer"
                                    @click="is_confirm_pwd = !is_confirm_pwd"
                                    />
                                </template>
                                </q-input>
                        </q-item-section>
                        </q-item>
                    </div>
                    <div class="col-6">
                        <q-item>
                        <q-item-section>
                            <q-item-label class="text-bold" label>Password</q-item-label>
                                <q-input :type="is_pwd ? 'password' : 'text'" no-pass-toggle v-model="user.password">
                                <template v-slot:append>
                                    <q-icon
                                    color="bg-grey-6"
                                    :name="is_pwd ? 'visibility_off' : 'visibility'"
                                    class="cursor-pointer"
                                    @click="is_pwd = !is_pwd"
                                    />
                                </template>
                                </q-input>
                        </q-item-section>
                        </q-item>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <q-item>
                            <q-item-section>
                                <q-file filled bottom-slots v-model="profile_picture_model" label="Profile Picture" counter max-files="1" accept=".png, .jpg, .jpeg"
                                    class="q-my-sm"
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
                    </div>
                </div>
            </q-card-section>
            <q-card-section>
                <div class="row">
                    <div class="col">
                        <q-btn-group spread>
                            <q-btn @click="validateUser()" size="16px" color="positive">Sign Up</q-btn>
                        </q-btn-group>
                    </div>
                </div>
                <div class="q-mt-sm row login-choice">
                    <div class="offset-4 col-4">
                        <span>OR</span>
                    </div>
                </div>
                <SocialSignUp @user="getSocialLoggedInUser" />
            </q-card-section>
        </q-card>
    </div>
    <div class="offset-4 col-2" style="margin-top:70px">
        <q-btn class="q-mr-md float-right" dense color="primary" icon="keyboard_backspace" to="/login">
        <q-tooltip>Back to Login</q-tooltip>
        </q-btn>
    </div>
</div>
</q-layout>
</template>

<script>
    import { QSpinnerPie } from 'quasar'
    import {mapState} from 'vuex';
    import default_img from "../assets/profile_photo_default.png"
    import default_male_img from "../assets/img_avatar_male.png"
    import default_female_img from "../assets/img_avatar_female.png"
    import SocialSignUp from "../components/SocialLoginSignup"

  export default {
    name: "signup",
    components: { SocialSignUp },
    data() {
      return {
        user: {},        
        sso_user:{},
        is_pwd:true,
        is_confirm_pwd:true,
        country_options:[],
        gender_options:[{"label":"Male", value:"male"},{"label":"Female", value:"female"}],
        selected_country:"",
        selected_gender:"",
        profile_photo_file:null,
        profile_picture_preview:'',
        profile_picture_model: null,
        default_img:true,
      }
    },
    created() {
        this.getAllCountries();
        this.profile_picture_preview = default_img;
    },
    methods: {

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
        selectedProfilePicture(){
            let self = this;
            let reader = new FileReader();
            let file = this.profile_picture_model;
            reader.onloadend = () => {
                self.profile_picture_preview = reader.result;
                self.default_img = false,
                self.profile_photo_file = file
            }
            reader.readAsDataURL(file)
        },
        removeProfilePicture(){
            this.default_img = true;
            this.profile_photo_file = null;
            this.profile_picture_model = '';
            if(this.selected_gender == "male"){
                this.profile_picture_preview = default_male_img;
            }else if(this.selected_gender == "female"){
                this.profile_picture_preview = default_female_img;
            }else{
                this.profile_picture_preview = default_img;
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
         getSocialLoggedInUser(user){
            this.sso_user = user;
            this.addUser(this.sso_user)
         },
         validateUser(){
            const emailRegex = RegExp(/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/);

            // Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character:
    
            const passwordRegex = RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,10}$/) 
            if (this.$refs.username.hasError || this.$refs.first_name.hasError || this.$refs.last_name.hasError || this.$refs.gender.hasError || this.$refs.country.hasError) {
                this.$q.notify({
                        message: 'Some of your fields are incorrect or empty',
                        type: 'warning',
                        color: 'warning',
                        textColor: 'black'
                });
            }else if(!emailRegex.test(this.user.email)){
                this.$q.notify({
                    message: 'Email is incorrect',
                    type: 'warning',
                    color: 'warning',
                    textColor: 'black'
                });  
            }else if(!passwordRegex.test(this.user.password)){
                this.$q.notify({
                    message: 'Password must contain Minimum six and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character',
                    color: 'warning',
                    textColor: 'black'
                }); 
            }else if(this.user.password != this.user.confirm_password){
                this.$q.notify({
                    message: 'Password and confirm password should be the same',
                    type: 'warning',
                    color: 'warning',
                    textColor: 'black'
                });
            }else{
                this.addUser(this.user)
            }
        },
        addUser(user){
            let post_data = {};
            post_data = user;
            post_data['country'] = this.selected_country;
            post_data['gender'] = this.selected_gender;
            post_data['profile_picture'] = this.profile_picture_preview;
            this.$axios.post('/api/add_user', {'post_data': post_data}).then(function (response) {
            if (response.data.ok) {
                this.$q.notify({
                    message: 'User Added successfully ',
                    type: 'positive',
                    color: 'positive',
                    textColor: 'black'
                });
                this.$router.push('/login');
            }
            }.bind(this)).catch(error => {
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
        }
    //   getUserData(){
    //     console.log(this.$route.params.user_id);
    //     this.$axios.get('/getUserData/'+this.$route.params.user_id).then(function (response) {
    //       if (response.data.ok)
    //       {
    //         this.new_user = response.data.user_data;
    //       }
    //     }.bind(this)).catch(error => {
    //         this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
    //       });
    //   },
    //   editUser(){
    //     let post_data = {};
    //     post_data = this.new_user;
    //     post_data['privilege'] = this.selected_privilege;
    //     post_data['id'] = this.$route.params.user_id;

    //     this.$axios.post('/edit_user',post_data).then(function (response) {
    //       if (response.data.ok) {
    //           this.$q.notify({
    //           message: 'User Edited successfully ',
    //           type: 'positive',
    //           color: 'positive',
    //           textColor: 'black'
    //         });
    //         this.$router.push('/usermanagement');
    //       }
    //     }.bind(this)).catch(error => {
    //         this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
    //       });
    //   }
    },
    watch:{
        'selected_gender': function(val){
            if(val == "male"){
                this.profile_picture_preview = default_male_img;
            }else if(val == "female"){
                this.profile_picture_preview = default_female_img;
            }
        }
    },
    computed: mapState({
        sessionData: (state) => {
            //pass
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
