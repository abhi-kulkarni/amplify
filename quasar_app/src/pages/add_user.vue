<template>
  <q-page class="q-pa-sm ">
    <h5 v-if="!this.$route.params.user_id" class="q-pa-none q-ma-none q-ml-sm q-my-sm">Add New User</h5>
    <h5 v-if="this.$route.params.user_id" class="q-pa-none q-ma-none q-ml-sm q-my-sm">Edit User</h5>
    <div class="row">
      <div class="col-lg-6">
        <q-card class="bg-white q-ml-sm">
          <q-card-title></q-card-title>
          <q-card-main>
            <q-item>
              <q-item-main>
                <q-item-tile class="text-bold" label>First Name</q-item-tile>
                <q-item-tile sublabel>
                  <q-field>
                    <q-input v-model="new_user.firstName">
                    </q-input>
                  </q-field>
                </q-item-tile>
              </q-item-main>
            </q-item>
            <q-item>
              <q-item-main>
                <q-item-tile class="text-bold" label>Last Name</q-item-tile>
                <q-item-tile sublabel>
                  <q-field>
                    <q-input v-model="new_user.lastName">
                    </q-input>
                  </q-field>
                </q-item-tile>
              </q-item-main>
            </q-item>
            <q-item>
              <q-item-main>
                <q-item-tile class="text-bold" label>Email Address</q-item-tile>
                <q-item-tile sublabel>
                  <q-field>
                    <q-input v-model="new_user.email">
                    </q-input>
                  </q-field>
                </q-item-tile>
              </q-item-main>
            </q-item>
            <q-item>
              <q-item-main>
                <q-item-tile class="text-bold" label>Privileges</q-item-tile>
                <q-item-tile sublabel>
                  <q-select
                    v-model="selected_privilege"
                    :options="privilege_options"
                  />
                </q-item-tile>
              </q-item-main>
            </q-item>
            <q-item v-if="!this.$route.params.user_id">
              <q-item-main>
                <q-item-tile class="text-bold" label>Password</q-item-tile>
                <q-item-tile sublabel>
                  <q-field>
                    <q-input type="password" no-pass-toggle v-model="new_user.password">
                      <q-icon color="grey-6" class="float-right q-mt-sm" name="lock"/>
                    </q-input>
                  </q-field>
                </q-item-tile>
              </q-item-main>
            </q-item>
            <q-item v-if="!this.$route.params.user_id">
              <q-item-main>
                <q-item-tile class="text-bold" label>Confirm Password</q-item-tile>
                <q-item-tile sublabel>
                  <q-field>
                    <q-input type="password" no-pass-toggle v-model="new_user.confirm_password">
                      <q-icon color="grey-6" class="float-right q-mt-sm" name="lock"/>
                    </q-input>
                  </q-field>
                </q-item-tile>
              </q-item-main>
            </q-item>
          </q-card-main>
          <q-card-actions align="end">
            <q-btn v-if="!this.$route.params.user_id" :disable="!new_user.firstName || !new_user.lastName || !new_user.email || !selected_privilege || !new_user.password || !new_user.confirm_password || (new_user.password!=new_user.confirm_password )" @click="addUser()" class="q-mr-md capitalize" color="secondary">Add New User</q-btn>
            <q-btn v-if="this.$route.params.user_id" :disable="!new_user.firstName || !new_user.lastName || !new_user.email || !selected_privilege" @click="editUser()" class="q-mr-md capitalize" color="secondary">Edit User</q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
  export default {
    name: "AddUser",
    data() {
      return {
        new_user: {},
        privilege_options: [
          {label: 'User', value: 'user'},
          {label: 'Administrator', value: 'admin'},
          {label: 'Manager', value: 'manager'},
        ],
        model_option: [],
        selected_privilege: 'user',
        selected_model: [],
        countries_option:[],
        selected_country:[]

      }
    },
    created() {
      if(this.$route.params.user_id){
        this.getUserData();
      }
    },
    methods: {
      addUser(){
        let post_data = {};
        post_data = this.new_user;
        post_data['privilege'] = this.selected_privilege;

        this.$axios.post('/new_user',post_data).then(function (response) {
          if (response.data.ok) {
              this.$q.notify({
              message: 'User Added successfully ',
              type: 'positive',
              color: 'positive',
              textColor: 'black'
            });
            this.$router.push('/usermanagement');
          }
        }.bind(this)).catch(error => {
            this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });
      },
      getUserData(){
        console.log(this.$route.params.user_id);
        this.$axios.get('/getUserData/'+this.$route.params.user_id).then(function (response) {
          if (response.data.ok)
          {
            this.new_user = response.data.user_data;
          }
        }.bind(this)).catch(error => {
            this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });
      },
      editUser(){
        let post_data = {};
        post_data = this.new_user;
        post_data['privilege'] = this.selected_privilege;
        post_data['id'] = this.$route.params.user_id;

        this.$axios.post('/edit_user',post_data).then(function (response) {
          if (response.data.ok) {
              this.$q.notify({
              message: 'User Edited successfully ',
              type: 'positive',
              color: 'positive',
              textColor: 'black'
            });
            this.$router.push('/usermanagement');
          }
        }.bind(this)).catch(error => {
            this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });
      }
    }
  }
</script>

<style scoped>

</style>
