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

path = 'C:/Users/Admin/source/repos/nltk_test/skills'
#Frequency destribution for Skills
def freq_skills():
    fields = ["Skills"]
    
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


#frequency distribution for all info
def freq_all():
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

#tfidf cosine similarity testing:
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
#'C:/Users/Admin/source/repos/csv_stuff/csv_stuff/Combine/Profiles so far.csv'

df = pd.read_csv('C:/Users/Admin/source/repos/csv_stuff/csv_stuff/Combine/Profiles so far1.csv')
print(df.head(5))
#['About','Experience', 'Education', 'Skills']
#df['Skills']
ted = df['Skills'].fillna('').values.astype('U').ravel()
#vectorizer.get_feature_names()[1400:1420] gives you the words in the text between the two numbers
vectorizer = TfidfVectorizer(stop_words = 'english')

#need to write values.astype('U') otherwise there is an error
# ravel joins the arrays together otherwise error
tfidf_matrix = vectorizer.fit_transform(ted)

print(tfidf_matrix.shape)
print(vectorizer.get_feature_names()[1400:1420])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape)
print(cosine_sim[1])
#print(cosine_sim)

#print(cosine_sim[0,1])
indices = pd.Series(df.index, index = df['Name']).drop_duplicates()
print(indices[:20])
# gets most similar profile to the given name. Input is the name of the profile.
def get_results(title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:11]
    result_indices = [i[0] for i in sim_scores]
    print(df.iloc[result_indices])

get_results("Jason Zintak", cosine_sim)

#change the query depending on what you want to search to compare
query_tfidf = vectorizer.transform(["Artificial Intelligence"])
cosine_sim2 = cosine_similarity(query_tfidf, tfidf_matrix)
# give
def query_get_results(cosine_sim = cosine_sim2):
    idx = 0
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    #change length of list here
    sim_scores = sim_scores[1:11]
    result_indices = [i[0] for i in sim_scores]
    print('LIST STARTS HERE:')
    print(df.iloc[result_indices])

query_get_results()

print(cosine_sim2)
sort_result = cosine_sim2.argsort()[::-1][:10]
print(sort_result)
print(df.iloc[sort_result[0][0]])

