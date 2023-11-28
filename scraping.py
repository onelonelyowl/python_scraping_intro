from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from slugify import slugify
# https://www.learndatasci.com/tutorials/ultimate-guide-web-scraping-w-python-requests-and-beautifulsoup/

#uncomment below block if you want to call another url again

# kdas = soup.select('.hitagi__sc-1ah81hi-0.gxAkuM')
# heroes = soup.select('.hitagi__sc-1ah81hi-0.hitagi__sc-19ps7xc-0.fZFVxV.eTLPcy *')
# win_loss = soup.find_all(True, {'class':['RfVMg', 'jIYDVq']})
# won_lost_lane = soup.find_all(True, {'class': ['hUGIEa', 'bXSGnY', 'cCWvMZ']})
# match_length = soup.find_all(class_="bKpSdi")
# performance_rating = soup.find_all(True, {'class': ["ekSEQz", "vPeZG"]})
# win_rate_last25 = soup.select('.hxxEyi')
# win_loss_array = [item.text for item in win_loss]
# wins = win_loss_array.count('W')
# losses = win_loss_array.count('L')
# wins_losses = np.array([wins, losses])
# plt.pie(wins_losses, labels = ['W', 'L'])
# plt.show()



# def print_recent_matches():
#     recentmatches = "roobarb's recent matches:"
#     print(f'{recentmatches.ljust(93)} Winrate in the last 25 games: {win_rate_last25[0].text[0:4]}')
#     for i in range(0, len(kdas) - 2, 3):
#         print (f"Result: {win_loss[i//3].text.ljust(5)} Hero: {get_hero_name(heroes[(i//3)]).ljust(20)} KDA: {kdas[i].text.strip().ljust(2) + ' / ' + kdas[i+1].text.strip().ljust(2) + ' / ' + kdas[i+2].text.strip().ljust(4)} Won/Lost Lane: {won_lost_lane[i//3].text.ljust(4) if len(won_lost_lane[i//3].text) > 0 else "n/a".ljust(4)} Match length: {match_length[i//3].text.ljust(8)} Performance rating: {performance_rating[i//3].text.ljust(4) if len(performance_rating[i//3]) > 0  else "n/a"}")



def scrape_user_data(user_id):
    url = f'https://stratz.com/players/{user_id}'
    r = requests.get(url)
    with open(f'{user_id}', 'wb') as f:
        f.write(r.content)

def get_user_from_id():
    username = soup.select_one('.hHdoEl').text
    username_noclan = re.search( r"(.*)(?= \[)" , username)
    username_noclan = username_noclan.group(0)
    username_slug = slugify(username_noclan, separator="_")
    return username_slug

def create_new_user_table(user_id):
    if type(user_id) is not int:
        raise TypeError("User ID must be a number")
    con = sqlite3.connect('playerdata.db')
    cur = con.cursor()
    username_slug = get_user_from_id()
    cur.execute(f"CREATE TABLE {username_slug}(win_loss, hero, kda, win_loss_lane, match_length, performance_rating)")
    print(f'table has been created for user {username_slug}')

def open_user_data(user_id):
    global soup
    with open(f"{user_id}", 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    kdas = soup.select('.hitagi__sc-1ah81hi-0.gxAkuM')
    heroes = soup.select('.hitagi__sc-1ah81hi-0.hitagi__sc-19ps7xc-0.fZFVxV.eTLPcy *')
    win_loss = soup.find_all(True, {'class':['RfVMg', 'jIYDVq']})
    won_lost_lane = soup.find_all(True, {'class': ['hUGIEa', 'bXSGnY', 'cCWvMZ']})
    match_length = soup.find_all(class_="bKpSdi")
    performance_rating = soup.find_all(True, {'class': ["ekSEQz", "vPeZG"]})
    return {
        'kdas': kdas,
        'heroes': heroes,
        'win_loss': win_loss,
        'won_lost_lane': won_lost_lane,
        'match_length': match_length,
        'performance_rating': performance_rating
    }

def get_hero_name(html_tag):
    regex_match = re.search( r"(?<=heroes\/)(.*)(?=_horz)" , str(html_tag))
    hero_string = regex_match.group(0)
    formatted = hero_string.replace('_', ' ').title()
    return formatted    

def add_to_database(user_id):    
    con = sqlite3.connect('playerdata.db')
    cur = con.cursor()
    data = []
    incoming_data = open_user_data(user_id)
    username_slug = get_user_from_id()
    for i in range(0, len(incoming_data['kdas']) - 2, 3):
        data.append((incoming_data['win_loss'][i//3].text, get_hero_name(incoming_data['heroes'][i//3]), str(incoming_data['kdas'][i].text.strip() + ' / ' + incoming_data['kdas'][i+1].text.strip() + ' / ' + incoming_data['kdas'][i+2].text.strip()), incoming_data['won_lost_lane'][i//3].text, incoming_data['match_length'][i//3].text, incoming_data['performance_rating'][i//3].text))
    try:
        cur.executemany(f"INSERT INTO {username_slug} VALUES(?, ?, ?, ?, ?, ?)", data)
        con.commit()
    except:
        raise Exception("SQLite insertion of data failed (check table exists/data is valid)")
    
def create_db_for_user(user_id):
    scrape_user_data(user_id)
    open_user_data(user_id)
    create_new_user_table(user_id)
    add_to_database(user_id)
    print(f"table added to database with id: {user_id}")
    
create_db_for_user(83093960)