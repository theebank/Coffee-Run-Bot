#imports
import asyncio
import os
import random
import discord
from discord import Reaction, Member
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = intents=discord.Intents.all()

orderstarted = False
coffeeorder = []
coffeegetter = ""

TOKEN = os.getenv('DISCORD_TOKEN')
Server = os.getenv('DISCORD_SERVER')
bot = commands.Bot(command_prefix='!',intents = intents)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the coffee server')


@bot.command(name = 'startcoffeerun',pass_context = True,help = 'starts a coffee run',no_pm=True)
async def start_coffee_run(ctx):
    msg = await ctx.send(f'@everyone! {ctx.message.author.name} is starting a coffee run! \n - React with ☕️ if you are down to go get the coffee!')

    await msg.add_reaction('☕')

    global orderstarted
    global coffeeorder
    global coffeegetter

    orderstarted = True
    coffeeorder = []
    coffeegetter = ""

@bot.command(name = 'order',no_pm = True,pass_context = True, help = 'If there is a coffee run already started, your order is added to the run. \n If there is not, nothing will happen.')
async def add_order_to_run(ctx,*,arg):
    order = []
    if orderstarted ==True:
        order.append(ctx.message.author.name)
        order.append(arg)
        global coffeeorder
        coffeeorder.append(order)


@bot.command(name = 'end',no_pm = True,pass_context = True,help = 'Ends the order')
async def end_order(ctx):
    await coffeegetter.create_dm()
    await coffeegetter.dm_channel.send(f"Looks like you're getting the coffee, here's the order:")
    for x in coffeeorder:
        string = x[0] + " wants: " + x[1] + '\n'
        await coffeegetter.dm_channel.send(string)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.content.endswith('if you are down to go get the coffee!'):
        if reaction.emoji == '☕':
            global coffeegetter
            coffeegetter = user
    else:
        print('hughuguhgug')

bot.run(TOKEN)