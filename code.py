from __future__ import print_function

import sys
from math import exp

currfile = sys.argv[1] if len(sys.argv) > 1 else "<<default>>"

# Print to stderr for non answer output
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# LINE 1
numBooks, numLibs, numDays = list(map(int, input().split()))

#eprint(numBooks, numLibs, numDays)

# LINE 2
bookScores = list(map(int, input().split()))
maxBookScore = max(bookScores)
minBookScore = min(bookScores)

libraries = [None for _ in range(numLibs)]

# REST OF INPUT
for i in range(numLibs):
    booksInLib, signDays, shipAmount = list(map(int, input().split()))
    books =  list(map(int, input().split()))
    libraries[i] = (i, booksInLib, signDays, shipAmount, books)

#eprint(libraries)

# every already selected book
chosenBooks = set()

# list of signed up libraries
chosenLibraries = []

# books we have chosen per library
# in order of signup time
booksPerLib = []

def preSortLibraries(libraries):
    for lib in libraries:
        lib[4].sort(key=lambda x: bookScores[x])

def prioritizeTime(library, daysLeft):
    scanAmount = library[3]
    scannableBooks = daysLeft * scanAmount

    scannableBooks = min(scannableBooks, len(library[4]))
    score = 0
    for i in range(scannableBooks):
        book = library[4][-i-1]
        score += bookScores[book]
    return score * (1 / library[2])

def longTimeOutput(library):
    numBooks = library[1]
    scanAmount = library[3]
    return numBooks / scanAmount

def averageBooks(library):
    # average score of the books in  library
    totalSum = 0
    for book in library[4]:
        totalSum += bookScores[book]
    return totalSum / len(library[4])

def test_kimi(library):
    avgBooks = averageBooks(library)
    longTimeOutput1 = longTimeOutput(library)
    return avgBooks * longTimeOutput1

def normalize_book_score(score):
    return (score - minBookScore) / (maxBookScore - minBookScore)

def sigmoid(x):
    return 1 / (1 + exp(-x))

def minValue(library):
    # minVal = 90000000000
    # for book in library[4]:
    #     bookVal = bookScores[book]
    #     if bookVal < minVal:
    #         minVal = bookVal
    # return minVal
    return min(library[4])

def maxValue(library):
    # maxValue = 0
    # for book in library[4]:
    #     if bookScores[book] > maxValue:
    #         maxValue = bookScores[book]
    return max(library[4])

def lowestSignDays(library):
    return library[2]

def limitedTime(library):
    k = 20
    books = library[4]
    if len(books) > k:
        score = 0
        for book in books[:-k]:
            score += bookScores[book]
        return score
    return 0

def most_unique(library):
    numNonUniques = 0
    totalNum = library[1]
    curSet = set(library[4])
    for lib in libraries:
        compSet = set(lib[4])
        curIntersect = len(curSet.intersection(compSet))
        if numNonUniques < curIntersect:
            numNonUniques = curIntersect
    return numNonUniques/totalNum

def sum_score(library):
    return sum(library[4])


# averages, min and max of library book score was <expletive>

totalScorePossible = sum(bookScores)
#eprint(currfile, "Max Possible: ", totalScorePossible)

preSortLibraries(libraries)
allBooks = set()
libraries.sort(key=lambda x: x[3])
for i, library in enumerate(libraries):
    #eprint("comparing set of", len(allBooks), "with library of size", len(set(library[4])))
    diff = set(library[4]).difference(allBooks)
    allBooks = allBooks.union(diff)
    libraries[i] = (library[0], library[1], library[2], library[3], list(diff))
#libraries.sort(key=averageBooks)
#libraries.sort(key=test_kimi)


libraries.sort(key=lambda x: prioritizeTime(x, numDays))


numDropped = 0
signUpBlock = 0 #block signup process for these days 
signingUpLibrary = None

for day in range(numDays):
    #eprint("day", day, "signupBlock", signUpBlock)
    # signup process

    if signUpBlock <= 0:
        # Library is done signup
        if signingUpLibrary is not None:
            #eprint("adding library", signingUpLibrary[0], "to chosen libs")
            # Biggest score at end of array

            # remove because presorting all the libraries
            #signingUpLibrary[4].sort(key=lambda x: bookScores[x])

            chosenLibraries.append(signingUpLibrary)
            booksPerLib.append([])
            signingUpLibrary = None
        
        # Signing up new library
        if len(libraries):
            #eprint("signing up new library")
        #while len(libraries):
            # AAAAH - Tim
            libraries.sort(key=lambda x: prioritizeTime(x, numDays-day))
            chosenLib = libraries.pop()
            #if (numDays-day) - chosenLib[2] < 0:
            #    continue
            signingUpLibrary = chosenLib
            signUpBlock = chosenLib[2]
        
    signUpBlock -= 1
    
    for i, lib in enumerate(chosenLibraries):
        scanAmount = lib[3]
        booksChosen = []
        while len(booksChosen) != scanAmount and len(lib[4]):
            book = lib[4].pop()
            if book in chosenBooks:
                numDropped += 1
                continue
            booksChosen.append(book) # local to the picking sesh
            chosenBooks.add(book) # globally chosen books
        booksPerLib[i].extend(booksChosen)

    # for i, library in enumerate(libraries):
    #     diff = set(library[4]).difference(chosenBooks)
    #     chosenBooks = chosenBooks.union(diff)
    #     libraries[i] = (library[0], library[1], library[2], library[3], list(diff))
    #     libraries.sort(key=sum_score, reverse=True)

                
# OUTPUT
    
numFull = 0
for i, library in enumerate(chosenLibraries):
    if len(booksPerLib[i]):
        numFull += 1

print(numFull)
for i, library in enumerate(chosenLibraries):
    if not len(booksPerLib[i]):
        continue
    print(library[0], len(booksPerLib[i]))

    # Potentially slow
    print(" ".join(list(map(str, booksPerLib[i]))))
    
eprint(currfile, "Num Dropped: ", numDropped)
eprint("finished set", sys.argv[1] if len(sys.argv) > 1 else "<<default>>")
