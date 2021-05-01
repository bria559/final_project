README

REQUIRED PACKAGES:
ast
requests
pandas
json
sqlite3
requests_oauthlib import OAuth1
plotly.express
numpy
plotly.graph_objS
plotly.offline import iplot
matplotlib.pyplot as plt

To interact with this program, provide the names of twitter accounts you would like to work with. DO NOT INCLUDE @ SYMBOL. Enter the account names without spaces and separate using commas. I recommend using twitter accounts with a high posting rate like foxnews.
After, choose the data visualization you would like to see.

Source Docs

Twitter API - https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api
Microsoft Azure Text Analytics API - https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/how-tos/text-analytics-how-to-call-api?tabs=synchronous

Source Access

I accessed the Twitter API data by obtaining the api key, secrets key, bearer token, and access tokens and
made a request to the API in the proper format. I specifically asked the API to return tweets that were not retweets so I can analyze the sentiment analysis of only original tweets. I also set the maximum amount of tweets returned to 100. In addition, the API can ony return tweets posted up to 7 days ago and not a day over. As a reult, the tweets that will be analyzed are pulled from within the week.

I applied for a microsoft azure account so that I could use there text analytics API which does sentiment analysis, opinion mining, etc. I focused on the sentiment analysis feature.

Source Fields

The Twitter API returns a json in the following format:

{"https://api.twitter.com/2/tweets/search/recent?max_results=100&query=from:bsimsphd -is:retweet": {"data": [{"id": "1387131199647371273", "text": "@EllrieAlllen Mad props for connecting the Jay."}, {"id": "1387130931933286401", "text": "@EllrieAlllen Me and my DMs, texts, and emails every semester right after grades post. https://t.co/u4g4foj5ps"}, {"id": "1387130248614092803", "text": "@charlie_markers #Hov"}, {"id": "1387075851188121610", "text": "And no I'm not through with it; in fact I'm just previewing it."}, {"id": "1387066511546855425", "text": "@Meik_SoICY https://t.co/RMsI1ka5ji"}, {"id": "1386915836716277760", "text": "https://t.co/6UqFyQZsJD https://t.co/PSrjOWR7as"}, {"id": "1386889064276799488", "text": "@jidebam @Meik_SoICY https://t.co/nDW4iVpd4u"}, {"id": "1386047844226830346", "text": "Past experiences with good friends increase in value over time."}, {"id": "1385432179975630853", "text": "My new house is on the river"}], "meta": {"newest_id": "1387131199647371273", "oldest_id": "1385432179975630853", "result_count": 9}}

Source Challenge

8
Twitter API 6 - (wasn't able to use Spotify do to Oauth issues)
JSON Files 2

Database Schema
The database was created using sqlite 3. It containes the average sentiment score and account name for each account passed to the program.

Presentation Description
Ploltly was used to create the bar graph and pie chart

Presentation Instructions
Enter the number corresponding to the visualization you would like to see

