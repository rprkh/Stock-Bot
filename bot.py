import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import pandas_datareader as pdr
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA

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

bot.run(DISCORD_TOKEN)