
# Imports
import json
from discord.ext import commands, tasks
import discord
import os
from ollama import embed
import yt_dlp
from discord import FFmpegPCMAudio

#testing...
from dotenv import load_dotenv
load_dotenv()
temptoken = os.getenv("token")




# import discord bot token from token.json
with open("configuration.json", "r") as token_json:
    load_token = json.load(token_json)
    token = load_token["Token"]
    prefix = load_token["command_prefix"]

# Defining bot and stuff with discordpy
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
        name="KuliNet - Music Function",
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
        name="KuliNet - Music Function",
        icon_url=bot.user.avatar.url
    )

    if ctx.author.voice is None or ctx.author.voice.channel is None:
       await ctx.send(embed=Error)
       return
 
    if ctx.author.voice:  
      await ctx.send(embed=joined)
      await ctx.author.voice.channel.connect()
 
@bot.command()
async def play(ctx,url):
    Error = discord.Embed(
        title=f"Error!",
        description="I'm not in a voice channel. use ```!join```",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
    )
    Error.set_author(
        name="KuliNet - Music Function",
        icon_url=bot.user.avatar.url
    )

    if not ctx.voice_client:
        return await ctx.send(embed=Error)
    
    
    if isinstance(url, str):
       Audio_Options = {
          "outtmpl": "music.%(ext)s",
          "format": "bestaudio"
       }
       with yt_dlp.YoutubeDL(Audio_Options) as Downloader:
        info_dict = Downloader.extract_info(url, download=True)
        title = info_dict.get("title")
        thumbnail = info_dict.get("thumbnail")
        author = info_dict.get("uploader")

       music = discord.Embed(
          title="Now playing...",
          description=f"User {ctx.author.mention} \n has requested to play **{title}** \n Author: **{author}**",
          timestamp=discord.utils.utcnow(),
       )

       music.set_author(
          name="KuliNet - Music Function",
          icon_url=bot.user.avatar.url
       )
       music.set_thumbnail(
          url=thumbnail
       )
       await ctx.send(embed=music)
       await ctx.voice_client.play(FFmpegPCMAudio("music.webm"))

@bot.command()
async def leave(ctx):
    left = discord.Embed(
        title=f"Left channel **{ctx.author.voice.channel.name}**",
        description="The bot successfully left the voice channel.",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
    )
    left.set_author(
        name="KuliNet - Music Function",
        icon_url=bot.user.avatar.url
    )
    await ctx.send(embed=left)
    await ctx.voice_client.disconnect()
      
@commands.has_permissions(manage_members=True)
@bot.command()
async def kick(ctx, user:discord.Member, reason):
    if user == bot:
       return
    if user == bot.user:
       return
    
    if reason is None:
        await user.kick(reason="No reason specified.")
        await ctx.reply(f"Successfully kicked {user} without specifing a reason")
    else:
        await user.kick(reason=reason)
        await ctx.reply(f"Successfully kicked {user} for {reason}")       
       


@kick.error
async def kickerror(ctx,error):
   if isinstance(error, commands.MissingPermissions):
    Error = discord.Embed(
        title=f"Error!",
        description="You dont have permission to use this command!",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
    )
    Error.set_author(
        name="KuliNet",
        icon_url=bot.user.avatar.url
    )
    await ctx.send(embed=Error)
      
   

    



bot.run(token=temptoken)