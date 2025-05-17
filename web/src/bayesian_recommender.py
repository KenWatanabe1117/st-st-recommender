import numpy as np
import pandas as pd

class BayesianRecommender():
    def __init__(self):
        self.df = pd.read_csv('src/storage/data/keywords.csv', index_col=0)
        self.belief = np.ones(len(self.df)) / len(self.df)
        self.state = np.zeros(len(self.df))
        self.asked = []

        self.ANSWER_SCORES = [1.0, 0.5, 0, -0.5, -1.0]
        self.BETA = -1.0

        self.urls = pd.read_csv("src/storage/data/urls.csv")
    
    def get_best_belief(self):
        return np.max(self.belief)
    
    def get_urls(self, song_name):
        return self.urls[self.urls["SongName"]==song_name]
    
    def get_keywords(self, song_name):
        return self.df.columns[self.df.loc[song_name]==1].to_list()

    def softmax(self, x):
        e_x = np.exp(x)
        return e_x / e_x.sum()
    
    def update_belief(self, question, answer_score):
        alpha = self.df[question].fillna(0).to_numpy()
        self.state += (answer_score - alpha)**2
        self.belief = self.softmax(self.BETA * self.state)
        return np.argmax(self.belief), np.max(self.belief)

    def information_gain(self, question):
        expected_entropy = 0

        for a_val in self.ANSWER_SCORES:
            alpha = self.df[question].fillna(0).to_numpy()
            likelihood = np.exp(self.BETA*((a_val - alpha)**2+self.state))
            p_a = np.sum(likelihood)
            if p_a == 0:
                continue
            ent_after  = - p_a * np.log(p_a + 1e-12)
            expected_entropy += ent_after

        return expected_entropy
    
    def select_best_question(self):
        candidates = [q for q in self.df.columns if q not in self.asked]
        scores = {q: self.information_gain(q) for q in candidates}
        best_question = max(scores, key=scores.get)
        self.asked.append(best_question)
        return best_question
    
    def recommend_top_k(self, k):
        top_k_idx = np.argsort(-self.belief)[:k]
        return top_k_idx, self.df.index[top_k_idx].values, -np.sort(-self.belief)[:k]