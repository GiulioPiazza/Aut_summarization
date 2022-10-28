import sys
import os
from pathlib import Path
from aux_func import *
import pandas as pd
import math
import evaluation as eva


path = os.path.dirname(__file__) + '/'


def evaluation_step(sum):

    #Evaluation phase  
    #BLEU precision score and ROGUE score  
 

    text = '\n'.join(document)
    gold_list = eva.get_keywords(text)
    text_sum = '\n'.join(sum)
    summ_list = eva.get_keywords(text_sum)
    blue = eva.precision(summ_list,gold_list)
    rogue = eva.recall(summ_list,gold_list)
      
        
    print("\nBLEU score of [{0}] = {1:.2f}".format(file.name,blue*100))
    print("ROUGE score of [{0}] = {1:.2f}\n".format(file.name,rogue*100))


    return blue, rogue


    
def parse_dd_small_nasari():

    #Parse the "dd-small-nasari-15.txt" file, and it converts into a Python dictionary.

    nasari = {}
    with open(path + "input/dd-small-nasari-15.txt", 'r', encoding="utf8") as file:
        for line in file.readlines():
            splits = line.split(";")
            vector_dict = {}
            for term in splits[2:]:
                t_score = term.split("_")
                if len(t_score) > 1: vector_dict[t_score[0]] = t_score[1]     # vector[term] = score

            nasari[splits[1].lower()] = vector_dict #split 1 = wikipage title
    #{word: {term:score}}
    return nasari

def parse_document(file):
    
    #parse the document and return a list of all paragraphs.
    
    document = []
    data = file.read_text(encoding='utf-8')
    lines = data.split('\n')

    for line in lines:
        #if the # is not present, we have a normal paragraph to append to the list.
        if line != '' and '#' not in line:  #if the "#" character is present, the line contains the original link of the doc.
            line = line[:-1]  # deletes the final "\n" character.
            document.append(line)

    return document

def summarization_step(document, nasari, percentage):

    #Applies summarization to the document with the input percentage (10/20/30)

    # getting the topics based on the document's title.
    topics = title_topic(document, nasari)
    paragraphs = []
    i = 0
    # for each paragraph, except the title (document[0])
    for paragraph in document[1:]:
        context = create_context(paragraph, nasari)
        paragraph_wo = 0  # Weighted Overlap average inside the paragraph.
        # Computing WO 
        for word_vector in context:   
            topic_wo = 0
            for topic_vector in topics:
                topic_wo += weighted_overlap(topic_vector, word_vector)
            if topic_wo != 0:
                topic_wo = topic_wo / len(topics)

            # Sum all words WO in the paragraph's WO
            paragraph_wo += topic_wo
           
        if len(context) > 0:
            paragraph_wo = paragraph_wo / len(context)
            # append in paragraphs a tuple with the index of the paragraph (to
            # preserve order), the WO of the paragraph and the paragraph's text.
            paragraphs.append((i, paragraph_wo, paragraph))
        i += 1

    to_keep = len(paragraphs) - int(round((percentage / 100) * len(paragraphs), 0))
    # Sort by highest score (WO) and keeps all the important entries. From first to "to_keep"
    keep_best_paragraph = sorted(paragraphs, key=lambda x: x[1], reverse=True)[:to_keep]
    # Restore the original order.
    sort_paragraphs = sorted(keep_best_paragraph, key=lambda x: x[0], reverse=False)
    
    final_summary = []
    for tuple in sort_paragraphs:
        final_summary.append(tuple[2])
    
    final_summary = [document[0]] + final_summary
    return final_summary


if __name__ == "__main__":

    path_to_input = Path(path + "/documents_to_summarize")
    documents = list(path_to_input.glob('./*.txt'))

    PERCENTAGE = 30
    total_blue_score = 0
    total_rouge_score = 0
    print("------------")
    print(f"Start Summarization task.  Percentage: {PERCENTAGE}")
    nasari = parse_dd_small_nasari()
    n_documents = 0 # n of documents
   
    for file in documents:
        n_documents += 1
        document = parse_document(file)
        # For each document do summarization.
        summary = summarization_step(document, nasari, PERCENTAGE)

        with open(path + "output/" + str(PERCENTAGE) + "_"+ file.name  ,'w', encoding='utf-8') as out:
            for paragraph in summary:
                out.write(paragraph + '\n')

        #start the evaluation for each document
        blue, rogue = evaluation_step(summary)
        total_blue_score += blue
        total_rouge_score += rogue
    print("Average BLUE score : {0:.2f}\nAverage ROUGE score : {1:.2f}".format(total_blue_score/n_documents,total_rouge_score/n_documents*100))

    print("------------")


       

  