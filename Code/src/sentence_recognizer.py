from image_preprocess import split_sentence, disp_image
import tensorflow as tf
import os,sys
from shutil import copyfile
import subprocess

def get_recognized_words_list(sentence_path) :
    recognized_words_list = list()
    os.system("rm w*.png")
    words_image_list = split_sentence(sentence_path)
    image_number = 1


    for each_word_image in words_image_list :
        destination_path = "../data/w" + str(image_number) + ".png"
        copyfile(each_word_image, destination_path)
        result = subprocess.run(['python3', 'main.py','--img_file',destination_path], stdout=subprocess.PIPE).stdout.decode('utf-8')
        result = result.strip()
        recognized_word = str()
        image_number += 1
        for i in range(len(result)) :
            if result[i] == '"' :
                i += 1
                while result[i] != '"' :
                    recognized_word += result[i]
                    i += 1
                break

        recognized_words_list.append(recognized_word)

    os.system("rm ../data/w*.png")
    return " ".join(recognized_words_list)

if __name__ == "__main__" :
    print("\n\n\nThe recognized sentence by our algorithm is follows -\n\n",get_recognized_words_list(sys.argv[1]),"\n\n")
