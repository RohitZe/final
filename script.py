import uuid
import time
import socket
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import random
import config

#i have used proxies from proxymesh
def rand_proxy():
    proxy = random.choice(config.ips)
    return proxy

def connect_to_mongodb():
    """Connects to MongoDB and returns the specified collection."""
    CONNECTION_STRING = "mongodb+srv://Rohit:Rohit1234@cluster0.lhrx5.mongodb.net/"
    client = MongoClient(CONNECTION_STRING)
    db = client["twitter_data"]  # Database name
    return db["whats_happening"]  # Collection name

def get_ip_address():
    """Returns the local machine's IP address."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def login_twitter(username: str, password: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    # Open the Twitter login page
    url = "https://twitter.com/i/flow/login"
    driver.get(url)

    # Enter the username
    username_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
    )
    username_input.send_keys(username)
    username_input.send_keys(Keys.ENTER)

    # Enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # Wait for the homepage to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Your Home Timeline"]')))

    return driver

def scrape_and_store_whats_happening(driver: webdriver.Chrome, collection):

    whats_happening_section = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Trending now"]'))
    )
    trending_items = whats_happening_section.find_elements(By.CSS_SELECTOR, 'div[dir="ltr"]')
    trends = [item.text.strip() for item in trending_items if item.text.strip()]

    # Record the scraped data
    unique_id = str(uuid.uuid4())
    ip_address = get_ip_address()
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "_id": unique_id,
        "nameoftrend1": trends[0] if len(trends) > 0 else "N/A",
        "nameoftrend2": trends[1] if len(trends) > 1 else "N/A",
        "nameoftrend3": trends[2] if len(trends) > 2 else "N/A",
        "nameoftrend4": trends[3] if len(trends) > 3 else "N/A",
        "nameoftrend5": trends[4] if len(trends) > 4 else "N/A",
        "end_time": end_time,
        "ip_address": ip_address,
    }

    collection.insert_one(record)
    print("Data successfully stored in MongoDB:", record)

def main():
  
    chrome_options=webdriver.ChromeOptions()
    proxy=rand_proxy()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=chrome_options)
    username = "rohitwork42"
    password = "Rohit@1234"

    # Connect to MongoDB
    collection = connect_to_mongodb()
    print("Connection to MongoDB established")

    # Log in to Twitter
    driver = login_twitter(username, password)

    try:
        time.sleep(5)  # Ensuring the page is fully loaded
        scrape_and_store_whats_happening(driver, collection)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
