import Vue from 'vue'
import Router from 'vue-router'
import SearchForm from './components/SearchForm'
import HeatMap from './components/HeatMap'
import GeneView from './components/GeneView'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: SearchForm
        },
        {
            path: '/heatmap',
            name: 'heatmap',
            component: HeatMap
        },
        {
            path: '/viewgene/:gene',
            name: 'viewgene',
            component: GeneView
        }
    ]
});
