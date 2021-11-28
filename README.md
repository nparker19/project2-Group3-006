# Start of Project 2, for Group 3 (Section 006)
https://git.heroku.com/nameless-basin-16999.git

# TODOit App
### TODOit is web application that allow user to schedule their daily tasks and then get time suggestions for other activies that can be added to schedules, and finally schedules are added to user google calender and update
- ***User is able to login with gmail account***
- ***user makes and submit schedule schedules of todo and***
- ***TODOit application pops up with suggestions for other activities that can be added in-between times***
- ***such such gym time, walking out, nap time, study time and other lifestyle-related activities***
- ***User can choose to update schedule tasks and submitted schedule***
- ***app then save schedule to Google calendar - with reminder set in place already***
### TODOit app is essentially design to fill help user manage and scheudule thier busy daily activities such that they can fill-in other essentiall event based on app suggestion. It is interesting that that many ToDo app by this particularly unique for the pop-up suggestions design.  

## This app is designed using Flask web framework as a tool for linking every pecies of the applications together a whole. 
- User Login is implemented using Google Sign-in to allow OAuth Login API for authenticating the user email for security and safety review.
- Implemented such that use is uniquely identifed in the app and in the linked database for the app.
- Heroku cloud application is used to eventually host this application and the database for the app operations. 
- Google Calender API was used mainly to link user activities on the TODOit app to user gmail calender updates and notification (https://developers.google.com/calendar/). 
- React was also you make the app for responsive and interactive user interface - to make the pap dynamic and ea-sy**

## To clone this app repository
-  user or developer will need to create the their own database set-up
- User will need to create account google developer and get access to Google Calender API  ( for more doc and how https://developers.google.com/calendar/ ) 
- Also for Google login and OAuth Login API https://developers.google.com/identity/protocols/oauth2 
- For most part the requirement.txt in the repository have essintail app need and can be run as 
``` 
pip install -r requirments.txt
```
- For set up react component set up and running see https://create-react-app.dev/docs/getting-started/

## Problem and Technical Issues in the course of design
- Setting up the Heroku app deployment was a huge challenge. Everthing for the deploymet was fine except for linking the Google Calender API credentials to Heroku config var: thid is still a challenge. 
- Also deleting from the calendar updae was a challenges> it is someworth a difficult task to fetch and delete directly via html form from google calendar

##  possible addition to app
- this may include scaling up the app such that user can add list of activities that the TODit app can add pop-ups of suggestion