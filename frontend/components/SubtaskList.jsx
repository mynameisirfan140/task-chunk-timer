import React, { useEffect, useState } from 'react';
import { fetchSubtasks } from '../utils/api';

const SubtaskList = ({ taskId }) => {
  const [subtasks, setSubtasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubtasks(taskId)
      .then(setSubtasks)
      .finally(() => setLoading(false));
  }, [taskId]);

  if (loading) return <p>Loading subtasks...</p>;

  return (
    <ul className="subtask-list">
      {subtasks.map((subtask) => (
        <li key={subtask.id}>
          {subtask.title}
          {subtask.completed_at && ' ✅'}
        </li>
      ))}
    </ul>
  );
};

export default SubtaskList;