import pandas as pd
import numpy as np

class DecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.tree = self._build_tree(X, y, depth=0)

    def predict(self, X):
        return X.apply(self._predict_row, axis=1)

    def _build_tree(self, X, y, depth):
        if self.max_depth is not None and depth >= self.max_depth:
            return y.mode()[0]

        if len(y.unique()) == 1:
            return y.iloc[0]

        best_feature, best_threshold = self._find_best_split(X, y)
        if best_feature is None:
            return y.mode()[0]

        left_indices = X[best_feature] <= best_threshold
        right_indices = X[best_feature] > best_threshold

        left_tree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_tree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return {
            'feature': best_feature,
            'threshold': best_threshold,
            'left': left_tree,
            'right': right_tree
        }

    def _find_best_split(self, X, y):
        best_gini = float('inf')
        best_feature = None
        best_threshold = None

        for feature in X.columns:
            thresholds = X[feature].unique()
            for threshold in thresholds:
                left_y = y[X[feature] <= threshold]
                right_y = y[X[feature] > threshold]

                gini = self._gini_impurity(left_y, right_y)
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def _gini_impurity(self, left_y, right_y):
        total = len(left_y) + len(right_y)
        left_gini = self._gini(left_y)
        right_gini = self._gini(right_y)
        return (len(left_y) / total) * left_gini + (len(right_y) / total) * right_gini

    def _gini(self, y):
        if len(y) == 0:
            return 0
        p = y.value_counts(normalize=True)
        return 1 - np.sum(np.square(p))

    def _predict_row(self, row):
        node = self.tree
        while isinstance(node, dict):
            if row[node['feature']] <= node['threshold']:
                node = node['left']
            else:
                node = node['right']
        return node

# Example usage
if __name__ == "__main__":
    # Create a simple dataset
    data = {
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        'label': [0, 0, 1, 0, 0, 1, 1, 0, 1, 1]
    }
    df = pd.DataFrame(data)

    X = df[['feature1', 'feature2']]
    y = df['label']

    # Train the decision tree
    tree = DecisionTree(max_depth=1)
    tree.fit(X, y)

    # Make predictions
    predictions = tree.predict(X)
    print(predictions)
