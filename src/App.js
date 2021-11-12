import './App.css';
import React, { useState, useRef } from 'react';



function App() {

  const [scheduleDict, setScheduleDict] = useState([]);

  const textInput = useRef('');
  const timeInput = useRef('');

  function Schedule(props) {

    function onDelete() {
      const newDict = scheduleDict.filter((item) => item.event !== props.item);
      setScheduleDict(newDict);
    }
    return (
      <h3>{props.item} at {props.time} <button onClick={onDelete}>X</button></h3>
    );
  }

  function onButtonClick() {
    let newTask = textInput.current.value;
    let newTime = timeInput.current.value;
    let newScheduleDict = [...scheduleDict, { "event": newTask, "time": newTime }];

    setScheduleDict(newScheduleDict);

    textInput.current.value = "";
    timeInput.current.value = "";
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
        <button onClick={() => onButtonClick()}> Add Event to Schedule </button>
      </div>
    </>


  );
}

export default App;
