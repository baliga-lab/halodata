import Vue from 'vue'
import VueMobileDetection from "vue-mobile-detection"
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'


Vue.config.productionTip = false
Vue.use(VueMobileDetection);

var app = new Vue({
    router,
    vuetify,
    render: h => h(App)
});

app.$mount('#app')
