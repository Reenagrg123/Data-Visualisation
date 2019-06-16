import re
from collections import Counter

# First of all I converted the whole text of the file into the words by 
# removing the punctuation because puncutaion are of no use..so its better to remove those
def convert_to_words(content): 
      words_list=re.findall(r'\w+', content.lower())
      #print(type(words_list))
      return words_list    

try:
    with open('big.txt') as f:
        reader=f.read()
        words_list=convert_to_words(reader)
        words_collection=Counter(words_list)
        #print(type(words_collection))
        #print(words_collection)

except Exception as e:
    print(e)

#Finding the occurence of each word in the file words
def find_occ(word):
    word_occ=words_collection[word]
    return word_occ

def find_prob(word):
    total_val=sum(words_collection.values()) 
    word_val=find_occ(word)
    prob_word=word_val/total_val
    #print(prob_word)
    return prob_word

#Finding all possible words that are formed by editing1 character i.e insertion,deletion,replace and transpose
def possible_words_edit1(word):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    edit1_insertion = []
    for i in range(0,len(word)+1):
        for c in chars:
            edit1_insertion.append(word[:i]+ c + word[i:])
    
    edit1_deletion = []
    #t = txt
    for i in range(0,len(word)):
        #t = txt
        edit1_deletion.append(word[:i] +  word[i+1:])

    edit1_replace = []
    for i in range(0,len(word)):
        for ch in chars:
            edit1_replace.append(word[:i] + ch +word[i+1:])
    
    edit1_swap = []
    for i in range(0,len(word)-1):
        word=list(word)
        #swapping of words by converting the word into list
        word[i], word[i+1] = word[i+1], word[i]
        edit1_swap.append(''.join(word))

    possible_words_edit1 = set(edit1_insertion + edit1_deletion + edit1_swap + edit1_replace)
    return possible_words_edit1

#Finding all possible words that are formed by editing2 character i.e insertion,deletion,replace and transpose
def possible_words_edit2(word): 
    edit2_list = []
    for w1 in possible_words_edit1(word):
        for w2 in possible_words_edit1(w1):
            edit2_list.append(w2)
    return edit2_list

#Finding all possible words that are formed by editing2 character i.e insertion,deletion,replace and transpose
# def possible_words_edit3(word): 
#     edit3_list = []
#     for w1 in possible_words_edit1(word):
#         for w2 in possible_words_edit1(w1):
#             for w3 in possible_words_edit1(w2):
#                 edit3_list.append(w3)
#     return edit3_list    


#finding out possible(known) words from the original list
def known_words(word):
    known_words = []
    for w in word:
        if w in words_collection:
            known_words.append(w)
    return set(known_words)

#finding out candidate words
def candidate_words(word):
    cand1 = word
    cand2 = known_words([word])
    cand3 = known_words(possible_words_edit1(word))
    cand4 = known_words(possible_words_edit2(word))
    #cand5 = known_words(possible_words_edit3(word))
    crct_cand=cand2 or cand3 or cand4 or cand1
    #print(crct_cand)
    return crct_cand

#finding the correct word by calculating the max frequency of each known word 
def correct_word(word):
    crct_word = max(candidate_words(word),key=find_prob)
    return crct_word


#Testing the Myspellchecker
def test_spellchecker():
    word=input("Enter any word: ")
    correct=correct_word(word)
    print("The correct word of {} is {}".format(word,correct))
    cand=candidate_words(word)
    print("The other possible words of {} are {}".format(word,cand))
    occ=find_occ(correct)
    print("The occurence of {} in this file is {} ".format(correct,occ))
    prob=find_prob(correct)
    print("The probability of {} is {} ".format(correct,prob))

test_spellchecker()
