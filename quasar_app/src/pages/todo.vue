<template>
    <div :style="{'height':win_height,'width':win_width, 'background-color':'#e8f4f8'}">
        <div class="row">
            <div class="q-ml-lg q-my-md offset-4 col-3">
                <q-card flat bordered>
                    <q-card-section horizontal>
                        <q-img
                        src="../assets/todo_list.jpg"
                        />
                        <q-separator vertical />
                        <q-card-actions vertical class="justify-around q-px-md">
                        <q-btn flat @click="openAddTodoModal()" round color="primary" icon="library_add"><q-tooltip>Add note</q-tooltip></q-btn>
                        <q-btn flat @click="deleteSelectedTodos(selected_todos)" round color="red" icon="delete"><q-tooltip>Delete Multiple</q-tooltip></q-btn>
                        </q-card-actions>
                        <q-separator vertical />
                        <q-card-actions vertical class="justify-around">
                            <q-checkbox @input="selectAllTodos(all_todo_selected_check)" color="grey-8" class="q-pa-none q-mt-xs q-ml-xs" size="xs" v-model="all_todo_selected_check">
                                <q-tooltip>
                                    <span >Select All Todos</span>
                                </q-tooltip>
                            </q-checkbox>
                            <q-btn @click="show_table=!show_table" flat round class="q-mt-sm" color="primary" :icon="show_table?'sticky_note_2':'table_view'">
                                <q-tooltip>
                                    <span v-if="!show_table">Show Tabular View</span>
                                    <span v-else>Show Notes</span>
                                </q-tooltip>
                            </q-btn>
                        </q-card-actions>
                    </q-card-section>
                </q-card>
            </div>
        </div>
        <div v-if="show_table" class="row">
                <div class="col">
                    <q-card>
                        <q-card-section class="bg-white">
                            <div class="row">
                                <div class="q-mt-sm col">
                                    <span class="text-h6 text-primary">Todos</span>
                                </div>
                                <div class="col float-right">
                                <q-input filled v-model="search" class="float-right" :after="[{icon: 'search', handler () {}}]"
                                        placeholder="Search"></q-input>
                            </div>
                            </div>
                        </q-card-section>
                        <q-card-section class="q-pa-none">
                            <q-table class="bg-grey-2" :filter="search" :pagination.sync="pagination" :data="todo_list" :columns="todo_management"
                            row-key="name">
                            <q-tr slot="body" slot-scope="props" :props="props">
                                <q-td key="title" :props="props">{{props.row.title}}</q-td>
                                <q-td  key="content" :props="props"><q-btn @click="openContent(props.row)" flat dense color="primary" icon="message"><q-tooltip>View Content</q-tooltip></q-btn></q-td>
                                <q-td key="status" :props="props">
                                    <q-chip size="12px" class="text-white" v-if="props.row.status" square dense color="primary">Completed</q-chip>
                                    <q-chip size="12px" class="text-white" v-else square dense color="positive">Active</q-chip>
                                </q-td>
                                <q-td key="created_on" :props="props">{{props.row.created_on}}</q-td>
                                <q-td key="alarm_time" :props="props">{{props.row.alarm_time}}</q-td>
                                <q-td key="action">
                                <q-btn-group outline>
                                   
                                    <q-btn flat dense @click="markComplete(props.row.id)" :icon="props.row.status?'check_circle_outline':'hourglass_full'" :color="!props.row.status?'positive':'green-5'" size="sm" class="cursor-pointer float-left">
                                        <q-tooltip><span v-if="!props.row.status">Mark Complete</span><span v-else>Completed</span></q-tooltip>
                                    </q-btn>
                                    <q-btn @click="openEditTodoModal(props.row)" dense style="box-shadow: none" class="q-mx-sm" size="sm">
                                    <q-icon name="edit" color="primary"/>
                                    <q-tooltip>Edit Todo</q-tooltip>
                                    </q-btn>
                                    <q-btn v-on:click="deleteTodo(props.row.id)" dense style="box-shadow: none"
                                        size="sm">
                                    <q-icon name="delete" color="red"/>
                                    <q-tooltip>Delete</q-tooltip>
                                    </q-btn>
                                </q-btn-group>
                                </q-td>
                            </q-tr>
                            </q-table>
                        </q-card-section>
                    </q-card>
                </div>
            </div>
            <div v-if="!show_table" class="row q-pa-none">
                <div v-if="todo_list.length == 0" class="offset-4 col-3">
                    <div class="q-mx-sm quote-container">
                        <i class="pin"/>
                        <blockquote id="note_data_default" class="note">
                            <span class="text-primary">Add Something, No todos added yet... !!</span><br><br>
                                <div class="row">
                                    <div class="col">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-2">
                                        <img class="float-right q-mb-xs q-mr-sm" id="bulb_img" @click="turnOnOff()" src="https://media.geeksforgeeks.org/wp-content/uploads/OFFbulb.jpg">
                                    </div>
                                    <div class="col-10">
                                        <q-icon class="q-mb-sm q-ml-md q-mr-sm" name="format_quote"></q-icon><span class="q-mb-md">Quote of the Day</span></span> <q-icon class="q-mb-md q-ml-xs" name="format_quote"></q-icon><br><br>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <span>We can't solve problems by using the same kind of thinking we used when we created them.</span>
                                        <cite class="text-primary author">- Albert Einstein</cite>
                                    </div>
                                </div>
                        </blockquote>
                    </div>
                </div>
                <div :v-if="todo_list.length > 0" id="note_data" v-for="todo in todo_list" :key="todo.id"  class="col-2">
                    <div class="q-mx-sm q-mb-sm quote-container">
                        <i @click="openEditTodoModal(todo)" class="pin"/>
                        <blockquote class="note">
                            <q-icon v-if="!todo.status" @click="markComplete(todo.id)" :name="todo.status?'check_circle_outline':'hourglass_empty'" color="primary" size="xs" class="cursor-pointer float-left">
                                <q-tooltip>Mark Complete</q-tooltip>
                            </q-icon>
                            <q-icon size="xs" v-if="new Date() <= new Date(todo.alarm_time) && todo.alarm_time" class="cursor-pointer float-right" color="red" name="alarm">
                                <q-tooltip>{{todo.alarm_time | formatDate}}</q-tooltip>
                            </q-icon>
                            <q-checkbox style="margin-left:28%" @input="selectTodo(todo.check, todo.id)" color="grey-8" class="todo_select q-pa-none q-mb-sm" size="xs" v-model="todo.check">
                            <q-tooltip>
                                    <span>Select Todo</span>
                                </q-tooltip>
                            </q-checkbox>
                            <br>
                            <!-- <q-btn class="float-right q-mx-xs" flat dense size="sm" icon="edit" color="primary">
                                <q-tooltip>Edit Todo</q-tooltip>
                            </q-btn> -->
                            <span class="ellipsis-3-lines">{{todo.content}}</span>
                        </blockquote>
                    </div>
                </div>
        </div>
        <q-dialog persistent v-model="edit_todo_modal">
            <q-card class="todo_modal_card" style="min-width: 350px">
                <q-card-section class="bg-grey-2">
                    <span class="text-subtitle1 text-primary">Edit Todo</span>
                    <q-btn class="float-right" dense color="negative" flat icon="close" v-close-popup>
                    <q-tooltip>Close</q-tooltip>
                </q-btn>
                </q-card-section>
                <q-card-section>
                    <q-item>
                        <q-item-section>
                            <q-item-label>Title</q-item-label>
                            <q-input
                                class="q-mt-sm"
                                v-model="edit_todo.title"
                                filled
                                />
                        </q-item-section>
                    </q-item>
                    <q-item>
                        <q-item-section>
                            <q-item-label>Todo</q-item-label>
                            <q-input
                                class="q-mt-sm"
                                v-model="edit_todo.content"
                                filled
                                type="textarea"
                                />
                        </q-item-section>
                    </q-item>
                    <q-item>
                        <q-item-section>
                            <q-item-label>Do you want to reset your alarm ?
                                <q-checkbox class="q-ml-sm" v-model="alarm_check" />
                            </q-item-label>
                        </q-item-section>
                    </q-item>
                    <q-item v-if="alarm_check">
                        <q-item-section>
                            <q-item-label>Alarm Time</q-item-label>
                             <q-input filled v-model="edit_todo.alarm_time" class="q-mt-sm">
                                <template v-slot:prepend>
                                    <q-icon name="event" class="cursor-pointer">
                                    <q-popup-proxy transition-show="scale" transition-hide="scale">
                                        <q-date v-model="edit_todo.alarm_time" mask="YYYY-MM-DD HH:mm" />
                                    </q-popup-proxy>
                                    </q-icon>
                                </template>

                                <template v-slot:append>
                                    <q-icon name="access_time" class="cursor-pointer">
                                    <q-popup-proxy transition-show="scale" transition-hide="scale">
                                        <q-time v-model="edit_todo.alarm_time" mask="YYYY-MM-DD HH:mm" format24h />
                                    </q-popup-proxy>
                                    </q-icon>
                                </template>
                                </q-input>
                        </q-item-section>
                    </q-item>
                </q-card-section>
                <q-separator />
                <q-card-actions align="right">
                <q-btn v-if="!show_table" size="md" class="q-mb-xs" @click="deleteTodo(edit_todo.id)" color="red" flat dense icon="delete">
                    <q-tooltip>Delete Todo</q-tooltip>
                </q-btn>    
                <q-btn class="float-right" @click="editTodo()" flat color="primary" label="Save" >
                    <q-tooltip>Save</q-tooltip>
                </q-btn>
                </q-card-actions>
            </q-card>
            </q-dialog>

            <q-dialog persistent v-model="todo_modal">
            <q-card class="todo_modal_card" style="min-width: 350px">
                <q-card-section class="bg-grey-2">
                    <span class="text-subtitle1 text-primary">Add Todo</span>
                    <q-btn class="float-right" dense color="negative" flat icon="close" v-close-popup>
                    <q-tooltip>Close</q-tooltip>
                </q-btn>
                </q-card-section>
                <q-card-section>
                    <q-item>
                        <q-item-section>
                            <q-item-label>Title</q-item-label>
                            <q-input
                                class="q-mt-sm"
                                v-model="todo.title"
                                filled
                                />
                        </q-item-section>
                    </q-item>
                    <q-item>
                        <q-item-section>
                            <q-item-label>Todo</q-item-label>
                            <q-input
                                class="q-mt-sm"
                                v-model="todo.content"
                                filled
                                type="textarea"
                                />
                        </q-item-section>
                    </q-item>
                    <q-item>
                        <q-item-section>
                            <q-item-label>Do you want to set an alarm ?
                                <q-checkbox class="q-ml-sm" v-model="alarm_check" />
                            </q-item-label>
                        </q-item-section>
                    </q-item>
                    <q-item v-if="alarm_check">
                        <q-item-section>
                            <q-item-label>Alarm Time</q-item-label>
                             <q-input filled v-model="todo.alarm_time" class="q-mt-sm">
                                <template v-slot:prepend>
                                    <q-icon name="event" class="cursor-pointer">
                                    <q-popup-proxy transition-show="scale" transition-hide="scale">
                                        <q-date v-model="todo.alarm_time" mask="YYYY-MM-DD HH:mm" />
                                    </q-popup-proxy>
                                    </q-icon>
                                </template>

                                <template v-slot:append>
                                    <q-icon name="access_time" class="cursor-pointer">
                                    <q-popup-proxy transition-show="scale" transition-hide="scale">
                                        <q-time v-model="todo.alarm_time" mask="YYYY-MM-DD HH:mm" format24h />
                                    </q-popup-proxy>
                                    </q-icon>
                                </template>
                                </q-input>
                        </q-item-section>
                    </q-item>
                </q-card-section>
                <q-separator />
                <q-card-actions align="right">
                <q-btn @click="addTodo()" flat color="primary" label="Save" />
                </q-card-actions>
            </q-card>
            </q-dialog>

            <q-dialog persistent v-model="view_content_modal">
            <q-card class="todo_modal_card" style="min-width: 350px">
                <q-card-section class="bg-grey-2">
                    <span class="text-subtitle1 text-primary">Content</span>
                    <q-btn class="float-right" dense color="negative" flat icon="close" v-close-popup>
                    <q-tooltip>Close</q-tooltip>
                </q-btn>
                </q-card-section>
                <q-card-section>
                <div class="row">
                    <div class="col">
                        <span class="q-ml-lg text-bold text-subtitle1">Title : <q-badge v-if="view_todo_title" dense>{{ view_todo_title }}</q-badge>
                        <q-badge v-else dense>Not specified</q-badge>
                        </span>
                    </div>
                </div>
                <div class="row">
                    <div style="word-wrap: break-word" class="col q-pa-lg q-mt-sm text-primary text-subtitle1">
                        {{ view_content }}
                    </div>
                </div>
                </q-card-section>
            </q-card>
            </q-dialog>
      </div>
