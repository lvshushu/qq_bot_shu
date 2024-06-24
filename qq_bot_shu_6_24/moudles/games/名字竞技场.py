import requests
from bs4 import BeautifulSoup
import codecs

def send_names(names):
    base64 = codecs.encode(names.encode('utf-8'), 'base64').decode('latin1').replace('+', '-').replace('/', '_')
    url = f'http://namerena.github.io/#n={base64}'
    response = requests.get(url)
    print(response.text)
    return response.text

def parse_winners(html):
    soup = BeautifulSoup(html, 'html.parser')
    winners = [w.text for w in soup.select('.winner')]
    return winners

def save_winners_to_file(winners, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for winner in winners:
            f.write(winner + '')

if __name__ == '__main__':
    names = '''名字1
    名字2
    名字3'''
    html = send_names(names)
    save_winners_to_file(html, 'winners1.txt')
    winners = parse_winners(html)
    save_winners_to_file(winners, 'winners.txt')
