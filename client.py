import requests
s = requests.Session()
BASE_URL = 'http://127.0.0.1:8000/'

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    response = s.post(f'{BASE_URL}register/', data={'username': username, 'password': password, 'email': email})
    
    if response.status_code == 201:
        print(response.text)
    else:
        print("Error: ",response.text)
        
def login(url):
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    full_url = f'http://{url}/login/'
    response = s.post(full_url, data={'username': username, 'password': password})
    
    if response.status_code == 200:
        print(response.text)
    elif response.status_code == 400:
        print("Error: ",response.text)
    else:
        print("Failed to login")
        
def logout(): 
    response = s.post(f'{BASE_URL}logout/')
    if response.status_code == 200:                
        print(response.text)
    else:
        print("Error: ",response.text)
    
def list_modules():
    response = s.get(f'{BASE_URL}list/')
    if response.status_code == 200:
        data = response.json()
        
        print('| Code     | Name                      | Year | Semester | Taught by')
        print('-' * 80)
        professors = []
        for module_instance in data:
            professors = [f"{professor['professor_id']}, {professor['professor_name']}" for professor in module_instance['professors']]
            professors = '\n                                                            '.join(professors)
            print(f"| {module_instance['module_code']:4} | {module_instance['module_name'][:25]:25} | {module_instance['year']} | {module_instance['semester']}        | {professors}")
            print('-' * 80)
    else:
        print(f"Error: {response.text}")
        
def view_professors():
    response = s.get(f'{BASE_URL}view/')
    if response.status_code == 200:
        data = response.json()
        
        for professor in data['professors']: #take the professors from the data
            avg_rating = professor['average_rating']
            stars = round(avg_rating)
            stars = '*' * stars 
            print(f"The rating of {professor['name']} ({professor['professor_id']}) is {stars}")
    else:
        print(f"Error: {response.text}")
        
def average_rating(professor_id, module_code):
    response = s.get(f'{BASE_URL}average/', params={'professor_id': professor_id, 'module_code': module_code})
    if response.status_code == 200:
        data = response.json() 
        stars = data['average_rating']
        if stars == '': #if there is no rating yet
            print(f'The rating of {professor_id} in module {module_code} is not available')
        else:
            print(f'The rating of {professor_id} in module {module_code} is {stars}')
            
    else:
        print(f"Error: {response.text}")
        
def rate_professor(professor_id, module_code, year, semester, rating):
    try:
        rating = int(rating)
        if not (1 <= rating <= 5):
            print("Error: Rating must be a whole number between 1 to 5")
            return
    except ValueError:
        print("Error: Rating must be an integer between 1 to 5")
        return
    
    response = s.post(f'{BASE_URL}rate/', data={
                'professor_id': professor_id,
                'module_code': module_code,
                'year': year,
                'semester': semester,
                'rating': rating
    })
    if response.status_code == 201:
        print(response.json()["message"])
    else:
        print(f"Error: {response.text}")               

while True:

    user_input = input("Enter command: ")

    if user_input == 'register': #1.register
        register()
        
    elif user_input.startswith('login'): #2.login
        parts = user_input.split()
        if len(parts) == 2:
            login(parts[1])            
        else:
            print("Usage: login url")
    
    elif user_input == 'logout': #3.logout
        logout()
        
    elif user_input == 'list': #4.list
        list_modules()
        
    elif user_input == 'view': #5.view
        view_professors()
        
    elif user_input.startswith('average'): #6.average
        parts = user_input.split() 
        if len(parts) == 3:
            average_rating(parts[1], parts[2])            
        else:
            print("Usage: average professor_id module_code")
                
    elif user_input.startswith('rate'): #7.rate
        parts = user_input.split()
        if len(parts) == 6:
            rate_professor(parts[1], parts[2], parts[3], parts[4], parts[5])
        else:
            print("Usage: rate professor_id module_code year semester rating")
               
    elif user_input == 'exit':
        print("Goodbye")
        break
    
    else:
        print("Invalid command")
            
            
                
                     
                
        
        
        

    
        