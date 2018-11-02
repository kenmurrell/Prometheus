import DataManager
import NLP_Engine
import datetime
from collections import Counter
from tqdm import tqdm


class Processor:

    def __init__(self):
        self.nlp = NLP_Engine.NLP()

    def process_since_last(self, prev = 365):
        print("Getting product list...")
        current_run = datetime.datetime.today()
        last_run = current_run-datetime.timedelta(days=prev)
        reviews = DataManager.get_reviews("6977", last_run, current_run)
        # get all products (real implementation, make it 'per client' loop)
        # reviews format, collection of (productID, review_text, rating)
        print("\n" + str(len(reviews)) + " reviews found")
        print("Last run: " + str(DataManager.get_last_run()))
        print("Processing reviews: ")
        product_scores = {}  # stores scores across all reviews for this product
        # list of rating groups.
        # each group, contains dict of product_id -> dict of entities -> dict of scores
        for review in tqdm(reviews):
            product_id = int(review[0])
            review_text = review[1]
            if review_text is None:
                continue
            review_rating = int(review[2])
            cleaned = self.nlp.clean_data(review_text)
            sentences = self.nlp.sentence_splitter(cleaned)
            review_scores = {}  # stores scores for all objects in the current review
            for sentence in sentences:
                extracted_entities = self.nlp.get_entities(sentence)
                score = self.nlp.fragment_score(sentence)
                if score == "NEUTRAL":
                    continue  # ignore neutral sentiments, irrelevant
                for entity in extracted_entities:  # add scores from this sentence to compound review scores
                    if entity not in review_scores.keys():
                        review_scores[entity] = {"SP": 0, "WP": 0, "WN": 0, "SN": 0}
                    review_scores[entity][score] += 1

            if product_id not in product_scores.keys():
                product_scores[product_id] = [{}, {}, {}, {}, {}]
            for entity, values in review_scores.items():  # merge into product_scores.
                if entity in product_scores[product_id][review_rating-1].keys():
                    product_scores[product_id][review_rating-1][entity] = \
                        Counter(product_scores[product_id][review_rating-1][entity]) + Counter(values)
                else:
                    product_scores[product_id][review_rating-1][entity] = values

        #  new scores for all reviews calculated here. then write to database
        for product_id, entities_by_rating in tqdm(product_scores.items()):
            for rating in range(1, 5):
                for entity, scores in entities_by_rating[rating].items():
                    DataManager.save_scores(current_run, entity, product_id, rating, scores)
            DataManager.update_last_run()
        #  object_scores format, list of 5 elements, one element for each rating.
        #       each element is a map of word -> map of the scores
        #  DataManager.store_scores(product, current_run, object_scores)

