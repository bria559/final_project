################################
######  Name: Briana Whyte #####
######  Uniqname: brianawh #####
################################

import ast
import requests
import pandas as pd
import json
import twitter_secrets as secrets
import sqlite3
from requests_oauthlib import OAuth1
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from plotly.offline import iplot
from wordcloud import WordCloud
import matplotlib.pyplot as plt

client_key = secrets.API_KEY
client_secret = secrets.API_SECRET
bearer_token = secrets.Bearer_token
access_token = secrets.access_token
access_token_secret = secrets.access_token_secret

azure_key = secrets.azure_key

oauth = OAuth1(client_key,
                client_secret=client_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret)

conn = sqlite3.connect('tweeter.db')
c = conn.cursor()
c.execute('''CREATE TABLE tweet_data (
            account text,
            sentiment_score real
            )''')
conn.commit()
# conn.close()

CACHE_FILENAME = "spo_cache.json"
CACHE_DICT = {}
'''
Goal of project is to return sentiment analysis of twitter user's tweets for the week, graph scores,nand output who had the
most positive week

present data in bar, line, pie, or word cloud

user will provide twitter names to search

'''

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def make_twitter_url(handle):
    max_results = 100
    max_results_string = f'max_results={max_results}'
    q = f"query=from:{handle} -is:retweet"
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        max_results_string, q
    )
    return url


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder, use an underscore ("_") 
    to join your baseurl with the params and all the key-value pairs from params
    E.g., baseurl_key1_value1
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    key_list = []

    for key in params.keys():
        key_list.append(key)

    key_list.sort()

    string_value = ""
    string_value += baseurl

    for key in key_list:
        string_value + '_' + key + '_' + str(params[key])
    return string_value

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    CACHE_DICT = open_cache()
    key_for_request = construct_unique_key(url, headers)
    if key_for_request in CACHE_DICT.keys():
        print('USING CACHE....')
        # print(CACHE_DICT[key_for_request])
        return CACHE_DICT[key_for_request]
    else:
        response = requests.get(url, headers=headers)
        CACHE_DICT[key_for_request] = response.json()
        lo = save_cache(CACHE_DICT)
        print('FETCHING CACHE.....')
        # print(CACHE_DICT[key_for_request])
        return CACHE_DICT[key_for_request]

def lang_data_shape(res_json):
    data_only = res_json["data"]
    doc_start = '"documents": {}'.format(data_only)
    str_json = "{" + doc_start + "}"
    dump_doc = json.dumps(str_json)
    doc = json.loads(dump_doc)
    return ast.literal_eval(doc)

def connect_to_azure(azure_key):
    azure_url = "https://week.cognitiveservices.azure.com/"
    language_api_url = "{}text/analytics/v2.1/languages".format(azure_url)
    sentiment_url = "{}text/analytics/v2.1/sentiment".format(azure_url)
    subscription_key = azure_key
    return language_api_url, sentiment_url, subscription_key

def azure_header(subscription_key):
    h = {'Ocp-Apim-Subscription-Key': subscription_key}
    return h


def generate_languages(headers, language_api_url, documents):
    response = requests.post(language_api_url, headers=headers, json=documents)
    return response.json()

def combine_lang_data(documents, with_languages):
    # print(with_languages)
    langs = pd.DataFrame(with_languages["documents"])
    lang_iso = [x.get("iso6391Name")
                for d in langs.detectedLanguages if d for x in d]
    data_only = documents["documents"]
    tweet_data = pd.DataFrame(data_only)
    tweet_data.insert(2, "language", lang_iso, True)
    json_lines = tweet_data.to_json(orient="records")
    return json_lines

def add_document_format(json_lines):
    docu_format = '"' + "documents" + '"'
    json_docu_format = "{}:{}".format(docu_format, json_lines)
    docu_align = "{" + json_docu_format + "}"
    jd_align = json.dumps(docu_align)
    jl_align = json.loads(jd_align)
    return ast.literal_eval(jl_align)

def sentiment_scores(headers, sentiment_url, document_format):
    response = requests.post(sentiment_url, headers=headers, json=document_format)
    # print(response.json())
    return response.json()

def get_true_scores(scores):
    score_list = []
    for x in scores['documents']:
        score_list.append(x['score'])
    return score_list

