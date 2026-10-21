const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fetchTasks = async () => {
  const response = await fetch(`${API_BASE}/tasks`);
  if (!response.ok) throw new Error('Failed to fetch tasks');
  return response.json();
};

export const fetchSubtasks = async (taskId) => {
  const response = await fetch(`${API_BASE}/tasks/${taskId}/subtasks`);
  if (!response.ok) throw new Error('Failed to fetch subtasks');
  return response.json();
};