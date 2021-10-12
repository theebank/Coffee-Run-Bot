#imports
import asyncio
import os
import random
import discord
import sqlite3
from sqlite3 import Error
from discord import Reaction, Member, Client
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intent = discord.Intents().all()

orderstarted = False
coffeeorder = []
coffeegetter = ""
members = []
TOKEN = os.getenv('DISCORD_TOKEN')
Server = os.getenv('DISCORD_SERVER')
bot = commands.Bot(command_prefix='!',intents = intent)

def grabconncurs():
    connection = sqlite3.connect('leaderboard.db')
    cursor = connection.cursor()
    return connection, cursor
def initialize():
    connection,cursor = grabconncurs()
    cursor.execute("DROP TABLE IF EXISTS users")
    table1 = """CREATE TABLE users(name TEXT, coffeeruns INTEGER)"""
    cursor.execute(table1)

    for i in members:
        cursor.execute("INSERT INTO users VALUES (?,0)",(i,))
    connection.commit()
    global errormsg
    errormsg=""

@bot.event
async def on_ready():
    clienti = Client()
    for guild in bot.guilds:
        for i in guild.members:
            members.append(i.name)
    initialize()
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
    connection,cursor = grabconncurs()
    await coffeegetter.create_dm()
    await coffeegetter.dm_channel.send(f"Looks like you're getting the coffee, here's the order:")
    #Adding total coffee runs
    cursor.execute("SELECT coffeeruns FROM users WHERE name = ?", (coffeegetter.name,))
    results = cursor.fetchall()
    newres = results[0][0]+1
    cursor.execute("UPDATE users SET coffeeruns = ? WHERE name = ?", (newres, coffeegetter.name))
    connection.commit()

    for x in coffeeorder:
        string = x[0] + " wants: " + x[1] + '\n'
        await coffeegetter.dm_channel.send(string)


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.content.endswith('if you are down to go get the coffee!'):
        if reaction.emoji == '☕':
            global coffeegetter
            coffeegetter = user

@bot.command(name = 'leaderboard',no_pm =True,pass_context = True, help = 'Shows the coffeerun leaderboard!')
async def get_leaderboard(ctx):
    connection,cursor = grabconncurs()
    cursor.execute("SELECT name,coffeeruns FROM users ORDER BY coffeeruns DESC")
    userlist = cursor.fetchall()
    gettertop = userlist[0][0]
    gettertopc = userlist[0][1]
    gettertop2 = userlist[1][0]
    gettertop2c = userlist[1][1]
    gettertop3 = userlist[2][0]
    gettertop3c = userlist[2][1]

    await ctx.send(f'@everyone! Here are your top 3 coffeerunners in the server! \n #1) {gettertop} with {gettertopc} runs!\n #2) {gettertop2} with {gettertop2c} runs!\n #3) {gettertop3} with {gettertop3c} runs!')
@bot.command(name = 'timer')
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 300:
            await ctx.send("I dont think im allowed to do go above 300 seconds.")
            raise BaseException
        if secondint <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        message = await ctx.send("Timer: {seconds}")
        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="Ended!")
                break
            await message.edit(content=f"Timer: {secondint}")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")
bot.run(TOKEN)