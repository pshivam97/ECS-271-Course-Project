import enchant
import nltk,sys
from sentence_recognizer import *
from nltk.corpus import brown
import pickle
import heapq

class PriorityQueue:

    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):

        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

def get_neighbours(state,sentence_words) :
    to_ret = []
    if len(state[0]) != 0 :
        for i in word_list :
            last_word= state[0][-1]
            dist = (1-lm[last_word].prob(i)) * lv_distance(sentence_words[len(state[0])],i)
            new_state = (state[0]+(i,), state[1] + dist)
            to_ret.append(new_state)

    else :
        for i in word_list :
#             dist =  (1)* lv_distance(sentence_words[len(state[0])],i)
            dist =  (1-(freq_1gram[i] / word_list_raw_len))* lv_distance(sentence_words[len(state[0])],i)
            new_state = ( (i,), dist)
            to_ret.append(new_state)
    return to_ret



def correct_text(sentence) :
    print("started ucs")
    fringe = PriorityQueue()
    initial_state = ((),0)
    fringe.push(initial_state, initial_state[1])
    while not fringe.isEmpty() :
        curr_state = fringe.pop()
        if len(curr_state[0]) == len(sentence) :
            final_state = curr_state
            break
        neighbours = get_neighbours(curr_state,sentence)
        for i in neighbours :
            fringe.push(i,i[1])

    return final_state[0]



def lv_distance(a, b):
    string1 = a
    string2 = b
    distance = 0
    n1 = len(string1)
    n2 = len(string2)

    if n1 >= n2:
        for i in range(n1):
            if i < n2:
                if string1[i] != string2[i]:
                    distance += 1
            else:
                distance += 1
    else:
        for i in range(n2):
            if i < n1:
                if string2[i] != string1[i]:
                    distance -= 1
            else:
                distance -= 1


    return abs(distance) + 0.5

with open('../model/language_model.pickle','rb') as f :
    lm = pickle.load(f)
    freq_1gram = pickle.load(f)
    word_list_raw_len = pickle.load(f)
    word_list = pickle.load(f)


sentence = get_recognized_words_list(sys.argv[1])
print("Output of CTC : ", sentence)
rec = correct_text(sentence)
print("Corrected Output : ", rec)
