import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ResultsView from '../views/ResultsView.vue'

const router = createRouter({
    history: createWebHashHistory(), // Using hash history for simpler local deployment
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/results/:jobId',
            name: 'results',
            component: ResultsView
        }
    ]
})

export default router
