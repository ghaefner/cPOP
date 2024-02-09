from cPOP.constants import DICT_LANGUAGES, Columns, PATH_TO_TAG_MODEL
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import re, os, joblib

# Preprocess tags and language names
def preprocess(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def train_tag_classifier(df, language_tags=DICT_LANGUAGES, model_path=PATH_TO_TAG_MODEL):
    # List of major programming languages
    major_languages = [lang for lang in language_tags.keys() if lang != 'r'] # remove r because it messes up the classifier

    # Filter DataFrame to include only tags associated with major programming languages
    df_major_languages = df[df[Columns.TAG].apply(lambda x: any(x.startswith(lang) for lang in major_languages))]

    # Preprocess tags
    preprocessed_tags = [preprocess(tag) for tag in df_major_languages[Columns.TAG]]

    # Create feature vectors using bag-of-words representation
    vectorizer = CountVectorizer(analyzer='word', lowercase=False)
    X = vectorizer.fit_transform(preprocessed_tags)

    # Train a random forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, df_major_languages[Columns.TAG])

    # Save the trained model
    joblib.dump((clf, vectorizer), model_path)



# Function to classify tags using the trained model
def classify_tag(tag, clf, vectorizer):
    # Preprocess tag
    tag = preprocess(tag)
    # Vectorize tag
    tag_vec = vectorizer.transform([tag])
    # Predict tag group
    prediction = clf.predict(tag_vec)[0]
    return prediction


def assign_tag_groups(df, language_tags=DICT_LANGUAGES, model_path=PATH_TO_TAG_MODEL):
    # Check if the model file exists
    if os.path.exists(model_path):
        # Load the trained model and vectorizer
        clf, vectorizer = joblib.load(model_path)
    else:
        # Train the model
        train_tag_classifier(df, language_tags, model_path)
        # Load the trained model and vectorizer
        clf, vectorizer = joblib.load(model_path)
    df[Columns.TAG_GROUP] = df[Columns.TAG].apply(lambda x: classify_tag(x, clf, vectorizer))

    return df

def make_tag_groups(df, language_dict=DICT_LANGUAGES):
    # Initialize an empty list to store the tag groups
    tag_groups = []

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        tag = row[Columns.TAG]
        # Initialize the tag group as 'other'
        group = 'other'
        # Iterate over the programminglanguages and their corresponding regular expressions
        for language, regex_list in language_dict.items():
            # Check if any of the regular expressions match the tag
            for regex in regex_list:
                if re.match(regex, tag, re.IGNORECASE):
                    group = language
                    break # If a match is found, break the inner loop
            if group != 'other':
                break # If a match is found, break the outer loop

        tag_groups.append(group)  # Append the tag group to the list outside the outer loop

    df[Columns.TAG_GROUP] = tag_groups

    return df