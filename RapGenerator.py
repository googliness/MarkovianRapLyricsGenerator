import random
import re


"""location of rap dataset"""
RAPFILELOCATION = 'Datasets/rap_lyrics.txt'


""" Calulating Transition Probabilities for next probable words using Markovian Model """
def getTransitionProb(rapLib, transProb):
    currWord = rapLib[0]
    for i in range(1, len(rapLib)):
        nextWord = rapLib[i]
        # if the current word is an unseen word
        if currWord not in transProb.keys():
            transProb[currWord] = {}
            transProb[currWord][nextWord] = 1
        # if the current word and the next word have not been seen simultaneously before
        elif nextWord not in transProb[currWord].keys():
            transProb[currWord][nextWord] = 1
        else:
            transProb[currWord][nextWord] += 1
        currWord = nextWord
    return transProb


""" Converting Trasition Probabilities to a Percentage """
def convertToPercentage(transProb):
    for currWord in transProb.keys():
        totalWords = sum(transProb[currWord].values())
        for nextWord in transProb[currWord].keys():
            transProb[currWord][nextWord] /= totalWords
    return transProb


""" Generating rap lyrics using the seed word taken as input by user
 and transition Probability calculated before """
def makeRap(latestWord, transProb, rapLib):
    rap = ''
    wordCount = 0
    while wordCount < 101:
        rap += latestWord + ' '
        wordCount += 1
        latestWord = getNextWord(latestWord, transProb, rapLib)
    return rap


""" Guessing the next most likely word using the current word """
def getNextWord(latestWord, transProb, rapLib):
    randomProb = random.uniform(0, 1)
    currProb = 0.0
    if latestWord not in rapLib:
        return random.choice(rapLib)
    else:
        for nextWord in transProb[latestWord].keys():
            currProb += transProb[latestWord][nextWord]
            if currProb > randomProb:
                return nextWord

    return random.choice(rapLib)


""" Reading the rap lyrics from raw dataset to python list """
def getRapLib():
    with open(RAPFILELOCATION, 'r') as f:
        rapLib = re.sub("\n", " \n", f.read()).lower().split(' ')
        return rapLib


if __name__ == '__main__':
    rapLib = getRapLib()
    print('What should the first word of your DOPE RAP be!!')
    firstWord = input()
    print('\n')
    transProb = getTransitionProb(rapLib, {})
    transProb = convertToPercentage(transProb)
    dopeRap = makeRap(firstWord, transProb, rapLib)
    print(dopeRap)




