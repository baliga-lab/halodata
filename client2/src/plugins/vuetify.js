import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: '#002967',
                secondary: '#22eceb',
                accent: '#550794',
                error: '#ff2000',
                warning: '#ff5f00',
                info: '#002664'
            }
        }
    }
});
