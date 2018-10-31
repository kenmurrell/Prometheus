import nltk
import regex as re

class NLP(object):

    def __init__(self):
        pass

    def clean_data(self, text):
        pass

    def get_objects(self,text):
        tagged = nltk.pos_tag(text)
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
        leaves = [subtree for subtree in tree.subtrees(filter = lambda t: t.label() in tag_list)]
        print(leaves)



nlp = NLP()
text = "The design of the keys and the backlights is broken"
objects = nlp.get_objects(text)
print(objects)
