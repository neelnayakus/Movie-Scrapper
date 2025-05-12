
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://multimovies.media"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_movie_links():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    movie_cards = soup.select(".ml-item")
    movie_urls = [card.a['href'] for card in movie_cards if card.a]
    return movie_urls

def fetch_movie_details(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        title = soup.find("h1").text.strip()
    except:
        title = "N/A"

    try:
        synopsis = soup.select_one(".mvic-desc p").text.strip()
    except:
        synopsis = "N/A"

    try:
        iframe = soup.find("iframe")
        iframe_url = iframe['src'] if iframe else "N/A"
    except:
        iframe_url = "N/A"

    try:
        genre_tags = soup.select(".mvici-left p span a")
        genres = ", ".join([g.text.strip() for g in genre_tags])
    except:
        genres = "N/A"

    try:
        year = soup.select_one(".mvici-right p").text.strip().split()[-1]
    except:
        year = "N/A"

    try:
        poster = soup.select_one(".thumb.mvic-thumb img")['src']
        poster_url = urljoin(BASE_URL, poster)
    except:
        poster_url = "N/A"

    return {
        "Title": title,
        "Synopsis": synopsis,
        "Genre": genres,
        "Year": year,
        "Poster URL": poster_url,
        "iFrame URL": iframe_url,
        "Page URL": url
    }

def main():
    movie_links = fetch_movie_links()
    print(f"Found {len(movie_links)} movies.")
    
    all_data = []
    for link in movie_links:
        print(f"Processing: {link}")
        data = fetch_movie_details(link)
        all_data.append(data)

    df = pd.DataFrame(all_data)
    df.to_excel("movies_data.xlsx", index=False)
    print("Data saved to movies_data.xlsx")

if __name__ == "__main__":
    main()
