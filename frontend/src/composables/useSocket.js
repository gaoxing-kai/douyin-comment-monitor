import { ref, onMounted, onUnmounted } from 'vue';
import { io } from 'socket.io-client';

export const useSocket = (taskId) => {
  const socket = io(import.meta.env.VITE_API_BASE_URL);
  const connected = ref(false);
  const error = ref(null);

  onMounted(() => {
    socket.on('connect', () => {
      connected.value = true;
      console.log('Socket connected');
      
      // 加入任务房间
      if (taskId.value) {
        socket.emit('join_task_room', taskId.value);
      }
    });

    socket.on('disconnect', () => {
      connected.value = false;
      console.log('Socket disconnected');
    });

    socket.on('connect_error', (err) => {
      error.value = err.message;
      console.error('Socket connection error:', err);
    });
  });

  onUnmounted(() => {
    // 离开任务房间
    if (taskId.value) {
      socket.emit('leave_task_room', taskId.value);
    }
    
    socket.disconnect();
  });

  return {
    socket,
    connected,
    error
  };
};    