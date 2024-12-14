import jwt
from datetime import datetime, timedelta
import requests
# Decode the JWT without verifying the signature


def gettoken():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6ImY0ZDc3YTc3LTliMWUtNDhkNi1hZGNjLTc4MDMxODMzMTZmNSIsImV4cCI6MTcyOTQ0NzYzNCwiaWF0IjoxNzI5NDQ0MDM0fQ.7OmnGELQWYqgs7nS4Es9RIQnlKtowh_XZEScM8oIcEo'
    decoded = jwt.decode(token, options={"verify_signature": False})

    # Increment the 'iat' claim by one day
    current_iat = datetime.fromtimestamp(decoded['iat'])
    new_iat = current_iat + timedelta(days=1)
    decoded['iat'] = int(new_iat.timestamp())

    # Re-encode the JWT
    # Note: You should replace 'your_secret_key' with the actual secret key used to sign the original token
    secret_key = 'blum'
    new_token = jwt.encode(decoded, key=None, algorithm='none')


    return new_token

def check_daily_reward(new_token):
    headers = {
        'Authorization': f'Bearer {new_token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/daily-reward', headers=headers)
        if response is not None:
            print(response.json())
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def main():
    new_token = gettoken()
    check_daily_reward(new_token)

main()