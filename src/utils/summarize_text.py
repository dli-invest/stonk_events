import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def ensure_punkt_installed():
    # ensures nltk is installed
    nltk.download('punkt')

def summarize_text(text: str, language= "english", sentences_count=12) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    summary = ""
    for sentence in summarizer(parser.document, sentences_count):
        summary += str(sentence)
    return summary
