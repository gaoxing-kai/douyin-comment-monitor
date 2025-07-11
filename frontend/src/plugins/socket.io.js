import { io } from 'socket.io-client';

export default {
  install(app) {
    const socket = io(import.meta.env.VITE_API_BASE_URL);
    app.provide('socket', socket);
  }
};    