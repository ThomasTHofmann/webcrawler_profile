import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import string
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
# nltk download location: C:\Users\Admin\AppData\Roaming\nltk_data
#nltk.download()



#Frequency destribution for Skills
fields = ["Skills"]
path = 'C:/Users/Admin/source/repos/nltk_test/skills'
df = pd.read_csv('C:/Users/Admin/source/repos/nltk_test/skills/AI_combined.csv', usecols=fields)

stop_words = set(stopwords.words("english"))
filtered_list = []

print(df.shape[0])
i = 1

while i <= df.shape[0]:
    try:
        a = word_tokenize(df.Skills[i])
    except:
        pass
    b = [word.lower() for word in a if word.isalpha()]
    for word in b:
        if word.casefold() not in stop_words:
            filtered_list.append(word)
    i = i + 1

frequency_distribution = FreqDist(filtered_list)
print(frequency_distribution.most_common(90)) 

print(frequency_distribution.get('artificial'))
frequency_distribution.plot(20, cumulative=False)

'''
#frequency distribution for all info
path = 'C:/Users/Admin/source/repos/nltk_test/skills'
df = pd.read_csv('C:/Users/Admin/source/repos/nltk_test/skills/AI_combined.csv')

stop_words = set(stopwords.words("english"))
filtered_list = []

print(df.shape[0])
i = 1

while i <= df.shape[0]:
    try:
        a = word_tokenize(df.Skills[i])
        a1 = word_tokenize(df.About[i])
        a2 = word_tokenize(df.Education[i])
        a3 = word_tokenize(df.Experience[i])
    except:
        pass
    b = [word.lower() for word in a if word.isalpha()]
    b1 = [word.lower() for word in a1 if word.isalpha()]
    b2 = [word.lower() for word in a2 if word.isalpha()]
    b3 = [word.lower() for word in a3 if word.isalpha()]
    for word in b:
        if word.casefold() not in stop_words:
            filtered_list.append(word)
    for word in b1:
        if word.casefold() not in stop_words:
            filtered_list.append(word)
    for word in b2:
        if word.casefold() not in stop_words:
            filtered_list.append(word)
    for word in b3:
        if word.casefold() not in stop_words:
            filtered_list.append(word)
    i = i + 1

frequency_distribution = FreqDist(filtered_list)
print(frequency_distribution.most_common(90))
print(frequency_distribution.get('artificial'))
print(frequency_distribution.get('intelligence'))
print(frequency_distribution.get('machine'))
print(frequency_distribution.get('learning'))

print(frequency_distribution.get('artificial'))
frequency_distribution.plot(20, cumulative=False)
'''