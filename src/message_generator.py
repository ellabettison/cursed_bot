from imageai.Detection import ObjectDetection
import pandas as pd
import os
from random import randint
from random import choice
import spacy

from MarkovChainGenerator.markov_chain_creator import generate_words, generate_sentence, read_from_file, write_to_file, \
    generate_hate_speech, generate_sexism


def check_grammar(sentence):
    nlp = spacy.load("en_core_web_sm")
    parsed = nlp(sentence)
    print(parsed)


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


# gen = MarkovTextGenerator()
# gen.startword = detections[0]["name"]
# gen.stopword = detections[1]["name"]
#
# print(gen.gen_text(20))

start_words = ["help", "retard", "fuck", "drink", "drugs", "coke", "weed", "titties", "sex", "drug", "blood",
               "leader", "fear", "dick", "pussy", "the", "but", "butt", "ok", "french", "english"]

# pivot = generate_sexism(0)
# word = pivot[pivot.columns[0]].tolist()
pivot = generate_hate_speech(randint(0, 3))
# write_to_file(pivot.astype(pd.SparseDtype("float", pd.np.nan)), str(i))
# pivot = read_from_file('reddit_sarcastic0.csv')
print(pivot)
print("read pivot")
print("GENERATING SENTENCE")
# for i in range(len(start_words)):
#     try:
#         print(generate_sentence(pivot, start_words[i], 20))
#     except:
#         print("could not generate sentence starting with word '" + start_words[i] + "'")
#         continue
word = list(pivot.index)
print(word)
for i in range(20):
    curr_word = choice(word)
    # print(curr_word)

# sentence = generate_sentence(pivot, "fart", 50)
    sent = generate_sentence(pivot, curr_word, 10)
    print(sent)
    # check_grammar(sent)
# print(sentence)
