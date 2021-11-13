import './App.css';
import React, { useState, useRef } from 'react';



function App() {

  const [scheduleDict, setScheduleDict] = useState([]);
  console.log(scheduleDict)
  const textInput = useRef('');
  const timeInput = useRef('');
  const messages = useRef('');
  function Schedule(props) {

    function onDelete() {
      const newDict = scheduleDict.filter((item) => item.event !== props.item);
      setScheduleDict(newDict);
    }
    return (
      <h3>{props.item} at {props.time} <button onClick={onDelete}>X</button></h3>
    );
  }

  function onAddClick() {
    let newTask = textInput.current.value;
    let newTime = timeInput.current.value;
    let newScheduleDict = [...scheduleDict, { "event": newTask, "time": newTime }];

    setScheduleDict(newScheduleDict);

    textInput.current.value = "";
    timeInput.current.value = "";
  }

  function onSaveClick() {


    fetch('/suggestions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "scheduleDict": scheduleDict }, { "messages": messages }),
    }).then(response => response.json()).then(data => {
      for (let i = 0; i < data.message_server.length; i++) {
        alert(data.message_server[i]);
        console.log(data.message_server)
      }
      setScheduleDict(data.schedule_server)
    })
  }

  function onCompleteClick() {

  }

  return (
    <>
      <h1>Create Schedule</h1>

      <div class="idList" align="center">
        <h3>{scheduleDict.map((dictItem) => <Schedule item={dictItem.event} time={dictItem.time} />)}</h3>
      </div>

      <div class="editSchedule" align="center">
        <input ref={textInput} type="text" placeholder="Input event" />
        <input ref={timeInput} type="text" placeholder="Input starting time for event" />
        <button onClick={() => onAddClick()}> Add Event to Schedule </button>
        <button onClick={() => onSaveClick()}> Save Schedule and receive suggestions</button>
        <button onClick={() => onCompleteClick()}> Complete Schedule and save to google calendar</button>
      </div>
    </>


  );
}

export default App;