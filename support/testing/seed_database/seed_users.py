import requests
import random
import os
import time
import json
import base64

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
restrictions_list = ["Vegetarian", "Vegan", "Lactose Intolerant", "Ovo", "Pescetarian", 
                     "Pollo", "Halal", "Kosher"]


def upload_review_image(user_data, review_id, image_path):
    # Prepare headers just for authorization, not content-type
    patch_headers = {
        'Authorization': f'Bearer {user_data["access_token"]}',
    }

    # Prepare multipart/form-data payload
    with open(image_path, 'rb') as img_file:
        files = {
            'review_id': (None, str(review_id), 'text/plain'),
            'image': (os.path.basename(image_path), img_file, 'image/png')
        }

        # Send the PATCH request
        response = requests.patch(f"{base_url}/reviews/image", headers=patch_headers, files=files)
        if response.status_code in [200, 201]:
            print(f'Successfully uploaded image for review {review_id}')
        else:
            print(f'Failed to upload image for review {review_id}: Status Code {response.status_code}')
            try:
                json_response = response.json()
                print(f'JSON Response: {json.dumps(json_response, indent=4)}')
            except ValueError:
                print(f'Response Text: {response.text}')

# Function to create users and update their preferences
def add_review(user_data, image_path):
    review_texts = [
        "It was a memorable experience, best meal ever!",
        "Truly a delightful visit with top-notch service!",
        "The ambiance was fantastic, and the food was out of this world!",
        "A culinary journey that I would highly recommend to anyone!",
        "Exceptional service and amazing flavors, will visit again!"
    ]
    review_text = random.choice(review_texts)
    review_data = {
        "text": review_text,
        "rating": random.randint(1, 5),
        "location": {
            "id": "ChIJTXV7SEKhmkcRcLisA93CPms",
            "name": "Bar am Wasser",
            "type": "bar",
            "coordinates": {"x": "47.367551", "y": "8.541579400000002"}
        }
    }
    auth_headers = {
        'Authorization': f'Bearer {user_data["access_token"]}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{base_url}/reviews", headers=auth_headers, json=review_data)
    if response.status_code in [200, 201]:
        review_id = response.json()['id']
        print(f'Successfully added review for {user_data["username"]}')

        # Prepare the image upload PATCH request
        upload_review_image(user_data, review_id, image_path)
       
    else:
        print(f'Failed to add review for {user_data["username"]}: {response.text}')

def decode_jwt(token):
    # Split the token to get header, payload, and signature
    header_b64, payload_b64, signature = token.split('.')
    # Decode the payload from base64
    payload_bytes = base64.urlsafe_b64decode(payload_b64 + '==')  # Padding may be required
    # Convert bytes to string, then to dictionary
    payload = json.loads(payload_bytes.decode('utf-8'))
    return payload

def follow(follower, followee):
    follower_bearer_token = follower['access_token']
    followee_id = decode_jwt(followee['access_token'])['sub']
    url = f"{base_url}/users/following/{followee_id}"  # Modify the base URL as necessary.
    headers = {
        'Authorization': f'Bearer {follower_bearer_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.patch(url, headers=headers)
    
    if response.status_code == 200:
        print('Follow request successful.')
    else:
        print(f'Failed to follow. Status code: {response.status_code} - Reason: {response.reason}')
    
    return response

def create_user(i):
    username = f'user{i}'
    email = f'{username}@uzh.ch'
    user_data = {
        "username": username,
        "email": email,
        "password": "user"
    }

    response = requests.post(base_url+"/authenticator/user", headers=headers, json=user_data)

    if response.status_code in [200, 201]:
        print(f'Successfully created {username}')
        access_token = response.json().get('access_token')
        id = response.json().get('id')
        if not access_token:
            raise Exception(f'Access token not found for {username}')
        user_data['access_token'] = access_token
        user_data['id'] = id

        return user_data
    else:
        raise Exception(f'Failed to create {username}: {response.text}')

def create_and_update_users():
    path_review_images = './images/review'
    image_files = os.listdir(path_review_images)
    for i in range(1, 11):
    # i = 29
    # for i in range(i, i+1):
        while True:
            try:
                user_data = create_user(i)
                access_token = user_data['access_token'] 
                username = user_data['username']
                user_array[username] = user_data

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
                    image_path = os.path.join(path_review_images, random.choice(image_files))
                    add_review(user_data, image_path)
                else:
                    print(f'Failed to update preferences for {username}: {update_response.text}')
                break
            except requests.ConnectionError as e:
                print(f'e: {e}')
                print(f'Failed to connect to {base_url}')
                print('Retrying in 5 seconds')
                time.sleep(5)
            except Exception as e:
                print(f'e: {e}')
                print(f'Failed to connect to {base_url}')
                print('Retrying in 5 seconds')
                time.sleep(5)

# Run the function to create and update users
print("Creating users and updating preferences...")

user_array = {}
create_and_update_users()

follow(user_array['user5'], user_array['user6'])
follow(user_array['user4'], user_array['user3'])
follow(user_array['user4'], user_array['user5'])
follow(user_array['user4'], user_array['user6'])
follow(user_array['user4'], user_array['user7'])
follow(user_array['user4'], user_array['user8'])
follow(user_array['user4'], user_array['user9'])
follow(user_array['user4'], user_array['user10'])