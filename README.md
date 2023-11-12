# CGPA Manager
#### Video Demo:  <URL HERE>
#### Description:
This is my final project for [CS50x](https://cs50.harvard.edu/x/).

It is a web app made using Flask that shows the user their cgpa along with some other useful information like how much gpa they need to score in each semester to achieve their targeted cgpa by the time they graduate. All user information along with their course and gpa data is stored securely in a database. Users can login and update their progress anytime they want. Users need to create an account and login to use this web app.

#### How to use:
After logging in users can set a target by clicking the "Change Target" button on the rightmost card. This will open up a new page that asks the user for their targeted cgpa and the total number of semesters that they have (this is capped at 12).

Now, regardless of whether a user has set a target or not, they can go ahead and start adding their completed semesters by clicking on the "Add Semester" button on the homepage. This will open up a new page that allows them to input course name, credit hours and gpa for each of their courses in that semester. After adding all the info, users need to click the save button to save their semester which will then redirect them back to the homepage. After adding semesters, options to view data of those semesters will also show up on the navbar.
You can watch the [Video Demo](https://github.com/BlasterOverlord/CS50x-Final-Project/tree/main#video-demo--) for a more visual presentation.

#### How I made this:
This web app was made using a python frameword called [Flask](https://flask.palletsprojects.com/en/3.0.x/) which was introduced to us on week 9 of CS50x. I admit that I was a bit lazy with implementing my own design and so I had just went with [C$50 Finance](https://finance.cs50.net/login)'s design.

Now for some nerdy talk, let's take a look at what makes this thing work.
In the root directory we have:
- `app.py` contains code for running most of everything as Flask requires it. It deals with managing routes, storing data to the SQL database and redirecting to different pages of the web app.
- `data.db` is the database where all information including user's login credentials are stored.
- `helpers.py` contains some helper functions that deals with most of the calculations.
- `requirements.txt` contains the names of the external packages that need to be installed on someone's computer if they want to build and run this project locally on their computer.

The `static` folder is where the favicon, CSS and JavaScript files are stored. Inside this folder you'll find `favicon.ico` which is the favicon used in this web app, `script.js` is the JavaScript file that contains code to handle adding and deleting rows when someone's adding a semester and `styles.css` which is the css file containing some navbar customisation and a few custom changes that I wanted to make. I have barely used any custom css and have mostly used Bootstrap to customise my web app. 

The `templates` folder contains all the html files.
- `add.html` is the web page that's displayed when someone clicks on the "Add Semester" button on the homepage.
- `index.html` is the web page that displays the homepage.
- `layout.html` is the jinja template that the other html pages use (except for `add.html` because I did not want to show the semester options on the navbar until after they saved a semester).
- `login.html` is the login page.
- `register.html` is the page that is shown when someone's registering a new account.
- `semester.html` is the web page that is shown when the user clicks one of the semester options shown in the navbar once they've saved a semester.
- `sorry.html` shows a customised apology page when an error is encountered like wrong login credentials etc.
- And finally `target.html` is the page that is shown when someone clicks the "Change Target" button on the homepage to set a target.
