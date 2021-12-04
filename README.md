# Start of Project 2, for Group 3 (Section 006)
https://pacific-tor-81329.herokuapp.com/

# TODOit App
### TODOit is web application that allow user to schedule their daily tasks and then get time suggestions for other activies that can be added to schedules, and finally schedules are added to user google calender and update
- ***User is able to login with gmail account***
- ***user makes and submit schedule schedules of todo and***
- ***TODOit application pops up with suggestions for other activities that can be added in-between times***
- ***such such gym time, walking out, nap time, study time and other lifestyle-related activities***
- ***User can choose to update schedule tasks and submitted schedule***
- ***app then save schedule to Google calendar - with  reminder set in place already***

### TODOit app is essentially design to fill help user manage and scheudule thier busy daily activities such that they can fill-in other essentiall event based on app suggestion. It is interesting that that many ToDo app by this particularly unique for the pop-up suggestions design.  

## This app is designed using Flask web framework as a tool for linking every pecies of the applications together a whole. 
- User Login is implemented using Google Sign-in to allow OAuth Login API for authenticating the user email for security and safety review.
- Implemented such that use is uniquely identifed in the app and in the linked database for the app.
- Heroku cloud application is used to eventually host this application and the database for the app operations. 
- Google Calender API was used mainly to link user activities on the TODOit app to user gmail calender updates and notification (https://developers.google.com/calendar/). 
- React was also you make the app for responsive and interactive user interface - to make the pap dynamic and easy

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
- Setting up the Heroku app deployment was a huge challenge. Everthing for the deploymet was fine except for linking the Google Calender API credentials to Heroku config var: thid is still a challenge but we finally got it done - deployed


##  possible addition to app
- this may include scaling up the app such that user can add list of activities that the TODit app can add pop-ups of suggestion
- Google calender operation will be implemanted and fixed challenges arround token_expiration.

## list pylint disable in the codes
    "--errors-only" to ignore none error
     "--load-plugins", to ignore plugins
    "--pylint_flask_sqlalchemy" to ignore flask sqlalchemy 
     "--pylint_flask" : to ignore flask import and function
    "--disable=C0103", to ignore style style for database 
    "--disable=W0621",  to ignore style standard that's not error
    "--disable=R0914",  to ignore calling standard complain
    "--disable=R1721", "--disable=W0703", to ignore exceptions complaint 
    "--disable=E1101", to ignore non error suggestions due to instance
    "--disable=W0702", to ignore a logic recommendation

- this may include scaling up the app such that user can add list of activities that the TODit app can add pop-ups of suggestion 

## Linting
- Disabled pylint C0330 (bad-continuation) in methods.py. Split up a string in order to avoid a different pylint error.However, the way black formated the indentation and spacing, disagreed with pylint. Anytime the spacing/indentation was fixed, black reformatted the spacing and indentation.
-Disabled eslint error: Function declared in a loop contains unsafe references to variable(s) 'i'  no-loop-func
Disabled this error because the function was just removing the object referenced at i from a dictionary declared outside of the loop. No unsafe actions resulted from this.
