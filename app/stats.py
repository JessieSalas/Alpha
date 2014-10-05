#Does some processing, gives metrics
import pickle
from behavioral_analysis import *

with open('sentiments.pickle', 'rb') as infile:
    sentiments = pickle.load(infile)

sentiment_words = set(sentiments.keys())

def getSleepRegularity(time_list):
#Returns a normalized notion of sleep regularity based on between 0 and 1. 
#Most values are very close to 1, unless we have reason to believe otherwise.
    temp = []
    late_posts = 0
    for time in time_list:
        t_refined = time.split('+')[0].split('T')[1]
        temp.append(  [int(nib) for nib in t_refined.split(':')]  ) # [hr, min, sec] representation
    for time in temp:
        t = time[0] #hours
        if t == 2 or t == 3 or t == 4: #if you post at 2,3, or 4 A.M.
            late_posts += 1
    late_ratio = float(late_posts)/ len(temp)
    if  late_ratio < 0.5: #if you post late less than half the time
        sleep_regularity = 1 - late_ratio #this is very logical
    else:
        sleep_reularity = 1 #then you might just be a late person

    return sleep_regularity

def getVariability(messages):
    ins = 0
    sents = []
    for word in messages:
        if word in sentiment_words:
            sents.append(sentiments[word])
    prev = 0
    curr = 1
    av = .01
    p = len(sents)
    for val in range(p-1):
        av += sents[curr] - sents[prev]
        prev += 1
        curr += 1
    if p != 0:
        av = av/p
    else:
        av = 0
    return av



def risk_metric(msg):
    """
    params:
        not used - sleep 0 to 1, 1 is regular
        five is result of big_five(msg) (dict of {trait : 0 to 1})
    returns:
        -1 to 1 metric 


    risk seeking: male, young (<25 arbitrarily?), 
        irregular sleep, extraverted, open
    risk averse: neuroticism, agreeable, conscientious

    note: opposing big five traits do no sum to one

    see tables 8, 9: http://www.london.edu/facultyandresearch/research/docs/risk.ps.pdf
    """
    five = big_five(msg)
    # this is totally statistically sound
    total = float(sum(five.values()))
    normed = {} 
    for trait in five:
        normed[trait] = five[trait]/total
    
    # currently arbitrary :\ 
    risk_weights = {"disagreeable":1, 
    "open": 1, 
    "extraversion":1, 
    "unconscientious":0.5, 
    "stability":0.5,
    "neurotic":-0.5, 
    "agreeable":-1, 
    "conscientious":-0.5, 
    "introversion":-1, 
    "closed":-1}

    risk = 0.0

    for trait in normed:
        risk += normed[trait] * risk_weights[trait]

    return risk



def getLikeIndex(likes):
#could be negative, or not
    l_sent = 0
    howmany = 0
    for like in likes:
        if like in sentiment_words:
            l_sent += sentimens[word]
            howmany += 1
    if howmany != 0:
        l_sent = l_sent/howmany  
    else:
        l_sent = 0
    return l_sent
