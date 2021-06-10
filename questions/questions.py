import nltk
import sys
import os
import string
import numpy

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    loaded_files = dict()

    for file in os.listdir(directory):
        with open(os.path.join(directory,file),'r') as f:
            loaded_files[file] = f.read()

    return loaded_files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    tokenized = nltk.word_tokenize(document)
    stopwords = nltk.corpus.stopwords.words("english")

    words = []

    for word in tokenized:
        if word not in stopwords and word not in string.punctuation:
            words.append(word)

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()

    # create a set to have one word each time
    words = set()

    for i in documents.values():
        for word in i:
            words.add(word)

    for word in words:
        n = 0
        for i in documents.values():
            if word in i:
                n += 1

        idfs[word] =  numpy.log(len(documents)/n)

    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = dict()

    for name,content in files.items():
        scores[name] = 0
        for word in query:
            if word in content:
                scores[name]+=content.count(word)*idfs[word]

    sorted_scores = sorted(scores, key=scores.get)[::-1]

    # checking if it sorted well:
    assert scores[sorted_scores[0]] >= scores[sorted_scores[1]]

    return sorted_scores[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # initializing a dict that will map sentences with tuples(idf,queryTermDensity)
    sentence_score = dict()

    for sentence, words in sentences.items():
        common_words = query.intersection(words)

        # calculating idf
        sentence_idf = 0
        for word in common_words:
            sentence_idf += idfs[word]

        # calculating query term density
        num_words = 0
        for i in words:
            if i in common_words:
                num_words += 1

        query_term_density = num_words / len(words)

        sentence_score[sentence] = (sentence_idf,query_term_density)

    sorted_sentences = sorted(sentence_score,key=sentence_score.get)[::-1]

    return sorted_sentences[:n]

if __name__ == "__main__":
    main()

