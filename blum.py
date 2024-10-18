# Made with ❤ by @adearman
# Join tele channel for update t.me/ghalibie
import argparse
import random
from urllib.parse import parse_qs, unquote
import requests
from requests.structures import CaseInsensitiveDict
import time
from datetime import datetime, timezone

start_time = datetime.now()  # Tentukan waktu mulai saat bot dijalankan

headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

def load_credentials():
    # Membaca token dari file dan mengembalikan daftar token
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        # print("Token berhasil dimuat.")
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return 
    except Exception as e:
        print("Terjadi kesalahan saat memuat query:", str(e))
        return 

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

def save(id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def update(id, new_token):
    tokens = json.loads(open("tokens.json").read())
    if str(id) in tokens.keys():
        tokens[str(id)] = new_token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))
    else:
        return None

def delete(id):
    tokens = json.loads(open("tokens.json").read())
    if str(id) in tokens.keys():
        del tokens[str(id)]
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))
    else:
        return None
    
def delete_all():
    open("tokens.json", "w").write(json.dumps({}, indent=4))


def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def make_request(method, url, headers, json=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, json=json)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, data=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json, data=data)
        else:
            raise ValueError("Invalid method.")
        
        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code: {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

def check_tasks(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    
    response = requests.get('https://game-domain.blum.codes/api/v1/tasks', headers=headers)
    if response.status_code == 200:
        mains = response.json()
        for main in mains:
            main_tasks = main.get('tasks',[])
            subSections = main.get('subSections',[])
            
            for subs in subSections:
                title_task = subs.get('title')
                print_(f"Main Task Title : {title_task}")
                tasks = subs.get('tasks')
                for task in tasks:
                    sub_title = task.get('title',"")
                    if 'invite' in sub_title.lower():
                        print_(f"{sub_title} Skipping Quest")
                    elif 'farm' in sub_title.lower():
                        print_(f"{sub_title} Skipping Quest")
                    else:
                        if task['status'] == 'CLAIMED':
                            print_(f"Task {title_task} claimed  | Status: {task['status']} | Reward: {task['reward']}")
                        elif task['status'] == 'NOT_STARTED':
                            print_(f"Starting Task: {task['title']}")
                            start_task(token, task['id'],sub_title)
                            validationType = task.get('validationType')
                            if validationType == 'KEYWORD':
                                time.sleep(2)
                                validate_task(token, task['id'],sub_title)
                            time.sleep(5)
                            claim_task(token, task['id'],sub_title)
                        elif task['status'] == 'READY_FOR_CLAIM':
                            claim_task(token, task['id'],sub_title)
                        elif task['status'] == 'READY_FOR_VALIDATE':
                            validate_task(token, task['id'],sub_title)
                            time.sleep(5)
                            claim_task(token, task['id'],sub_title)
                        else:
                            print_(f"Task already started: {sub_title} | Status: {task['status']} | Reward: {task['reward']}")
    else:
        print_(f"Failed to get tasks")
    

def start_task(token, task_id, title):
    time.sleep(2)
    url = f'https://earn-domain.blum.codes/api/v1/tasks/{task_id}/start'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = make_request('post', url, headers=headers)
        if response is not None:
            print_(f"Task {title} started")
        else:
            print_(f"Failed to start task {title}")
        return 
    except:
        print_(f"Failed to start task {title} ")

def validate_task(token, task_id, title, word=None):
    time.sleep(2)
    url = f'https://earn-domain.blum.codes/api/v1/tasks/{task_id}/validate'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    payload = {'keyword': word}
    try:
        response =  response = make_request('post',url, headers=headers, json=payload)
        if response is not None:
            print_(f"Task {title} validating")
        else:
            print_(f"Failed to validate task {title}")
        return 
    except:
        print_(f"Failed to validate task {title} ")

def claim_task(token, task_id,title):
    time.sleep(2)
    print_(f"Claiming task {title}")
    url = f'https://earn-domain.blum.codes/api/v1/tasks/{task_id}/claim'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response =  response = make_request('post',url, headers=headers)
        if response is not None:
            print_(f"Task {title} claimed")
        else:
            print_(f"Failed to claim task {title}")
    except:
        print_(f"Failed to claim task {title} ")

        
def get_new_token(query_id):
    import json
    # Header untuk permintaan HTTP
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "priority": "u=1, i",
        "referer": "https://telegram.blum.codes/"
    }

    data = json.dumps({"query": query_id})
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    time.sleep(2)
    print_(f"Getting Token...")
    response = make_request('post',url, headers=headers, data=data)
    if response is not None:
        print_(f"Token Created")
        response_json = response.json()
        return response_json['token']['refresh']
    else:
        print_(f"Failed get token")
        return None

# Fungsi untuk mendapatkan informasi pengguna
def get_user_info(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response =  response = make_request('get','https://gateway.blum.codes/v1/user/me', headers=headers)
    if response is not None:
        return response.json()

def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response =  response = make_request('get','https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_(f"Failed getting data balance")
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Failed ")

def play_game(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = make_request('post','https://game-domain.blum.codes/api/v2/game/play', headers=headers)
        if response is not None:
            return response.json()
        else:
            return None
    except Exception as e:
        print_(f"Failed play game, Error {e}")

def claim_game(token, game_id, point, dogs):
    time.sleep(2)
    url = "https://game-domain.blum.codes/api/v2/game/claim"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["authorization"] = "Bearer "+token
    headers["content-type"] = "application/json"
    headers["origin"] = "https://telegram.blum.codes"
    headers["priority"] = "u=1, i"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    data = create_payload(game_id=game_id, point=point, dogs=dogs)
    payload = {'payload' : data}
    try:
        response = make_request('post', url, headers=headers, data=json.dumps(payload))
        if response is not None:
            return response
        else:
            return None
    
    except Exception as e:
        print_(f"Failed Claim game, error: {e}")
    return None

def get_game_id(token):
    game_response = play_game(token)
    trying = 5
    if game_response is None or game_response.get('gameId') is None:
        while True:
            if trying == 0:
                break
            print_("Play Game : Game ID is None, retrying...")
            game_response = play_game(token)
            if game_response is not None:
                game_id = game_response.get('gameId', None)
            else:
                game_id = None
            if game_id is not None:
                return game_response['gameId']
                break
            else:
                print_('Game id Not Found, trying to get')
            trying -= 1
    else:
        return game_response['gameId']

def claim_balance(token):
    
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        time.sleep(2)
        response = make_request('post','https://game-domain.blum.codes/api/v1/farming/claim', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_("Failed Claim Balance")

    except Exception as e:
        print_(f"Failed claim balance, error: {e}")
    return None

def start_farming(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
 
        time.sleep(2)
        response = make_request('post','https://game-domain.blum.codes/api/v1/farming/start', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_("Failed Claim Balance")

    except Exception as e:
        print_(f"Failed claim balance, error: {e}")
    return None

def check_balance_friend(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = make_request('get', 'https://user-domain.blum.codes/api/v1/friends/balance', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_("Failed Check ref")
    
    except Exception as e:
        print_(f"Failed Check ref, error: {e}")
    return None

def claim_balance_friend(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = make_request('post', 'https://user-domain.blum.codes/api/v1/friends/claim', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_("Failed Claim ref Balance")
    except Exception as e:
        print_(f"Failed Claim ref, error: {e}")
    return None

# cek daily 
import json
def check_daily_reward(token):
    headers = {
        'Authorization': f'Bearer {token}',
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
        response = make_request('post','https://game-domain.blum.codes/api/v1/daily-reward?offset=-420', headers=headers)
        if response is not None:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
      
    return None


def check_tribe(token):
    url = 'https://game-domain.blum.codes/api/v1/tribe/my'
    headers = {
        'Authorization': f'Bearer {token}',
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
        response = make_request('get', url, headers=headers)
        if response is not None:
            return response.json()
        else:
            return None
    except Exception as e:
        print_(f"Failed Check Tribe, error: {e}")
    return None


def join_tribe(token):
    url ='https://game-domain.blum.codes/api/v1/tribe/a8e9ee05-b615-4c46-812c-1f8c5a42f93e/join'
    headers = {
        'Authorization': f'Bearer {token}',
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
        response = make_request('post', url, headers=headers)
        if response is not None:
            return "OK"
        else:
            js = response
            print_(js.get('message'))
            return None
    except Exception as e:
        print_(f"Failed join tribe, error: {e}")
    return None
checked_tasks = {}

def elig_dogs(token):
    url = 'https://game-domain.blum.codes/api/v2/game/eligibility/dogs_drop'
    headers = {
        'Authorization': f'Bearer {token}',
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
        response = make_request('get', url, headers=headers)
        if response is not None:
            data = response.json()
            eligible = data.get('eligible',False) 
            print_(f"Eligible Dogs Drop: {eligible}")
            return eligible

    except Exception as e:
        print_(f"Failed join tribe, error: {e}")
    return None

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")

def generate_token():
    queries = load_credentials()
    for index, query in enumerate(queries, start=1):
        parse = parse_query(query)
        user = parse.get('user')
        print_(f"Account {index}  | {user.get('username','')}")
        token = get(user['id'])
        if token == None:
            print_("Generate token...")
            time.sleep(2)
            token = get_new_token(query)
            save(user.get('id'), token)
            print_("Generate Token Done!")

def get_verification():
    url = 'https://raw.githubusercontent.com/boytegar/BlumBOT/refs/heads/master/verif.json'
    data = requests.get(url=url)
    return data.json()

def get_data_payload():
    url = 'https://raw.githubusercontent.com/zuydd/database/main/blum.json'
    data = requests.get(url=url)
    return data.json()

def create_payload(game_id, point, dogs):
    data = get_data_payload()
    payload_server = data.get('payloadServer',[])
    filtered_data = [item for item in payload_server if item['status'] == 1]
    random_id = random.choice([item['id'] for item in filtered_data])
    url = f'https://{random_id}.vercel.app/api/blum'
    payload = {
            'game_id': game_id,
            'points': point,
            'dogs': dogs
        }
    response = requests.post(url, json=payload)
    if response is not None:
        data = response.json()
        if "payload" in data:
            return data["payload"]
        return None

def find_by_id(json_data, id):
    for key, value in json_data.items():
        if key == id:
            return value
    return None

def main():

    claim_ref_enable = input("want claim ref? y/n  : ").strip().lower()      
    # check_task_enable = input("want claim task? y/n  : ").strip().lower()
    check_task_enable = 'n'
    selector_game = input("auto playing game ? y/n  : ").strip().lower()
    total_blum = 0
    while True:
        delete_all()
        queries = load_credentials()
        delay_time = random.randint(3600, 3620)*8
        start_time = time.time()
        now = datetime.now().isoformat(" ").split(".")[0]
        for index, query in enumerate(queries, start=1):
            useragents = getuseragent(index)
            parse = parse_query(query)
            user = parse.get('user')
            time.sleep(2)
            print_(f"===== Account {index}  | {user.get('username','')} =====")
            token = get(user['id'])
            if token == None:
                print_("Generate token...")
                time.sleep(2)
                token = get_new_token(query)
                save(user.get('id'), token)
                print_("Generate Token Done!")
            
            print_(f"Getting Info....")
            balance_info = get_balance(token)
            if balance_info is None:
                print_(f"Failed to Get information")
                continue
            else:
                available_balance_before = balance_info['availableBalance']  

                balance_before = f"{float(available_balance_before):,.0f}".replace(",", ".")
                total_blum += float(available_balance_before)
                print_(f"Balance       : {balance_before}")
                print_(f"Tiket Game    : {balance_info['playPasses']}")
                data_tribe = check_tribe(token)
                time.sleep(2)
                if data_tribe is not None:
                    print_(f"Tribe         : {data_tribe.get('title')} | Member : {data_tribe.get('countMembers')} | Balance : {data_tribe.get('earnBalance')}")
                else:
                    print_(f'Tribe not Found')
                    time.sleep(1)
                    print_(f'Joininng Tribe...')
                    join = join_tribe(token)
                    if join is not None:
                        print_(f'Join Tribe Done')

                farming_info = balance_info.get('farming')
        
                if farming_info:
                    end_time_ms = farming_info['endTime']
                    end_time_s = end_time_ms / 1000.0
                    end_utc_date_time = datetime.fromtimestamp(end_time_s, timezone.utc)
                    current_utc_time = datetime.now(timezone.utc)
                    time_difference = end_utc_date_time - current_utc_time
                    hours_remaining = int(time_difference.total_seconds() // 3600)
                    minutes_remaining = int((time_difference.total_seconds() % 3600) // 60)
                    farming_balance = farming_info['balance']
                    farming_balance_formated = f"{float(farming_balance):,.0f}".replace(",", ".")
                    print_(f"Claim Balance : {hours_remaining} jam {minutes_remaining} menit | Balance: {farming_balance_formated}")

                    if hours_remaining < 0:
                        print_(f"Claim Balance: Claiming balance...")
                        claim_response = claim_balance(token)
                        if claim_response is not None:
                            print_(f"Claim Balance : Claimed: {claim_response['availableBalance']}                ")
                            print_(f"Claim Balance : Starting farming...")
                            start_response = start_farming(token)
                            if start_response:
                                print_(f"Claim Balance : Farming started.")
                            else:
                                print_(f"Claim Balance : Failed start farming")
                        else:
                            print_(f"Claim Balance : Failed claim")
                            start_response = start_farming(token)
                            if start_response is not None:
                                print_(f"Claim Balance : Farming started.")
                            else:
                                print_(f"Claim Balance : Failed start farming")
                else:
                    print_(f"Claim Balance : failed get farming information")
                    print_(f"Claim Balance : Claiming balance...")
                    claim_response = claim_balance(token)
                    if claim_response is not None:
                        print_(f"Claim Balance : Claimed               ")
                        print_(f"Claim Balance : Starting farming...")
                        start_response = start_farming(token)
                        if start_response:
                            print_(f"Claim Balance : Farming started.")
                        else:
                            print_(f"Claim Balance : Failed start farming")
                    else:
                        print_(f"Claim Balance : failed claim")
                        start_response = start_farming(token)
                        if start_response:
                            print_(f"Claim Balance : Farming started.")
                        else:
                            print_(f"Claim Balance : Failed start farming")

            print_(f"Daily Reward : Checking daily reward...")
            daily_reward_response = check_daily_reward(token)
            if daily_reward_response is None:
                print_(f"Daily Reward : Failed Check Daily Reward.")
            else:
                if daily_reward_response.get('message') == 'same day':
                    print_(f"Daily Reward : Daily Reward Claimed")
                elif daily_reward_response.get('message') == 'OK':
                    print_(f"Daily Reward : Daily Reward Done Claim!")
                else:
                    print_(f"Daily Reward : Failed Check Daily Reward. {daily_reward_response}")

            elig_dogs(token)
            print_(f"Reff Balance : Checking reff balance...")
            if claim_ref_enable == 'y':
                friend_balance = check_balance_friend(token)
                if friend_balance is not None:
                    if friend_balance['canClaim']:
                        print_(f"Reff Balance: {friend_balance['amountForClaim']}")
                        print_(f"Claiming Ref balance.....")
                        friend_balance = friend_balance.get('amountForClaim',"0")
                        if friend_balance != "0":
                            claim_friend_balance = claim_balance_friend(token)
                            if claim_friend_balance:
                                claimed_amount = claim_friend_balance['claimBalance']
                                print_(f"Reff Balance : Claim Done : {claimed_amount}")
                            else:
                                print_(f"Reff Balance : Failed Claim")
                        else:
                            print_('Not enough reff balance')
                    else:
                        can_claim_at = friend_balance.get('canClaimAt')
                        if can_claim_at is not None:
                            claim_time = datetime.fromtimestamp(int(can_claim_at) / 1000)
                            current_time = datetime.now()
                            time_diff = claim_time - current_time
                            hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print_(f"Reff Balance : Claimed inf {hours} hours {minutes} minutes")
                        else:
                            print_(f"Reff Balance : False                                 ")
                else:
                    print_(f"Reff Balance : False cek reff balance")
            else:
                print_(f"Reff Balance : Skipped !                    ")
        # break    
        
        if selector_game =='y':
            for index, query in enumerate(queries, start=1):
                mid_time = time.time()
                waktu_tunggu = delay_time - (mid_time-start_time)
                if waktu_tunggu <= 0:
                    break
                time.sleep(3)
                parse = parse_query(query)
                user = parse.get('user')
                token = get(user['id'])
                print_(f"XXXX==XXXX Account {index}  | {user.get('username','')} XXXX==XXXX")
                if token == None:
                    print_("Generate token...")
                    time.sleep(2)
                    token = get_new_token(query)
                    save(user.get('id'), token)
                    print_("Generate Token Done!")

                balance_info = get_balance(token)
                available_balance_before = balance_info['availableBalance'] 
                balance_before = f"{float(available_balance_before):,.0f}".replace(",", ".")
                # if check_task_enable == 'y':  
                #     print_(f"Checking tasks...")
                #     check_tasks(token)
                # continue

                if balance_info.get('playPasses') <= 0:
                    total_blum += float(available_balance_before) 
                    print_('No have ticket For Playing games')
                data_elig = elig_dogs(token)
                while balance_info['playPasses'] > 0:
                    print_(f"Play Game : Playing game...")
                    gameId = get_game_id(token)
                    print_(f"Play Game : Checking game...")
                    taps = random.randint(260, 280)
                    delays = random.randint(35, 45)
                    dogs = random.randint(25,30)*5
                    time.sleep(delays)
                    if data_elig:
                        claim_response = claim_game(token, gameId, taps, dogs)
                    else:
                        dogs = 0
                        claim_response = claim_game(token, gameId, taps, dogs)
                    if claim_response is None:
                        print_(f"Play Game : Game still running waiting...")
                    while True:
                        if claim_response.text == '{"message":"game session not finished"}':
                            time.sleep(10)  
                            print_(f"[{now}] Play Game : Game still running waiting....")
                            claim_response = claim_game(token, gameId, taps, dogs)
                            if claim_response is None:
                                print_(f"[{now}] Play Game : Failed Claim game point, trying...")
                        elif claim_response.text == '{"message":"game session not found"}':
                            print_(f"[{now}] Play Game : Game is Done")
                            mid_time = time.time()
                            waktu_tunggu = delay_time - (mid_time-start_time)
                            if waktu_tunggu <= 0:
                                break
                            break
                        elif 'message' in claim_response and claim_response['message'] == 'Token is invalid':
                            print_(f"[{now}] Play Game : Token Not Valid, Take new token...")
                            continue  
                        else:
                            print_(f"Play Game : Game is Done, Reward Blum Point : {taps} , Dogs : {dogs}")
                            break

                    balance_info = get_balance(token) 
                    if balance_info is None: 
                        print_(f"Play Game failed get information ticket")
                    else:
                        available_balance_after = balance_info['availableBalance'] 
                        
                        before = float(available_balance_before) 
                        after =  float(available_balance_after)
                        
                        total_balance = after - before  
                        print_(f"Play Game: You Got Total {total_balance} From Playing Game")
                        if balance_info['playPasses'] > 0:
                            print_(f"Play Game : Tiket still ready, Playing game again...")
                            continue  
                        else:
                            total_blum += before
                            total_blum += total_balance
                            print_(f"Play Game : Tiket Finished.")
                            break

        end_time = time.time()
        delete_all()
        print_(f"========= ALL ID DONE =========")
        total_acc = len(queries)
        
        waktu_tunggu = delay_time - (end_time-start_time)
        print_(f"Total Account = {total_acc} | Total Points Blum = {round(total_blum)}")
        printdelay(waktu_tunggu)
        if waktu_tunggu >= 0:
            time.sleep(waktu_tunggu)

def completed_task(token, stask):
    sub_title = stask.get('title',"")
    if stask.get('status','') == 'CLAIMED':
        print_(f"Task {sub_title} claimed  | Status: {stask.get('status','')} | Reward: {stask['reward']}")
    elif stask.get('status','') == 'NOT_STARTED':
        print_(f"Starting Task: {stask['title']}")
        start_task(token, stask['id'],sub_title)
        validationType = stask.get('validationType')
        if validationType == 'KEYWORD':
            time.sleep(2)
            verif = get_verification()
            words = find_by_id(verif, stask['id'])
            print_(f"Verification : {words}")
            validate_task(token, stask['id'],sub_title, word=words)
        time.sleep(5)
        claim_task(token, stask['id'],sub_title)
    elif stask.get('status','') == 'READY_FOR_CLAIM':
        claim_task(token, stask['id'],sub_title)
    elif stask.get('status','') == 'READY_FOR_VERIFY': 
        validationType = stask.get('validationType')
        if validationType == 'KEYWORD':
            verif = get_verification()
            words = find_by_id(verif, stask['id'])
            print_(f"Verification : {words}")
            time.sleep(2)
            validate_task(token, stask['id'],sub_title, word=words)
        else:
            validate_task(token, stask['id'],sub_title)
        time.sleep(5)
        claim_task(token, stask['id'],sub_title)
    else:
        print_(f"Task already started: {sub_title} | Status: {stask.get('status','')} | Reward: {stask['reward']}")

def task_main():  
    delete_all()
    queries = load_credentials()
    now = datetime.now().isoformat(" ").split(".")[0]
    for index, query in enumerate(queries, start=1):
            time.sleep(3)
            parse = parse_query(query)
            user = parse.get('user')
            token = get(user['id'])
            print_(f"[ === Account {index}  | {user.get('username','')} === ]")
            if token == None:
                print_("Generate token...")
                time.sleep(2)
                token = get_new_token(query)
                save(user.get('id'), token)
                print_("Generate Token Done!")

            print_(f"Checking tasks...")

            time.sleep(2)
            headers = {
                'Authorization': f'Bearer {token}',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'content-length': '0',
                'origin': 'https://telegram.blum.codes',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
            }
    
            response = make_request('get','https://earn-domain.blum.codes/api/v1/tasks', headers=headers)
            if response is not None:
                mains = response.json()
                for main in mains:
                    main_tasks = main.get('tasks',[])
                    subSections = main.get('subSections',[])
                    title = main.get('title', "")
                    if title == "New":
                        print_(f"Title : {title} Skip")
                    else:
                        print_(f"Title : {title} Start")
                        for task in main_tasks:
                            sub_title = task.get('title',"")
                            subtask = task.get('subTasks',[])
                            for stask in subtask:
                                sub_title = stask.get('title',"")
                                if 'invite' in sub_title.lower():
                                    print_(f"{sub_title} Skipping Quest")
                                elif 'farm' in sub_title.lower():
                                    print_(f"{sub_title} Skipping Quest")
                                else:
                                    completed_task(token, stask)
                            
                            if 'invite' in sub_title.lower():
                                print_(f"{sub_title} Skipping Quest")
                            elif 'farm' in sub_title.lower():
                                print_(f"{sub_title} Skipping Quest")
                            else:
                                completed_task(token, task)

                    for subs in subSections:
                        title = subs.get('title')
                        if title == "New":
                            print_(f"Title : {title} Skip")
                        else:
                            print_(f"Title : {title} Start")
                            print_(f"Main Task Title : {title}")
                            tasks = subs.get('tasks')
                            for task in tasks:
                                sub_title = task.get('title',"")
                                if 'invite' in sub_title.lower():
                                    print_(f"{sub_title} Skipping Quest")
                                elif 'farm' in sub_title.lower():
                                    print_(f"{sub_title} Skipping Quest")
                                else:
                                    completed_task(token, task)
            else:
                print_(f"Failed to get tasks")
            # continue

def start():
    print(r"""
        
                    BLUM BOT
    find new airdrop & bot here: t.me/sansxgroup
              
        select this one :
        1. claim daily & auto play game
        2. clear task
          
          """)
    selector = input("Select the one  : ").strip().lower()

    if selector == '1':
        main()
    elif selector == '2':
        task_main()
    else:
        exit()
def printdelay(delay):
    now = datetime.now().isoformat(" ").split(".")[0]
    hours, remainder = divmod(delay, 3600)
    minutes, sec = divmod(remainder, 60)
    print(f"{now} | Waiting Time: {hours} hours, {minutes} minutes, and {round(sec)} seconds")

if __name__ == "__main__":
    start()
