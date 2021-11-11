import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import pandas_datareader as pdr
from datetime import datetime
import pandas as pd
import re

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix = "--", help_command = None)

@bot.event
async def on_ready():

    print('Logged in as {0.user}'.format(bot))

    guild_count = 0

    for guild in bot.guilds:
        print("Guild ID:", guild.id)
        print("Guild Name:", guild.name)
        guild_count = guild_count + 1

    if(guild_count == 1):
        print("Stock Bot is in", guild_count, "guild")
    else:
        print("Stock Bot is in", guild_count, "guilds")

# @bot.event
# async def on_message(message):

#     if(message.content == "--hello"):
#         await message.channel.send("Hey moron !!")

#     await bot.process_commands(message)

# @bot.command (name = "ping")
# async def pogo(ctx, *args):
#     await ctx.channel.send("pong")

# =================================================================================================================================
# accept commands with 2020/01/15 format
# allow user to store data in excel file
# make sure date range is valid
@bot.command(name = "get", aliases = ["historical"])
async def send_historical_stock_data(ctx, stock_symbol = None, start_date = None, end_date = None):

    file_path = os.getenv("file_path")

    stock_symbol = stock_symbol.upper()

    start_date_extract = datetime.strptime(start_date, "%d-%m-%Y") 
    end_date_extract = datetime.strptime(end_date, "%d-%m-%Y")

    # yyyymmdd format
    stock_data = pdr.get_data_yahoo(
        symbols = stock_symbol, 
        start = datetime(start_date_extract.year, start_date_extract.month, start_date_extract.day + 1), 
        end = datetime(end_date_extract.year, end_date_extract.month, end_date_extract.day + 1)
    )

    saved_to_csv = stock_data.to_csv(file_path + stock_symbol + '.csv', header = True, index = True)
    await ctx.send(file = discord.File(file_path + stock_symbol + '.csv'))
# =================================================================================================================================

# command to visualize the stock data
# command to offer predictions using ARIMA
# command to offer predictins using LSTM

bot.run(DISCORD_TOKEN)