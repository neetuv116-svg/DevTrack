# DevTrack 
Django backend API for tracking engineering issues, similar to a stripped-down GitHub Issues. Reporters file issues, issues have a priority and a status, and everything is stored in two JSON files.

# Project structure:

devtrack/
  manage.py
  issues.json          # issue data
  reporters.json       # reporter data
  devtrack/
    settings.py
    urls.py
  issues/
    models.py          # OOP classes (BaseEntity, Reporter, Issue, CriticalIssue, LowPriorityIssue)
    views.py
    urls.py

<img width="940" height="500" alt="image" src="https://github.com/user-attachments/assets/b86aa289-1fa4-47be-bf5b-c11cecc94261" />

# How to run :
1.	Clone the repository and open the project folder.
2.	Created  and activate a virtual environment
3.	Install Django:
 pip install django
4.	 server:
       python manage.py runserver
5.	The API is now available at http://127.0.0.1:8000/. I have Tested it with Postman.



# Responses
•	201 Created: the record was created.
•	400 Bad Request: validation failed, for example {"error": "Title cannot be empty"}.
•	404 Not Found: no record matches the ID, for example {"error": "Issue not found"}.
# OOP design
•	BaseEntity is an abstract base class with an abstract validate() and a shared to_dict().
•	Reporter and Issue both inherit from BaseEntity.
•	CriticalIssue and LowPriorityIssue inherit from Issue and override describe().
•	In POST /api/issues/, the view creates CriticalIssue for critical, LowPriorityIssue for low, and the base Issue for medium and high. It then calls validate() and returns to_dict() plus the describe() message.


   

