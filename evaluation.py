from rake_nltk import Rake

""" EVALUATION MEASURES"""

def get_keywords(text):
 
    #function that returns the keyword ranked highest to  lowest of the given text 
    #Rapid Automatic Keyword Extraction algorithm, is a domain independent keyword extraction algorithm which tries to determine key phrases 
    #in a body of text by analyzing the frequency of word appearance and its co-occurance with other words in the text.
    
    rake = Rake()  # Uses stopwords for english from NLTK, and all puntuation characters.
    rake.extract_keywords_from_text(text)

    return rake.get_ranked_phrases()  

def precision(summ_list, gold_list):
  
    #function that compute the BLUE score.

    retrieved_lines = summ_list
    relevant_lines = gold_list
 
    #print(retrieved_lines,'\n',relevant_lines)

    count=0

    for line in relevant_lines:
        if line in retrieved_lines:
            count+=1

    return count/len(retrieved_lines)


def recall(summ_list, gold_list):
  
    # function that compute the ROGUE score.


    retrieved_lines = summ_list
    relevant_lines = gold_list

    # print(retrieved_lines, '\n', relevant_lines)

    count = 0

    for line in retrieved_lines:
        if line in relevant_lines:
            count += 1

    return count / len(relevant_lines)