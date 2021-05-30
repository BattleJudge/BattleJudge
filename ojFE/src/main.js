import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import {codemirror} from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'

import md5 from 'js-md5'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import 'default-passive-events'
import VueClipboard from 'vue-clipboard2'

Vue.use(VueClipboard)
Vue.config.productionTip = false
Vue.use(ViewUI);
Vue.prototype.$md5 = md5

Vue.use(codemirror)
Vue.use(ElementUI);

Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios
axios.defaults.baseURL = "后台链接";


// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
router.beforeEach((to, from, next) => {

        if (to.meta.requireAuth) {
            // console.log(store.state.user.token)
            if (store.state.user.token) {   //如果存在token则直接跳转
                next()
            } else {
                next({            //否则跳回登录界面
                    path: '/',
                    query: {redirect: to.fullPath}
                })
            }
        } else {
            next()
        }
    }
)
// eslint-disable-next-line no-unused-vars
let isRefreshing = false;
// 存储请求的数组
let refreshSubscribers = [];

/*将所有的请求都push到数组中*/
function subscribeTokenRefresh(cb) {
    refreshSubscribers.push(cb);
}

// 数组中的请求得到新的token之后执行，用新的token去请求数据
// eslint-disable-next-line no-unused-vars
function onRrefreshed(token) {
    refreshSubscribers.map(cb => cb(token));
}

// eslint-disable-next-line no-unused-vars
function isExpired() {
    let time = sessionStorage.getItem("TokenTime");
    let nowTime = new Date().getTime();
    let stamp = nowTime - time;
    let minutes = parseInt((stamp % (1000 * 60 * 60)) / (1000 * 60));
    return minutes >= 4 ? true : false;
}


axios.interceptors.request.use(
    config => {
        // 判断是否存在token，如果存在的话，则每个http header都加上token
        let token = sessionStorage.getItem('token')
        if (config.url.indexOf('/api/token/refresh/') >= 0) {
            return config
        }
        if (!Object.prototype.hasOwnProperty.call(config.headers, "Authorization") && token) {
            if (!isExpired()) {
                config.headers.Authorization = "JWT " + token;
            } else {
                if (!isRefreshing) {
                    isRefreshing = true;
                    axios.post("后台链接",
                        {"refresh": sessionStorage.getItem("refreshToken")})
                        .then(Response => {
                            isRefreshing = false;
                            store.commit('SET_TOKEN', Response.data.access)   //保存token用于拦截
                            sessionStorage.setItem("token", Response.data.access)
                            sessionStorage.setItem("TokenTime", new Date().getTime());//token刷新

                            onRrefreshed(Response.data.access);
                            /*执行onRefreshed函数后清空数组中保存的请求*/
                            refreshSubscribers = []
                        })
                        .catch(failResponse => {
                            console.log(failResponse);
                        });

                }


                let retry = new Promise((resolve) => {
                    /*(token) => {...}这个函数就是回调函数*/
                    subscribeTokenRefresh((token) => {
                        config.headers.Authorization = "JWT " + token;
                        resolve(config)
                    })
                });
                return retry;
            }

        }
        return config;
    },
);


/* eslint-disable no-new */
new Vue({
    el: '#app',
    render: h => h(App),
    router,
    store,
    components: {App},
    template: '<App/>'
})