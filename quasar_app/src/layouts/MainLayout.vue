<template>
  <q-layout view="hHh Lpr lFf">
    <q-layout-header>
      <q-toolbar
        :inverted="$q.theme === 'ios'"
        style="color: #dd4b39"
      >
<!--        <img class="float-left" src="../assets/company-logo.jpg" style="height:25px;"/>-->
        <q-btn
          flat
          dense
          round
          @click="left_drawer_open = !left_drawer_open;left_mini_drawer_open = !left_mini_drawer_open;"
          aria-label="Menu"
        >
          <q-icon name="menu"/>
        </q-btn>

        <!--<q-btn-->
        <!--v-if="left_mini_drawer_open"-->
        <!--flat-->
        <!--dense-->
        <!--round-->
        <!--@click="left_mini_drawer_open = !left_mini_drawer_open;left_drawer_open = !left_drawer_open"-->
        <!--aria-label="Menu"-->
        <!--&gt;-->
        <!--<q-icon name="menu" />-->
        <!--</q-btn>-->

        <q-toolbar-title>
          <div class="float-right ">
            <q-btn color="primary text-white capitalize" flat>
              <q-icon name="account_circle" class="q-pr-sm"></q-icon>
              {{sessionData['userName']}}
              <q-popover style="width: 280px;">
                <q-card>
                  <q-card-title class="bg-primary text-white">
                    <div class="text-center"><img class="avatar " src="../assets/icon-user-default.png"
                                                  style="width: 90px;height: 90px;"/>
                      <div class="q-caption q-pb-none q-mb-none">{{sessionData['userName']}}</div>
                      <div class="q-caption q-pt-none q-mt-none">{{ sessionData['userEmail'] }}</div>
                    </div>

                  </q-card-title>
                  <q-card-main class="bg-grey-2">
                    <q-btn v-bind:to="'/changePassword'" class="q-mt-sm no-border text-grey-8" size="sm">
                      Change Password
                    </q-btn>
                    <q-btn @click="logout" class="q-mt-sm float-right no-border text-grey-8" size="sm">
                      Sign out
                    </q-btn>
                  </q-card-main>
                </q-card>
              </q-popover>
            </q-btn>
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-layout-header>

    <q-layout-drawer
      v-model="left_drawer_open"
      :content-class="$q.theme === 'mat' ? 'bg-grey-2 no-shadow' : null"
      :overlay="true"
      :content-style="{zIndex: '4000'}"
    >
      <q-list
        no-border
        link
        inset-delimiter
      >
        <q-item @click.native="openMiniDrawer" :class="$route.name=='/'?'active':''" to="/" active-class="q-item-no-link-highlighting">
          <q-item-side icon="dashboard"/>
          <q-item-main label="Dashboard"/>
        </q-item>

        <q-item :class="$route.name=='usermanagement'?'active':''" to="/usermanagement" @click.native="openMiniDrawer">
          <q-item-side icon="group"/>
          <q-item-main label="User Management"/>
        </q-item>

      </q-list>
    </q-layout-drawer>
    <q-layout-drawer
      v-model="left_mini_drawer_open"
      :mini="true"
      :overlay="false"
      :content-class="$q.theme === 'mat' ? 'bg-grey-2' : null"
    >
      <q-list
        no-border
        inset-delimiter
      >
        <q-item :class="$route.name=='/'?'active':''" to="/" active-class="q-item-no-link-highlighting">
          <q-item-side icon="dashboard">
          </q-item-side>
          <q-tooltip color="bg-grey-2" anchor="center right" self="center left" :offset="[5, 5]">Dashboard</q-tooltip>
        </q-item>

        <q-item :class="$route.name=='usermanagement'?'active':''" to="/usermanagement">
          <q-item-side icon="group">
          </q-item-side>
          <q-tooltip anchor="center right" self="center left" :offset="[5, 5]">User Management</q-tooltip>
        </q-item>

      </q-list>
    </q-layout-drawer>


    <q-page-container class="bg-grey-2" style="padding-left: 60px;">
      <router-view/>
    </q-page-container>

    <q-layout-footer v-model="footer_modal" class="no-shadow" style="left: 0">
      <q-toolbar
        inverted
        class="bg-grey-2"
      >
        <q-toolbar-title>
          <div class="float-left text-black caption">
            <span class="caption" style="font-size: small"><strong>Copyright &copy; 2019
              <a href="#" style="text-decoration: none">Company Name</a>.</strong> All rights reserved.</span>
          </div>
          <div class="float-right">
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-layout-footer>
  </q-layout>
</template>

<script>
  import {openURL} from 'quasar';
  import {mapState} from 'vuex';


  export default {
    name: 'MyLayout',
    data() {
      return {
        left_drawer_open: false,
        left_mini_drawer_open: true,
        footer_modal: true,
      }
    },
    created() {
    },
    methods: {
      openMiniDrawer() {
        this.left_mini_drawer_open = true;
        this.left_drawer_open = false;
      },
      logout(){
        this.$axios.get('/logout').then(function (response) {
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
        return {"userName":state.session.user_name,"userEmail":state.session.user_email}
      }
    })
  }
</script>

<style>
</style>
