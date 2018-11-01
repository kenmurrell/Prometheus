import DataManager
import NLP_Engine
import datetime
from collections import Counter


class Processor:

    def __init__(self):
        nlp = NLP_Engine.NLP()
        # dataManager.connect()

    def process_since_last(self):
        products = []  # DataManager.getProducts()  # get all products (real implementation, make it 'per client' loop)
        for product in products:
            pass
            last_run = datetime.date.today() - datetime.timedelta(days=1)
            current_run = datetime.date.today()
            reviews = []  # DataManager.getReviews(product, current_run, last_run)
            object_scores = {}  # stores scores across all reviews for this product
            for review in reviews:
                cleaned = self.nlp.clean_data(review)
                sentences = self.nlp.sentence_splitter(cleaned)
                review_scores = {}  # stores scores for all objects in the current review
                for sentence in sentences:
                    extracted_entities = self.nlp.get_objects(sentence)
                    score = self.nlp.fragment_score(sentence)
                    if score == "NEUTRAL":
                        continue  # ignore neutral sentiments, irrelevant
                    for entity in extracted_entities:  # add/update score for this object
                        if entity not in review_scores.keys():
                            review_scores[entity] = {"SP": 0, "WP": 0, "WN": 0, "SN": 0}
                        review_scores[entity][score] += 1
                object_scores = Counter(object_scores) + Counter(review_scores)

            #  new scores for product calculated here. then write to database

            #  DataManager.store_scores(current_run,product,object_scores)
