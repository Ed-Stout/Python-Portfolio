import re
import pandas as pd
import spacy
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from nltk.stem import SnowballStemmer
#from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

#Question a
csv_path = Path.cwd() / "p2-texts" / "hansard40000.csv"

df = pd.read_csv(csv_path)

df['party'] = df['party'].replace('Labour (Co-op)', 'Labour') #1
df = df[df['party'] != 'Speaker'] #2c

party_counts = df['party'].value_counts() #2a
#print(party_counts)

sorted_counts = party_counts.sort_values(ascending=False) #2b
#print(sorted_counts)

top_parties = list(sorted_counts.index[:4]) #2c
print(f"\nTop 4 parties: {top_parties}")

df = df[df['party'].isin(top_parties)] #2d
df = df[df['speech_class'] == 'Speech'] #3
df = df[df['speech'].str.len() >= 1000] #4

#new_party_counts = df['party'].value_counts().sort_values(ascending=False) 
#print(new_party_counts)
print(df.shape)

#Question b
vectorizer = TfidfVectorizer(stop_words='english', max_features=3000) #omits stop words
X = vectorizer.fit_transform(df['speech']) #dependent variable
y = df['party'] #predictor variable

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=26
)

# Print out the resulting shapes and class distributions
print("X_train and X_test shapes: ", X_train.shape, X_test.shape)

print("Class distribution in training set: ", y_train.value_counts()) #samples/features in training set
print("Class distribution in test set: ", y_test.value_counts()) #samples/features in test set

#question c

rf_clf  = RandomForestClassifier(n_estimators=300, random_state=26) #300 trees
svm_clf = SVC(kernel='linear', random_state=26)

rf_clf.fit(X_train, y_train)
svm_clf.fit(X_train, y_train)

y_pred_rf  = rf_clf.predict(X_test)
y_pred_svm = svm_clf.predict(X_test)

print("Random Forest F1 Score: ", f1_score(y_test, y_pred_rf,  average='macro'))
print("Classification Report: ", classification_report(y_test, y_pred_rf, zero_division=0))

print("SVM (linear kernel) F1 Score: ", f1_score(y_test, y_pred_svm,  average='macro'))
print("Classification Report: ", classification_report(y_test, y_pred_svm, zero_division=0))

#question d

vectorizer = TfidfVectorizer(stop_words='english', max_features=3000, ngram_range=(1, 3)) #bigrams and trigrams
X = vectorizer.fit_transform(df['speech'])
y = df['party']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y, 
    random_state=26
)

# Print out the resulting shapes and class distributions
print("X_train and X_test shapes: ", X_train.shape, X_test.shape)

print("Class distribution in training set: ", y_train.value_counts())
print("Class distribution in test set: ", y_test.value_counts())

rf_clf  = RandomForestClassifier(n_estimators=300, random_state=26)
svm_clf = SVC(kernel='linear', random_state=26)

rf_clf.fit(X_train, y_train)
svm_clf.fit(X_train, y_train)

y_pred_rf  = rf_clf.predict(X_test)
y_pred_svm = svm_clf.predict(X_test)

print("Random Forest F1 Score: ", f1_score(y_test, y_pred_rf,  average='macro'))
print("Classification Report: ", classification_report(y_test, y_pred_rf, zero_division=0))

print("SVM (linear kernel) F1 Score: ", f1_score(y_test, y_pred_svm,  average='macro'))
print("Classification Report: ", classification_report(y_test, y_pred_svm, zero_division=0))

#question e
issue_terms = {
    'benefits', 'immigration', 'asylum', 'nhs', 'health', 'doctors', 'economy',
    'russia', 'brexit', 'covid', 'lockdown', 'furlough', 'testing', 'ppe',
    'ventilators', 'vaccines', 'masks', 'restrictions', 'education',
    'universities', 'unemployment', 'recession', 'hospitality', 'retail',
    'aviation', 'environment', 'transport', 'railways', 'cycling', 'renewables',
    'housing', 'evictions', 'homelessness', 'inequality', 'statues',
    'colonialism', 'policing', 'protests', 'crime', 'violence', 'poverty',
    'mental', 'care', 'elderly', 'racism', 'security', 'climate', 'energy',
    'trade', 'fishing', 'agriculture', 'huawei', 'digital', 'misinformation',
    'cybersecurity', 'china', 'defense', 'aid', 'relations', 'schools',
    'exams', 'fees', 'HS2', 'COP26', 'Trump'
} #adding political issue terms form 2020

stop_words = ENGLISH_STOP_WORDS.union(issue_terms) 

import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser','ner']) #POS filtering, spaCy tokenizer

def politics_tokenizer(text):
    cleaned = re.sub(r'[^\w\s]', '', text.lower()) #lowercase and remove punctuation
    doc = nlp(cleaned)

    lemmas = []
    for token in doc:
        pos = token.pos_
        lemma = token.lemma_
        if pos in {'NOUN', 'VERB', 'ADJ', 'ADV'} and lemma not in stop_words: #only keep nouns, verbs, adjectives, and political words
            lemmas.append(lemma)

    return lemmas

vectorizer = TfidfVectorizer(
    tokenizer=politics_tokenizer,
    token_pattern=None,   
    ngram_range=(1, 3),    #trigrams and bigrams
    max_features=3000
)

X = vectorizer.fit_transform(df['speech'])
y = df['party']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=26
)

classifiers = {
    "Random Forest (100 trees)" : RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=26),
    "Linear SVM"                : SVC(kernel='linear', class_weight='balanced', random_state=26),
    "Naive Bayes"            : MultinomialNB()
} #Added Naive Bayes classifier because the spec said 3 classifiers should be used

for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"{name:} macro-F1 = {f1_score(y_test, y_pred, average='macro')}")

print("Classification Report: ", classification_report(y_test, y_pred_svm, zero_division=0)) #print svm, the best performing classifier