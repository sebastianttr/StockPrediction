import wikipedia
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import torch
from keybert import KeyBERT



# More advanced approach: Use TF-IDF (Term Frequency-Inverse Document Frequency)
# vectorizer = TfidfVectorizer(stop_words='english')
# tfidf_matrix = vectorizer.fit_transform([tesla_text])
#
# # Get feature names (words) and their TF-IDF scores
# feature_names = vectorizer.get_feature_names_out()
# tfidf_scores = tfidf_matrix.toarray()[0]
#
# # Sort scores and select top keywords
# sorted_indices = tfidf_scores.argsort()[-20:][::-1]  # Adjust number of keywords as needed
# tesla_keywords = [feature_names[index] for index in sorted_indices]
#


def extract_keywords_nltk():
    nltk.download('punkt')  # For word tokenization
    nltk.download('stopwords')  # For stopword removal

    # get the content from the wikipedia page
    tesla_page = wikipedia.page("Tesla, Inc.")
    tesla_text = tesla_page.content

    # Convert to lowercase and remove punctuation
    tesla_text = tesla_text.lower()
    tesla_text = re.sub(r"[^\w\s]", "", tesla_text)

    # Tokenize the text into words
    words = word_tokenize(tesla_text)

    # Remove stopwords (common words that don't add much value)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]


    # Simple approach: Identify frequently occurring words
    keyword_counts = {}
    for word in filtered_words:
        keyword_counts[word] = keyword_counts.get(word, 0) + 1

    return [word for word, count in keyword_counts.items() if count > 5]  # Adjust threshold as needed

def extract_keywords_keybert():
    kw_model = KeyBERT()

    # doc = """
    #      Supervised learning is the machine learning task of learning a function that
    #      maps an input to an output based on example input-output pairs. It infers a
    #      function from labeled training data consisting of a set of training examples.
    #      In supervised learning, each example is a pair consisting of an input object
    #      (typically a vector) and a desired output value (also called the supervisory signal).
    #      A supervised learning algorithm analyzes the training data and produces an inferred function,
    #      which can be used for mapping new examples. An optimal scenario will allow for the
    #      algorithm to correctly determine the class labels for unseen instances. This requires
    #      the learning algorithm to generalize from the training data to unseen situations in a
    #      'reasonable' way (see inductive bias).
    #   """

    # get the content from the wikipedia page
    tesla_page = wikipedia.page("Tesla, Inc.")
    tesla_text = tesla_page.content

    pattern = re.compile(r'=+[^=\n]*=+')

    # Use the sub function to replace the matched pattern with an empty string
    tesla_text_sub = re.sub(pattern, '', tesla_text)

    # print(tesla_text_sub)

    seed_keywords = ["tesla"]

    doc_embeddings, word_embeddings = kw_model.extract_embeddings(tesla_text_sub, min_df=1, stop_words="english")

    keywords = kw_model.extract_keywords(tesla_text_sub, min_df=1, stop_words="english",
                                         doc_embeddings=doc_embeddings,
                                         word_embeddings=word_embeddings)

    print(doc_embeddings)
    return keywords


keywords_tesla_keybert = extract_keywords_keybert()

print("keywords: ", keywords_tesla_keybert)
