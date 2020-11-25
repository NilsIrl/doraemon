import discord
import os
import asyncio
import prismapy
import random
from discord.ext import commands
from discord.utils import get
from discord.utils import find
import database
import env_file


client = commands.Bot(command_prefix="-")
analytics = prismapy.Prismalytics("2oZ3tPpluuZ3V0DtSqcEjQ", client, save_server=True)
client.remove_command("help")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(name="You using my Gadgets [-help]", type=3),
    )
    print(f'Bot is running as "{client.user}"')
    print("=========================================")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # guild = database.find_guild(message.guild.id)
    # if guild is None:
    #     profile = {
    #         "guild_id": message.guild.id,
    #         "prefix": "-",
    #         "welcome_channel": None,
    #         "welcome_message": "Hey {user.mention} welcome to {guild.name}",
    #         "welcome_type": "channel",
    #         "subreddits": ["memes", "dankmemes"],
    #         "autorole": False,
    #         "on_join_role": None,
    #     }

    #     database.add_guild(profile)
    #     print(f"Profile has been created for {message.guild.name}:{message.guild.id}")
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    embed = discord.Embed(
        colour=0x2859B8,
        description="""Hello, Thanks for adding Doraemon!
        Doraemon is a multipurpose Discord Bot that has the commands commonly used on every server. It can also helps you do a lot of things right in discord.
        
        There are a lot of things you can do with Doraemon. Simply use the `-help` command to see a list of commands you can use.
        """,
    )
    embed.add_field(
        name="**__Usefull Links__**",
        inline=False,
        value="""
    Consider upvoting **[Doraemon](https://top.gg/bot/709321027775365150)** on Top.gg
    Have an issue/suggestion? Join the **[Support Server](https://discord.gg/yMkdWMg)**
    You can find the source code on **[Doraemon's GitHub page](https://github.com/pratishrai/doraemon)**
    """,
    )
    await channel.send(embed=embed)


# @client.event
# async def on_guild_remove(guild):
#     database.remove_guild(guild.id)


@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if member.guild.id == 699037304836063292:
        print(f"Hey {member.mention}, Welcome to {member.guild}")
    else:
        await channel.send(f"Hey {member.mention}, Welcome to {member.guild}")


def is_it_me(ctx):
    return ctx.author.id == 690922103712776202


@client.event
async def on_command_error(ctx, error):
    print(error)


@client.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.channel.typing():
            embed = discord.Embed(
                title="Help",
                colour=0x2859B8,
                description="""
    Here's the list of commands you can use:
    """,
            )
            embed.add_field(
                name="**__General__**", value="```\nping\ngithub\nstats\ninvite```"
            )
            embed.add_field(name="**__Fun__**", value="```\nmeme\ngif\njoke\n-```")
            embed.add_field(
                name="**__Utility__**", value="```\nlmgtfy\npoll\nreddit\n-```"
            )
            embed.add_field(
                name="**__Reactions__**",
                value="```\nlaugh\nshrug\nhug\ncry\npat\n-```",
            )
            embed.add_field(
                name="**__Moderation__**",
                value="```\nclear\nkick\nban\nunban\ninfo\nserverinfo\n```",
            )
            embed.add_field(name="**__Other__**", value="```\n-\n-\n-\n-\n-\n-```")
            embed.add_field(
                name="\u200b",
                inline=False,
                value="Use `-help <command name>` to know more about each command",
            )
        await ctx.send(embed=embed)


@help.command()
async def ping(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-ping")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="Check bot's latency")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-ping`",
        )
    await ctx.send(embed=embed)


@help.command()
async def github(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-github")
        embed.add_field(name="Alias", value="`-gh`")
        embed.add_field(name="Usage", inline=False, value="Bot's Github Repo")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-github`\n`-gh`",
        )
    await ctx.send(embed=embed)


@help.command()
async def stats(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-stats")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="Check the bot's statistics")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-stats`",
        )
    await ctx.send(embed=embed)


