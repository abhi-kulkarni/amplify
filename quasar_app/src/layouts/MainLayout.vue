<template>
  <div class="q-pa-none">
    <q-layout view="hHh Lpr lFf" :style="{'height': win_height}" class="shadow-2 rounded-borders">
      <q-header elevated :style="{'background-color':sessionData['appThemeColor']}">
        <q-toolbar>
          <q-btn flat @click="miniState = !miniState" round dense icon="menu_book" />
          <q-toolbar-title class="cursor-pointer"><span @click="home()">Amplify</span></q-toolbar-title>
          <q-btn dense @click="logout()" flat round icon="login">
            <q-tooltip>Logout</q-tooltip>
          </q-btn>
        </q-toolbar>
      </q-header>
  
       <q-drawer
        show-if-above
        :mini="miniState"
        @mouseover="miniState = false"
        @mouseout="miniState = true"
        :width="200"
        :breakpoint="500"
        bordered
        content-class="bg-grey-3"
      >
        <q-scroll-area :style="{'height': 'calc(100% - 150px)', 'margin-top': !miniState?'150px':'0px', 'border-right': '1px solid #ddd'}">
          <q-list padding>
            
            <q-item :to="'/profile'" :active="$route.name=='/profile'" clickable v-ripple>
              <q-item-section avatar>
                <q-avatar size="30px">
                  <img :src="profile_picture">
                </q-avatar>
              </q-item-section>
              <q-item-section>
                Profile
              </q-item-section>
            </q-item>

            <q-item :to="'/home'" :active="$route.name=='/home'" clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="home" />
              </q-item-section>
              <q-item-section>
                Home
              </q-item-section>
            </q-item>

            <q-item :to="'/todo'" :active="$route.name=='/todo'" clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="sticky_note_2" />
              </q-item-section>
              <q-item-section>
                Todo
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>

        <div id="profile_div" v-if="!miniState">
        <q-img class="q-pa-none q-ma-none absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
          <div class="q-pa-none q-ma-none absolute-bottom bg-transparent">
            <div class="q-mb-md row">
              <div class="col">
                <q-avatar size="56px">
                  <q-img :src="profile_picture"/>
                </q-avatar>
              </div>
              <div class="col q-mt-sm">
                  Last Login
              </div>
            </div>
            <div class="row text-weight-bold">{{user.first_name}} {{user.last_name}}</div>
            <div class="row">@{{user.username}}</div>
          </div>
        </q-img>
        </div>
      </q-drawer>

      <q-page-container>
        <router-view/>
        <!-- <q-page padding>
          <q-card>
            <q-card-section>
              <q-carousel
                animated
                v-model="slide"
                arrows
                navigation
                infinite
              >
                <q-carousel-slide :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
                <q-carousel-slide :name="2" img-src="https://cdn.quasar.dev/img/parallax1.jpg" />
                <q-carousel-slide :name="3" img-src="https://cdn.quasar.dev/img/parallax2.jpg" />
                <q-carousel-slide :name="4" img-src="https://cdn.quasar.dev/img/quasar.jpg" />
              </q-carousel>
            </q-card-section>
          </q-card>
        </q-page> -->
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
  import {openURL} from 'quasar';
  import {mapState} from 'vuex';
  import { QSpinnerPie } from 'quasar'

  export default {
    name: 'MyLayout',
    data() {
      return {
        user:{},
        profile_picture:'',
        left_drawer_open: false,
        left_mini_drawer_open: true,
        slide: 1,
        miniState:true
      }
    },
    created() {
      this.getUserData();
    },
    methods: {
      openMiniDrawer() {
        this.left_mini_drawer_open = true;
        this.left_drawer_open = false;
      },
      home(){
        this.$router.push('/home');
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
                    this.profile_picture = this.user.profile_picture;
                }
            }.bind(this)).catch(error => {
                this.$q.loading.hide();
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
        },
      logout(){
        this.$axios.get('/api/logout').then(function (response) {
          if (response.data.ok)
          {
            this.$store.dispatch('destroyLoginSession');
            this.$router.push('/login');
          }
        }.bind(this));
      }
    },
    computed: mapState({
      sessionData: (state) => {
        return {
          "user_id":state.session.user_id,
          "userName":state.session.user_name,
          "userEmail":state.session.user_email,
          "appThemeColor": state.session.app_theme_color
          }
      },
      win_height(){
        return this.$q.screen.height
      }
    })
  }
</script>

<style>
  #profile_div {
    pointer-events:none
  }
</style>
