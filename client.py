import requests
s = requests.Session()
while True:

    user_input = input("Enter command: ")

    if user_input == 'register':
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")
        response = s.post(f'http://127.0.0.1:8000/register/', data={'username': username, 'password': password, 'email': email})
        
        if response.status_code == 201:
            print(response.text)
        else:
            print("Error: ",response.text)
        
    if user_input == 'login':
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = s.post(f'http://127.0.0.1:8000/login/', data={'username': username, 'password': password})
        
        if response.status_code == 200:
            print(response.text)
        elif response.status_code == 400:
            print("Error: ",response.text)
        
        
    if user_input == 'logout':
        response = s.post(f'http://127.0.0.1:8000/logout/')
        
        print(response.text)
        
    if user_input == 'list':
        response = s.get(f'http://127.0.0.1:8000/list/')
        if response.status_code == 200:
            data = response.json()
            print('| Code     | Name                      | Year | Semester | Taught by')
            print('-' * 80)
            for module_instance in data['module_instances']:
                print(f"| {module_instance['module_code']:4} | {module_instance['module_name'][:25]:25} | {module_instance['year']} | {module_instance['semester']}        | {module_instance['professors']}")
                print('-' * 80)
        else:
            print(f"Error: {response.text}")
        
    if user_input == 'view':
        response = s.get(f'http://127.0.0.1:8000/view/')
        data = response.json()
        
        for professor in data['professors']: #take the professors from the data
            avg_rating = professor['average_rating']
            stars = round(avg_rating)
            stars = '*' * stars 
            print(f"The rating of {professor['name']} ({professor['professor_id']}) is {stars}")
            
    if user_input.startswith('average'): #expect 3 inputs at once
        parts = user_input.split()
        if len(parts) != 3:
            print("Usage: average professor_id module_code")
        else:
            professor_id = parts[1]
            module_code = parts[2]
            
            response = s.get(f'http://127.0.0.1:8000/average/', params={
                'professor_id': professor_id,
                'module_code': module_code
            })
            if response.status_code == 200:
                data = response.json()
                stars = data['average_rating']
                if stars == '': #if there is no rating yet
                    print(f'The rating of {professor_id} in module {module_code} is not available')
                else:
                    print(f'The rating of {professor_id} in module {module_code} is {stars}')
                    
            else:
                print(f"Error: {response.text}")
                
    if user_input.startswith('rate'):
        parts = user_input.split()
        if len(parts) != 6:
            print("Usage: rate professor_id module_code year semester rating")
               
        else:
            professor_id = parts[1]
            module_code = parts[2]
            year = parts[3]
            semester = parts[4]
            rating = parts[5]
            
            response = s.post(f'http://127.0.0.1:8000/rate/', data={
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
                
                     
                
        
        
        

    
        