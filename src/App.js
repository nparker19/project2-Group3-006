import './App.css';
import React, { useState, useRef } from 'react';


function App() {

  const [scheduleDict, setScheduleDict] = useState([]);
  const [suggestDict, setSuggestDict] = useState([]);
  const eventInput = useRef('');
  const startTimeInput = useRef('');
  const endTimeInput = useRef('');
  const dateInput = useRef('');
  const messages = useRef('');
  const suggestDuration = useRef('');
  const suggestInput = useRef('');

  //React component which returns the schedule list
  function Schedule(props) {

    function onDelete() {
      const newDict = scheduleDict.filter((item) => item.event !== props.item);
      setScheduleDict(newDict);
    }
    return (
      <h2>{props.item} from {props.startTime} to {props.endTime}<button onClick={onDelete}>X</button></h2>
    );
  }
  //React component which returns the suggestions list
  function Suggest(props) {

    function onDelete() {
      const newSuggestDict = suggestDict.filter((item) => item.suggestion !== props.suggest);
      setSuggestDict(newSuggestDict);
    }
    return (
      <h2>{props.suggest} for {props.duration} hours<button onClick={onDelete}>X</button></h2>
    );
  }
  //Function which handles the add schedule event button
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
  //Function which handles the add an event suggestion button
  function onAddClickSuggest() {

    let newSuggest = suggestInput.current.value;
    let newSuggestDuration = suggestDuration.current.value;

    let newSuggestDict = [...suggestDict, { "suggestion": newSuggest, "duration": newSuggestDuration }];

    setSuggestDict(newSuggestDict);

    suggestInput.current.value = "";
    suggestDuration.current.value = "";
  }

  function onSaveClick() {

    fetch('/suggestions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "scheduleDict": scheduleDict, "suggestDict": suggestDict, "messages": messages }),
    }).then(response => response.json()).then(data => {
      for (let i = 0; i < data.message_server.length; i++) {
        alert(data.message_server[i]);
      }
      setScheduleDict(data.schedule_server);
      setSuggestDict(data.suggest_server);
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
    <div>
      <table>
        <td class="suggestions">
          <div class="display" align="center">
            <h1>What I would like to do</h1>
            <div class="suggestList" align="center">
              <h2>{suggestDict.map((dictItem) => <Suggest suggest={dictItem.suggestion} duration={dictItem.duration} />)}</h2>
            </div>

            <input ref={suggestInput} type="text" placeholder="Input activity" />
            <label for="len">Duration: </label>
            <input ref={suggestDuration} type="text" placeholder="00:00 (Hour:Min)" id="len" />
            <button onClick={() => onAddClickSuggest()}> Add Event</button>
          </div>
        </td>
        <td class="schedule">
          <div class="display" align="center">
            <h1>What I have to do</h1>

            <input ref={dateInput} type="date" />

            <div class="scheduleList" align="center">
              <h2>{scheduleDict.map((dictItem) => <Schedule item={dictItem.event} startTime={dictItem.startTime} endTime={dictItem.endTime} />)}</h2>
            </div>

            <div class="editSchedule" align="center">
              <input ref={eventInput} type="text" placeholder="Input event" data-testid="event_input" />
              <label for="start">start time: </label>
              <input ref={startTimeInput} type="time" id="start" data-testid="start_input" />
              <label for="end">end time: </label>
              <input ref={endTimeInput} type="time" id="end" data-testid="end_input" />

              <button onClick={() => onAddClick()}> Add Event </button>
            </div>

          </div>
        </td>
      </table>
      <div class="Save" align="center">
        <button onClick={() => onSaveClick()}> Save Schedule and receive suggestions</button>
      </div>
      <div class="Complete" align="center">
        <button onClick={() => onCompleteClick()}> Complete Schedule and save to google calendar</button>
      </div>
    </div>

  );
}

export default App;
