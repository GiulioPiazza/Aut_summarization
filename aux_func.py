from nltk.corpus import stopwords
import nltk



def bag_of_word(text):

   # Transforms the sentence in input according to the bag of words approach, apply lemmatization, stop words and punctuation removal.

    list_tokens = []
    stop_words = set(stopwords.words('english'))
    punctuation = {',', ';', '(', ')', '{', '}', ':', '?', '!'}
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    
    for t in tokens:
        if t not in stop_words and t not in punctuation:
            list_tokens.append(t)

    return set(wnl.lemmatize(t) for t in list_tokens)


def create_context(text, nasari):

    #It creates a list of Nasari vectors (a list of {term:score}). Every vector is linked to one text term.
 
    tokens = bag_of_word(text)
    vectors = []
    for word in tokens:
        if word in nasari.keys():
            vectors.append(nasari[word])

    return vectors


def title_topic(document, nasari):

    #Creates a list of Nasari vectors based on the document's title.
 
    title = document[0]
    tokens = bag_of_word(title)

    vectors = []
    for word in tokens: #for word in topic 
        if word in nasari.keys(): 
            vectors.append(nasari[word])  #[{term : score,....}, {...}] lista di vettori nasari 
    return vectors
    

def rank(lemma, nasari_vector):

    #Computes the rank of the input vector.

    for i in range(len(nasari_vector)):
        if nasari_vector[i] == lemma:
            return i + 1


def weighted_overlap(topic_nasari_vector, paragraph_nasari_vector):
    
    #function that return the square-rooted Weighted Overlap if exist, 0 otherwise.


    overlap_keys = topic_nasari_vector.keys() & paragraph_nasari_vector.keys()
    overlaps = list(overlap_keys)  #lemmi comuni ad entrambi i vettori (vettore topic e vettore paragrafo)
    
    if len(overlaps) > 0:
        # sum 1/(rank() + rank())
        num = sum(1 / (rank(q, list(topic_nasari_vector)) + rank(q, list(paragraph_nasari_vector))) for q in overlaps)
        # sum 1/(2*i)
        den = 0
        for i in range(1,len(overlaps)+1):
            den += 1/ (2 * i)

        return num / den

    return 0






