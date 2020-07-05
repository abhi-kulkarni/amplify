<template>
  <q-page class="q-pa-sm">
        <q-card class="no-shadow">
          <q-card-title>
            User Management
            <div class="float-right">
              <q-input v-model="search" class="float-right" :after="[{icon: 'search', handler () {}}]"
                       placeholder="Search"></q-input>
              <q-btn @click="addUser" class="bg-grey-3 q-pa-sm q-mr-sm float-right text-blue" icon="add" flat></q-btn>
            </div>
          </q-card-title>
          <q-card-main>
            <q-table class="bg-white" :pagination.sync="pagination" :filter="search" :data="users" :columns="column_user_management"
                     row-key="name">
              <q-tr slot="body" slot-scope="props" :props="props">
                <q-td key="name" :props="props">{{props.row.firstName}} {{props.row.lastName}}</q-td>
                <q-td key="email" :props="props">{{props.row.email}}</q-td>
                <q-td key="role" :props="props">
                  <q-chip square dense color="light-blue-13">{{props.row.role}}</q-chip>
                </q-td>
                <q-td key="created_on" :props="props">{{props.row.created_on}}</q-td>
                <q-td key="action">
                  <q-btn-group outline>
                    <q-btn dense v-bind:to="'/edit_user/'+props.row.id+'/'" style="box-shadow: none" class="q-mr-sm"
                           size="sm">
                      <q-icon name="edit" color="light-blue-13"/>
                      <q-tooltip>Edit</q-tooltip>
                    </q-btn>
                    <q-btn v-on:click="" dense style="box-shadow: none" class="q-mr-sm" size="sm">
                      <q-icon name="lock" color="light-blue-13"/>
                      <q-tooltip>Reset Password</q-tooltip>
                    </q-btn>
                    <q-btn v-on:click="deleteUser(props.row.id)" dense style="box-shadow: none" class="q-mr-sm"
                           size="sm">
                      <q-icon name="delete" color="light-blue-13"/>
                      <q-tooltip>Delete</q-tooltip>
                    </q-btn>
                  </q-btn-group>
                </q-td>

              </q-tr>
            </q-table>
          </q-card-main>
        </q-card>
  </q-page>
</template>

<script>
  import { QSpinnerPie } from 'quasar'


  export default {
    name: "QuotaUserManagement",
    data() {
      return {
        selected_tab: 'user_management',
        pagination: {
          rowsPerPage: 5 // current rows per page being displayed
        },
        search: '',
        column_user_management: [
          {
            name: 'name',
            required: true,
            label: 'Name',
            align: 'left',
            field: 'name',
            sortable: false
          },
          {
            name: 'email',
            required: true,
            label: 'Email Id',
            align: 'left',
            field: 'email',
            sortable: false
          }, {
            name: 'role',
            required: true,
            label: 'Role',
            align: 'left',
            field: 'role',
            sortable: false
          }, {
            name: 'created_on',
            required: true,
            label: 'Created On',
            align: 'left',
            field: 'created_on',
            sortable: false
          }, {
            name: 'action',
            required: true,
            label: 'Actions',
            align: 'left',
            field: 'action',
            sortable: false
          }
        ],
        users: []
      }
    },
    created() {
      this.loadUserData();
    },
    methods: {
      loadUserData() {
        this.$q.loading.show({
                              spinner: QSpinnerPie,
                              spinnerColor: 'orange-5',
                              spinnerSize: 50});

        let self = this;

        self.$axios.get('/userManagementData').then(function (response) {
          if (response.data.ok) {

            self.users = response.data.users;

            this.$q.loading.hide();
          }
          else {
            this.$q.notify({message: response.data['error'], color: 'negative', textColor: 'black', icon: 'warning'});
            this.$q.loading.hide();
          }
        }.bind(this)).catch(error => {
            this.$q.loading.hide();
            this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });
      },
      addUser() {
        this.$router.push('/add_user');
      },
      deleteUser(id) {
        this.$q.dialog({
          title: 'Delete',
          message: 'Are you sure you want to delete this User ? ',
          ok: 'Delete',
          cancel: 'Cancel'
        }).then(() => {
          this.$axios.delete('/delete_user/' + id).then(function (response) {
            if (response.data.ok) {
              this.$q.notify({
                message: 'User Deleted successfully ',
                type: 'positive',
                color: 'positive',
                textColor: 'black'
              });
              this.loadUserData();
            }
          }.bind(this)).catch(error => {
            this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
          });

        })
      }
    }
  }
</script>

<style scoped>

</style>
