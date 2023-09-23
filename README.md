# API Development and Documentation Tunga Accessment

## Online Note App

The online Notes is be use by staff to log thier personal notes. The online noe app is developed using Django Rest Framework (DRF).

### Features

1. User Registration - User should be able to register with the follwing details:

- First name
- Last name
- Email
- Password

2. User login: User can log in with:

   - Email
   - Password

3. Password recovery: users can recovery password when forgotton, by upadting/reseting password using `Email link`.

4. User can perform CRUD operation on Dairy notes beloging to them.

5. User can order notes based on lastest

6. User can filter notes based on:

   - Unfinished
   - Overdute notes
   - Done notes

7. Sort all note by:

   - Due date
   - Priority
   - Created-time

8. Export notes list to pdf and csv

9. Share or publish th notes over an email

10. Set email reminder for notes

## Starting

#### Prerequisite

- Note: You need to have python3.x [installed](https://www.tutorialspoint.com/how-to-install-python-in-windows) on you machine.

##### Steps

1.  Clone the project into your machine.

    ```cmd
          git clone https://github.com/Ginohmk/online-note-book-drf.git
    ```

2.  Navigate into the project folder.

    ```cmd
       cd online-note-book-drf
    ```

3.  Start your virtual environment (mac/linux and windows)

    ```cmd
      source/bin/activate
    ```

    Or

    ```cmd
      \venv\Scripts\activate.bat
    ```

4.  Install project dependencies.

    ```cmd
      pip install -r requirements.txt
    ```

5.  Start server

    ```
      ./manage.py runserver
    ```

### Folder Structure

### Backend APIs

### Attributes
