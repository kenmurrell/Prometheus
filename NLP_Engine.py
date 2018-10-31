import nltk
import regex as re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class NLP(object):

    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def clean_data(self, text):
        #remove emojis
        #remove special characters and symbols
        #break buts
        pass

    def get_objects(self,text):
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        # ? 0 or 1
        # * 0 or many
        # + 1 or many
        grammar = r"""
        NP: {<J.+>*<N.+>+}
        ADJ: {<RB>?<J.+>+}
        """
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(tagged)
        tag_list=["NP","ADJ"]
        leaves = [subtree.leaves()[0] for subtree in tree.subtrees(filter = lambda t: t.label() in tag_list)]
        objects = [object for object,tag in leaves]
        print(objects)

    def fragment_score(self,fragment):
        words = " ".join([word[0] for word in fragment])

        ss = self.sid.polarity_scores(words)
        if ss["compound"] > 0.6:
            return "SP"
        elif ss["compound"] > 0.1:
            return "WP"
        elif ss["compound"] > -0.1:
            return "NEUTRAL"
        elif ss["compound"] > -0.6:
            return "WN"
        else:
            return "SN"


nlp = NLP()
text = "The design of the keys and the backlights is broken"
objects = nlp.get_objects(text)
print(objects)
