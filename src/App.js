import './App.css';
import React, { useState, useRef } from 'react';


function App() {

  const [scheduleDict, setScheduleDict] = useState([]);
  const eventInput = useRef('');
  const startTimeInput = useRef('');
  const endTimeInput = useRef('');
  const dateInput = useRef('');
  const messages = useRef('');

  function Schedule(props) {

    function onDelete() {
      const newDict = scheduleDict.filter((item) => item.event !== props.item);
      setScheduleDict(newDict);
    }
    return (
      <h3>{props.item} from {props.startTime} to {props.endTime}<button onClick={onDelete}>X</button></h3>
    );
  }

  function onAddClick() {
    let newEvent = eventInput.current.value;
    let newStartTime = startTimeInput.current.value;
    let newEndTime = endTimeInput.current.value;
    let newScheduleDict = [...scheduleDict, { "event": newEvent, "startTime": newStartTime, "endTime": newEndTime }];

    setScheduleDict(newScheduleDict);

    eventInput.current.value = "";
    startTimeInput.current.value = "";
    endTimeInput.current.value = "";
  }

  function onSaveClick() {

    fetch('/suggestions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "scheduleDict": scheduleDict, "messages": messages }),
    }).then(response => response.json()).then(data => {
      for (let i = 0; i < data.message_server.length; i++) {
        alert(data.message_server[i]);
      }
      setScheduleDict(data.schedule_server);
    });
  }

  function onCompleteClick() {
    const response_data = JSON.stringify({ "scheduleDict": scheduleDict, "currentDate": dateInput.current.value });
    fetch('/complete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: response_data,
    }).then(response => response.json()).then(data => {
      setScheduleDict(data.schedule_server);
      window.location.replace("/");
    });

  }

  return (
    <>
      <h1>Create Schedule</h1>

      <input ref={dateInput} type="date" />

      <div class="idList" align="center">
        <h3>{scheduleDict.map((dictItem) => <Schedule item={dictItem.event} startTime={dictItem.startTime} endTime={dictItem.endTime} />)}</h3>
      </div>

      <div class="editSchedule">
        <input ref={eventInput} type="text" placeholder="Input event" />
        <label for="start">Input event start time</label>
        <input ref={startTimeInput} type="time" id="start" />
        <label for="end">Input event end time</label>
        <input ref={endTimeInput} type="time" id="end" />
        <button onClick={() => onAddClick()}> Add Event to Schedule </button>
        <button onClick={() => onSaveClick()}> Save Schedule and receive suggestions</button>
        <button onClick={() => onCompleteClick()}> Complete Schedule and save to google calendar</button>
      </div>
    </>


  );
}

export default App;