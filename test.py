import requests

# Flask app running on localhost
BASE_URL = 'http://127.0.0.1:5000'

# Step 1: Log in to set the session cookie
login_data = {'username': 'admin', 'password': 'password'}
login_response = requests.post(f"{BASE_URL}/login", json=login_data)

print('POST Response (Login):', login_response.json())

if login_response.status_code != 200:
    print("Login failed, aborting further requests")

# Extract the session cookie from the login response
session_cookie = login_response.cookies.get('session')

if not session_cookie:
    print("Session cookie not found, aborting further requests")
else:
    # Prepare headers with the cookie for subsequent requests
    headers = {
        'Cookie': f'session={session_cookie}'
    }

    # Step 2: POST to set the session
    post_data = {'my_key': 'initial_value'}
    post_response = requests.post(f"{BASE_URL}/session", json=post_data, headers=headers)
    # print('POST Response (Check Session):', get_response.json()['session']['my_key'], '\n\nfull session:', get_response.json())

    # Step 3: GET to check the session
    get_response = requests.get(f"{BASE_URL}/session", headers=headers)
    print('GET Response value:', get_response.json()['session']['my_key'], '\n\nfull session:', get_response.json())

    # Step 4: POST to modify the session
    post_data = {'my_key': 'updated_value'}
    post_response = requests.post(f"{BASE_URL}/session", json=post_data, headers=headers)
    # print('POST Response (Check Session):', get_response.json()['session']['my_key'], '\n\nfull session:', get_response.json())

    # Step 5: GET to check if session is modified
    get_response = requests.get(f"{BASE_URL}/session", headers=headers)
    print('\n\nGET Response value:', get_response.json()['session']['my_key'], '\n\nfull session:', get_response.json())
    
    assert get_response.json()['session']['my_key'] == 'updated_value'
