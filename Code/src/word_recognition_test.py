from image_preprocess import split_sentence, disp_image
import tensorflow as tf
import os,sys
from shutil import copyfile
import subprocess

def get_recognized_words_list(word_path ) :
    recognized_words_list = list()
    words_image_list = [word_path]

    for each_word_image in words_image_list :
        copyfile(each_word_image, "../data/test.png")
        result = subprocess.run(['python3', 'main.py'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        result = result.strip()
        recognized_word = str()

        for each_char_index in range(len(result)-2 , 0 , -1) :
            if result[each_char_index] == '"' :
                recognized_word = recognized_word[::-1]
                recognized_words_list.append(recognized_word)
                break
            else :
                recognized_word += result[each_char_index]

    #os.system("rm w*.png")
    return recognized_words_list

if __name__ == "__main__" :
    pd = '../../../../Downloads/'
    f = open(pd + 'words.txt','r').read().split('\n')

    lines = []
    for each_line in f:
        lines.append(each_line.split())

    new_lines = []

    for each_line in lines:
        if len(each_line) > 2:
            if each_line[1] == 'ok':
                new_lines.append((each_line[0],each_line[-1]))


    predictions = []
    actual = []

    for i in range(300):
        s = new_lines[i][0].split('-')
        filename = pd + 'words/' + s[0] + '/' + "-".join(s[:2]) + '/' + new_lines[i][0] + '.png'
        x = get_recognized_words_list(filename)
        predictions.append(x[0])
        actual.append(new_lines[i][-1])

    error = 0
    total = 0

    for x,y in zip(predictions,actual):
        if x == y:
            pass
        else:
            error += 1
        total += 1

    print(predictions)
    print(actual)

    print(1 - (error/total))
