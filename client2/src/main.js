import Vue from 'vue'
import Router from 'vue-router'
import App from './App.vue'
import vuetify from './plugins/vuetify'
//import igv from 'igv'
import SearchForm from './components/SearchForm'

Vue.use(Router)
Vue.config.productionTip = false

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: SearchForm
        }
    ]
});

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
