import React, { useState, useEffect } from 'react';

const WORK_MINUTES = 25;
const BREAK_MINUTES = 5;

const Timer = ({ running, onStart, onStop, interval }) => {
  const [secondsLeft, setSecondsLeft] = useState(interval * 60);
  const [phase, setPhase] = useState('work'); // 'work' or 'break'

  const totalWorkSeconds = WORK_MINUTES * 60;
  const totalBreakSeconds = BREAK_MINUTES * 60;

  const formatTime = (sec) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const tick = () => {
    setSecondsLeft((prev) => {
      if (prev <= 1) {
        // Switch phase when the current interval ends
        const newPhase = prev === totalWorkSeconds ? 'break' : 'work';
        setPhase(newPhase);
        if (newPhase === 'work') {
          return totalWorkSeconds;
        } else {
          return totalBreakSeconds;
        }
      }
      return prev - 1;
    });
  };

  useEffect(() => {
    if (!running) return;
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [running]);

  const handleStart = () => {
    setSecondsLeft(interval * 60);
    setPhase('work');
    setRunning(true);
  };

  const handleStop = () => {
    setRunning(false);
  };

  return (
    <div className="timer">
      <h2>Pomodoro Timer</h2>
      <p className="time">{formatTime(secondsLeft)}</p>
      <p className="phase">{phase.toUpperCase()}</p>
      <button onClick={running ? handleStop : handleStart}>
        {running ? 'Pause' : 'Start'}
      </button>
    </div>
  );
};

export default Timer;