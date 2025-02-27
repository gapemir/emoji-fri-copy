from nltk.corpus import wordnet
from collections import Counter

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())  # Get synonym names
    return list(synonyms)


def get_phrase_synonyms(phrase, top_n=3):
    words = phrase.split()
    synonyms = Counter()

    for word in words:
        for syn in wordnet.synsets(word):  # Get synsets for each word
            for lemma in syn.lemmas():
                if lemma.name() not in words:  # Exclude input words
                    n = lemma.name()
                    n = n.replace('_', ' ')
                    synonyms[n] += 1  # Count occurrences
    
    # Get top N synonyms sorted by frequency
    return [word for word, count in synonyms.most_common(top_n)]



def add_synonims(data):
    splited = data.split('\"')
    out = []
    for piece in splited:
        if '['in piece or ']' in piece or ',' in piece:
            out.append(piece)
            continue
        #print("piece: ", piece)
        synonyms = [piece]
        synonyms += get_phrase_synonyms(piece)
        #print("synonyms: ", synonyms)
        out.append('\",\"'.join(synonyms))
        #print('\",\"'.join(synonyms))
    return '\"'.join(out)


def main():
    print("reading...")
    with open('data_extractor/keywords_new.js', 'r') as file:
        input_data = file.read()
    print("processing...")
    out = add_synonims(input_data)
    print("writing...")
    with open('data_extractor/keywords_new_synonyms.js', 'w') as file_out:
        file_out.write(out)
    print("done")

if __name__ == "__main__":
    main()
