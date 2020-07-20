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
                        <q-item>
                            <q-item-section class="offset-8 col">
                                <q-btn @click="editUser()" flat dense size="md" class="q-pa-none q-ml-md" color="primary" icon="save">
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
                                <q-input :rules="[val => !!val || 'Username is required']" ref="username" filled v-model="user.username" label="Username" />
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
                            <div class="col q-mt-xs">
                                <q-item>
                                    <q-item-section>
                                        <q-input :rules="[val => !!val || 'Email is required']" ref="email" filled v-model="user.email" label="Username" type="email" />
                                    </q-item-section>
                                </q-item>
                            </div>
                        </div>  
                    </q-card-section>
                </q-card-section>
            </q-card>
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
            user:{},
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
                    }
                }.bind(this)).catch(error => {
                    this.$q.loading.hide();
                    this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
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
