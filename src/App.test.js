import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import App from './App';

test('renders buttons', () => {
  render(<App />);
  const addButton = screen.getByText('Add Event');
  expect(addButton).toBeInTheDocument();
  const saveButton = screen.getByText('Save Schedule and receive suggestions');
  expect(saveButton).toBeInTheDocument();
  const completeButton = screen.getByText('Complete Schedule and save to google calendar');
  expect(completeButton).toBeInTheDocument();
});

test('add event', () => {
  render(<App />);
  const addButton = screen.getByText('Add Event');
  const eventInput = screen.getByTestId('event_input');
  const endInput = screen.getByTestId('end_input');
  const startInput = screen.getByTestId('start_input');

  fireEvent.change(eventInput, { target: { value: 'Workout' } });
  fireEvent.change(startInput, { target: { value: '10:00 AM' } });
  fireEvent.change(endInput, { target: { value: '11:00 AM' } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText('Workout');
  const startEntry = screen.getByText('10:00');
  const endEntry = screen.getByText('11:00');
  const deleteButton = screen.getByText('X');
  expect(eventEntry).toBeInTheDocument();
  expect(startEntry).toBeInTheDocument();
  expect(endEntry).toBeInTheDocument();
  expect(deleteButton).toBeInTheDocument();
});

test('delete event', () => {
  render(<App />);
  const addButton = screen.getByText('Add Event');
  const eventInput = screen.getByTestId('event_input');
  const endInput = screen.getByTestId('end_input');
  const startInput = screen.getByTestId('start_input');
  fireEvent.change(eventInput, { target: { value: 'Workout' } });
  fireEvent.change(startInput, { target: { value: '10:00 AM' } });
  fireEvent.change(endInput, { target: { value: '11:00 AM' } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText('Workout');
  const startEntry = screen.getByText('10:00');
  const endEntry = screen.getByText('11:00');
  const deleteButton = screen.getByText('X');
  expect(eventEntry).toBeInTheDocument();
  expect(startEntry).toBeInTheDocument();
  expect(endEntry).toBeInTheDocument();
  expect(deleteButton).toBeInTheDocument();

  fireEvent.click(deleteButton);
  expect(eventEntry).not.toBeInTheDocument();
  expect(startEntry).not.toBeInTheDocument();
  expect(endEntry).not.toBeInTheDocument();
  expect(deleteButton).not.toBeInTheDocument();
});
