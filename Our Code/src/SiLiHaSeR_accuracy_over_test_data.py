from SiLiHaSeR_phase1_image_preprocess import split_sentence, disp_image
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
    return " ".join(recognized_words_list).strip()

def run_test_data() :
    array_of_predicted_strings = list()

    first_test_image_index = 0
    last_test_image_index = 33

    for i in range(first_test_image_index, last_test_image_index + 1) :
        array_of_predicted_strings.append(get_recognized_words_list("test"+str(i)+".png"))
    print(array_of_predicted_strings)
    test_data = {
        "test0":"or work on line level",
        "test1":"My name is Shivam",
        "test2":"God helps those who help themselves",
        "test3":"Quick brown fox jumps over the lazy dog",
        "test4":"Adversity and loss make a man wise",
        "test5":"A fool and his money are soon parted",
        "test6":"All good things come to an end",
        "test7":"Always put your best foot forward",
        "test8":"All's fair in love and war",
        "test9":"Necessity is the mother of invention",
        "test10":"No news is good news",
        "test11":"She doesn't study geometry on Sunday",
        "test12":"Life is a dream for the wise",
        "test13":"Religion is regarded by the commons as true",
        "test14":"Learn to speak well and listen better",
        "test15":"Give more than you take",
        "test16":"Yesterday is the deadline for all complaints",
        "test17":"No one can ruin your day without your permission",
        "test18":"Do difficult things while they are easy",
        "test19":"The greatest wealth is to live content with little",
        "test20":"Happiness and freedom begin with one principle",
        "test21":"Actions speak louder than words",
        "test22":"A computer is able to learn from experience",
        "test23":"Predicting the future isn't magic, it's aritificial intelligence",
        "test24":"A bad workman always blames his tools",
        "test25":"Better late than never",
        "test26":"Ignorance is bliss",
        "test27":"Cleanliness is next to Godliness",
        "test28":"Familiarity breeds Contempt",
        "test29":"Fortune favors the brave",
        "test30":"Blood is thicker than water",
        "test31":"All that glitters is not Gold",
        "test32":"A drowning man will clutch at a straw",
        "test33":"Five boxing wizards jumped quickly"}


    total_words = 0
    correct_predicted_CS = 0
    correct_predicted_NCS = 0

    for i in range(first_test_image_index, last_test_image_index + 1):
        image_name = "test" + str(i)
        predicted_label = array_of_predicted_strings[i-first_test_image_index]
        predicted_label_lower = array_of_predicted_strings[i-first_test_image_index].lower()
        true_label_list = test_data[image_name].split()

        total_words += len(true_label_list)
        for i in range(len(true_label_list)):
            word = true_label_list[i]
            if word in predicted_label:
                correct_predicted_CS += 1
            if word.lower() in predicted_label_lower:
                correct_predicted_NCS += 1

    print("Accuracy (considering case-sensitivity) = ", correct_predicted_CS/total_words)
    print("Accuracy (not considering case-sensitivity) = ", correct_predicted_NCS/total_words)
    return

run_test_data()
