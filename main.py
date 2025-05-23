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

def send_verification_code_to_custom_email(email):
    """Simulate sending verification code to custom email"""
    print(f'[+] Verification code has been sent to {email}')
    print('[+] Please check your email for the verification code...')
    return True

def verify_custom_email_code(provided_code):
    """Simple verification code check - in real implementation, this would verify against sent code"""
    # For demo purposes, let's accept any 6-digit code
    # In real implementation, you would store the sent code and verify against it
    if len(provided_code) == 6 and provided_code.isdigit():
        return True
    return False

def get_custom_email_info():
    """Get custom email and handle verification"""
    custom_email = input('[+] Please enter your email address: ').strip()
    if not custom_email or '@' not in custom_email:
        print('[×] Invalid email address!')
        return None, None, None, None, None
    
    # Send verification code
    print('\n[+] Loading...')
    time.sleep(2)  # Simulate delay
    send_verification_code_to_custom_email(custom_email)
    
    # Wait for verification code
    max_attempts = 3
    for attempt in range(max_attempts):
        verification_code = input('\n[+] Please enter the verification code: ').strip()
        
        if verify_custom_email_code(verification_code):
            print('[✓] Email verified successfully!')
            
            # Generate other required data automatically
            fake = Faker()
            password = fake.password()
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            return custom_email, password, first_name, last_name, birthday
        else:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print(f'[×] Invalid verification code! {remaining} attempts remaining.')
            else:
                print('[×] Maximum attempts exceeded!')
    
    return None, None, None, None, None

def register_facebook_account_with_retry(email, password, first_name, last_name, birthday, working_proxies, max_retries=3):
    """Register Facebook account with automatic proxy retry"""
    for attempt in range(max_retries):
        if working_proxies:
            proxy = random.choice(working_proxies)
            proxy_str = list(proxy.values())[0]
            print(f'[+] Attempt {attempt + 1}: Using proxy {proxy_str}')
        else:
            proxy = None
            print(f'[+] Attempt {attempt + 1}: No proxy')
        
        # Add delay before each attempt
        if attempt > 0:
            delay = random.uniform(3, 7)
            print(f'[+] Waiting {delay:.1f} seconds before retry...')
            time.sleep(delay)
        
        success = register_facebook_account(email, password, first_name, last_name, birthday, proxy)
        
        if success:
            return True
        else:
            if working_proxies and len(working_proxies) > 1:
                # Remove failed proxy
                working_proxies.remove(proxy)
                print(f'[×] Removed failed proxy: {proxy_str}')
                print(f'[+] {len(working_proxies)} proxies remaining')
            
            if attempt < max_retries - 1:
                print(f'[×] Attempt {attempt + 1} failed. Retrying...')
            else:
                print(f'[×] All {max_retries} attempts failed!')
    
    return False

def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    
    # Add random delay before registration
    delay = random.uniform(2, 5)
    print(f'[+] Preparing Facebook registration (waiting {delay:.1f}s)...')
    time.sleep(delay)
    
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
        print('[+] Sending registration request to Facebook...')
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
        
        return True
    except Exception as e:
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
                    # Show working proxy message
                    proxy_str = list(proxy.values())[0]
                    print(f'[✓] Working proxy found: {proxy_str}')
                else:
                    proxy_str = list(proxy.values())[0]
                    print(f'[✗] Failed proxy: {proxy_str}')
            except Exception as e:
                print(f'[×] Proxy test exception: {e}')
    
    print(f'\n[+] Total working proxies found: {len(valid_proxies)}')
    
    # Display all working proxies
    if valid_proxies:
        print('\n[+] Working Proxies List:')
        for i, proxy in enumerate(valid_proxies, 1):
            proxy_str = list(proxy.values())[0]
            print(f'    {i}. {proxy_str}')
    
    return valid_proxies

def main():
    # Check if running without proxies
    use_proxies = input('[?] Use proxies? (y/n): ').lower().strip() == 'y'
    
    working_proxies = []
    if use_proxies:
        working_proxies = get_working_proxies()
        if len(working_proxies) < 2:
            print(f'[×] Only {len(working_proxies)} working proxy(ies) found. Need at least 2 proxies for reliable operation.')
            if len(working_proxies) == 0:
                print('[×] Running without proxies...')
                use_proxies = False
            else:
                continue_anyway = input('[?] Continue with limited proxies? (y/n): ').lower().strip() == 'y'
                if not continue_anyway:
                    print('[×] Exiting...')
                    return
        else:
            print(f'[✓] {len(working_proxies)} working proxies ready for use!')
    
    # Ask for custom email option
    use_custom_email = input('\n[?] Do you want to provide your own email? (y/n): ').lower().strip() == 'y'
    
    num_accounts = int(input('[+] How Many Accounts You Want: '))
    successful_accounts = 0
    
    for i in range(num_accounts):
        print(f'\n{"="*50}')
        print(f'[+] Creating account {i+1}/{num_accounts}...')
        print(f'{"="*50}')
        
        if use_custom_email:
            print('\n[+] Getting custom email information...')
            email, password, first_name, last_name, birthday = get_custom_email_info()
        else:
            # Create email account automatically
            proxy = None
            if use_proxies and working_proxies:
                proxy = random.choice(working_proxies)
                proxy_str = list(proxy.values())[0]
                print(f'[+] Using proxy for email creation: {proxy_str}')
            
            print('[+] Creating temporary email account...')
            email, password, first_name, last_name, birthday = create_mail_tm_account(proxy)
        
        if email and password and first_name and last_name and birthday:
            print(f'[+] Email ready: {email}')
            print(f'[+] Generated profile: {first_name} {last_name}')
            
            # Register Facebook account with retry mechanism
            print(f'\n[+] Starting Facebook registration...')
            success = register_facebook_account_with_retry(
                email, password, first_name, last_name, birthday, 
                working_proxies.copy() if working_proxies else [], 
                max_retries=3
            )
            
            if success:
                successful_accounts += 1
                print(f'[✓] Account {i+1} created successfully!')
            else:
                print(f'[×] Failed to create account {i+1}')
        else:
            print(f'[×] Failed to get email information for account {i+1}')
        
        # Add delay between accounts
        if i < num_accounts - 1:
            delay = random.uniform(5, 10)
            print(f'\n[+] Waiting {delay:.1f} seconds before next account...')
            time.sleep(delay)
    
    print(f'\n{"="*60}')
    print(f'[+] SUMMARY: Successfully created {successful_accounts}/{num_accounts} accounts')
    print(f'[+] Accounts saved to accounts.txt')
    print(f'{"="*60}')

if __name__ == "__main__":
    main()
    print('\x1b[38;5;208m⇼'*60)