@help.command()
async def invite(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-invite")
        embed.add_field(name="Alias", value="None")
        embed.add_field(
            name="Usage", inline=False, value="Get the invite link for the bot"
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-invite`",
        )
    await ctx.send(embed=embed)


@help.command()
async def meme(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-meme")
        embed.add_field(name="Alias", value="`-m`")
        embed.add_field(
            name="Usage", inline=False, value="Get a random meme from reddit."
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-meme`\n`-m`",
        )
    await ctx.send(embed=embed)


@help.command()
async def gif(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-gif")
        embed.add_field(name="Alias", value="`-g`")
        embed.add_field(
            name="Usage",
            inline=False,
            value="Get a random GIF from tanor on the specified query.",
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-gif <search term>`\n`-gif hello`\n`-g bye`",
        )
    await ctx.send(embed=embed)


@help.command()
async def joke(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-joke")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="Get a random joke.")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-joke`",
        )
    await ctx.send(embed=embed)


@help.command()
async def lmgtfy(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-lmgtfy")
        embed.add_field(name="Alias", value="None")
        embed.add_field(
            name="Usage",
            inline=False,
            value="Returns a [lmgtfy.com](https://lmgtfy.com/) link.",
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-lmgtfy <question>`\n`-lmgtfy `",
        )
    await ctx.send(embed=embed)


@help.command()
async def poll(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-poll")
        embed.add_field(name="Alias", value="`-strawpoll` `-sp`")
        embed.add_field(
            name="Usage",
            inline=False,
            value="Create polls on [StrawPoll](https://strawpoll.com/) right in discord.",
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-poll <title>|<option 1>|<option 2>|<option n>`\n`-poll How was our day|nice|fine|bad|idk`",
        )
    await ctx.send(embed=embed)


@help.command()
async def reddit(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-reddit")
        embed.add_field(name="Alias", value="`-r`")
        embed.add_field(
            name="Usage", inline=False, value="Search for reddit posts in a subreddit."
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-reddit <subreddit>|<search term>`\n`-r memes|lol`",
        )
    await ctx.send(embed=embed)


@help.command()
async def clear(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-clear")
        embed.add_field(name="Alias", value="`-c`")
        embed.add_field(
            name="Usage",
            inline=False,
            value="Clears the specified no. of messages in a channel",
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-clear <no. of messages>`\n`-clear` (deletes the last message)\n`-clear 10`",
        )
    await ctx.send(embed=embed)


@help.command()
async def kick(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-kick")
        embed.add_field(name="Alias", value="`-yeet`")
        embed.add_field(
            name="Usage", inline=False, value="Kick a member out of the server."
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-kick <@user> <reason>`\n`-kick @xyz some weird reason`",
        )
    await ctx.send(embed=embed)


@help.command()
async def ban(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-ban")
        embed.add_field(name="Alias", value="None")
        embed.add_field(
            name="Usage", inline=False, value="Ban a member from the server."
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="-ban <@user> <reason>`\n`-ban @xyz some weird reason`",
        )
    await ctx.send(embed=embed)


@help.command()
async def unban(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-unban")
        embed.add_field(name="Alias", value="None")
        embed.add_field(
            name="Usage", inline=False, value="Unban a member from the server."
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="-unban <user#discriminator>`\n`-unban xyz#6179`",
        )
    await ctx.send(embed=embed)


@help.command()
async def info(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-info")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="General Info of a member.")
        embed.add_field(
            name="Example",
            inline=False,
            value="-info <@user>`\n`-info @xyz`\n`-info` (shows your info)",
        )
    await ctx.send(embed=embed)


@help.command()
async def serverinfo(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-serverinfo")
        embed.add_field(name="Alias", value="`-sinfo`")
        embed.add_field(name="Usage", inline=False, value="General Info of the Server")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-serverinfo`\n`-sinfo`",
        )
    await ctx.send(embed=embed)


@help.command(aliases=["laugh", "pat", "shrug", "hug", "cry"])
async def reactions(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="reactions")
        embed.add_field(
            name="Alias",
            value="`-laugh`, `-pat <@user>`, `-shrug`, `-hug @user`, `-cry`",
        )
        embed.add_field(name="Usage", inline=False, value="Quickly send gif reactions.")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-laugh`\n`-pat <@user>`\n`-shrug`\n`-hug @user`\n`-cry`",
        )
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="Ping",
            colour=0x2859B8,
            description=f"Pong! `Latency: {round(client.latency * 1000)} ms`",
        )
    await ctx.send(embed=embed)


@client.command(aliases=["gh"])
async def github(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="GitHub Repo",
            colour=0x2859B8,
            description="https://github.com/pratishrai/doraemon",
        )
    await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
            description="Invite me to your server using [this link](https://discord.com/api/oauth2/authorize?client_id=709321027775365150&permissions=8&scope=bot)",
        )
    await ctx.send(embed=embed)


@client.event
async def on_command(ctx):
    await analytics.send(ctx)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

token = env_file.get()

client.run(token["BOT_TOKEN"])