from __future__ import division
from tabulate import *

# Given a list of words, return a dictionary of
# word-frequency pairs.
def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist, wordfreq))

#get a list of stop words
def getListStopwords():
    fo = open("stopwordlist.txt")
    stopwords = fo.read()
    stopwords = stopwords.split('\n')
    fo.close()
    return stopwords

#get a list of positive words
def getListPositivewords():
    fo = open("positive_words.txt")
    pword = str.casefold(fo.read())
    pword = pword.split("\n")
    fo.close()
    return pword

#get a list of negative words
def getListNegativewords():
    fo = open("negative_words.txt")
    nword = str.casefold(fo.read())
    nword = nword.split("\n")
    fo.close()
    return nword

#classify stop words using Rabin Karp
def rbkarp_stop(pattern):
    text = getListStopwords()
    NoStopWord = []
    for i in pattern:
        for n in text:
            found = RabinKarp(i, n)
            if found == True:
                break
        if found == False:
            NoStopWord.append(i)
    return NoStopWord

#classify negative words using Rabin Karp
def rbkarp_negat(pattern):
    text = getListNegativewords()
    negativew = []
    for i in pattern:
        for n in text:
            found = RabinKarp(i, n)
            if found == True:
                negativew.append(i)
                break
        #if found == True:
    return negativew

#classify positive words using Rabin Karp
def rbkarp_posit(pattern):
    text = getListPositivewords()
    positivew = []
    for i in pattern:
        for n in text:
            found = RabinKarp(i, n)
            if found == True:
                positivew.append(i)
                break
        #if found == True:
    return positivew

def AnalysisFreq(percent):
    print ("Article is", max(percent, key=lambda i: percent[i]))

def getPercent(fpositive, fnegative, ffullword):
    ratio = 100/ffullword
    percent = {"Positive": fpositive*ratio,
    "Negative": fnegative*ratio}
    return percent

def getFreq(positive, negative, fullword, dic):
    fpositive = 0
    fnegative = 0
    ffullword = 0
    for i in positive:
        fpositive += dic[i]
    for i in negative:
        fnegative += dic[i]
    for i in dic.keys():
        ffullword += dic[i]
    freq = {"Positive": fpositive, "Negative": fnegative, "Full": ffullword}
    return freq

def get_dic(keys, ori_dic):
    new_dic = {}
    for i in keys:
        new_dic[i] = ori_dic[i]
    return new_dic

def sortFreqDict(freqdict):
    aux = [[freqdict[key], key] for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def AnalaysisArticle(positive, negative,  fullword, dic):
    freq = getFreq(positive, negative,  fullword, dic)
    percent = getPercent(freq["Positive"], freq["Negative"], freq["Full"])
    results = {"freq": freq, "percent": percent}
    return results

def printAnalysis(results):
    table_header = ["Type","Total Words", "Percentage (%)"]
    table_body = [
    ["Positive", results["freq"]["Positive"], "%.1f" % results["percent"]["Positive"]],
    ["Negative", results["freq"]["Negative"], "%.1f" % results["percent"]["Negative"]]
    ]

    print (tabulate(table_body, table_header),
           "\n\nTotal Words after removed stop words: ", results["freq"]["Full"])
    AnalysisFreq(results["percent"])

def RabinKarp(pat, txt): ## Rabin Karp Algorithm
    q = 101
    d = 256
    M = len(pat)
    N = len(txt)
    j = 0
    p = 0    # hash value for pattern
    t = 0    # hash value for txt
    h = 1
    if N < M:
        return 0
    for i in range(M-1):
        h = (h*d) % q

    # Calculate the hash value of pattern and first window of text
    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    # Slide the pattern over text one by one
    for i in range(N-M+1):
        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break
            j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == M:
                if (i == 0):
                    if(M == N):
                        return True
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q
            if t < 0:
                t = t+q

def data(file): # to call all the function
    # to open and read file
    f = open(file, "r")
    frequency_list = {}
    for word in f.read().split():
        for char in '"-.,"\n':
            word = word.replace(char,'')
        frequency_list[word] = frequency_list.get(word,0)+1

    noStop_list = rbkarp_stop(frequency_list)#to remove stop words
    dictionary = wordListToFreqDict(noStop_list)
    sorteddict = sortFreqDict(dictionary)
    positivew = rbkarp_posit(dictionary)  # List of positive words
    negativew = rbkarp_negat(dictionary)  # List of negative words
    # Get Dictionary for P/N/Ne
    positivew_dic = get_dic(positivew, dictionary)
    negativew_dic = get_dic(negativew, dictionary)
    # Create a combination of dictionary
    Classified_dic = {
        'Positive': positivew_dic,
        'Negative': negativew_dic,
    }

    results = AnalaysisArticle(positivew, negativew, noStop_list, dictionary)
    # Printing Analysis
    print("\n\nfile:", file)
    printAnalysis(results)

def main():
    # while loop to continue search for file and 'q' to quit the loop
    while True:
        file = input("Enter text file ('q' to quit) : ")
        if file !="q":
            data(file);
        else:
            print("End")
            break
if __name__ =="__main__":
    main()

    #print(f.read())
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\columbia.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\us.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\france.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\newark.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\taiwan.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\hongkong.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\doha.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\narita.txt
    #C:\\Users\\ziyee\\Dropbox\\year2sem2\\WIA2005\\Assignment\\uk.txt
