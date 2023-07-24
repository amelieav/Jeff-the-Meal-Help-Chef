from asyncio.tasks import sleep
import random
import discord
import os
import processUserInput
import getRecommendationsFromIngredients

from discord.ext import commands
from dotenv import load_dotenv

# Load in the Discord API key from your .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialise a bot object with a command prefix
bot = commands.Bot(command_prefix='&', intents=discord.Intents.all())

guild_ids = os.getenv('SERVER_ID')  # Tech Testing Server, add any extra servers to this list

top5urls = [
    "input ingredients to get recipes",
    "input ingredients to get recipes",
    "input ingredients to get recipes",
    "input ingredients to get recipes",
    "input ingredients to get recipes",
]
mealCounter = 0

@bot.event
async def on_ready():
    print('Bot running')
    await bot.change_presence(activity=discord.Game(name="with a knife"))

@bot.event
async def on_message(message):
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)

list_of_creepy = ["Where are you hiding?", "Hi... My name is Jeff", "I love to make (whipped) cream! Do you?",
                  "I think I heard someone say they are... hungry?     :)", "I can smell something delicious! Is it you?",
                  "Food is my second favourite thing in the world... hehe?", "Is anyone there?",
                  "Sometimes I like to sit alone... quietly...", "My favourite Chef is Gordon Ramsay, how about you?",
                  "You look like you'd taste nice in a soup...", "Chop Chop Chop!", "*slices carrot slowly*", "hehe",
                  "Stir the soup!", "I like rusty spoons...",
                  "When I was a young robot, my mother used to spank me with a spatula!"]

is_saythings_active = False

@bot.command(name='saythings')
async def saythings(ctx):
    global is_saythings_active
    if is_saythings_active:
        is_saythings_active = False
        await ctx.send("I will stop saying creepy things now.")
    else:
        is_saythings_active = True
        while is_saythings_active:
            await sleep(random.randint(1000, 2000))
            await ctx.send(content="*" + list_of_creepy[random.randrange(0, len(list_of_creepy))] + "*")


@bot.command(name="mealhelp")
async def mealhelp(ctx):
    await ctx.send('To get recipe suggestions, input \"/meal\", followed by a space, then a list of ingredients, each separated by \",\"')
    await ctx.send('To specify dietary requirements, add these by including another list (formatted the same as the ingredient list) after, again separate the two lists with a space')
    await ctx.send('If you don\'t like the meal suggested (leave. Just kidding! ha. Ha. ha. haaaaa. ha!), enter\'/another\' to get a different suggestion')
    await ctx.send('For allergens, state the specific allergen(s) you have, for example for a lactose intolerance, say \"lactose\"')

@bot.command(name="meal")
async def meal(ctx, ingredients: str, requirements: str = "none"):
    global top5urls
    global mealCounter
    mealCounter = 0
    ingredients = [x.strip() for x in ingredients.split(',')]
    dietList = processUserInput.getDietList(requirements)

    top5 = getRecommendationsFromIngredients.getHighest(
        getRecommendationsFromIngredients.get_freq(ingredients, dietList),
        number=5
    )

    top5urls = [top5[i][1]["recipe"].url for i in range(5)]
    mealCounter = mealCounter + 1
    sayings = ["YUM.", "Now that looks... good", "If I were you, I'd eat up ;)", "Don't burn those lips!", "I hope you don't accidentally leave the gas on...", "Here's one I made earlier...", "Enjoy...      are you enjoying it?", "I personally despise this one but knock yourself out."]
    await ctx.send("**" + top5[0][1]["recipe"].name + ":**" + "\n" + top5urls[0])
    await ctx.send("*" + sayings[random.randrange(0, len(sayings))] + "*")

@bot.command(name="another")
async def another(ctx):
    global top5urls
    global mealCounter
    if (mealCounter > 4):
        await ctx.send("Sorry, all meals suggested, try another set of ingredients")
        return
    await ctx.send(top5urls[mealCounter])
    sayings = ["YUM.", "", "If I were you, I'd eat up ;)", "Don't burn those lips!", "I hope you don't accidentally leave the gas on...", "Here's one I made earlier...", "Enjoy...      are you enjoying it?", "I personally despise this one but knock yourself out."]
    await ctx.send(sayings[random.randrange(0, len(sayings))])
    mealCounter = mealCounter + 1

@bot.command(name="ping")
async def ping(ctx):
    print("ping!", ctx)
    await ctx.send("pong")

# Start the bot using the API key
bot.run(TOKEN)