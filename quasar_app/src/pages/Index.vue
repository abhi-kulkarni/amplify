<template>
  <q-page class="q-pa-sm">
    <h5 class="q-pa-none q-ma-none q-my-sm">Home</h5>
      <q-card class="q-pa-none q-ma-none bg-white">
        <q-card-section class="q-pa-sm q-ma-none">
          <div class="row">
            <div class="q-mt-sm col-2">
              <q-btn @click="getCovidGraphData('India')" color="primary" icon="refresh">
                  <q-tooltip>Refresh Data</q-tooltip>
              </q-btn>
            </div>
            <div class="q-mt-sm offset-3 col-3">
                <q-btn @click="getCovidGraphData('India')" color="red" icon="trending_up">
                  <q-tooltip>Show COVID Charts</q-tooltip>
                </q-btn>
                  <span class="q-ml-md text-h6 text-red">COVID-19 Information</span>
            </div>
            <div class="offset-1 col-3">
              <q-select
                filled
                map-options
                emit-value
                @input="getCovidGraphData(selected_state)"
                v-model="selected_state"
                :options="states"
                label="Select State"
            /> 
            </div>        
          </div>
          
        </q-card-section>
        <q-separator />
        <q-card-section>
          <div class="q-mt-md row">
            <div class="q-ml-lg col-6">
              <div style="wdith:500px; height:500px" id="covid_state_wise_bar_chart">

              </div>
            </div>
            <div class="q-mt-sm q-ml-xl col-5">
              <div class="q-mt-sm q-ml-md" style="wdith:500px; height:500px" id="covid_state_wise_pie_chart">

              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-page>
</template>

<style>
</style>

<script>
import echarts from 'echarts'
import {mapState} from 'vuex';
import { QSpinnerPie } from 'quasar'

export default {
  name: 'home',
  mounted(){
    this.getUserData();
    this.getCovidGraphData('India');
  },
  data(){
    return {
      user:{},
      covid_data:[],
      states: [],
      active_cases:[],
      state_data:[],
      selected_state:'',
      state_district_dict:{},
      chart_data:{},
    }
  },
  methods: {
    async getCovidData(){
      let self = this;
      return new Promise(function(resolve, reject) {
        self.$axios.get('https://api.covid19india.org/state_district_wise.json').then(function (response) {
            self.covid_data = response.data;
            delete self.covid_data['State Unassigned']
            self.state_data = Object.keys(self.covid_data);
            let state_data = Object.keys(self.covid_data);
            self.states = state_data.map(function(item){
              return {"label": item, "value": item}
            });
          Object.values(state_data).map(function(state_item){
            let active_case_count = 0;
            let district_data = self.covid_data[state_item]['districtData'];
            self.state_district_dict[state_item] = district_data
            let state_district = self.covid_data[state_item];
            Object.keys(district_data).map(function(d_item){
              active_case_count += district_data[d_item]['active']
            })
            self.active_cases.push(active_case_count)
          })
          Object.keys(self.state_district_dict).map(function(item){
            let temp_dict = {};
            let d_data = self.state_district_dict[item];
            let d_data_keys = Object.keys(d_data);
            Object.values(d_data).map(function(d_item, index){
              temp_dict[d_data_keys[index]] = d_item['active']
            })
            self.chart_data[item] = temp_dict
            resolve(self.covid_data)
          });   
         }.bind(this)).catch(error => {
              self.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
              return reject(error)
          });
      });
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
                }
            }.bind(this)).catch(error => {
                this.$q.loading.hide();
                this.$q.notify({message: 'Error Occurred', color: 'negative', textColor: 'black', icon: 'warning'});
            });
    },
    async getCovidGraphData(selected){
      const result = await this.getCovidData();
      this.$nextTick(function () {
        var selected_chart_data = {};
        var chart_data = [];
        let self = this;
        let x_data = [];
        let y_data = [];
        if(selected == 'India'){
            this.selected_state = '';
            x_data = this.state_data;
            y_data = this.active_cases;
            this.state_data.map(function(item, index){
                let temp = {};
                temp['name'] = item
                temp['value'] = self.active_cases[index]
                chart_data.push(temp)
            })
        }else{
            selected_chart_data = this.chart_data[selected];
            x_data = Object.keys(selected_chart_data);
            y_data = Object.values(selected_chart_data);
            x_data.map(function(item, index){
                let temp = {};
                temp['name'] = item
                temp['value'] = y_data[index]
                chart_data.push(temp)
            })
        }
        let covid_state_wise_chart_bar_dom = document.getElementById('covid_state_wise_bar_chart');
        let covid_state_wise_chart_pie_dom = document.getElementById('covid_state_wise_pie_chart');
        echarts.dispose(covid_state_wise_chart_bar_dom);
        echarts.dispose(covid_state_wise_chart_pie_dom);
        let covid_state_chart_bar = echarts.init(covid_state_wise_chart_bar_dom);
        let covid_state_chart_pie = echarts.init(covid_state_wise_chart_pie_dom);
        var itemStyle = {
            normal: {
            },
            emphasis: {
                barBorderWidth: 1,
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowColor: 'rgba(0,0,0,0.5)'
            }
        };
        let covid_state_wise_chart_options_bar = {
            backgroundColor: '#eee',
            legend: {
                align: 'left',
                left: 10,
                show:true
            },
            tooltip: {},
            xAxis: {
                data: x_data,
                name: 'X Axis',
                silent: false,
                axisLine: {onZero: true},
                splitLine: {show: false},
                splitArea: {show: false},
                axisLabel: {
                  fontWeight: 'bold',
                  rotate:50
                }
            },
            yAxis: {
                inverse: false,
                splitArea: {show: false}
            },
            grid: {
                left: 60,
                bottom:140
            },
            series: [
                {
                    name: 'Active Cases '+selected,
                    type: 'bar',
                    itemStyle: itemStyle,
                    data: y_data
                }
            ]
        };

        let covid_state_wise_chart_options_pie = {
          title: {
              text: 'Active Cases',
              subtext: selected,
              left: 'center'
          },
          tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          legend: {
              show:true,
              type: 'scroll',
              orient: 'vertical',
              right: 10,
              top: 20,
              bottom: 20,
              data: y_data,
              selected:x_data
          },
          series: [
              {
                  name: 'State :',
                  type: 'pie',
                  radius: '55%',
                  center: ['40%', '50%'],
                  data:chart_data,
                  emphasis: {
                      itemStyle: {
                          shadowBlur: 10,
                          shadowOffsetX: 0,
                          shadowColor: 'rgba(0, 0, 0, 0.5)'
                      }
                  }
              }
          ]
      };
        covid_state_chart_bar.setOption(covid_state_wise_chart_options_bar);
        covid_state_chart_pie.setOption(covid_state_wise_chart_options_pie);
      })

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
