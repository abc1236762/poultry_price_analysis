import '@mdi/font/css/materialdesignicons.css';
import '@/assets/fonts/style.scss';
import '@/styles/global.scss';

import Vue from 'vue';
import App from '@/App.vue';
import router from '@/router';
import vuetify from '@/plugins/vuetify';

Vue.config.productionTip = false;

// import tf from '@/plugins/tensorflow';

// const a = tf.tensor1d([1, 2, 3, 4]);
// const b = tf.tensor1d([10, 20, 30, 40]);

// a.add(b).print();
// console.log(tf.engine());

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
