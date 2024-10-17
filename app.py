from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    duckduckgo_results = search_duckduckgo(query)
    bing_results = search_bing(query)
    yahoo_results = search_yahoo(query)
    yandex_results = search_yandex(query)

    # Combine all results into one list
    all_results = duckduckgo_results + bing_results + yahoo_results + yandex_results

    return jsonify(all_results)

def search_duckduckgo(query):
    response = requests.get(f'https://api.duckduckgo.com/?q={query}&format=json&no_html=1')
    data = response.json()

    return [{
        'title': topic['Text'],
        'url': topic['FirstURL'],
        'description': topic['Text']
    } for topic in data['RelatedTopics']]

def search_bing(query):
    # Bing search scraping (adjust user-agent as needed)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(f'https://www.bing.com/search?q={query}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.find_all('li', class_='b_algo'):
        title = item.find('h2').get_text()
        url = item.find('a')['href']
        description = item.find('p').get_text() if item.find('p') else ''
        results.append({'title': title, 'url': url, 'description': description})

    return results

def search_yahoo(query):
    # Yahoo search scraping
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(f'https://search.yahoo.com/search?p={query}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.find_all('div', class_='dd algo algo-sr'):
        title = item.find('h3').get_text()
        url = item.find('a')['href']
        description = item.find('p').get_text() if item.find('p') else ''
        results.append({'title': title, 'url': url, 'description': description})

    return results

def search_yandex(query):
    # Yandex search scraping
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(f'https://yandex.com/search/?text={query}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.find_all('li', class_='serp-item'):
        title = item.find('h2').get_text()
        url = item.find('a')['href']
        description = item.find('div', class_='text-container').get_text() if item.find('div', class_='text-container') else ''
        results.append({'title': title, 'url': url, 'description': description})

    return results

if __name__ == '__main__':
    app.run(debug=True)
