import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
from faker import Faker
import time

print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @jatintiwari0 
> › By      :- JATIN TIWARI
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                """)
print('\x1b[38;5;208m⇼'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;208m⇼'*60)

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def get_mail_domains(proxy=None):
    url = "https://api.mail.tm/domains"
    try:
        response = requests.get(url, proxies=proxy, timeout=10)
        if response.status_code == 200:
            return response.json()['hydra:member']
        else:
            print(f'[×] E-mail Error : {response.text}')
            return None
    except Exception as e:
        print(f'[×] Error getting domains: {e}')
        return None

def create_mail_tm_account(proxy=None):
    fake = Faker()
    mail_domains = get_mail_domains(proxy)
    if mail_domains:
        domain = random.choice(mail_domains)['domain']
        username = generate_random_string(10)
        password = fake.password()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
        first_name = fake.first_name()
        last_name = fake.last_name()
        url = "https://api.mail.tm/accounts"
        headers = {"Content-Type": "application/json"}
        data = {"address": f"{username}@{domain}", "password": password}       
        try:
            response = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=10)
            if response.status_code == 201:
                return f"{username}@{domain}", password, first_name, last_name, birthday
            else:
                print(f'[×] Email Error : {response.status_code} - {response.text}')
                return None, None, None, None, None
        except Exception as e:
            print(f'[×] Error creating email: {e}')
            return None, None, None, None, None
    else:
        return None, None, None, None, None

def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    req = {
        'api_key': api_key,
        'attempt_login': True,
        'birthday': birthday.strftime('%Y-%m-%d'),
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': first_name,
        'format': 'json',
        'gender': gender,
        'lastname': last_name,
        'email': email,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig
    api_url = 'https://b-api.facebook.com/method/user.register'
    
    try:
        reg = _call(api_url, req, proxy)
        if 'new_user_id' in reg and 'session_info' in reg:
            id = reg['new_user_id']
            token = reg['session_info']['access_token']
            print(f'''
-----------GENERATED-----------
EMAIL : {email}
ID : {id}
PASSWORD : {password}
NAME : {first_name} {last_name}
BIRTHDAY : {birthday} 
GENDER : {gender}
-----------GENERATED-----------
Token : {token}
-----------GENERATED-----------''')
            
            # Save to file
            with open('accounts.txt', 'a') as f:
                f.write(f"{email}:{password}:{token}\n")
            return True
        else:
            print(f'[×] Facebook Registration Error: {reg}')
            return False
    except Exception as e:
        print(f'[×] Error registering Facebook account: {e}')
        return False

def _call(url, params, proxy=None, post=True):
    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
    }
    try:
        if post:
            response = requests.post(url, data=params, headers=headers, proxies=proxy, timeout=15)
        else:
            response = requests.get(url, params=params, headers=headers, proxies=proxy, timeout=15)
        return response.json()
    except Exception as e:
        print(f'[×] API Call Error: {e}')
        return {}

def test_proxy_helper(proxy):
    try:
        # Test multiple endpoints for better reliability
        test_urls = [
            'https://httpbin.org/ip',
            'https://api.mail.tm/domains',
            'https://www.google.com'
        ]
        
        for url in test_urls:
            response = requests.get(url, proxies=proxy, timeout=8)
            if response.status_code != 200:
                return False
        
        print(f'✓ Working proxy: {list(proxy.values())[0]}')
        return True
    except Exception as e:
        print(f'✗ Failed proxy: {list(proxy.values())[0]} - {e}')
        return False

def load_proxies():
    try:
        with open('proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        
        formatted_proxies = []
        for proxy in proxies:
            # Support multiple proxy formats
            if '://' in proxy:
                # Already formatted (http://ip:port or socks5://ip:port)
                if proxy.startswith('http://'):
                    formatted_proxies.append({'http': proxy, 'https': proxy})
                elif proxy.startswith('socks5://'):
                    formatted_proxies.append({'http': proxy, 'https': proxy})
            else:
                # Plain ip:port format
                formatted_proxies.append({
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                })
        
        return formatted_proxies
    except FileNotFoundError:
        print('[×] proxies.txt file not found!')
        return []
    except Exception as e:
        print(f'[×] Error loading proxies: {e}')
        return []

def get_working_proxies():
    print('[+] Loading proxies...')
    proxies = load_proxies()
    
    if not proxies:
        print('[×] No proxies loaded!')
        return []
    
    print(f'[+] Testing {len(proxies)} proxies...')
    valid_proxies = []
    
    # Use ThreadPoolExecutor for better thread management
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(test_proxy_helper, proxy): proxy for proxy in proxies}
        
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    valid_proxies.append(proxy)
            except Exception as e:
                print(f'[×] Proxy test exception: {e}')
    
    print(f'[+] Found {len(valid_proxies)} working proxies')
    return valid_proxies

def main():
    # Check if running without proxies
    use_proxies = input('[?] Use proxies? (y/n): ').lower().strip() == 'y'
    
    working_proxies = []
    if use_proxies:
        working_proxies = get_working_proxies()
        if not working_proxies:
            print('[×] No working proxies found. Running without proxies...')
            use_proxies = False
    
    num_accounts = int(input('[+] How Many Accounts You Want: '))
    successful_accounts = 0
    
    for i in range(num_accounts):
        print(f'\n[+] Creating account {i+1}/{num_accounts}...')
        
        proxy = None
        if use_proxies and working_proxies:
            proxy = random.choice(working_proxies)
            print(f'[+] Using proxy: {list(proxy.values())[0]}')
        
        # Create email account
        email, password, first_name, last_name, birthday = create_mail_tm_account(proxy)
        
        if email and password and first_name and last_name and birthday:
            # Register Facebook account
            if register_facebook_account(email, password, first_name, last_name, birthday, proxy):
                successful_accounts += 1
            else:
                print(f'[×] Failed to register Facebook account for {email}')
        else:
            print(f'[×] Failed to create email account')
        
        # Add delay to avoid rate limiting
        if i < num_accounts - 1:
            time.sleep(random.uniform(2, 5))
    
    print(f'\n[+] Successfully created {successful_accounts}/{num_accounts} accounts')
    print('[+] Accounts saved to accounts.txt')

if __name__ == "__main__":
    main()
    print('\x1b[38;5;208m⇼'*60)
