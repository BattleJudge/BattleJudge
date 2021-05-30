import Vue from 'vue'
import Router from 'vue-router'
import Vuex from "vuex"




Vue.use(Router)
Vue.use(Vuex)
export default new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: (resolve)=>require(["../components/Pages/Login"],resolve),
            meta: {
                keepAlive: false
            }
        },
        {
            path: '/Information',
            component: (resolve)=>require(["../components/Pages/Information"],resolve),
            meta: {
                keepAlive: true,
                requireAuth: true
            }
        },
        {
            path: '/Rank',
            component: (resolve)=>require(["../components/Pages/Rank"],resolve),
            meta: {
                keepAlive: true,
                requireAuth: true
            }
        },
        {
            path: '/history',
            component: (resolve)=>require(["../components/Pages/History"],resolve),
            meta: {
                keepAlive: true,
                requireAuth: true
            }
        },





        {
            path: '/HistoryDetail',
            component: (resolve)=>require(["../components/Pages/HistoryDetail"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/Contest',
            component: (resolve)=>require(["../components/Pages/Contest"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },

        {
            path: '/SingleSolution',
            component: (resolve)=>require(["../components/Pages/SingleSolution"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/SingleOjHistory',
            component: (resolve)=>require(["../components/Pages/SingleOjHistory"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/MySolution',
            component: (resolve)=>require(["../components/Pages/MySolution"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/SingleOj',
            component: (resolve)=>require(["../components/Pages/SingleOj"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/User/List',
            component: (resolve)=>require(["../components/Pages/UserList"],resolve),
            meta: {
                keepAlive: true,
                requireAuth: true
            }
        },
        {
            path: '/Problem/List',
            component: (resolve)=>require(["../components/Pages/ProblemList"],resolve),
            meta: {
                keepAlive: true,
                requireAuth: true
            }
        },
        {
            path: '/Regular/Problem/List',
            component: (resolve)=>require(["../components/Pages/RegularProblemList"],resolve),
            meta: {
                keepAlive: true,
                requireAuth: true
            }
        },
        {
            path: '/Admin/Problem/Add',
            component: (resolve)=>require(["../components/Admin/ProblemAdd"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/Admin/Problem/Update',
            component: (resolve)=>require(["../components/Admin/ProblemAdd"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },
        {
            path: '/Admin/Problem/Detail',
            component: (resolve)=>require(["../components/Admin/ProblemDetail"],resolve),
            meta: {
                keepAlive: false,
                requireAuth: true
            }
        },







    ]
})
