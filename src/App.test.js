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

  fireEvent.change(eventInput, { target: { value: 'Analysis II' } });
  fireEvent.change(startInput, { target: { value: '03:45 PM' } });
  fireEvent.change(endInput, { target: { value: '05:00 PM' } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText('Analysis II from 15:45 to 17:00 ');
  const deleteButton = screen.getByText('X');
  expect(eventEntry).toBeInTheDocument();
  expect(deleteButton).toBeInTheDocument();
});

test('delete event', () => {
  render(<App />);
  const addButton = screen.getByText('Add Event');
  const eventInput = screen.getByTestId('event_input');
  const endInput = screen.getByTestId('end_input');
  const startInput = screen.getByTestId('start_input');


  fireEvent.change(eventInput, { target: { value: 'Analysis II' } });
  fireEvent.change(startInput, { target: { value: '03:45 PM' } });
  fireEvent.change(endInput, { target: { value: '05:00 PM' } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText('Analysis II from 15:45 to 17:00 ');
  const deleteButton = screen.getByText('X');
  expect(eventEntry).toBeInTheDocument();
  expect(deleteButton).toBeInTheDocument();

  fireEvent.click(deleteButton);
  expect(eventEntry).not.toBeInTheDocument();
  expect(startEntry).not.toBeInTheDocument();
  expect(endEntry).not.toBeInTheDocument();
  expect(deleteButton).not.toBeInTheDocument();
});
