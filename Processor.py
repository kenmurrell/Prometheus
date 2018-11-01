import DataManager
import NLP_Engine
import datetime
from collections import Counter


class Processor:

    def __init__(self):
        dataManager = DataManager()
        nlp = NLP_Engine()
        # dataManager.connect()

    def process_since_last(self):
        products = []  # dataManager.getProducts()
        for product in products:
            pass
            last_run = self.last_runtime()
            current_run = datetime.now
            reviews = []  # dataManager.getReviews(product, current_run, last_run)
            objectScores = {}
            for review in reviews:
                cleaned = self.nlp.clean_data(review)
                sentences = self.nlp.sentence_splitter(cleaned)
                sentence_scores = {}
                for sentence in sentences:
                    extracted_entities = self.nlp.get_objects(sentence)
                    score = self.nlp.fragment_score(sentence)
                    if score == "NEUTRAL":
                        continue
                    for entity in extracted_entities:
                        if entity not in sentence_scores.keys():
                            sentence_scores[entity] = {"SP": 0, "WP": 0, "WN": 0, "SN": 0}
                        sentence_scores[entity][score] += 1
                



            self.update_runtime(current_run)

    def last_runtime(self):
        pass
        return 5
        # get last runtime, from local file?

    def update_runtime(self, new_runtime):
        pass
        # store new_runtime to file
