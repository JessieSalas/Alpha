#Does some processing, gives metrics
import pickle

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
