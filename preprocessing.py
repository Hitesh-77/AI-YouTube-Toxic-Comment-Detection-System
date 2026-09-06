import re 
import string
import contractions
import nltk
import emoji

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")

stop_words = set(stopwords.words("english"))
correct_negations = {
    "not",
    "cannot",
    "no",
    "nor",
    "never",
    "none",
    "nothing",
    "nobody",
    "nowhere",
    "neither"
}
custom_stopwords = stop_words - correct_negations

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1]

    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def clean_text(txt):
    txt = txt.lower()
    txt = re.sub(r"https?://\S+|www\.\S+", "", txt)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = emoji.replace_emoji(txt, replace = "")
    txt = contractions.fix(txt)
    txt = txt.translate(str.maketrans("","", string.punctuation))
    tokens = word_tokenize(txt)
    tokens = [word for word in tokens if word not in custom_stopwords]
    tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens]
    tokens = [word for word in tokens if word.strip()]
    return " ".join(tokens)
    