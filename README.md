# COMP3011CW1
# USAGE:
To start the project: open a command line terminal and type 'python manage.py runserver'
To open the client application: open another terminal and type 'python client.py'
Note: There are 7 commands available in this client application:
1. register: register for an account to the service. This requires a username, email and password.
2. login: log in to the application
3. logout: logs out of the application
4. list: lists all module instances and the professor(s) teaching them
5. view: view the rating of all professors
6. average: view the average ratings of a certain professor in a certain module. The syntax for this command is 'average professor_id module_code'. professor_id is the unique id of a professor and module_code is the code of a module. 
7. rate: allows the user to rate the teaching of a professor in a certain module instance. The syntax for this command is 'rate professor_id module_code year semester rating'. professor_id is the unique id of a professor, module_code is the code of a module, year is the teaching year, semester is a semester number and rating is an integer value between 1 to 5. 