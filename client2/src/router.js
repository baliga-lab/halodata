import Vue from 'vue'
import Router from 'vue-router'
import HeatMap from './components/HeatMap'
import HeatMapStatic from './components/HeatMapStatic'
import GeneView from './components/GeneView'
import DataTables from './components/DataTables'
import AboutPage from './components/AboutPage'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: DataTables
        },
        {
            path: '/heatmap',
            name: 'heatmap',
            component: HeatMap
        },
        {
            path: '/heatmapstatic',
            name: 'heatmapstatic',
            component: HeatMapStatic
        },
        {
            path: '/viewgene/:gene',
            name: 'viewgene',
            component: GeneView
        },
        /*
        {
            path: '/datatables',
            name: 'datatables',
            component: DataTables
        },*/
        {
            path: '/about',
            name: 'about',
            component: AboutPage
        }
    ]
});
