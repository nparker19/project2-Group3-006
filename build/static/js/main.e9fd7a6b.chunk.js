(this.webpackJsonpundefined=this.webpackJsonpundefined||[]).push([[0],{12:function(e,t,n){},13:function(e,t,n){},15:function(e,t,n){"use strict";n.r(t);var c=n(1),r=n.n(c),i=n(5),u=n.n(i),s=(n(12),n(7)),o=n(6),a=(n(13),n(0));var l=function(){var e=Object(c.useState)([]),t=Object(o.a)(e,2),n=t[0],r=t[1],i=Object(c.useRef)(""),u=Object(c.useRef)(""),l=Object(c.useRef)(""),d=Object(c.useRef)("");function j(e){return Object(a.jsxs)("h3",{children:[e.item," at ",e.time," ",Object(a.jsx)("button",{onClick:function(){var t=n.filter((function(t){return t.event!==e.item}));r(t)},children:"X"})]})}return Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)("h1",{children:"Create Schedule"}),Object(a.jsx)("input",{ref:l,type:"date"}),Object(a.jsx)("div",{class:"idList",align:"center",children:Object(a.jsx)("h3",{children:n.map((function(e){return Object(a.jsx)(j,{item:e.event,time:e.time})}))})}),Object(a.jsxs)("div",{class:"editSchedule",children:[Object(a.jsx)("input",{ref:i,type:"text",placeholder:"Input event"}),Object(a.jsx)("input",{ref:u,type:"text",placeholder:"Input starting time for event"}),Object(a.jsx)("button",{onClick:function(){return function(){var e=i.current.value,t=u.current.value,c=[].concat(Object(s.a)(n),[{event:e,time:t}]);r(c),i.current.value="",u.current.value=""}()},children:" Add Event to Schedule "}),Object(a.jsx)("button",{onClick:function(){fetch("/suggestions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({scheduleDict:n,messages:d})}).then((function(e){return e.json()})).then((function(e){for(var t=0;t<e.message_server.length;t++)alert(e.message_server[t]);r(e.schedule_server)}))},children:" Save Schedule and receive suggestions"}),Object(a.jsx)("button",{onClick:function(){return function(){var e=JSON.stringify({scheduleDict:n,currentDate:l.current.value});fetch("/complete",{method:"POST",headers:{"Content-Type":"application/json"},body:e}).then((function(e){return e.json()})).then((function(e){r(e.schedule_server),window.location.replace("/")}))}()},children:" Complete Schedule and save to google calendar"})]})]})},d=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,16)).then((function(t){var n=t.getCLS,c=t.getFID,r=t.getFCP,i=t.getLCP,u=t.getTTFB;n(e),c(e),r(e),i(e),u(e)}))};u.a.render(Object(a.jsx)(r.a.StrictMode,{children:Object(a.jsx)(l,{})}),document.getElementById("root")),d()}},[[15,1,2]]]);
//# sourceMappingURL=main.e9fd7a6b.chunk.js.map