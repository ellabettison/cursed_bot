from imageai.Detection import ObjectDetection
import pandas as pd
import os
from random import randint
from random import choice
from enum import Enum

from MarkovChainGenerator import markov_chain_creator
from MarkovChainGenerator.ginger import ginger_check_grammar
from MarkovChainGenerator.markov_chain_creator import generate_pol


class CommentType(Enum):
    SARCASTIC = 1
    HATE = 2
    SEXIST = 3


def check_grammar(sentence):
    ginger_check_grammar(sentence)


def analyse_image():
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "S-CI37.jpg"),
                                                 output_image_path=os.path.join(execution_path, "S-CI37-2.jpg"))

    for object in detections:
        print(object["name"], " : ", object["percentage_probability"])


def randomly_generate(type):
    pivot = markov_chain_creator.get_pivot(type)
    word = list(pivot.index)
    for i in range(20):
        curr_word = choice(word)
        # print(curr_word)

        # sentence = generate_sentence(pivot, "fart", 50)
        from MarkovChainGenerator.markov_chain_creator import generate_sentence
        sent = generate_sentence(pivot, curr_word, 10)
        # check_grammar(sent)
        print(sent)



start_words = ["help", "retard", "fuck", "drink", "drugs", "coke", "weed", "titties", "sex", "drug", "blood",
               "leader", "fear", "dick", "pussy", "the", "but", "butt", "ok", "french", "english"]

generate_pol(0)
