# Made with ❤ by @adearman
# Join tele channel for update t.me/ghalibie
import argparse
import random
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

def load_token():
    try:
        with open('token.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        # print("Token berhasil dimuat.")
        return queries
    except FileNotFoundError:
        print("File token.txt tidak ditemukan.")
        return 
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return 

def settoken(token):
    with open("query_id.txt", "w") as file:
        file.write(token + "\n")

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



def parse_arguments():
    parser = argparse.ArgumentParser(description='Blum BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], help='Cek and Claim Task (y/n)')
    parser.add_argument('--reff', type=str, choices=['y', 'n'], help='Apakah ingin claim ref? (y/n, default n)')
    args = parser.parse_args()

    if args.task is None:
        # Jika parameter --task tidak diberikan, minta input dari pengguna
        task_input = input("Apakah Anda ingin cek dan claim task? (y/n, default n): ").strip().lower()
        # Jika pengguna hanya menekan enter, gunakan 'n' sebagai default
        args.task = task_input if task_input in ['y', 'n'] else 'n'

    if args.reff is None:
        # Jika parameter --claim_ref tidak diberikan, minta input dari pengguna
        reff_input = input("Apakah ingin claim ref? (y/n, default n): ").strip().lower()
        # Jika pengguna hanya menekan enter, gunakan 'n' sebagai default
        args.reff = reff_input if reff_input in ['y', 'n'] else 'n'

    return args



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
    try:
        response = requests.get('https://game-domain.blum.codes/api/v1/tasks', headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                titlenya = task['title']
                if task['status'] == 'CLAIMED':
                    print(f"Task {titlenya} claimed  | Status: {task['status']} | Reward: {task['reward']}")
                elif task['status'] == 'NOT_STARTED':
                    print(f"Starting Task: {task['title']}")
                    start_task(token, task['id'],titlenya)
                    time.sleep(5)
                    claim_task(token, task['id'],titlenya)
                else:
                    print(f"Task already started: {task['title']} | Status: {task['status']} | Reward: {task['reward']}")
        else:
            print(f"Failed to get tasks")
    except:
        print(f"Failed to get tasks {response.status_code} ")

def start_task(token, task_id,titlenya):
    time.sleep(2)
    url = f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/start'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"Task {titlenya} started")
        else:
            print(f"Failed to start task {titlenya}")
        return 
    except:
        print(f"Failed to start task {titlenya} {response.status_code} ")

def claim_task(token, task_id,titlenya):
    time.sleep(2)
    print(f"Claiming task {titlenya}")
    url = f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"Task {titlenya} claimed")
        else:
            print(f"Failed to claim task {titlenya}")
    except:
        print(f"Failed to claim task {titlenya} {response.status_code} ")

        
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

    # Data yang akan dikirim dalam permintaan POST
    data = json.dumps({"query": query_id})

    # URL endpoint
    url = "https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"

    # Mencoba mendapatkan token hingga 3 kali
    for attempt in range(3):
        time.sleep(2)
        print(f"Mendapatkan token...")
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print(f"Token berhasil dibuat")
            response_json = response.json()
            return response_json['token']['refresh']
        else:
            print(response.json())
            print(f"Gagal mendapatkan token, percobaan {attempt + 1}", flush=True)
    # Jika semua percobaan gagal

    print(f"Gagal mendapatkan token setelah 3 percobaan.", flush=True)
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
    response = requests.get('https://gateway.blum.codes/v1/user/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        hasil = response.json()
        if hasil['message'] == 'Token is invalid':
            print(f"Token salah, mendapatkan token baru...")
            # Mendapatkan token baru
            new_token = get_new_token()
            if new_token:
                print(f"Token baru diperoleh, mencoba lagi...")
                return get_user_info(new_token)  # Rekursif memanggil fungsi dengan token baru
            else:
                print(f"Gagal mendapatkan token baru.")
                return None
        else:
            print(f"Gagal mendapatkan informasi user")
            return None

# Fungsi untuk mendapatkan saldo
def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    for attempt in range(3):
        time.sleep(2)
        try:
            response = requests.get('https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
            # print(response.json())
            if response.status_code == 200:
                # print(f"Berhasil mendapatkan saldo")
                return response.json()
            else:
                print(f"Gagal mendapatkan saldo, percobaan {attempt + 1}", flush=True)
        except requests.exceptions.ConnectionError as e:
            print(f"Koneksi gagal, mencoba lagi {attempt + 1}", flush=True)
        except Exception as e:
            print(f"Error: {str(e)}", flush=True)
        except:
            print(f"Gagal mendapatkan saldo, mencoba lagi {attempt + 1}", flush=True)
    print(f"Gagal mendapatkan saldo setelah 3 percobaan.", flush=True)
    return None

# Fungsi untuk memainkan game
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
        response = requests.post('https://game-domain.blum.codes/api/v1/game/play', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal bermain game karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal bermain game karena error: {e}")
    return None

def claim_game(token, game_id, points):
    time.sleep(2)
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["authorization"] = "Bearer "+token
    headers["content-type"] = "application/json"
    headers["origin"] = "https://telegram.blum.codes"
    headers["priority"] = "u=1, i"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    data = f'{{"gameId":"{game_id}","points":{points}}}'

    try:
        resp = requests.post(url, headers=headers, data=data)
        return resp
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal mengklaim hadiah game karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal mengklaim hadiah game karena error: {e}")
    return None

def get_game_id(token):
    game_response = play_game(token)
    trying = 5
    while game_response is None or game_response.get('gameId') is None:
        if trying == 0:
            break
        print("Play Game : Game ID is None, retrying...")
        time.sleep(3)
        game_response = play_game(token)
        trying -= 1
        return game_response['gameId']
    return game_response['gameId']

def claim_balance(token):
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
        response = requests.post('https://game-domain.blum.codes/api/v1/farming/claim', headers=headers)
        if response.status_code >= 500:
            print(response.json())
            return None
        elif response.status_code >= 400:
            print(response.json())
            return None
        elif response.status_code >= 200:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal mengklaim saldo karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal mengklaim saldo karena error: {e}")
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
        response = requests.post('https://game-domain.blum.codes/api/v1/farming/start', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal memulai farming karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal memulai farming karena error: {e}")
    return None

def refresh_token(old_refresh_token):
    time.sleep(2)
    url = 'https://gateway.blum.codes/v1/auth/refresh'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'origin': 'https://telegram.blum.codes',
        'referer': 'https://telegram.blum.codes/'
    }
    data = {
        'refresh': old_refresh_token
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Gagal refresh token untuk: {old_refresh_token}")
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal refresh token karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal refresh token karena error: {e}")
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
        response = requests.get('https://gateway.blum.codes/v1/friends/balance', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal mendapatkan saldo teman karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal mendapatkan saldo teman karena error: {e}")
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
        response = requests.post('https://gateway.blum.codes/v1/friends/claim', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal mengklaim saldo teman karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal mengklaim saldo teman karena error: {e}")
    return None

# cek daily 
import json
def check_daily_reward(token):
    time.sleep(2)
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
        response = requests.post('https://game-domain.blum.codes/api/v1/daily-reward?offset=-420', headers=headers, timeout=10)
        if response.status_code == 400:
            try:
                return response.json()
            except json.JSONDecodeError:
                if response.text == "OK":
                    return response.text
                # print(f"Json Error: {response.text}")
                return None
        else:
            try:
                return response.json()
            except json.JSONDecodeError:
                print(f"Json Error: {response.text}")
                return None
            # response.raise_for_status()  # Menangani status kode HTTP yang tidak sukses
            return None
    except requests.exceptions.Timeout:
        print(f"Gagal claim daily: Timeout")
    except requests.exceptions.RequestException as e:
        return response.json()
      
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
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal mengklaim saldo teman karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal mengklaim saldo teman karena error: {e}")
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
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return "OK"
        else:
            js = response.json()
            print(js.get('message'))
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Gagal mengklaim saldo teman karena masalah koneksi: {e}")
    except Exception as e:
        print(f"Gagal mengklaim saldo teman karena error: {e}")
    return None
checked_tasks = {}

args = parse_arguments()
cek_task_enable = args.task
claim_ref_enable = args.reff

def main():
    
    print(r"""
              
            Created By Snail S4NS Group
    find new airdrop & bot here: t.me/sansxgroup
    
              
          """)
    while True:
        tokens = []
        queries = load_credentials()
        delay_time = random.randint(28800, 29300)
        start_time = time.time()
        now = datetime.now().isoformat(" ").split(".")[0]
        for index, query_id in enumerate(queries):
            headers = getuseragent(index)
            token = get_new_token(query_id)
            tokens.append(token)
            user_info = get_user_info(token)
            if user_info is None:
                continue
            print(f"==================  {user_info['username']}  ==================")  
            print(f"Getting Info....")
            balance_info = get_balance(token)
            if balance_info is None:
                print(f"Failed to Get information", flush=True)
                continue
            else:
                available_balance_before = balance_info['availableBalance']  

                balance_before = f"{float(available_balance_before):,.0f}".replace(",", ".")

                print(f"[{now}] Balance       : {balance_before}", flush=True)
                print(f"[{now}] Tiket Game    : {balance_info['playPasses']}")
                data_tribe = check_tribe(token)
                time.sleep(2)
                if data_tribe is not None:
                    print(f"[{now}] Tribe         : {data_tribe.get('title')} | Member : {data_tribe.get('countMembers')} | Balance : {data_tribe.get('earnBalance')}")
                else:
                    print(f'[{now}] Tribe not Found')
                    time.sleep(1)
                    print(f'[{now}] Joininng Tribe...')
                    join = join_tribe(token)
                    if join is not None:
                        print(f'[{now}] Join Tribe Done')

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
                    print(f"[{now}] Claim Balance : {hours_remaining} jam {minutes_remaining} menit | Balance: {farming_balance_formated}")

                    if hours_remaining < 0:
                        print(f"[{now}] Claim Balance: Claiming balance...")
                        claim_response = claim_balance(token)
                        if claim_response:
                            print(f"[{now}] Claim Balance : Claimed: {claim_response['availableBalance']}                ", flush=True)
                            print(f"[{now}] Claim Balance : Starting farming...")
                            start_response = start_farming(token)
                            if start_response:
                                print(f"[{now}] Claim Balance : Farming started.", flush=True)
                            else:
                                print(f"[{now}] Claim Balance : Failed start farming", start_response, flush=True)
                        else:
                            print(f"[{now}] Claim Balance : Failed claim", claim_response, flush=True)
                            start_response = start_farming(token)
                            if start_response:
                                print(f"[{now}] Claim Balance : Farming started.", flush=True)
                            else:
                                print(f"[{now}] Claim Balance : Failed start farming", start_response, flush=True)
                else:
                    print(f"[{now}] Claim Balance : Gagal mendapatkan informasi farming", flush=True)
                    print(f"[{now}] Claim Balance : Claiming balance...")
                    claim_response = claim_balance(token)
                    if claim_response:
                        print(f"[{now}] Claim Balance : Claimed               ", flush=True)
                        print(f"[{now}] Claim Balance : Starting farming...")
                        start_response = start_farming(token)
                        if start_response:
                            print(f"[{now}] Claim Balance : Farming started.", flush=True)
                        else:
                            print(f"[{now}] Claim Balance : Failed start farming", start_response, flush=True)
                    else:
                        print(f"[{now}] Claim Balance : Gagal claim", claim_response, flush=True)
                        start_response = start_farming(token)
                        if start_response:
                            print(f"[{now}] Claim Balance : Farming started.", flush=True)
                        else:
                            print(f"[{now}] Claim Balance : Failed start farming", start_response, flush=True)

            print(f"[{now}] Daily Reward : Checking daily reward...")
            daily_reward_response = check_daily_reward(token)
            if daily_reward_response is None:
                print(f"[{now}] Daily Reward : Failed Check Daily Reward.", flush=True)
            else:
                if daily_reward_response.get('message') == 'same day':
                    print(f"[{now}] Daily Reward : Daily Reward Claimed", flush=True)
                elif daily_reward_response.get('message') == 'OK':
                    print(f"[{now}] Daily Reward : Daily Reward Done Claim!", flush=True)
                else:
                    print(f"[{now}] Daily Reward : Failed Check Daily Reward. {daily_reward_response}", flush=True)

            if cek_task_enable == 'y':
                if query_id not in checked_tasks or not checked_tasks[query_id]:
                    print(f"[{now}] Checking tasks...")
                    check_tasks(token)
                    checked_tasks[query_id] = True

            
            print(f"[{now}] Reff Balance : Checking reff balance...")
            if claim_ref_enable == 'y':
                friend_balance = check_balance_friend(token)
                if friend_balance:
                    if friend_balance['canClaim']:
                        print(f"[{now}] Reff Balance: {friend_balance['amountForClaim']}", flush=True)
                        print(f"[{now}] Claiming Ref balance.....", flush=True)
                        claim_friend_balance = claim_balance_friend(token)
                        if claim_friend_balance:
                            claimed_amount = claim_friend_balance['claimBalance']
                            print(f"[{now}] Reff Balance : Sukses claim total: {claimed_amount}", flush=True)
                        else:
                            print(f"[{now}] Reff Balance : Gagal mengklaim saldo ref", flush=True)
                    else:
                        can_claim_at = friend_balance.get('canClaimAt')
                        if can_claim_at:
                            claim_time = datetime.fromtimestamp(int(can_claim_at) / 1000)
                            current_time = datetime.now()
                            time_diff = claim_time - current_time
                            hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print(f"[{now}] Reff Balance : Klaim pada {hours} jam {minutes} menit lagi", flush=True)
                        else:
                            print(f"[{now}] Reff Balance : False                                 ", flush=True)
                else:
                    print(f"[{now}] Reff Balance : Gagal cek reff balance", flush=True)
            else:
                print(f"[{now}] Reff Balance : Skipped !                    ", flush=True)
            
        
        for index, token in enumerate(tokens):
            time.sleep(3)
            balance_info = get_balance(token)
            available_balance_before = balance_info['availableBalance'] 
            balance_before = f"{float(available_balance_before):,.0f}".replace(",", ".")
            print(f"======== Account {index+1} ========")
            if balance_info.get('playPasses') <= 0:
                print('No have ticket For Playing games')
            while balance_info['playPasses'] > 0:
                now = datetime.now().isoformat(" ").split(".")[0]
                print(f"[{now}] Play Game : Playing game...")
                gameId = get_game_id(token)
                print(f"[{now}] Play Game : Checking game...")
                taps = random.randint(230, 250)
                delays = random.randint(30, 40)
                time.sleep(delays)
                claim_response = claim_game(token, gameId, taps)
                if claim_response is None:
                    print(f"[{now}] Play Game : Game still running waiting...", flush=True)
                while True:
                    if claim_response.text == '{"message":"game session not finished"}':
                        time.sleep(10)  
                        print(f"[{now}] Play Game : Game still running waiting....", flush=True)
                        claim_response = claim_game(token, gameId, taps)
                        if claim_response is None:
                            print(f"[{now}] Play Game : Failed Claim game point, trying...", flush=True)
                    elif claim_response.text == '{"message":"game session not found"}':
                        print(f"[{now}] Play Game : Game is Done", flush=True)
                        break
                    elif 'message' in claim_response and claim_response['message'] == 'Token is invalid':
                        print(f"[{now}] Play Game : Token Not Valid, Take new token...")
                        token = get_new_token(query_id)
                        continue  
                    else:
                        print(f"Play Game : Game is Done: {claim_response.text}", flush=True)
                        break
               
                balance_info = get_balance(token) 
                if balance_info is None: 
                    print(f"[{now}] Play Game Gagal mendapatkan informasi tiket", flush=True)
                else:
                    available_balance_after = balance_info['availableBalance'] 
                    before = float(available_balance_before) 
                    after =  float(available_balance_after)
                   
                    total_balance = after - before  
                    print(f"[{now}] Play Game: You Got Total {total_balance} From Playing Game", flush=True)
                    if balance_info['playPasses'] > 0:
                        print(f"[{now}] Play Game : Tiket still ready, Playing game again...", flush=True)
                        continue  
                    else:
                        print(f"[{now}] Play Game : Tiket Finished.", flush=True)
                        break
            end_time = time.time()

        print(f"========= ALL ID DONE =========")
        waktu_tunggu = delay_time - (end_time-start_time)
        printdelay(waktu_tunggu)
        if waktu_tunggu >= 0:
            time.sleep(waktu_tunggu)
   
def printdelay(delay):
    now = datetime.now().isoformat(" ").split(".")[0]
    hours, remainder = divmod(delay, 3600)
    minutes, sec = divmod(remainder, 60)
    print(f"{now} | Waiting Time: {hours} hours, {minutes} minutes, and {round(sec)} seconds")

if __name__ == "__main__":
    main()
