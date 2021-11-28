import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import App from "./App";

test("renders buttons", () => {
  render(<App />);


  const addButton = screen.getByText("Add Event");
  expect(addButton).toBeInTheDocument();
  const addButton = screen.getByText("Add Activity");
  expect(addButton).toBeInTheDocument();
  const saveButton = screen.getByText("Receive suggestions");
  expect(saveButton).toBeInTheDocument();
  const completeButton = screen.getByText("Complete Schedule and save to google calendar");
  expect(completeButton).toBeInTheDocument();
});

test("add suggestion", () => {
  render(<App />);
  const addButton = screen.getByText("Add Activity");
  const eventInput = screen.getByTestId("activity_input");
  const hourInput = screen.getByTestId('hour_input');
  const minuteInput = screen.getByTestId('hour_input');

  fireEvent.change(eventInput, { target: { value: "Workout" } });
  fireEvent.change(hourInput, { target: { value: "2" } });
  fireEvent.change(minuteInput, { target: { value: "45" } });
  fireEvent.click(addButton);

  const eventEntry = screen.getByText((content) => content.startsWith("Workout"));
  expect(eventEntry).toBeInTheDocument();
});

