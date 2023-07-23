from time import sleep

import re
import requests
import argparse

COLLECTION_MATCHER = re.compile('href="/recipes/collection/([A-z0-9-]*?)"')
RECIPE_MATCHER = re.compile('href="/recipes/([A-z0-9-]*?)"')
RATELIMIT = 5 # seems to work without throttling?

GOODFOOD_COLLECTIONS_SEARCH_URL = "https://www.bbcgoodfood.com/search/recipe-collections/page/"
GOODFOOD_COLLECTIONS_URL = "https://www.bbcgoodfood.com/recipes/collection/"
GOODFOOD_RECIPE_URL = "https://www.bbcgoodfood.com/recipes/"

def get_collections(num_pages: int, filename: str):
    """Fetch a list of collections from BBC Goodfood"""
    urls_masterlist = set()

    try:
        for page_id in range(1, num_pages+1):
            page = requests.get(f"{GOODFOOD_COLLECTIONS_SEARCH_URL}{page_id}/", timeout=10)

            for url in COLLECTION_MATCHER.findall(page.text):
                urls_masterlist.add(GOODFOOD_COLLECTIONS_URL + url)

            print(f"Page {page_id} of {num_pages}, {len(urls_masterlist)} collections found",
                  end="    \r")

            sleep(1/RATELIMIT)

    except KeyboardInterrupt:
        print("keyboard interrupt - cancelling!")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(urls_masterlist))

    print("\nCollections Scrape Complete!")

def get_recipes(filename="recipes.txt", collections_filename="collections.txt"):
    """Fetch a list of recipes from a collection"""
    with open(collections_filename, "r", encoding="utf-8") as f:
        urls = f.readlines()

    urls_masterlist = set()

    try:
        for i, url in enumerate(urls):
            page = requests.get(url.strip(), timeout=10)

            recipe_urls = RECIPE_MATCHER.findall(page.text)
            for r_url in recipe_urls:
                urls_masterlist.add(GOODFOOD_RECIPE_URL + r_url)

            print(f"Collection {i + 1} of {len(urls)}, {len(urls_masterlist)} recipes found",
                  end="     \r")

            sleep(1/RATELIMIT)

    except KeyboardInterrupt:
        print("keyboard interrupt - cancelling!")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(urls_masterlist))

    print("\nCollections Scrape Complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapey.')
    parser.add_argument("--pages", type=int, help="number of pages to scrape", default=93)
    args = parser.parse_args()

    get_collections(args.pages, filename="collections.txt")
    get_recipes(filename="recipes.txt", collections_filename="collections.txt")
