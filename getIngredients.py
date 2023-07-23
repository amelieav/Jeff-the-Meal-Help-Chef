# %%
import argparse
from collections import Counter
from pprint import pprint
from random import random
from math import sqrt

from processUserInput import getDietList
from recipeParser import RecipeList

recipes = RecipeList(["rec.json", "rec2.json"])

def get_freq(array_of_ingredients, avoid_ingredients=[]):
    recipe_score_dict = {}
    # iterate through all recipies in json
    for recipe in recipes.recipes:
        num_matches_raw = 0
        num_matches = 0
        num_unmatches = 0
        bad_ingredients = 0
        ingredients_dictionary = Counter(recipe.ingredients)
        num_ingredients = len(recipe.ingredients)
        # return dict of each word and frequency

        for ingredient in array_of_ingredients:
            ingredient_matched = False
            for recipe_ingredient, count in ingredients_dictionary.items():
                if ingredient in recipe_ingredient:
                    num_matches += count
                    num_matches_raw += 1
                    ingredient_matched = True
            
            if not ingredient_matched:
                num_unmatches += 1
        
        for bad_ingredient in avoid_ingredients: # supporting veganism since 2021
            for recipe_ingredient, count in ingredients_dictionary.items():
                if bad_ingredient in recipe_ingredient:
                    bad_ingredients += 1

        # recipe_score_dict[recipe.name] = (recipe, num_matches, num_matches_raw, num_unmatches, num_ingredients)
        recipe_score_dict[recipe.name] = {
            "recipe": recipe,
            "num_matches": num_matches,
            "num_matches_raw": num_matches_raw,
            "num_unmatches": num_unmatches,
            "num_ingredients": num_ingredients,
            "bad_ingredients": bad_ingredients
        }

    return recipe_score_dict


def getHighest(dictionary, number=3):
    def scoreRecipe(value):
        if value["bad_ingredients"] != 0:
            return 0

        matches_full = value["num_matches"]
        ingredients = value["num_ingredients"]

        matches = value["num_matches_raw"]
        unmatches = value["num_unmatches"]
        return sqrt(matches_full / ingredients) * (matches / (matches + unmatches)) + 0.08 * random()

    dictionary = sorted(dictionary.items(), reverse=True,
                        key=lambda item: scoreRecipe(item[1]))

    # return [x[1]["recipe"] for x in dictionary[0:number]]
    return dictionary[0:number]

# returns dict with highest score recipies


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("ingredients", metavar="I", type=str, nargs="+", help="recipe ingredients")
    parser.add_argument("--preference", default="none")
    parser.add_argument("--number", type=int, default=3)

    args = parser.parse_args()

    # food = ['pasta', 'tomato', 'onion', 'cheese']

    dietList = getDietList(args.preference)
    print(dietList)
    dictOfFreq = get_freq(args.ingredients, dietList)
    highest = getHighest(dictOfFreq, args.number)
    pprint(highest)
