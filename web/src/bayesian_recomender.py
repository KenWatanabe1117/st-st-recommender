import pandas as pd
import numpy as np

class BayesianRecomender():
    def __init__(self):
        self.df = pd.read_csv('storage/data/keywords.csv', index_col=0)
        self.belief = np.ones(len(self.df)) / len(self.df)
        self.state = np.zeros(len(self.df))
        self.asked = []

        self.ANSWER_SCORES = [1.0, 0.5, 0, -0.5, -1.0]
        self.BETA = -1.0

        self.urls = None
    
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
    
    def update_belief(self, question, answer_score):
        alpha = self.df[question].fillna(0)
        self.state += (answer_score - alpha)**2
        self.belief = self.softmax(self.BETA * self.state)
        return self.df.index[np.argmax(self.belief)], np.max(self.belief)

    def information_gain(self, question):
        ent_before = -np.sum(self.belief * np.log(self.belief + 1e-12))
        expected_entropy = 0

        for a_val in self.ANSWER_SCORES:
            alpha = self.df[question].fillna(0)
            likelihood = np.exp(self.BETA*(a_val - alpha)**2+self.BETA*self.state)
            p_a = np.sum(likelihood)
            if p_a == 0:
                continue
            ent_after  = - p_a * np.log(p_a + 1e-12)
            expected_entropy += ent_after

        return ent_before - expected_entropy
    
    def select_best_question(self):
        candidates = [q for q in self.df.columns if q not in self.asked]
        scores = {q: self.information_gain(self, q) for q in candidates}
        best_question = max(scores, key=scores.get)
        self.asked.append(best_question)
        return best_question
    
    def recomend_top_k(self, k):
        top_k_idx = np.argsort(self.belief)[k-1::-1]
        return self.df.index[top_k_idx], self.urls.iloc[top_k_idx], np.sort(self.belief)[k-1::-1]