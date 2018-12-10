import datetime
import pandas
import requests
from bs4 import BeautifulSoup

starttime = datetime.datetime.now()

letters = ["i", "z", "e", "h", "s", "g", "l", "b", "o"]
letterDict = {"i":1, "z":2, "e":3, "h":4, "s":5, "g":6, "l":7, "b":8, "o":0}
numberDict = {"1":"i", "2":"z", "3":"e", "4":"h", "5":"s", "6":"g", "7":"l", "8":"b", "0":"o"}


realwordlist = []
definitionlist = []
backnumberlist = []
sumslist = []


def loadWords():
    '''Loads and sorts word list'''

    wordlist=[]
    inFile = open("words.txt", 'r')

    for line in inFile:
        line = line.replace('\n','')
        wordlist.append(line)

    inFile.close()

    wordlist.sort()
    print(wordlist)
    print(len(wordlist), "words loaded.")

    return wordlist


def isCalc(wordlist):
    calcwordlist=[]

    for word in wordlist:

        if len(word) <= 10:

            calcable = True

            for letter in word:
                if letter not in letters:
                    calcable = False

            if calcable == True:
                calcwordlist.append(word)

    return calcwordlist

def getDefiniations(calcwordlist):
    for word in calcwordlist:
        url = "https://www.collinsdictionary.com/dictionary/english/" + word
        r = requests.get(url)
        c = r.content

        soup = BeautifulSoup(c, "html.parser")

        all = soup.find("div", {"class": "def"})

        try:
            all = all.text
            all = all.replace('\n','')
            print(word, all)
            realwordlist.append(word)
            definitionlist.append(all)
        except:
            print(word, "is not a word")

    return realwordlist


def getNumbers(realwordlist):
    for word in realwordlist:
        number = ""
        for letter in word:
            number += str(letterDict[letter])

        backnumber = ""
        for digit in number:
            backnumber = digit + backnumber

        backnumberlist.append(backnumber)

    return backnumberlist


def getSums(backnumberlist):

    count = 1
    numofloops = len(backnumberlist)**3
    percentcomplete = (numofloops / count) * 100

    for num1 in backnumberlist:
        percentcomplete = int((count / numofloops) * 100)
        sums = []
        for num2 in backnumberlist:
            for num3 in backnumberlist:
                print(str(percentcomplete) + "% complete.  Testing: " + num1 + " = " + num2 + " + " + num3)
                if int(num1) == int(num2) + int(num3):

                    word2 = ""
                    for digit in num2:
                        word2 = numberDict[digit] + word2

                    word3 = ""
                    for digit in num3:
                        word3 = numberDict[digit] + word3

                    duplicate = num3 + " + " + num2 + " (" + word3 + " + " + word2 + ")"
                    if duplicate not in sums:
                        sums.append(num2 + " + " + num3 + " (" + word2 + " + " + word3 + ")")

                print(str(percentcomplete) + "% complete.  Testing: " + num1 + " = " + num2 + " - " + num3)
                if int(num1) == int(num2) - int(num3):

                    word2 = ""
                    for digit in num2:
                        word2 = numberDict[digit] + word2

                    word3 = ""
                    for digit in num3:
                        word3 = numberDict[digit] + word3

                    sums.append(num2 + " - " + num3 + " (" + word2 + " - " + word3 + ")")

                print(str(percentcomplete) + "% complete.  Testing: " + num1 + " = " + num2 + " * " + num3)
                if int(num1) == int(num2) * int(num3):

                    word2 = ""
                    for digit in num2:
                        word2 = numberDict[digit] + word2

                    word3 = ""
                    for digit in num3:
                        word3 = numberDict[digit] + word3

                    duplicate = num3 + " * " + num2 + " (" + word3 + " * " + word2 + ")"
                    if duplicate not in sums:
                        sums.append(num2 + " * " + num3 + " (" + word2 + " * " + word3 + ")")

                print(str(percentcomplete) + "% complete.  Testing: " + num1 + " = " + num2 + " / " + num3)
                if int(num1) == int(num2) / int(num3):

                    word2 = ""
                    for digit in num2:
                        word2 = numberDict[digit] + word2

                    word3 = ""
                    for digit in num3:
                        word3 = numberDict[digit] + word3

                    sums.append(num2 + " / " + num3 + " (" + word2 + " / " + word3 + ")")

                count += 1

        sumslist.append(", ".join(sums))

    return sumslist


def makeDataFrame():

    getSums(getNumbers(getDefiniations(isCalc(loadWords()))))

    columns = ['Word', 'Number', 'Definition', 'Sums']
    df = pandas.DataFrame(columns=columns)
    df['Word'] = realwordlist
    df['Number'] = backnumberlist
    df['Definition'] = definitionlist
    df['Sums'] = sumslist
    df = df.set_index('Word')

    return df


def makeFiles(df):

    endtime=datetime.datetime.now()

    '''generates Excel file'''
    writer = pandas.ExcelWriter("CalcDict_excel"+str(endtime)+".xlsx")
    df.to_excel(writer, 'Calculator Dictionary')
    writer.save()

    '''generates html file'''
    html_results = open("CalcDict_html"+str(endtime)+".html", "w")
    html_results.write("<table>\n  <tr>\n    <th>Word</th>\n    <th>Calculator</th>\n    <th>Number</th>\n    <th>Definition</th>\n    <th>Sums</th>\n  </tr>\n")
    for i in range (len(realwordlist)):
        html_results.write("  <tr>\n    <td>"+str(realwordlist[i]).capitalize()+"</td>\n    <td><p3>"+str(realwordlist[i])+"</p3></td>\n    <td>"+str(backnumberlist[i])+"</td>\n    <td>"+str(definitionlist[i])+"</td>\n    <td>"+str(sumslist[i])+"</td>\n  </tr>\n")
    html_results.write("</table>")
    html_results.close()

    print('Started at', starttime)
    print('Finished at', endtime)
    print('Running time:', endtime - starttime)

makeFiles(makeDataFrame())
