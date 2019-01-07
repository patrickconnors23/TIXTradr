import pickle
from sklearn.linear_model import LassoCV

class linReg():
    def __init__(self, path="linearCV.pkl"):
        self.model = LassoCV(cv=5)
        self.pathName = path
    
    def train(self, X, y):
        self.model = self.model.fit(X, y)
    
    def evaluate(self, X, y):
        print(self.model.score(X, y))
        pass
    
    def predict(self, X):
        return self.model.predict(X)
    
    def saveModel(self):
        pickle.dump(self.model, open(f"lib/{self.pathName}", "wb"))