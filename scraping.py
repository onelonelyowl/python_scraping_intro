from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
# https://www.learndatasci.com/tutorials/ultimate-guide-web-scraping-w-python-requests-and-beautifulsoup/

#uncomment below block if you want to call another url again

# url = 'https://stratz.com/players/<id here>'
# r = requests.get(url)

# def save_html(html, path):
#     with open(path, 'wb') as f:
#         f.write(html)
              
# save_html(r.content, 'stratz_tom')

def open_html(path):
    with open(path, 'rb') as f:
        return f.read()
    
html = open_html('stratz_tom')

soup = BeautifulSoup(html, 'html.parser')

kdas = soup.select('.hitagi__sc-1ah81hi-0.gxAkuM')
heroes = soup.select('.hitagi__sc-1ah81hi-0.hitagi__sc-19ps7xc-0.fZFVxV.eTLPcy *')
win_loss = soup.find_all(True, {'class':['RfVMg', 'jIYDVq']})
won_lost_lane = soup.find_all(True, {'class': ['hUGIEa', 'bXSGnY', 'cCWvMZ']})
match_length = soup.find_all(class_="bKpSdi")
performance_rating = soup.find_all(True, {'class': ["ekSEQz", "vPeZG"]})
win_rate_last25 = soup.select('.hxxEyi')
win_loss_array = [item.text for item in win_loss]
wins = win_loss_array.count('W')
losses = win_loss_array.count('L')
wins_losses = np.array([wins, losses])
print(win_loss_array, wins, losses)
plt.pie(wins_losses, labels = ['W', 'L'])
plt.show()


print(len(won_lost_lane[8].text))
def get_hero_name(html_tag):
    regex_match = re.search( r"(?<=heroes\/)(.*)(?=_horz)" , str(html_tag))
    hero_string = regex_match.group(0)
    formatted = hero_string.replace('_', ' ').title()
    return formatted    
recentmatches = "roobarb's recent matches:"
print(f'{recentmatches.ljust(93)} Winrate in the last 25 games: {win_rate_last25[0].text[0:4]}')
for i in range(0, len(kdas) - 2, 3):
    print (f"Result: {win_loss[i//3].text.ljust(5)} Hero: {get_hero_name(heroes[(i//3)]).ljust(20)} KDA: {kdas[i].text.strip().ljust(2) + ' / ' + kdas[i+1].text.strip().ljust(2) + ' / ' + kdas[i+2].text.strip().ljust(4)} Won/Lost Lane: {won_lost_lane[i//3].text.ljust(4) if len(won_lost_lane[i//3].text) > 0 else "n/a".ljust(4)} Match length: {match_length[i//3].text.ljust(8)} Performance rating: {performance_rating[i//3].text.ljust(4) if len(performance_rating[i//3]) > 0  else "n/a"}")

