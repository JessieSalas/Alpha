import pickle

s = open('sentiments.csv', 'r') 
d = {}
for row in s:
    if len(row.split(',')[0].split()) == 1:
        d[row.split(',')[0]] = float(row.split(',')[1][:-1])

with open('sentiments.pickle', 'wb') as outfile:
    pickle.dump(d,outfile)

        

