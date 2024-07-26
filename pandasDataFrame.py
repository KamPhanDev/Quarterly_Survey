#! Python3

import pandas as pd
import Config, openpyxl
import re
import nltk
from nltk.corpus import stopwords

def getTextData(fileName):
    with open(fileName, 'r') as txt:
        ref = txt.readline().capitalize()
        return ref.split(',')

refFeedback = getTextData('feedbackKeyword.txt')
print(refFeedback)

refImprovement = getTextData('improvementKeyword.txt')
print(refImprovement)

refeeling = getTextData('feelingKeyword.txt')
print(refeeling)


print(stopwords.words('english'))
feedbackGivenCol = 'If you wish, please give further feedback on these scores.'
feedbackKeywordsCol = 'Further Feedback Key Words'
improvementSuggestionCol = 'How can we improve your experience with UK SBS services?'
improvementKeywordCol = 'Improvement Key Words'
feelingCol = 'Please describe how you feel about UK SBS.'
feelingKeywordCol = 'Feeling Key Words'


data = pd.read_excel(Config.fileName, sheet_name=Config.responseData)



for index, row in data.iterrows():
    print(row[feedbackGivenCol])
    if str(row[feedbackGivenCol]) != 'nan':
        keywords = str(row[feedbackGivenCol].lower())
        keywords = keywords.replace(',', '')
        keywords = keywords.replace('.', '')
        keywords = keywords.split()
        keywords = [word for word in keywords if word.lower() not in stopwords.words('english')]
        keywords = [word for word in keywords if word.capitalize() in refFeedback]
        keywords = list(dict.fromkeys(keywords))
        row[feedbackKeywordsCol] = ','.join(keywords)

    if str(row[improvementSuggestionCol]) != 'nan':
        keywords1 = str(row[improvementSuggestionCol])        
        keywords1 = keywords1.replace(', ', '')
        keywords1 = keywords1.replace('.', '')
        keywords1 = keywords1.split()
        keywords1 = [word for word in keywords1 if word.lower() not in stopwords.words('english')]
        keywords1 = [word for word in keywords1 if word.capitalize() in refImprovement]
        keywords1 = list(dict.fromkeys(keywords1))
        print(keywords1)
        row[improvementKeywordCol] = ','.join(keywords1)
        print(row[improvementKeywordCol])

    if str(row[feelingCol]) != 'nan':
        keywords2 = str(row[feelingCol])        
        keywords2 = keywords2.replace(', ', '')
        keywords2 = keywords2.replace('.', '')
        keywords2 = keywords2.split()
        keywords2 = [word for word in keywords2 if word.lower() not in stopwords.words('english')]
        keywords2 = [word for word in keywords2 if word.capitalize() in refeeling]
        keywords2 = list(dict.fromkeys(keywords2))
        print(keywords2)
        row[feelingKeywordCol] = ','.join(keywords2)
        print(row[feelingKeywordCol])

        
data.to_excel('test1.xlsx', sheet_name=Config.responseData, index=False)
data2 = pd.read_excel('test1.xlsx', sheet_name=Config.responseData)
# feedbackList = []
# improvementList = []
# feelingList = []
# for index, row in data2.iterrows():
#     if str(row[feedbackKeywordsCol]) != 'nan':
#         print(str(row[feedbackKeywordsCol]))
#         feedbackList.extend(str(row[feedbackKeywordsCol]).split(','))
#         print(feedbackList)
#         print(len(feedbackList))

#     if str(row[improvementKeywordCol]) != 'nan':
#         improvementList.extend(row[improvementKeywordCol].split(','))

#     if str(row[feelingKeywordCol]) != 'nan':
#         feelingList.extend(row[feelingKeywordCol].split(','))

# feedbackDict = {key: 0 for key in feedbackList}

# print(feedbackDict)
# improvementDict = dict.fromkeys(improvementList)
# feelingDict = dict.fromkeys(feelingList)

