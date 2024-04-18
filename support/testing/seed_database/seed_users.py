import requests
import random
import os
import time

# Define the base URL and headers for requests
# get base URL from enviroment varables
base_url = os.getenv('BASE_URL') or "http://localhost:8000"
headers = {'Content-Type': 'application/json'}

print("such testing is currently working only with docker compose")
# try to connect to the base_url, when alive 
while True:
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print(f"Connected to {base_url}")
            break
    except requests.ConnectionError:
        print(f"Failed to connect to {base_url}, retrying in 5 seconds")
        time.sleep(5)

# Define all available preferences and restrictions
preferences_list = ["Fast Food", "Fusion", "Street Food", "French", "Spanish", "Italian", "Greek", 
                    "Portuguese", "Norwegian", "German", "Czech", "Turkish", "Japanese", 
                    "Indian", "Chinese", "Korean", "Eritrean"]
restrictions_list = ["Vegetarian", "Vegan", "lactose_intolerant", "Ovo", "Pescetarian", 
                     "Pollo", "Halal", "Kosher"]

# Function to create users and update their preferences
def create_and_update_users():
    for i in range(1, 11):
        username = f'user{i}'
        email = f'{username}@uzh.ch'
        user_data = {
            "username": username,
            "email": email,
            "password": "user"
        }

        # Create user
        while True:
            try:
                response = requests.post(base_url+"/authenticator/user", headers=headers, json=user_data)
                if response.status_code in [200, 201]:
                    print(f'Successfully created {username}')
                    # Extract the access_token from the response
                    access_token = response.json().get('access_token')
                    if access_token:
                        # Randomly select preferences and restrictions
                        chosen_preferences = random.sample(preferences_list, 5)
                        chosen_restrictions = random.sample(restrictions_list, random.randint(0, 1))

                        # Prepare the data for updating user preferences
                        update_data = {
                            "preferences": chosen_preferences,
                            "restrictions": chosen_restrictions
                        }

                        # Set the authorization header with the access token
                        auth_headers = {
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {access_token}'
                        }

                        # Update user preferences
                        update_response = requests.patch(f'{base_url}/users', headers=auth_headers, json=update_data)
                        if update_response.status_code in [200, 201]:
                            print(f'Successfully updated preferences for {username}')
                        else:
                            print(f'Failed to update preferences for {username}: {update_response.text}')
                    else:
                        print(f'Access token not found for {username}')
                else:
                    print(f'Failed to create {username}: {response.text}')
                break
            except requests.ConnectionError:
                print(f'Failed to connect to {base_url}')
                print(f'Retrying in 5 seconds')
                time.sleep(5)

# Run the function to create and update users
create_and_update_users()