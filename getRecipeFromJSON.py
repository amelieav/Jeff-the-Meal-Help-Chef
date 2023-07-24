# %%
import re
import json
from typing import Dict, List

# %%

# %%
class RecipeList:
    "Data structure to store recipe list"
    def __init__(self, filenames) -> None:
        self.raw_data = []
        for filename in filenames:
            self.raw_data += json.load(open(filename, "r"))["recipes"]
        self.recipes = []
        for recipe in self.raw_data:
            self.recipes.append(Recipe(recipe))
        print(f"Loaded {self.numRecipes} recipes")
    
    def __getitem__(self, key):
        return self.recipes[key]

    @property
    def numRecipes(self):
        return len(self.recipes)

# %%
class Recipe:
    CUPS_MATCHER = re.compile("^[0-9\/\-a]+ (?:cup)[s]? (?:of )?(.*)")
    SPOONS_MATCHER = re.compile("^[0-9\/\-a]+ (?:.*spoon)[s]? (?:of )?(.*)")
    QUANTITY_MATCHER = re.compile("^[0-9\/\-a]+ (.*)")
    ANNOYING_WORDS = ["to taste", "small ", "medium ", "large ", "whole ", "ounces ",
                      "ounces, ", "ounce ", "ounce, ", "pounds ", "pound ", "gram ",
                      "optional", "slices", ", sliced", ", diced", ", finely chopped",
                      "()"]

    def __init__(self, recipe_data: Dict[str, str]) -> None:
        self.raw_data = recipe_data
        self.name = recipe_data["name"]
        self.ingredients_raw = recipe_data["ingredients"]
        self.ingredients = self.ingredientParser(self.ingredients_raw)
        self.description = recipe_data["description"]
        self.image = recipe_data["image"]
        self.url = recipe_data["url"]

    def ingredientParser(self, ingredients: List[str]):
        output_array: List[str] = []

        for value in ingredients:
            value = value.strip().lower()
            if " or " in value:
                for i, item in enumerate(value.split(" or ")):
                    for j, item2 in enumerate(item.split(",")):
                        if item2 != "" and (i == 0 or j == 0):
                            item2 = self.quantityRemover(item2)
                            if item2:
                                output_array.append(item2)
            elif " and " in value:
                for i, item in enumerate(value.split(" and ")):
                    for j, item2 in enumerate(item.split(",")):
                        if item2 != "" and (i == 0 or j == 0):
                            item2 = self.quantityRemover(item2)
                            if item2:
                                output_array.append(item2)
            else:
                value = self.quantityRemover(value)
                if value:
                    output_array.append(value)

        return output_array

    def quantityRemover(self, ingredient: str):
        ingredient = ingredient.strip()

        cups_match = self.CUPS_MATCHER.match(ingredient)
        if cups_match:
            ingredient = cups_match.group(1)

        spoons_match = self.SPOONS_MATCHER.match(ingredient)
        if spoons_match:
            ingredient = spoons_match.group(1)
        
        quantity_match = self.QUANTITY_MATCHER.match(ingredient)
        if quantity_match:
            ingredient = quantity_match.group(1)

        for word in self.ANNOYING_WORDS:
            if word in ingredient:
                ingredient = ingredient.replace(word, '')

        return ingredient
    
    def __repr__(self):
        return f"Recipe('{self.name}')"
# %%
