import './App.css';
import React, { useState, useRef } from 'react';



function App() {

  const [scheduleDict, setScheduleDict] = useState([]);

  const textInput = useRef('');
  const timeInput = useRef('');

  console.log(scheduleDict)
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

      <div class="idList" align="right">
        <h3>{scheduleDict.map((dictItem) => <Schedule item={dictItem.event} time={dictItem.time} />)}</h3>
      </div>
      <div class="editSchedule" align="center">
        <input ref={textInput} type="text" />
        <input ref={timeInput} type="text" placeholder="Input time for task" />
        <button onClick={() => onButtonClick()}> Add </button>
      </div>
    </>


  );
}

export default App;
