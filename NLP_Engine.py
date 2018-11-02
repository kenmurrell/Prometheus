from typing import List, Any

import nltk
import regex as re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import itertools


class NLP(object):

    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.stemmer = nltk.stem.porter.PorterStemmer()

    @staticmethod
    def clean_data(text):
        # split sentences with contrasting ideas
        coordinating_conjunctions = re.compile(r"""((?<![\.][\s])
                                                   (?<![\.])
                                                   (but|yet).)""", re.IGNORECASE | re.VERBOSE)
        text = re.sub(coordinating_conjunctions, ".", text)
        # capitalize reflexive pronouns (i) so the tagger doesnt count them as nouns
        reflexive_pronoun = re.compile(r"""[^\d\w]i[^\d\w]""")
        text = re.sub(reflexive_pronoun, "I", text)
        return text

    @staticmethod
    def isEmpty(sentence):
        garbage = re.compile(r"[\W|\d]", re.VERBOSE)
        rm = re.sub(garbage, "", sentence)
        return len(sentence) == 0

    @staticmethod
    def sentence_splitter(sentences):
        return nltk.sent_tokenize(sentences)

    def get_entities(self, sentence):
        tokens = nltk.word_tokenize(sentence.lower())
        tagged = nltk.pos_tag(tokens)
        # ? 0 or 1
        # * 0 or many
        # + 1 or many
        grammar = r"""
        A: {<DT><J.+>*<NN>*<VB.+><RB>?<DT><J.+>*<N.+>*} #the object should be the last noun
        B: {<DT><J.+>*<NN>*<VB.+><RB>?<J.+>(<CC><J.+>)?} #the object should be the first noun
        C: {(<J.+>*<N.+>+)+} # the object should be the only noun
        D: {(^<VB.*><DT><JJ>*<N.+>)+} # the object should be the first noun
        E: {<PRP><VB.+><RB>?<DT><JJ>*<N.+>+} # the object should be the last noun
        """
        # ADNOUN: { < J. + > + < N. + >}
        # NOUNAD: { < N. + > < J. + > +}
        # ADVB: { < J. + > + < VB.? > +}
        # ADVBP: { < RB.? > + < VB.? > +}
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(tagged)
        sentence_entities = self.confirm_type(tree)
        sentence_entities = [self.stemmer.stem(ent) for ent in sentence_entities if self.valid_entity(ent)]
        return sentence_entities

    @staticmethod
    def confirm_type(tree):
        entities = []
        example_filter = lambda a, b: a.label() == b
        flatten = lambda l: list(itertools.chain(*l))
        type_A: List[Any] = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "A")]
        type_B = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "B")]
        type_C = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "C")]
        type_D = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "D")]
        type_E = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == "E")]
        nouns = ["NN", "NNP", "NNPS", "NNS"]
        if len(type_A):
            entities.extend([val for val, tag in flatten(type_A) if tag in nouns])
        elif len(type_B):
            entities.extend([val for val, tag in flatten(type_B) if tag in nouns])
        elif len(type_C):
            entities.extend([val for val, tag in flatten(type_C) if tag in nouns])
        elif len(type_D):
            entities.extend([val for val, tag in flatten(type_D) if tag in nouns])
        elif len(type_E):
            entities.extend([val for val, tag in flatten(type_E) if tag in nouns])
        else:
            return []
        return entities

    def fragment_score(self, sentence):
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

    @staticmethod
    def valid_entity(entity):
        # remove entites with invalid characters and only 1 character
        garbage = re.compile(r"[\W|\d]")
        valid1 = not bool(re.findall(garbage, entity))
        valid2 = len(entity)>1
        return valid1 and valid2

    def _test(self, fragment):
        # words = " ".join([word for word, tag in fragment])
        # ss = self.sid.polarity_scores(words)
        ss = self.sid.polarity_scores(fragment)  # remove
        return ss["compound"]