def get_mean_score(scores):
    score_list = []
    for x in scores['documents']:
        score_list.append(x['score'])
    # print(score_list)
    return (sum(score_list)/len(score_list))

def week_logic(week_score):
    if week_score > 0.75 or week_score == 0.75:
        return (f"{week_score} This user has a positive score")
    elif week_score > 0.45 or week_score == 0.45:
        return (f"{week_score} This user has a neutral score")
    else:
        return (f"{week_score} This user has a negative score")
# response = requests.get()


if __name__ == "__main__":

    # url = make_twitter_url('bsimsphd')
    # connect = twitter_auth_and_connect(bearer_token, url)
    
    # documents = lang_data_shape(connect)
    # language_api_url, sentiment_url, subscription_key = connect_to_azure(azure_key)
    # headers = azure_header(subscription_key)
    # with_languages = generate_languages(headers, language_api_url, documents)

    # df = combine_lang_data(documents, with_languages)
    # a = add_document_format(df)
    # scores = sentiment_scores(headers, sentiment_url, a)

    # week_score = get_mean_score(scores)
    # print(week_logic(week_score))


    def get_user_input():
        while True:
            user_input = input('Please enter the Twitter handles you would like to analyze, separated by a comma with NO SPACES: ')
            handles = user_input.split(',')
            pie_list = []
            score_list = []
            sentiment_scores_dict = {}
            sentiment_scores_dict['handles'] = handles
            # sentiment_scores_dict['sentiment'] = []

            for handle in handles:
                url = make_twitter_url(handle)
                connect = twitter_auth_and_connect(bearer_token, url)
                documents = lang_data_shape(connect)
                language_api_url, sentiment_url, subscription_key = connect_to_azure(azure_key)
                headers = azure_header(subscription_key)
                with_languages = generate_languages(headers, language_api_url, documents)
                df = combine_lang_data(documents, with_languages)
                a = add_document_format(df)

                scores = sentiment_scores(headers, sentiment_url, a)
                week_score = get_mean_score(scores)
                pie_list.append(week_score)

                true_scores = get_true_scores(scores) # gets the actual scores, not the mean
                score_list.append(true_scores)


                sentiment_scores_dict['sentiment'] = score_list

                sqlite_insert_with_param = """INSERT INTO tweet_data
                          (account, sentiment_score)
                          VALUES (?, ?);"""
                week_logic_s = week_logic(week_score)
                data_tuple = (handle, week_score)
                conn.execute(sqlite_insert_with_param, data_tuple)
                conn.commit()
                print(f"{handle}'s score is {week_logic(week_score)}")
            # print(pie_list)
            conn.close()
            while True:
                graph_input = input('Please enter a number for the visualization you would like to see. 1 = pie chart, 2 = bar graph and dataframe: ')
                validation_list = ['a', 'b', 'c']
                if graph_input.isnumeric() == True:
                    graph_input = int(graph_input)
                    if graph_input <= len(validation_list):
                        if graph_input == 1:
                            trace = go.Pie(labels=handles, values=pie_list,
                                            hoverinfo='label+percent', textinfo='value',
                                            textfont=dict(size=25),marker=dict(line=dict(color='#000000', width=3))
                            )
                            iplot([trace])
                        elif graph_input == 2:
                            data = {'handles': handles,
                                    'sentiment': pie_list
                                    }
                            df = pd.DataFrame(data, columns = ['handles', 'sentiment'])
                            print(df)
                            fig = px.bar(df, x='handles', y='sentiment', title="Bar Graph of Twitter Account's Sentiment Analysis")
                            fig.show()

                            # cars = {'handle': handles,
                            #         'sentiment': score_list
                            #     }
                            # sentiment_scores_dict['sentiment'] = score_list

                            # df2 = pd.DataFrame(cars, columns = ['handles', 'sentiment'])
                            # print(df2.corr())
                            # print(df2)

                            # array_rep = np.array(df2.sentiment)
                            # print(np.array(df2.sentiment))
                            # print(np.corrcoef(array_rep))
                            # print(df2)
                    else:
                        print('Please enter a legitamite number: ')
                else:
                    print('Please enter a number: ')




    get_user_input()
