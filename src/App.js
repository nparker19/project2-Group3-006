import "./App.css";
import React, { useState, useRef } from "react";

function App() {
  const [scheduleDict, setScheduleDict] = useState([]);
  const [suggestDict, setSuggestDict] = useState([]);
  const eventInput = useRef('');
  const startTimeInput = useRef('');
  const endTimeInput = useRef('');
  const dateInput = useRef('');
  const suggestDuration = useRef('');
  const suggestInput = useRef('');

  //React component which returns the schedule list
  function Schedule(props) {

    function onDelete() {
      const newDict = scheduleDict.filter((item) => item.event !== props.item);
      setScheduleDict(newDict);
    }
    return (

      <h2>
        {props.item} from {props.startTime} to {props.endTime}
        <button onClick={onDelete}>X</button>
      </h2>
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
    let newScheduleDict = [
      ...scheduleDict,
      { event: newEvent, startTime: newStartTime, endTime: newEndTime },
    ];
    //Schedule is automatically sorted upon event addition
    fetch("/sorting", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "unsortedSchedule": newScheduleDict }),
    }).then(response => response.json()).then(data => {
      if (data.message_server.length === 1) {
        alert(data.message_server[0]);
      } else {
        setScheduleDict(data.server_sorted_Schedule);
        eventInput.current.value = "";
        startTimeInput.current.value = "";
        endTimeInput.current.value = "";
      }
    });



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

    fetch("/suggestions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "scheduleDict": scheduleDict, "suggestDict": suggestDict }),
    }).then(response => response.json()).then(data => {
      if (data.message_server.length === 1) {
        alert(data.message_server[0]);
      } else {
        var scheduleUpdate = data.schedule_server;
        var suggestUpdate = data.suggest_server;
        var addedSuggestions = [];
        var suggestList = data.suggestions_server;

        for (var i in suggestList) {
          var suggestNotif = suggestList[i];
          var suggest = suggestNotif.suggestion;
          //If statement makes sure that a suggestion for this event has not been accepted already, and if the user accepts the suggestion
          if (addedSuggestions.indexOf(suggestNotif.suggestEvent) === -1 && window.confirm(suggest) === true) {

            let newScheduleDict = [
              ...scheduleUpdate,
              { event: suggestNotif.suggestEvent, startTime: suggestNotif.suggestStartTime, endTime: suggestNotif.suggestEndTime }
            ];
            scheduleUpdate = newScheduleDict;
            //Schedule is kept in order by sorting function on the server side
            fetch("/sorting", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ "unsortedSchedule": scheduleUpdate }),
            }).then(response => response.json()).then(data => {
              if (data.message_server.length === 1) {
                alert(data.message_server[0]);
              } else {
                setScheduleDict(data.server_sorted_Schedule);
              }
            });
            // eslint-disable-next-line
            suggestUpdate = suggestUpdate.filter((item) => item.suggestion !== suggestNotif.suggestEvent);
            setSuggestDict(suggestUpdate);
            //Event is now added to the addedSuggestions list so that other suggestions for this even do not appear
            addedSuggestions.push(suggestNotif.suggestEvent);

          }

        }

      }

    });


  }

  function onCompleteClick() {
    const response_data = JSON.stringify({
      scheduleDict: scheduleDict,
      currentDate: dateInput.current.value,
    });
    fetch("/complete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: response_data,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message_server.length === 1) {
          alert(data.message_server[0]);
        } else {
          setScheduleDict(data.schedule_server);
          alert("Schedule was successfully saved to your google calendar! You will be redirected to the home page after exiting out of this message");
          setTimeout(function () { window.location.replace("/") }, 3000);
        }
      });
  }

  return (
    <div>
      <table>
        <td class="suggestions">
          <div class="display" align="center">
            <h1>What I would like to do</h1>
            <div class="suggestList" align="center">
              <h2>{suggestDict.map((suggestNotif) => <Suggest suggest={suggestNotif.suggestion} duration={suggestNotif.duration} />)}</h2>
            </div>

            <input ref={suggestInput} type="text" placeholder="Input activity" />
            <label for="len">Duration: </label>
            <input ref={suggestDuration} type="text" placeholder="00:00 (Hour:Min)" id="len" />
            <button onClick={() => onAddClickSuggest()}> Add </button>
          </div>
        </td>
        <td class="schedule">
          <div class="display" align="center">
            <h1>What I have to do</h1>

            <input ref={dateInput} type="date" />

            <div class="scheduleList" align="center">
              <h2>{scheduleDict.map((suggestNotif) => <Schedule item={suggestNotif.event} startTime={suggestNotif.startTime} endTime={suggestNotif.endTime} />)}</h2>
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
        <button onClick={() => onSaveClick()}> Receive suggestions</button>
      </div>
      <div class="Complete" align="center">
        <button onClick={() => onCompleteClick()}> Complete Schedule and save to google calendar</button>
      </div>
    </div>

  );
}

export default App;