</template>

<script>
    import { QSpinnerPie, Dialog } from 'quasar'
    import {mapState} from 'vuex';
    import moment from 'moment';

    export default {
    name: "todo",
    data() {
        return {
            alarm_check:false,
            todo_list:[],
            todo:{},
            edit_todo: {},
            search:'',
            todo_id_list:[],
            show_table:false,
            todo_modal:false,
            edit_todo_modal:false,
            selected_todos: [],
            all_todo_selected_check:false,
            pagination: {
                rowsPerPage: 10
            },
            todo_management: [
            {
                name: 'title',
                required: true,
                label: 'Title',
                align: 'left',
                field: 'title',
                sortable: false
            },
            {
                name: 'content',
                required: true,
                label: 'Content',
                align: 'left',
                field: 'content',
                sortable: false
            }, {
                name: 'status',
                required: true,
                label: 'Status',
                align: 'left',
                field: 'status',
                sortable: false
            }, {
                name: 'created_on',
                required: true,
                label: 'Created On',
                align: 'left',
                field: 'created_on',
                sortable: false
            }, {
                name: 'alarm_time',
                required: true,
                label: 'Alarm Time',
                align: 'left',
                field: 'alarm_time',
                sortable: false
            }, 
            {
                name: 'action',
                required: true,
                label: 'Actions',
                align: 'left',
                field: 'action',
                sortable: false
            }
        ],
        view_content_modal: false,
        view_content:'',
        view_todo_title:''
        }
    },
    created() {
        this.getAllTodoList();
    },
    methods: {
        
        turnOnOff() {
            let image = document.getElementById('bulb_img'); 
            if (image.src.match("ONbulb")){
                image.src = "https://media.geeksforgeeks.org/wp-content/uploads/OFFbulb.jpg"; 
            }else{
                image.src = "https://media.geeksforgeeks.org/wp-content/uploads/ONbulb.jpg"; 
            }
        },
        openContent(todo){
            this.view_content_modal = true;
            this.view_content = todo.content;
            this.view_todo_title = todo.title;
        },
        selectTodo(check, id){
            if(check){
                this.todo_list.map(function(item){
                    if(item.id == id){
                        item.check=true;
                    }
                });
                this.selected_todos.push(id);
            }else{
                let index = this.selected_todos.indexOf(id);
                if (index > -1) {
                    this.selected_todos.splice(index, 1);

                }
            }
        },
        selectAllTodos(check){
            let self = this;
            if(check){
                this.todo_id_list = [];
                this.todo_list.map(function(item){
                    self.todo_id_list.push(item.id)
                    item.check = true;
                });
                this.selected_todos = JSON.parse(JSON.stringify(this.todo_id_list));
            }else{
                this.todo_list.map(function(item){
                    item.check = false;
                });
                this.selected_todos = [];
            }
        },
        markComplete(id){
            this.$q.dialog({
                title: 'Mark as complete',
                message: 'Are you sure you want to mark the selected todo as completed ? ',
                ok: 'Mark',
                cancel: 'Cancel'
            }).onOk(() => {
                this.todo_list = this.todo_list.map(function(item){
                    if(item.id == id){
                        item.status = true;
                    }
                    return item
                });
            });
        },
        getAllTodoList() {
            this.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
            let self = this;
            this.$axios.get('/api/get_all_todo_data').then(function (response) {
                if (response.data.ok) {
                    this.$q.loading.hide();
                    this.todo_list = response.data.todos;
                    this.todo_list.map(function(item){
                        if(item.alarm_time){
                            item.alarm_time = item.alarm_time.replace(/T|Z/g, ' ');
                        }
                    });
                }
            }.bind(this)).catch(error => {
                this.$q.loading.hide();
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
        },
        openEditTodoModal(data){
                this.edit_todo_modal=true; 
                this.edit_todo=JSON.parse(JSON.stringify(data));
                this.alarm_check=false;
        },
        openAddTodoModal(action, data){
            this.todo_modal=true; 
            this.todo={}
            this.alarm_check=false;
        },
        addTodo(){
            this.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
            this.$axios.post('/api/add_todo', {"post_data": this.todo}).then(function (response) {
                if (response.data.ok) {
                    this.$q.loading.hide();
                    this.todo_modal=false;
                    this.getAllTodoList();
                    this.$q.notify({
                        message: 'Todo Added successfully ',
                        type: 'positive',
                        color: 'positive',
                        textColor: 'black'
                    });
                }
            }.bind(this)).catch(error => {
                this.$q.loading.hide();
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
        },
        editTodo(){
            this.$q.loading.show({
                spinner: QSpinnerPie,
                spinnerColor: 'orange-5',
                spinnerSize: 50
            });
            this.$axios.put('/api/edit_todo', {"post_data": this.edit_todo}).then(function (response) {
                if (response.data.ok) {
                    this.edit_todo_modal=false; 
                    this.getAllTodoList();
                    this.$q.loading.hide();
                    this.$q.notify({
                        message: 'Todo Edited successfully ',
                        type: 'positive',
                        color: 'positive',
                        textColor: 'black'
                    });
                }
            }.bind(this)).catch(error => {
                this.$q.loading.hide();
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
        },
        deleteSelectedTodos(selected_todos){
                let self = this;
                this.$q.dialog({
                    title: 'Delete',
                    message: 'Are you sure you want to delete the selected Todos ? ',
                    ok: 'Delete',
                    cancel: 'Cancel'
                }).onOk(() => {
                    if(selected_todos.length > 0){
                        this.$q.loading.show({
                            spinner: QSpinnerPie,
                            spinnerColor: 'orange-5',
                            spinnerSize: 50
                        });
                        this.$axios.post('/api/delete_selected_todos', {"selected_todos": selected_todos}).then(function (response) {
                            if (response.data.ok) {
                                this.$q.loading.hide();
                                this.getAllTodoList();
                                this.$q.notify({
                                    message: 'Todos Deleted successfully ',
                                    type: 'positive',
                                    color: 'positive',
                                    textColor: 'black'
                                });
                            }
                        }.bind(this)).catch(error => {
                            this.$q.loading.hide();
                            this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
                        });
                    }else{
                        this.$q.notify({
                            message: 'Select Atleast One Todo to Delete',
                            type: 'warning',
                            color: 'warning',
                            textColor: 'black'
                        });
                    }
                });
            
        },
        deleteTodo(id){
            this.$q.dialog({
                title: 'Delete',
                message: 'Are you sure you want to delete this Todo ? ',
                ok: 'Delete',
                cancel: 'Cancel'
            }).onOk(() => {
                this.$q.loading.show({
                    spinner: QSpinnerPie,
                    spinnerColor: 'orange-5',
                    spinnerSize: 50
                });
                this.$axios.delete('/api/delete_todo/'+id).then(function (response) {
                    if (response.data.ok) {
                        this.edit_todo_modal=false; 
                        this.$q.loading.hide();
                        this.getAllTodoList();
                        this.$q.notify({
                            message: 'Todo Deleted successfully ',
                            type: 'positive',
                            color: 'positive',
                            textColor: 'black'
                        });
                    }
                }.bind(this)).catch(error => {
                    this.$q.loading.hide();
                    this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
                });
            });
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
    },
    filters: {
        formatDate: function(value){
            if (!value){
                return ''
            }
            let date_future = new Date(value);
            let date_now = new Date();

            let seconds = Math.floor((date_future - (date_now))/1000);
            let minutes = Math.floor(seconds/60);
            let hours = Math.floor(minutes/60);
            let days = Math.floor(hours/24);
            
            hours = hours-(days*24);
            minutes = minutes-(days*24*60)-(hours*60);
            seconds = seconds-(days*24*60*60)-(hours*60*60)-(minutes*60);
            // let result = {'hours': hours, 'mins': minutes, 'seconds': seconds, 'days': days};
            if(days <= 0){
                if(hours <= 0){
                    if(minutes <= 0){
                        if(seconds <= 0){
                            return ""
                        }else{
                            return seconds + " secs left "
                        }
                    }else{
                        return minutes + " mins left "
                    }
                }else{
                    return hours + " hrs left "
                }
            }else{
                return days + " days left "
            }
        }
    },
    computed: mapState({
        sessionData: (state) => {
            return {
                "user_id":state.session.user_id,
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

#bulb_img {
    width:40%;
    -webkit-transform: rotate(4deg);
    -moz-transform: rotate(4deg);
    -o-transform: rotate(4deg);
    -ms-transform: rotate(4deg);
    transform: rotate(4deg);
}

#note_data_default {
    background:ivory;
    height:200px;
    -webkit-transform: rotate(4deg);
    -moz-transform: rotate(4deg);
    -o-transform: rotate(4deg);
    -ms-transform: rotate(4deg);
    transform: rotate(4deg);
}

#note_data:nth-child(even) blockquote{
   background: #eae672;
  -webkit-transform: rotate(4deg);
  -moz-transform: rotate(4deg);
  -o-transform: rotate(4deg);
  -ms-transform: rotate(4deg);
  transform: rotate(4deg);
}

#note_data:nth-child(odd) blockquote{
   background: #eae672;
  -webkit-transform: rotate(-5deg);
  -moz-transform: rotate(-5deg);
  -o-transform: rotate(-5deg);
  -ms-transform: rotate(-5deg);
  transform: rotate(-5deg);
}


.quote-container {
  margin-top: 50px;
  position: relative;
}

.note {
  color: #333;
  position: relative;
  width: 90%;
  word-wrap: break-word;
  height:150px;
  min-height:150px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  font-size: 12px;
  box-shadow: 0 10px 10px 2px rgba(0,0,0,0.3);
}

.note .author {
  display: block;
  margin: 40px 0 0 0;
  text-align: right;
}

.pin {
  background-color: #aaa;
  cursor: pointer;
  display: block;
  height: 32px;
  width: 2px;
  position: absolute;
  left: 50%;
  top: -16px;
  z-index: 1;
}

.pin:after {
  background-color: #A31;
  background-image: radial-gradient(25% 25%, circle, hsla(0,0%,100%,.3), hsla(0,0%,0%,.3));
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px hsla(0,0%,0%,.1),
              inset 3px 3px 3px hsla(0,0%,100%,.2),
              inset -3px -3px 3px hsla(0,0%,0%,.2),
              23px 20px 3px hsla(0,0%,0%,.15);
  content: '';
  height: 12px;
  left: -5px;
  position: absolute;
  top: -10px;
  width: 12px;
}


.pin:before {
  background-color: hsla(0,0%,0%,0.1);
  box-shadow: 0 0 .25em hsla(0,0%,0%,.1);
  content: '';

  height: 24px;
  width: 2px;
  left: 0;
  position: absolute;
  top: 8px;

 
  transform: rotate(57.5deg);
  -moz-transform: rotate(57.5deg);
  -webkit-transform: rotate(57.5deg);
  -o-transform: rotate(57.5deg);
  -ms-transform: rotate(57.5deg);

  transform-origin: 50% 100%;
  -moz-transform-origin: 50% 100%;
  -webkit-transform-origin: 50% 100%;
  -ms-transform-origin: 50% 100%;
  -o-transform-origin: 50% 100%;
}

</style>
