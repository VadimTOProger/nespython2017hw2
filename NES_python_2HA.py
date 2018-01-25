##### Importing needed libraries: beginning #####

import pandas as pd
import numpy as np
import requests
import itertools
import re
import urllib.request
from bs4 import BeautifulSoup
import html5lib

##### Importing needed libraries: end #####

##### Problem 1: beginning #####

def problem1(n = None):
    sum_n = 0
    i = 0
    while i < n:
        if i%3 == 0 or i%5 == 0:
            sum_n = sum_n + i
        i = i + 1
    return sum_n

print('\n\nProblem 1\n\n\nOutput for n = 100:',problem1(100),'\nOutput for n = 10,000:',problem1(10000))

##### Problem 1: end #####


##### Problem 2: beginning #####

def fibo(n):
    if n >= 0:
        if n == 0: return 0
        elif n == 1: return 1
        else: return fibo(n-1)+fibo(n-2)
    else:
        if n == -1: return 1
        else: return fibo(n+2)-fibo(n+1)


fibo_seq = []
indx= []
results = pd.DataFrame({})
for i in range(-10,11):
    fibo_seq.append(fibo(i))
    indx.append(i)
    
results['N - element'] = indx
results['Fibonacci number'] = fibo_seq

print('\n\nProblem 2.\n\n\nFibonacci numbers for n from -10 to 10 \n',results)

###UNECCESSARY PART: JUST TRYING TO PARSE DATA BEFORE PROBLEM 7: BEGINNING###
url = "https://ru.wikipedia.org/wiki/Числа_Фибоначчи"
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')
soup_p = soup.prettify()

tab = soup.prettify()[soup_p.find('<img alt="F_{n}" aria-hidden="true" class="mwe-math-fallback-image-inline" src="https://wikimedia.org/api/rest_v1/media/math/render/svg/76cdf519c21deec43f984815e57e15d2dd3575d7" style="vertical-align: -0.671ex; width:2.713ex; height:2.509ex;"/>'):soup_p.find('</table>\n      <p>\n       Легко заметить, что\n')]

test = tab[tab.find('<td>\n'):]
tab2 = test.split('\n        </td>\n        <td>\n         ')
tab2 = tab2[1:-1]
tab2 = pd.Series(tab2)
tab2 = pd.to_numeric(tab2.str.replace('−','-'))

print('Calculated values matches Fibonacci numbers from WikiPedia:',sum((tab2 == results['Fibonacci number'])*1) == len(tab2))
###UNECCESSARY PART: JUST TRYING TO PARSE DATA BEFORE PROBLEM 7:END###

#print('Fibonacci number for n = 200\n', fibo(200))

##### Problem 2: end #####


##### Problem 3: beginning #####

path = input("\n\nProblem 3.\n\n\nPlease specify a path to 'words-list-russian.txt' file:\n")
#name = r'words-list-russian.txt'
words = pd.read_csv(path,header = None)
words.columns = ['Словарь']


# Firstly, in order to limit huge data set, I am going to convert words to lists, sort them, and then join it back.
#Then I will choose only duplicities and continue working with them, as these words have at least 1 anagram.
tt = words['Словарь'].apply(lambda x: list(x))
tt = tt.apply(lambda x: list(pd.Series(x).sort_values(ascending = True)))
ttt = tt.apply(lambda x: ''.join(x))


ett = ttt[ttt.duplicated(False)] # False means that we take all duplicates without any execption. In other words,
#dropping only unique values (words without any anagram)
e_df = pd.DataFrame(ett)



#Calculating number of duplicates in order to limit our data frame
n_dup = []
for i in range(len(ett)):
    n_dup.append(sum((ett == ett.iloc[i])*1))

e_df['N of duplicates'] = n_dup



# restricting our data set: choosing only words with 3 or more anagrams
ff_df = e_df[e_df['N of duplicates']>=4]

new_dict = words['Словарь'][ff_df.index]


#defining function which find anagrams
def anagr(str1 = None,str2 = None):
    str1 = list(str1)
    str1.sort()
        
    str2 = list(str2)
    str2.sort()
    
    if str1 == str2:
        return True
    else:
        return False

#searching for anagrams
list_of_lists = []
for j in range(len(new_dict)):
    list_anagr = []
    
    for i in range(len(new_dict)):
        if anagr(new_dict.iloc[j],new_dict.iloc[i]):
            list_anagr.append(new_dict.iloc[i])
    list_of_lists.append(list_anagr)



#deleting duplicated groups of anagrams
anagrams = pd.Series(list_of_lists)
anagrams = anagrams.apply(lambda x: ','.join(x))
anagrams.drop_duplicates(inplace = True)


#getting list of anagrams with at least 4 words
print('\n\n',anagrams,'\n\n')


print('We have %s groups of anagrams with at least 4 words:\n\n' % len(anagrams))
for i in range(len(anagrams)):
    print(str(i+1)+'.',anagrams.iloc[i]+';\n')

##### Problem 3: end #####

##### Problem 4: beginning #####

key_word = 'лекарство'

'''
### OUTDATED METHOD - compiling too long
new_words = []
for i in range(2,len(key_word)):
    for j in itertools.permutations(key_word, i):
        s_word = ''.join(j)
        if len(words[words['Словарь'].isin([s_word])]) != 0:
            new_words.append(s_word)


result_words = pd.Series(new_words).drop_duplicates()
print(len(result_words))
'''

