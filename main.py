
# Imports
import json
from discord.ext import commands, tasks
import discord
import os
import yt_dlp
from discord import FFmpegPCMAudio

#testing...
from dotenv import load_dotenv
load_dotenv()
temptoken = os.getenv("token")




# import config stuff from JSON
with open("configuration.json", "r") as token_json:
    config = json.load(token_json)
    token = config["Token"]
    prefix = config["command_prefix"]
    loggingchannel = int(config["LogChannelID"])

# Defining bot and stuff with discordpy
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=prefix, intents=intents)
logchannel = bot.get_channel(loggingchannel)

@bot.command()
async def join(ctx):
    Error = discord.Embed(
        title=f"Error!",
        description="The bot doesn't know where to join make sure to join a channel first before execution of ```!join```",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
    )
    Error.set_author(
        name=f"{bot.user}",
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
        name=f"{bot.user}",
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
        name=f"{bot.user}",
        icon_url=bot.user.avatar.url
    )
    playlog = discord.Embed(
        title=f"User {ctx.author.mention}",
        description=f"has requested to play **{title}** \n by: **{author}**",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
    )
    playlog.set_author(
        name=f"{bot.user}",
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
          name=f"{bot.user}",
          icon_url=bot.user.avatar.url
       )
       music.set_thumbnail(
          url=thumbnail
       )
       await ctx.send(embed=music)
       await loggingchannel.send(embed=playlog)
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
        name=f"{bot.user}",
        icon_url=bot.user.avatar.url
    )
    await ctx.send(embed=left)
    await ctx.voice_client.disconnect()
      
@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, user:discord.Member, reason):
    kicklog = discord.Embed(
       title=f"User Disconnected (By Force)",
       description=f"An admin/mod {ctx.author.mention} has kicked {user} for {reason}",
       timestamp=discord.utils.utcnow(),
       color=discord.Color.red()
    )
    kicklog.set_author(
       name=f"{bot.user}",
       icon_url=bot.user.avatar.url
    )
    if user == bot:
       return await ctx.send("Can't kick a bot!")
    if user == bot.user:
       return await ctx.send(f"Can't kick {bot.user} using this command!")
    
    await user.kick(reason=reason)
    await ctx.reply(f"Successfully kicked {user} for {reason}")       
    await loggingchannel.send(embed=kicklog)
       


@kick.error
async def kick_error(ctx,error):
     if isinstance(error, commands.MissingPermissions):
        Error = discord.Embed(
        title=f"Error!",
        description="You dont have permission to use this command!",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
        )
        Error.set_author(
        name=f"{bot.user}",
        icon_url=bot.user.avatar.url
        )
        await ctx.send(embed=Error)
     else:
        await ctx.send(f"{error}")
   


@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, user:discord.Member, reason):
    banlog = discord.Embed(
       title=f"Ban hammer has struck!⚡",
       description=f"An admin/mod {ctx.author.mention} has banned {user} for {reason}",
       timestamp=discord.utils.utcnow(),
       color=discord.Color.red()
    )
    banlog.set_author(
       name=f"{bot.user}",
       icon_url=bot.user.avatar.url
    )

    if user == bot:
       return await ctx.send("Can't ban a bot!")
    if user == bot.user:
       return await ctx.send(f"Can't ban {bot.user} using this command!")
    
    await user.kick(reason=reason)
    await ctx.reply(f"Successfully banned {user} for {reason}")   
    await loggingchannel.send(embed=banlog)
    
@kick.error
async def ban_error(ctx,error):
     if isinstance(error, commands.MissingPermissions):
        Error = discord.Embed(
        title=f"Error!",
        description="You dont have permission to use this command!",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.red()
        )
        Error.set_author(
        name=f"{bot.user}",
        icon_url=bot.user.avatar.url
        )
        await ctx.send(embed=Error)
     else:
        await ctx.send(f"{error}")





bot.run(token=temptoken)