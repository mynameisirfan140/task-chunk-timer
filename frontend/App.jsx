import React, { useState, useEffect } from 'react';
import Timer from '../components/Timer';
import TaskList from '../components/TaskList';
import SubtaskList from '../components/SubtaskList';
import { fetchTasks, fetchSubtasks, createTask, createSubtask, updateTask, deleteTask } from '../utils/api';

const App = () => {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [timerRunning, setTimerRunning] = useState(false);
  const [currentInterval, setCurrentInterval] = useState(0);

  // Load tasks when the component mounts
  useEffect(() => {
    const load = async () => {
      const data = await fetchTasks();
      setTasks(data);
    };
    load();
  }, []);

  const handleTaskClick = (taskId) => {
    setSelectedTaskId(taskId);
  };

  const handleTimerStart = () => {
    setTimerRunning(true);
  };

  const handleTimerStop = () => {
    setTimerRunning(false);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Task Chunk Timer</h1>
        <Timer
          running={timerRunning}
          onStart={handleTimerStart}
          onStop={handleTimerStop}
          interval={currentInterval}
        />
      </header>

      <main className="main">
        <TaskList tasks={tasks} onSelect={handleTaskClick} />
        {selectedTaskId && <SubtaskList taskId={selectedTaskId} />}
      </main>
    </div>
  );
};

export default App;