### New Method
#creating function for making dictonaries from words
def dictionaring(x=None):
    lt = list(x)
    ul = np.unique(lt)
    dic = {i:lt.count(i) for i in ul}
    return dic


#applying function mentioned above
words['Dictionaring'] = words['Словарь'].apply(lambda x: dictionaring(x))


#Loop: finding new words
y = dictionaring(key_word)
new_words=[]

for i in range(len(words)):
    x = words['Dictionaring'][i]
    if len(set(x.items()) & set(y.items())) == len(x):
        new_words.append(words['Словарь'][i])
new_words = pd.Series(new_words)


#Checking
print('\n\nProblem 4.\n\n\nChecking: whether there are words from task description\n', new_words[new_words.isin(['отсек','рвота','река'])],'\n\n')


#couting number of words
print("We managed to create %s new words from word 'лекарство\n\n\n'" %len(new_words))

##### Problem 4: end #####


##### Problem 5: beginning #####


duplicated_letters = words['Словарь'].apply(lambda x: sum((pd.Series(list(x)).duplicated())*1))
words['Duplicated letters'] = duplicated_letters

#restricting dataframe
words_game = words[words['Duplicated letters']==0]['Словарь']
words_game = words_game[words_game.str.len()==5]


#GAME
print('Problem 5.\n\n\nStart of the game')
guess = []
little_hack = 'я сдаюсь!'
k = 0
set_word = words_game.iloc[np.random.randint(len(words_game))]

while set_word != guess:
    guess = input('Enter your guess:')
    k+=1
    
    if guess == little_hack:
        print('You gave up after',k,'attempts, shame on you. The word was %s' %set_word)
        break
    elif len(guess) != 5:
        print('Your word contains more than or less than 5 letters! Enter one more time.')
    elif sum(pd.Series(list(guess)).duplicated()*1) != 0:
        print('Your word contains duplicated letters! Enter one more time.')
    else:
        if sum(words_game.isin([guess])*1) == 1:
            if set_word == guess:
                print('End of the game. Count of attempts: %s' %k)
            else:
                print('%s letter in common'%len(set(list(guess))&set(list(set_word))))
        else:
            print('I don\'t know such word. Enter one more time')

##### Problem 5: end #####


##### Problem 6: beginning #####

'''
duplicated_letters = words['Словарь'].apply(lambda x: sum((pd.Series(list(x)).duplicated())*1))
words['Duplicated letters'] = duplicated_letters
#restricting dataframe
words_game = words[words['Duplicated letters']==0]['Словарь']
words_game = words_game[words_game.str.len()==5]
'''

#Game
words_game2 = words_game.copy(deep=True)
set_word=input('\n\nProblem 5.\n\n\nStart of the game\nSet your word:\n')
#if sum(words_game.isin([set_word])*1)==1:
guess = []
k=0

while set_word != guess:
    if sum(words_game.isin([set_word])*1)==1:
        guess = words_game2.iloc[np.random.randint(len(words_game2))]
        k+=1
        print('My guess:',guess)
        rlt = input('How many letters are right?\n')
        if int(rlt) == 0:
            mask = words_game2.apply(lambda x: len(set(list(x))&set(list(guess))))==0
            words_game2 = words_game2[mask]
        elif int(rlt) < 5:
            words_game2.drop(words_game2.index[words_game2.isin([guess])][0],0,inplace = True)
        elif int(rlt) == 5:
            mask = words_game2.apply(lambda x: len(set(list(x))&set(list(guess))))==5
            words_game2 = words_game2[mask]
    else: 
        print('I don\'t know this word!')
        set_word=input('Start of the game\nSet your word:\n')
print('I\'ve finnaly done it','after %s attempts!\n\n' %k)


##### Problem 6: end #####


##### Problem 7: beginning #####

link = 'http://www.belstat.gov.by/ofitsialnaya-statistika/makroekonomika-i-okruzhayushchaya-sreda/natsionalnye-scheta/godovye-dannye_11/proizvodstvo-valovogo-vnutrennego-produkta/'

response = urllib.request.urlopen(link)
html = response.read()

data_raw = pd.read_html(html)
df_raw = data_raw[0]

n_names = list(df_raw.loc[0])
n_names[0] = df_raw[0][1]
df_raw.columns = n_names

df_raw = df_raw.iloc[2:]
df_raw.reset_index(inplace = True, drop = True)


df_raw[df_raw.columns[1:]] = df_raw[df_raw.columns[1:]].applymap(lambda x: x.replace(u'\xa0',''))
df_raw[df_raw.columns[1:]] = df_raw[df_raw.columns[1:]].applymap(lambda x: x.replace(' ',''))
df_raw[df_raw.columns[1:]] = df_raw[df_raw.columns[1:]].apply(lambda x: x.replace('x',np.nan))


df = df_raw.convert_objects(convert_numeric=True)


df.set_index(df['Валовой внутренний продукт'], drop = True, inplace = True)
df.drop('Валовой внутренний продукт',1, inplace = True)
df.iloc[1] = df.iloc[1]/10

print('\n\nProblem 7.\n\n\n',df)

##### Problem 7: end #####