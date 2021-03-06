import discord
import os
import json
import random
import pyjokes
import prismapy
from discord.ext import commands


def get_prefix(client, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
analytics = prismapy.Prismalytics("Key", client)
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(name="Nobita doing his homework.", type=3))
    print('The Bot is ready.')


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '-'

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.command(aliases=['prefix'])
@commands.has_permissions(manage_guild=True)
async def change_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)
    embed = discord.Embed(
        title="Prefix",
        description=f'Prefix changed to: `{prefix}` on {ctx.guild}')
    await ctx.send(embed=embed)


def is_it_me(ctx):
    return ctx.author.id == 690922103712776202


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description="This command doesn't exist.")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error",
            description="You don't have the permissions to use this command.")
        await ctx.send(embed=embed)


@client.command()
async def about(ctx):
    embed = discord.Embed(
        title="About",
        description="""Hello, I'm **Doraemon**,
I am not a 22nd century bot, I have been built in 21st century by [**Pratish**](http://programmingwizard.tech/).
I am a multi functional bot. I can be used for Fun, Moderation, . I can also play music.
Use the `help` command to know my commands and their functions.
Please [`invite`](https://discord.com/api/oauth2/authorize?client_id=709321027775365150&permissions=32668710&scope=bot) me to your server:
""")
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Doraemon's commands:",
        description="""
> To use a  command type `<prefix><command>`.

**General Commands**

`about` - To know about the bot.
`ping` - Check the bot's latency.
`github` - Github Repo.
`stats` - Check the bot's statistics.
`8ball <your question>` - Play magic 8 Ball and get the answers to all your questions.
`count` - Count of messages in a channel.
`joke` - A random joke.
`info` - General Info of a member.

**Moderation Commands**

`clear <amount of messages>` - Clears the specified no. of messages.(default=5)
`kick <member> <reason>` - Kicks a member out of the server.
`ban <member> <reason>` - Bans a member in the server.
`unban <member>` - Unbans the member in the server.
`prefix <new prefix>` - Changes the Prefix for a specific server.
""")
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title="Ping",
        description=f'Pong! `Latency: {round(client.latency * 1000)} ms`')
    await ctx.send(embed=embed)


@client.command()
async def github(ctx):
    embed = discord.Embed(
        title="GitHub Repo",
        description="GitHub Repo:\n https://github.com/programming-wizard/doraemon")
    await ctx.send(embed=embed)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        'It is certain.',
        'As I see it, yes.',
        'Reply hazy, try again.',
        "Don't count on it.",
        'It is decidedly so.',
        'Most likely.',
        'Ask again later.',
        'My reply is no.',
        'Without a doubt.',
        'Outlook good.',
        'Better not tell you now.',
        'My sources say no.',
        'Yes – definitely.',
        'Yes.',
        'Cannot predict now.',
        'Outlook not so good.',
        'You may rely on it.',
        'Signs point to yes.',
        'Concentrate and ask again.',
        'Very doubtful.',
    ]
    embed = discord.Embed(
        title="Magic 8 Ball",
        description=f'Question: {question}\nAnswer: {random.choice(responses)}')
    await ctx.send(embed=embed)


@client.command()
async def joke(ctx):
    embed = discord.Embed(
        title="Joke",
        description=f'{pyjokes.get_joke()}')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command(aliases=['yeet'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title="Kicked",
        description=f'{member.mention} has been kicked.')
    await member.kick(reason=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title="Banned",
        description=f'{member.mention} has been banned.')
    await member.ban(reason=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title="Banned",
                description=f'{user.mention} has been unbanned.')
            await ctx.send(embed=embed)
            return


@client.command()
async def count(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    embed = discord.Embed(
        title="Total Messages",
        description=f"There were {count} messages in {channel.mention}")
    await ctx.send(embed=embed)


@client.command()
async def info(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Name:", value=member.display_name)

    embed.add_field(name=f"Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role: ", value=member.top_role.mention)

    embed.add_field(name="Bot? ", value=member.bot)

    await ctx.send(embed=embed)


@client.command()
async def spam(ctx, *, message):
    counter = 0
    while counter < 10:
        await ctx.send(message)
        counter += 1


@client.event
async def on_command(ctx):
    analytics.send(ctx)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('Bot Token')
