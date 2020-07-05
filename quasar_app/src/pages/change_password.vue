<template>
  <q-page class="q-pa-sm ">
    <!--<h5 class="q-pa-none q-ma-none q-ml-sm q-my-sm">Change Password</h5>-->
    <div class="row">
      <div class="col-lg-6">
        <q-card class="bg-white q-ml-sm">
          <q-section class="text-bold label">Change Password </q-section>
          <q-separator />
          <q-card-section>
            <q-item>
              <q-item-section>
                <q-item-section class="text-bold" label>Current Password</q-item-section>
                <q-item-section sublabel>
                  <q-field>
                    <q-input type="password" no-pass-toggle v-model="current_password">
                      <q-icon color="grey-6" class="float-right q-mt-sm" name="lock"/>
                    </q-input>
                  </q-field>
                </q-item-section>
              </q-item-section>
            </q-item><q-item>
              <q-item-main>
                <q-item-section class="text-bold" label>New Password</q-item-section>
                <q-item-section sublabel>
                  <q-field>
                    <q-input type="password" no-pass-toggle v-model="new_password">
                      <q-icon color="grey-6" class="float-right q-mt-sm" name="lock"/>
                    </q-input>
                  </q-field>
                </q-item-section>
              </q-item-main>
            </q-item>
            <q-item>
              <q-item-section>
                <q-item-section class="text-bold" label>Confirm Password</q-item-section>
                <q-item-section sublabel>
                  <q-field>
                    <q-input type="password" no-pass-toggle v-model="confirm_password">
                      <q-icon color="grey-6" class="float-right q-mt-sm" name="lock"/>
                    </q-input>
                  </q-field>
                </q-item-section>
              </q-item-section>
            </q-item>
          </q-card-section>
           <div v-if="error">
              <q-item class="bg-red q-ml-md  q-mr-md q-pl-md q-pr-md text-white">
                {{error}}
                </q-item>
            </div>
          <q-card-actions align="end">

            <q-btn @click="changePassword" class="q-mr-md capitalize" color="secondary">Change Password</q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
  export default {
    name: "ChangePassword",
    data() {
      return {
        current_password:'',
        new_password:'',
        confirm_password:'',
        error:''
      }
    },
    methods:{
      changePassword(){
        let post_data = {};
        post_data['currentPassword'] = this.current_password;
        post_data['confirmPassword'] = this.confirm_password;
        post_data['newPassword'] = this.new_password;

        this.$axios.post('/changePassword', post_data).then(function (response) {
          if (response.data.msg) {
            this.$q.notify({
              message: 'Password is changed successfully. Please sign-in with new password.',
              type: 'positive',
              color: 'positive',
              textColor: 'black'
            });
            this.error = '';
          }
          else {
            this.error = response.data.error;
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
