import React, { useEffect, useState } from 'react';
import { fetchTasks } from '../utils/api';
import SubtaskList from './SubtaskList';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);

  useEffect(() => {
    fetchTasks()
      .then(setTasks)
      .catch(console.error);
  }, []);

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="task-card"
          onClick={() => setSelectedTaskId(task.id)}
        >
          <h3>{task.title}</h3>
          <p>{task.total_duration} seconds</p>
          {selectedTaskId === task.id && <SubtaskList taskId={task.id} />}
        </div>
      ))}
    </div>
  );
};

export default TaskList;