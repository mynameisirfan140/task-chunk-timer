import { render, screen, fireEvent, act } from '@testing-library/react';
import Timer from './Timer';
import { act } from 'react-dom/test-utils';

jest.useFakeTimers();

test('timer counts up when started', () => {
  render(<Timer />);

  // Initially timer shows 0
  expect(screen.getByText(/0\ss/i)).toBeInTheDocument();

  // Click start button
  fireEvent.click(screen.getByRole('button', { name: /start/i }));

  // Advance timers by 1 second (1000 ms)
  act(() => {
    jest.advanceTimersByTime(1000);
  });

  // Timer should now show 1 second
  expect(screen.getByText(/1\ss/i)).toBeInTheDocument();
});