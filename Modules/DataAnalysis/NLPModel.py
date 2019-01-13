import pandas as pd
from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import TaggedDocument
from gensim.utils import simple_preprocess
from gensim.models.doc2vec import Doc2Vec
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


def to_tagged_doc(doc, additional_stop_words=None):
    additional_stop_words = additional_stop_words if additional_stop_words else {}
    sno = SnowballStemmer('english')
    pd.options.mode.chained_assignment = None
    stop_words = set(stopwords.words('english')).union(additional_stop_words)
    processed = doc['messages'].map(lambda x: simple_preprocess(x))
    processed = processed.map(lambda x: map(sno.stem, x))
    processed = processed.map(lambda x: list(filter(lambda s: s not in stop_words, x)))

    return [TaggedDocument(words=w, tags=[c]) for w, c in zip(processed, doc['class'])]

def read_and_preprocess(path='./data/ProcessedData.csv', is_training=False, test_size=0.2,
                        additional_stop_words=None, random_state=None):
    additional_stop_words = additional_stop_words if additional_stop_words else {}
    df = pd.read_csv(path)
    df.drop(['date'], axis=1, inplace=True)
    if is_training:
        train, test = train_test_split(df, test_size=test_size, random_state=random_state)

        return to_tagged_doc(train, additional_stop_words), to_tagged_doc(test, additional_stop_words)
    else:
        stop_words = set(stopwords.words('english')).union(additional_stop_words)
        sno = SnowballStemmer('english')
        processed = [simple_preprocess(x) for x in df['messages']]
        processed = [[sno.stem(x) for x in doc] for doc in processed]

        return [list(filter(lambda x: x not in stop_words, doc)) for doc in processed]

def infered_vectors(model, messages, steps=100, alpha=0.025, min_alpha=0.01):
    return zip(*[(model.infer_vector(doc.words, steps=steps, alpha=alpha,
                                     min_alpha=min_alpha), doc.tags[0]) for doc in messages])

def build_model(path_to_data='./data/ProcessedData.csv',
                is_model_saved=True,
                path_to_model_dir='./model/nlp.model',
                test_size=0.2,
                split_data_random_state=None,
                additional_stop_words=None,
                **params):

    additional_stop_words = additional_stop_words if additional_stop_words else {}
    train_tagged, test_tagged = read_and_preprocess(path=path_to_data, test_size=test_size, is_training=True,
                                                    additional_stop_words=additional_stop_words,
                                                    random_state=split_data_random_state)

    model_PVDBOW = Doc2Vec(train_tagged, dm=0, vector_size=params['vector_size'], window=params['window'],
                           min_count=params['min_count'], epochs=params['epochs'], alpha=params['alpha'],
                           min_alpha=params['min_alpha'])

    Xx, yy = infered_vectors(model_PVDBOW, train_tagged)
    Xt, yt = infered_vectors(model_PVDBOW, test_tagged)

    if is_model_saved:
        model_PVDBOW.save(path_to_model_dir)

    return Xx, yy, Xt, yt, model_PVDBOW