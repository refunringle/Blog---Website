# Blog-project

This blog page uses Flask, a Python library.
Blog posts can be viewed by readers, who can then comment on them.
Only those who register as users are able to write and publish blog entries.

A registered user can submit a profile picture, change their email, username, and password, and have access to a dashboard, among other key features, that are highlighted on this website.
Additionally, they have the ability to add and delete categories and posts. 

Backend : Python, Flask, Jinja templating
Frontend : HTML 5, CSS 3, Javascript



**Usage**

* Create a Virtual environment and install requirements.txt  
> pip install -r requirements.txt


**Commands for running the project**

* To Create database named as blog
    
    * To create tables 
    - python3 app.py createdb  

* To run the Flask app 

    - python3 app.py run

* To drop database

    - python3 app.py dropdb
