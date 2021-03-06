import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import App from "./App";

test("renders buttons", () => {
  render(<App />);


  const addEventButton = screen.getByText("Add Event");
  expect(addEventButton).toBeInTheDocument();
  const addActivityButton = screen.getByText("Add Activity");
  expect(addActivityButton).toBeInTheDocument();
  const saveButton = screen.getByText("Receive suggestions");
  expect(saveButton).toBeInTheDocument();
});

test("add suggestion", () => {
  render(<App />);
  const addButton = screen.getByText("Add Activity");
  const eventInput = screen.getByTestId('activity_input');
  const hourInput = screen.getByTestId('hour_input');
  const minuteInput = screen.getByTestId('minute_input');

  fireEvent.change(eventInput, { target: { value: "Workout" } });
  fireEvent.change(hourInput, { target: { value: "2" } });
  fireEvent.change(minuteInput, { target: { value: "45" } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText((content) => content.startsWith("Workout"));
  expect(eventEntry).toBeInTheDocument();
});

