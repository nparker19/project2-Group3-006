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

  fireEvent.change(eventInput, { target: { value: 'Analysis II' } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText((content) => content.startsWith('Analysis'));
  const deleteButton = screen.getByText('X');
  expect(eventEntry).toBeInTheDocument();
  expect(deleteButton).toBeInTheDocument();
});

test('delete event', () => {
  render(<App />);
  const addButton = screen.getByText('Add Event');
  const eventInput = screen.getByTestId('event_input');



  fireEvent.change(eventInput, { target: { value: 'Analysis II' } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText((content) => content.startsWith('Analysis'));
  const deleteButton = screen.getByText('X');
  expect(eventEntry).toBeInTheDocument();
  expect(deleteButton).toBeInTheDocument();

  fireEvent.click(deleteButton);
  expect(eventEntry).not.toBeInTheDocument();
  expect(deleteButton).not.toBeInTheDocument();
});
