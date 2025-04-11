# Imports
import json
from discord.ext import commands
import discord

# import discord bot token from token.json
with open("configuration.json", "r") as token_json:
    load_token = json.load(token_json)
    token = load_token["Token"]
    prefix = load_token["command_prefix"]

# Defining bot
bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    joined = discord.Embed(
        title=f"Joined to {channel.name}",
        description="The bot successfully joined the voice channel.",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.green()
    )
    if ctx.author.voice:
        await channel.connect()
        await ctx.send(embed=joined)