from time import sleep

import os
import re
import html
import requests
import argparse
import json
from bs4 import BeautifulSoup


LINK_MATCHER = re.compile("<a class=\"standard-card-new__article-title(.*?)\" href=\"(.*?)\">")
RECIPE_TITLE_MATCHER = re.compile("<h1 class=\"heading-1\">(.*?)<\/h1>")
RECIPE_DESC_MATCHER = re.compile("<div class=\"mt-sm pr-xxs hidden-print\"><div class=\"editor-content\"><p>(.*?)<\/p>")
RECIPE_INGREDIENTS_MATCHER = re.compile("<li class=\"pb-xxs pt-xxs list-item list-item--separator\">(.*?)<\/li>")
RECIPE_RATING_MATCHER = re.compile("<span class=\"sr-only\">A star rating of ([0-9.]*) out of 5.(?:.*?)<span class=\"rating__count-text body-copy-small\">([0-9]+) ratings")

RATELIMIT = 5 # seems to work without throttling?

def get_recipes(num_pages=40, filename="links.txt", sort_key="popular"):
    url = lambda page: f"https://www.bbcgoodfood.com/search/page/{page}/recipes?sort=-{sort_key}" # top n recipes, each page has 24 pages, 400ish pages total

    urls_masterlist = []

    try:
        for i in range(1, num_pages+1):
            page = requests.get(url(i))

            urls = ["https://www.bbcgoodfood.com" + x[1] for x in LINK_MATCHER.findall(page.text)] # get all links to recipes
            print(f"page {i} of {num_pages}, {len(urls)} urls found", end=" \r")
            urls_masterlist = urls_masterlist + urls
            print(f"page {i} of {num_pages}, {len(urls_masterlist)} urls matched", end=" \r")

            sleep(1/RATELIMIT)

    except KeyboardInterrupt:
        print("keyboard interrupt - cancelling!")

    with open(filename, "w") as f:
        f.write("\n".join(urls_masterlist))
        print(f"\nURLs written to {filename}")

    print("\nURL Scrape Complete!")

# Add this regular expression to filter out invalid characters from URLs
URL_CLEANUP_REGEX = re.compile(r"https://www\.bbcgoodfood\.com/recipes/[a-zA-Z0-9\-]+")

def load_recipes(filename="links.txt"):
    with open(filename, "r") as f:
        urls = [x.strip() for x in f.readlines()]
        return [url for url in urls if URL_CLEANUP_REGEX.match(url)]

def load_recipes_to_set(filename="links.txt"):
    recipes = load_recipes(filename)
    return set(recipes)


def scrape_recipe(url):
    page = requests.get(url) # load recipe from url
    title = RECIPE_TITLE_MATCHER.search(page.text).group(1) # find title
    description_match = RECIPE_DESC_MATCHER.search(page.text)
    description = description_match.group(1) if description_match else ""

    # Use BeautifulSoup to parse the page and extract ingredients
    soup = BeautifulSoup(page.text, 'html.parser')
    ingredients = soup.find_all('li', class_='pb-xxs pt-xxs list-item list-item--separator')
    ingredients = [ingredient.text.strip() for ingredient in ingredients]

    # Check if any matches are found for the rating
    rating_matches = RECIPE_RATING_MATCHER.findall(page.text)
    if rating_matches:
        rating_stars, rating_count = map(float, rating_matches[0]) # find rating
        rating_count = int(rating_count)
    else:
        rating_stars, rating_count = 0.0, 0

    # remove html things
    title = html.unescape(title)
    description = html.unescape(description)

    return url, title, description, ingredients, rating_stars, rating_count



def jsonify_recipe(url, title, description, ingredients, r_s, r_c):
    # Properly format the ingredients using json.dumps to handle special characters
    ingredients_string = json.dumps(ingredients, ensure_ascii=False)

    # Create a dictionary representing the recipe data
    recipe_data = {
        "name": title,
        "ingredients": ingredients_string,
        "url": url,
        "description": description,
        "rating_stars": r_s,
        "rating_count": r_c,
        "image": ""
    }

    # Serialize the recipe data as a JSON-formatted string
    return json.dumps(recipe_data, ensure_ascii=False)

def get_available_rec_number():
    rec_number = 1
    while os.path.isfile(f"rec{rec_number}.json"):
        rec_number += 1
    return rec_number

def scrape_all_recipes(output_filename, recipes_filename="links.txt"):  # Update function signature here
    rec_number = get_available_rec_number()
    recipes = []
    try:
        num_recipes_to_scrape = 20  # Set the desired number of recipes to scrape
        for n, recipe in enumerate(load_recipes(recipes_filename)):
            print(f"scraping recipe #{n+1}", end=" \r")
            data = scrape_recipe(recipe)
            recipes.append(jsonify_recipe(*data))
            sleep(1/RATELIMIT)

            # Check if the desired number of recipes has been scraped
            if n + 1 >= num_recipes_to_scrape:
                break
    except KeyboardInterrupt:
        pass

    recipes_string = '{"recipes": [\n' + ",\n".join(recipes) + "\n]}"
    with open(output_filename, "w", encoding="utf-8") as f:  # Specify utf-8 encoding when writing
        f.write(recipes_string)

    print("\nScrape Complete!")

output_filename = f"rec{get_available_rec_number()}.json"
scrape_all_recipes(output_filename)

