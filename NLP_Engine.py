import nltk
import regex as re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import itertools


class NLP(object):

    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    @staticmethod
    def clean_data(text):
        # split sentences with contrasting ideas
        coordinating_conjunctions = re.compile(r"""((?<![\.][\s])
                                                   (?<![\.])
                                                   (but|yet).)""", re.IGNORECASE | re.VERBOSE)
        text = re.sub(coordinating_conjunctions, ".", text)
        reflexive_pronoun = re.compile
        return text
        # sample = pattern.split(r'', sample)
        # remove emojis
        # remove special characters and symbols
        # break buts

    def sentence_splitter(self, sentences):
        return nltk.sent_tokenize(sentences)

    def get_objects(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        # ? 0 or 1
        # * 0 or many
        # + 1 or many
        grammar = r"""
        A: {<DT><JJ>*<NN>*<VBZ><RB>?<DT><JJ>*<NN>*} #the object should be the last noun
        B: {<DT><JJ>*<NN>*<VBZ><RB>?<JJ>(<CC><JJ>)?} #the object should be the first noun
        C: {(<JJ>*<NN>+)+} # the object should be the only noun
        D: {(^<VB.*><DT><JJ>*<NN>)+} # the object should be the first noun
        E: {<PRP><VBZ><RB>?<DT><JJ>*<NN>+} # the object should be the last noun
        ADNOUN: {<J.+>+<N.+>}
        NOUNAD: {<N.+><J.+>+}
        ADVB:   {<J.+>+<VB.?>+}
        ADVBP:  {<RB.?>+<VB.?>+}
        """
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(tagged)
        sentence_objects = self.confirm_type(tree)
        return sentence_objects

    def confirm_type(self, tree):
        objects = []
        example_filter = lambda a, b: a.label() == b
        type_A = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "A")]
        type_B = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "B")]
        type_C = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "C")]
        type_D = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "D")]
        type_E = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "E")]
        if len(type_A):
            objects.extend([val for val, tag in list(itertools.chain(*type_A)) if tag == "NN"])
        elif len(type_B):
            objects.extend([val for val, tag in list(itertools.chain(*type_B)) if tag == "NN"])
        elif len(type_C):
            objects.extend([val for val, tag in list(itertools.chain(*type_C)) if tag == "NN"])
        elif len(type_D):
            objects.extend([val for val, tag in list(itertools.chain(*type_D)) if tag == "NN"])
        elif len(type_E):
            objects.extend([val for val, tag in list(itertools.chain(*type_E)) if tag == "NN"])
        else:
            return 0
        return objects

    def fragment_score(self,sentence):
        # send a sentence, receive a score
        ss = self.sid.polarity_scores(sentence)
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

    def test(self, fragment):
        # words = " ".join([word for word, tag in fragment])

        # ss = self.sid.polarity_scores(words)

        ss = self.sid.polarity_scores(fragment) # remove
        return ss["compound"]


