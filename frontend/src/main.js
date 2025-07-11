import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import SocketIOPlugin from './plugins/socket.io';

const app = createApp(App);

app.use(ElementPlus);
app.use(router);
app.use(createPinia());
app.use(SocketIOPlugin);

app.mount('#app');    