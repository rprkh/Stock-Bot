import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import time
import pandas_datareader as pdr
from datetime import datetime
import pandas as pd
import numpy as np
import lxml
from lxml import html
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
import yfinance as yf
import requests

load_dotenv()

file_path = os.getenv("file_path")
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

# gets historical stock data for the specified company in the selected range
@bot.command(name = "get", aliases = ["historical"])
async def send_historical_stock_data(ctx, stock_symbol = None, start_date = None, end_date = None):

    stock_symbol = stock_symbol.upper()
    
    # accept input in dd-mm-yyyy format
    start_date_extract = datetime.strptime(start_date, "%d-%m-%Y") 
    end_date_extract = datetime.strptime(end_date, "%d-%m-%Y")

    # pass data in yyyymmdd format
    stock_data = pdr.get_data_yahoo(
        symbols = stock_symbol, 
        start = datetime(start_date_extract.year, start_date_extract.month, start_date_extract.day + 1), 
        end = datetime(end_date_extract.year, end_date_extract.month, end_date_extract.day)
    )

    saved_to_csv = stock_data.to_csv(file_path + stock_symbol + '.csv', header = True, index = True)
    await ctx.send(file = discord.File(file_path + stock_symbol + '.csv'))

# visualize the stock data using different parameters
@bot.command(name = "visualize", aliases = ["plot", "display"])
async def plot_stock_data(ctx, stock_symbol = None, x_data = None, y_data = None):

    stock_symbol = stock_symbol.upper()
    x_data = x_data.title()
    if(y_data == "adj-close"):
        y_data = "Adj Close"
    else:
        y_data = y_data.title()    

    df = pd.read_csv(file_path + stock_symbol + '.csv')

    fig = go.Figure([go.Scatter(x = df[x_data], y = df[y_data])])
    
    fig.update_layout(
        title = {
            'text': stock_symbol + " Stock Data",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title = x_data,
        yaxis_title = y_data,
        font = dict(
            family = "Times New Roman",
            size = 15,
            color = "Black"
        )
    )

    fig.write_image(file_path + stock_symbol + ".jpg")
    await ctx.send(file = discord.File(file_path + stock_symbol + '.jpg'))

# displays the pe ratio of the company
@bot.command(name = "p/e-ratio")
async def peratio(ctx, stock_symbol = None):

    stock_symbol = stock_symbol.upper()
    stock_symbol_info = yf.Ticker(stock_symbol)
    await ctx.channel.send(stock_symbol_info.info['trailingPE'])

# displays information about a specific company
@bot.command(name = "information")
async def information(ctx, stock_symbol = None, type_of_information = None):

    stock_symbol = stock_symbol.upper()
    stock_symbol_info = yf.Ticker(stock_symbol)

    if(type_of_information == "all"):
        for key, value in stock_symbol_info.info.items():
            await ctx.channel.send(f"{key}: {value}")
    else:
        await ctx.channel.send(stock_symbol_info.info[type_of_information])

# extracts the income statement, balance sheet and cash flow for the desired company
@bot.command(name = "financials")
async def data_scraper(ctx, stock_symbol = None, type_of_data = None):

    if (type_of_data == "income-statement"):
        join = 'financials'
        url = 'https://finance.yahoo.com/quote/' + stock_symbol.upper() + '/' + join + '?p=' + stock_symbol.upper()
    if (type_of_data == "balance-sheet"):
        url = 'https://finance.yahoo.com/quote/' + stock_symbol.upper() + '/' + type_of_data + '?p=' + stock_symbol.upper()
    if (type_of_data == "cash-flow"):
        url = 'https://finance.yahoo.com/quote/' + stock_symbol.upper() + '/' + type_of_data + '?p=' + stock_symbol.upper()

    # simulating a request from the Chrome browser
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1', # Do Not Track Request Header 
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
    
    web_page = requests.get(url, headers = headers)
    tree = html.fromstring(web_page.content)

    for i in tree.xpath("//h1/text()"):
        type_of_data = type_of_data.title()
        await ctx.channel.send(type_of_data + " for " + i)

    rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
    assert len(rows) > 0

    extracted_rows = []

    for row in rows:
        extracted_row = []
        element = row.xpath("./div")

        count = 0

        for el in element:
            try:
                (text, ) = el.xpath('.//span/text()[1]')
                extracted_row.append(text)
            except ValueError:
                extracted_row.append(np.NaN)
                count = count + 1

        if (count < 4):
            extracted_rows.append(extracted_row)

    df = pd.DataFrame(extracted_rows)
    df = df.set_index(0)
    df = df.transpose()

    columns = list(df.columns)
    columns[0] = 'Date'
    df = df.set_axis(columns, axis = 'columns', inplace = False)

    numeric_columns = list(df.columns)[1::]

    for col in numeric_columns:
        df[col] = df[col].str.replace(',', '') # remove the comma seperators
        df[col] = df[col].astype(np.float64) # convert the type from object to float64

    csv_save = df.to_csv(file_path + stock_symbol.upper() + '-' + type_of_data + '.csv', header = True, index = False)
    await ctx.send(file = discord.File(file_path + stock_symbol.upper() + '-' + type_of_data + '.csv'))
    
bot.run(DISCORD_TOKEN)