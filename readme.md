Nittany Path 
===
Course management system
---

Description
---
    This is the phase 2 for of Nittany Path. The system allows a student or a faculty member to log in using their email and a password assigned to them.
    
    The database has been populated based on the dataset provided by Dr. Wang Chein Lee on Canvas. I divided the dataset provided into smaller csv sheets both manually and by using Python's Pandas. The csv files are then imported to an sqlite database. 
 
    The front-end is designed using HTML, CSS , Bootstrap and JavaScript. The back-end is handled by a Python's Flask Framework. An sqlite database is used to store the names entered.

Requirements
---
    Following are the software requirements that must be installed in order to run the project:
        
        1. Python with Flask and Virtualenv.
        2. PyCharm or Other Editor.
        3. Browser with JavaScript support.

    Important Libraries -
        1. flask_bcrypt - For password hashing.
        2. flask_bootstrap - Adding style elements
        3. flask_login - To create a user login system
        4. flask_sqlalchemy - ORM for Database
        5. flask_wtf - For forms
    If error arises where a module is not found, please make sure that the above libraries are properly installed.

Getting Started
---

    In order to run the project, the following steps must be followed:
    
    1. Create a new flask project in PyCharm and give it a name.
   
    2. Browse to the project directory.
   
    3. Copy all the '.html' files to the 'templates' directory
        ```
        YOUR_FLASK_PROJECT/templates
        ```
   
    4. Copy 'app.py' file to the project root directory and over-rite the existing app.py file.
        ```
        YOUR_FLASK_PROJECT/
        ```
   
    5. Use PyCharm to run the flask app or type the following command in your UNIX terminal.
        ```
        $export FLASK_APP=app
        $flask run app
        ```
   
    6. Browse to the IP address that appears in the terminal.

Navigation
---
* Use the Navigation Bar to navigate between pages.
* On the dashboard, actions are available which can be performed based on the required task.

SQL Database
---
    Names are added to patients table of an sqlite database.

    User has to create an sqlite database named 'nittanypathdb.db'. This is automatically done by PyCharm while creating a new project. However, can be created manually by the following UNIX command.
        ```
        $sqlite3 nittanypathdb.db
        ```  
    
    Data is distributed in the following tables-
       1. Professor
       2. assignments
       3. departments
       4. major_in
       5. teaching_teams
       6. Student
       7. assists_tt
       8. enrolls
       9. posts
       10. works_in      
       11. User
       12. comments
       13. exams
       14. sections
       15. zip_codes     
       16. assignment_assigned
       17. exam_assigned
       18. courses
       19. heads_tt
       20. teaches   
    Required tables are already created and are preloaded with data provided in the sample dataset.

HTML Templates
---

    There are 14 html templates : 

        1. index.html -> Actually the login page to make users login to the system.
        
        2. baseLayout.html -> Base Layout which is extended by the other pages of the web application
        
        3. dashboard.html -> Allows users to navigate between allowed functions.
        
        4. checkInfo.html -> (For Students Only) Displays Personal and Course Information to the users.
        
        5.createAssign -> (For Faculty) To create new assignments and exams.

        6. dropCourse.html -> (For Students) To drop a course.
        
        7. assignments.html -> (For TAs and Faculty) To select assignments to view and update grades.
        
        8. assignGrade.html -> (For TAs and Faculty) To update and assign grades to students on assignments.
        
        9. post.html -> View posts for a course.
        
        10. newPost.html -> Post a new post for any course either teaching or taking.
        
        11. comments.html -> View and post comments on a post
        
        12. registerUser.html -> Register a new user into the users database. (Primarily Used for Extra Credit).
        
        13. newCourse.html -> Create a new course and add it to the database.(Primarily Used for Extra Credit).
        
        14. login.html -> Provides the login form for users to log in.
        

    ** All the HTML templates must be placed inside the 'templates' directory for the project to work properly.**

Python Flask
---

    The code for the flask app is written in the file named 'app.py'. The code contains routes and method to perform functions like redirecting the user to the desired page, adding and deleting names. 

    There are multiple functions divided into several routes. 

    Also, in order to connect the sqlite database to Flask, SQLAlchemy (Object Relational Mapping) has been used to make database queries easier.

    Classes has been created for all the tables which has been used. These classes act as a connection between Python and SQLite.

    Also, for forms, Flask WTForms has been used.

EXTRA CREDIT
---
ADMINISTRATOR - New Administrator can be created with the email 'admin@Nittanystate.edu'. The admin is provided with special privilleges to add a new course, and perform certain functions like adding students, professors etc.

However, for this assignment, Only add a new course has been implemented. 

I have written the code for Add Student as well, however, it has bugs.

Author
---
  * Manan Gupta- MFG5480@psu.edu
  
    Edited code originally provided in starter_code_431W.zip on Canvas by PENN STATE UNIVERSITY.
    
    DATASET for database provided in project_dataset_sp2020_v1.1.zip on Canvas by PENN STATE UNIVERSITY

Citations
---
1.  [Bootstrap Forms](https://getbootstrap.com/docs/4.0/components/forms/) - Used to format the forms.
2. [Flask Login](https://flask-login.readthedocs.io/en/latest/) - Library to log users in.
3. [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/) - Object Relational Mapping for the Database.
4. [Bootstrap Getting Started](https://getbootstrap.com/docs/3.3/getting-started/) - Used to import the base layout, and the navbar.
