# from googlesearch import search
from GoogleNews import GoogleNews
import re
import requests
import numpy as np
from bs4 import BeautifulSoup

# labels for testing, no longer accurate
#labels = [1,0,1,1,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,1,1,1,1,0,0,0,1,1]

# define dictionaries of positive and negative sentiment words
positiveDict = {}
negativeDict = {}

# add to dictionary takes an individual word and it's associated label and stores it in corresponding dictionary
def addToDictionary(word, label):
    if label == 0:
        if word in negativeDict:
            negativeDict[word] = negativeDict[word] + 1
        else:
            negativeDict[word] = 1
    if label == 1:
        if word in positiveDict:
            positiveDict[word] = positiveDict[word] + 1
        else:
            positiveDict[word] = 1

# parse article takes a text and splits the words
def parseArticle(article_body, label):
    lines = article_body.split("\n")
    for line in lines:
        # line = re.sub(r'|:^https?:\/\/.*[\r\n\']*', '', line)
        # line = re.sub('<[^>]+>', '', line)
        line = ''.join(char for char in line if char.isalnum() or char == ' ')
        line = line.lower()
        print(line)
        words = line.split(' ')
        for word in words:
            addToDictionary(word, label)

# open article uses beautiful soup & requests to get the body of an article from the url and pass it into parsing
def openArticle(article_url, label):
    soup = BeautifulSoup(requests.get(url=article_url).text, 'html.parser')
    parseArticle(soup.body.get_text(), label)

# runQuery gets the results of a Google News query and parses the articles
def runQuery(query, numresults):
    googlenews = GoogleNews()
    googlenews.setperiod(period='7d')
    # googlenews.setTimeRange('04/01/2022', '04/14/2022')
    googlenews.get_news(query)
    count = 0
    for result in googlenews.results():

        # print(result['title'])
        parseArticle(result['title'], labels[count])
        count = count + 1
        if count == len(labels):
            break

# get thie probability of a word in a dictionary
def probWordIs(word, dict):
    return np.log(dict.get(word, 1)/sum(dict.values()))


# classifies article (currently based on title) by comparing it to dictionaries
def classifyArticle(article_title):
    # article title gets non alphanumeric characters removed
    article_title = ''.join(char for char in article_title if char.isalnum() or char == ' ')
    article_title = article_title.lower()
    # split words into array
    words = article_title.split(' ')
    # get the log of the total percentage 
    pPos = np.log(calcPercentagePositive())
    pNeg = np.log(1-calcPercentagePositive())
    for word in words:
        # add the probability for each word to the overall percentage
        pPos += probWordIs(word, positiveDict)
        pNeg += probWordIs(word, negativeDict)
    # get the overall percentages for positive and negative to divide the individual percentages
    percentPos = (sum(positiveDict.values()))/(sum(positiveDict.values())+sum(negativeDict.values()))
    percentNeg = (sum(negativeDict.values()))/(sum(positiveDict.values())+sum(negativeDict.values()))
    pPos /= percentPos
    pNeg /= percentNeg
    # return the greater probability
    if pPos > pNeg:
        return 1
    return 0

# determine total percentage of positive words as a percentage of total words
def calcPercentagePositive():
    one = 0
    total = 0
    for label in labels:
        if label == 1:
            one += 1
        total += 1
    return (one + 0.0) / total

# fill the dictionary with words by getting the latest data and storing it
def fillDict():
    # run Query currently runs the query, gets results, and passes it along to the next code
    runQuery(query="AMC News", numresults=1)
    # printing the dictionaries after the queries have finished sorting
    print(len(positiveDict))
    print(positiveDict)
    print(len(negativeDict))
    print(negativeDict)


fillDict()
print(classifyArticle("This is an Article Title It is good and I like it very much Great stuff Excellent"))