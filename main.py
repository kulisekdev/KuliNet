# Imports
import json
from discord.ext import commands
import discord
import os

#testing...
from dotenv import load_dotenv
load_dotenv()
temptoken = os.getenv("token")




# import discord bot token from token.json
with open("configuration.json", "r") as token_json:
    load_token = json.load(token_json)
    token = load_token["Token"]
    prefix = load_token["command_prefix"]

# Defining bot and stuff
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.command()
async def join(ctx):
    Error = discord.Embed(
        title=f"Error!",
        description="The bot doesn't know where to join make sure to join a channel first before execution of ```!join```",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
    )
    Error.set_author(
        name="KuliNet",
        icon_url=bot.user.avatar.url
    )

    if ctx.author.voice is None or ctx.author.voice.channel is None:
       await ctx.send(embed=Error)
       return
    
    joined = discord.Embed(
        title=f"Joined to **{ctx.author.voice.channel.name}**",
        description="The bot successfully joined the voice channel.",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.green()
    )
    joined.set_author(
        name="KuliNet",
        icon_url=bot.user.avatar.url
    )

    if ctx.author.voice is None or ctx.author.voice.channel is None:
       await ctx.send(embed=Error)
       return
 
    if ctx.author.voice:  
      await ctx.send(embed=joined)
      await ctx.author.voice.channel.connect()
 


bot.run(token=temptoken)