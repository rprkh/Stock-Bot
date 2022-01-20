# Stock Bot

Discord Bot that provides a convenient way to access stock data from the internet. Visualize stock data in any time range, get stock recommendations and much more !!   
The bot is hosted on Heroku and is online 24/7.

## Add the Bot to a Server

**Step 1**: 

Simply paste this link into a new tab in your browser.

https://discord.com/api/oauth2/authorize?client_id=906905618739245058&permissions=271972432&scope=bot

**Step 2**: 

Login to your Discord account if you haven't already and select the server you want the Stock Bot to get added to. 

Next click on `Continue`.

#### Note: Make sure you have Manage Server permissions. If you do not have the necessary permissions you can request the server owner to give it to you or you can create your own Discord server.

**Step 3**:

Approve all the permission for the Stock Bot to make use of all its functions.

Click on `Authorize` and you should be good to go. The Stock Bot will get added to your server.

That's it !!

Just 3 simple steps to follow and now you can use the Stock Bot in your server with your friends.

## Commands

The following command list best describes the functions of the Stock Bot.

**Command List**

| Description                             | Command                                                   |
| :-------------------------------------- | :-------------------------------------------------------- |
| Extracts historical stock data          | `--get`, `--historical`                                   |
| Plots a graphical visualization         | `--visualize`, `--plot`, `--display`                      |
| Displays the PE ratio of the company    | `--p/e-ratio`                                             |
| Displays general stock information      | `--information`                                           |
| Displays the company's financials       | `--financials`                                            |
| Displays the company's recommendations  | `--recommendations`                                       |

## Using the Bot

#### Note: All commands should begin with `--`.

## 1. Get Historical Stock Data

```bash
--get googl 25-06-2014 10-01-2021
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h3.PNG)

You can change the name of the company and vary the time range based on your preference. 

Alternately you could also replace `--get` and use the command's alias `--historical` instead, like this:

```bash
--historical googl 25-06-2014 10-01-2021
```

The output would be the same for both the cases.

## 2. Visualize Stock Data

```bash
--visualize tsla date adj-close 05-08-2015 19-12-2021
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h4.PNG)

You can change the company name, X-axis, Y-axis and time range for the visualization as demonstrated below:

```bash
--visualize ibm date volume 16-02-2019 25-09-2019
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h5.PNG)

## 3. Get the PE Ratio of the Company

```bash
--p/e-ratio aapl
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h6.PNG)

## 4. General Stock Information

This command will print out all the publicly available information about Netflix.

```bash
--information nflx all
```

In case you want specific company information you should use:

```bash
--information nflx shortRatio
```

```bash
--information nflx bookValue
```

```bash
--information nflx beta
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h7.PNG)

Depending on the use case both the company name and the type of information can be modified.

## 5. Get Company Financials

The 3 types of financials that can be extracted are:
 - Balance Sheet
 - Cash Flow
 - Income Statement

The followings command sends a `.csv` file to the text channel of the server.

```bash
--financials msft balance-sheet
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h8.PNG)

```bash
--financials msft cash-flow
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h9.PNG)

```bash
--financials msft income-statement
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h10.PNG)

## 6. Stock Recommendations

Displays the stock recommendations (Buy / Sell)

The following command can be used to display the stocks information:

```bash
--recommendations amzn
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h11.PNG)

For S&P500 companies the recommendations will be sent from A-Z in the form of a message to the text channel followed by a `.csv` file containing the recommendations of all the companies.

You can use the following command to look at recommendations for all the S&P500 companies.

```bash
--recommendations sp500
```

![Nav Bar](https://github.com/rprkh/Stock-Bot/blob/main/images/h12.PNG)