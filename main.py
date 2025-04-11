# Imports
import json
from discord.ext import commands
import discord

# import discord bot token from token.json
with open("configuration.json", "r") as token_json:
    load_token = json.load(token_json)
    token = load_token["Token"]

# Defining bot
bot = commands.Bot(command_prefix="")

@bot.slash