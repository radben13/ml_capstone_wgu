
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def get_training_data():
    training_data = get_weather_training_data()
    training_data = training_data.dropna()
    y = training_data['IS_SEVERE']
    X = training_data.drop(columns=['IS_SEVERE'])
    return train_test_split(X, y, random_state=1)


def get_random_forest_classifier(**kwargs):
    train_X, _, train_y, _ = get_training_data()
    model = RandomForestClassifier(random_state=1, **kwargs)
    model.fit(train_X, train_y)
    return model