import nltk
import regex as re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class NLP(object):

    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def clean_data(self, text):
        # remove emojis
        # remove special characters and symbols
        # break buts
        pass

    def get_objects(self,text):
        sentences = nltk.sent_tokenize(text)
        review_objects = []
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokens)
            print(tagged)
            # ? 0 or 1
            # * 0 or many
            # + 1 or many
            grammar = r"""
            ADNOUN: {<J.+>+<N.+>}
            NOUNAD: {<N.+><J.+>+}
            ADVB:   {<J.+>+<VB.?>+}
            ADVBP:  {<RB.?>+<VB.?>+}
            """
            cp = nltk.RegexpParser(grammar)
            tree = cp.parse(tagged)
            tag_list = ["ADNOUN", "NOUNAD", "ADVB", "ADVBP"]
            leaves = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() in tag_list)]

            subject_tags = ["NN", "NNS", "NNP","NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
            sentence_objects = [word[0] for leaf in leaves for word in leaf if word[1] in subject_tags]
            review_objects.append((sentence, sentence_objects))

        return review_objects

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
text = "These are OK. Cut great. The rubber-like grips inside the plastic handles help with precise cutting but make the handles tighter than typical scissors handles. I have small hands and even I find them a bit tight. I would do better with a size larger scissors than I'd normally use. Also, the rubber-like material was flawed inside on of the scissors, but it works fine. Just cosmetic."
objects = nlp.get_objects(text)
print(objects)