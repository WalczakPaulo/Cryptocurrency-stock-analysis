import pandas as pd
from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import TaggedDocument
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models.doc2vec import Doc2Vec

def to_tagged_doc(doc):
    pd.options.mode.chained_assignment = None
    doc['messages'] = doc['messages'].map(remove_stopwords)
    return doc.apply(lambda x: TaggedDocument(words=simple_preprocess(x['messages']), tags=[x['class']]), axis=1)

def read_and_preprocess(path='./data/ProcessedData.csv', is_training=False, test_size=0.2, random_state=None):
    df = pd.read_csv(path)
    df.drop(['date'], axis=1, inplace=True)
    to_tagged_doc(df)
    if is_training:
        train, test = train_test_split(df, test_size=test_size, random_state=random_state)
        return to_tagged_doc(train), to_tagged_doc(test)
    else:
        return [simple_preprocess(x) for x in df['messages']]

def infered_vectors(model, messages, steps=100, alpha=0.025, min_alpha=0.01):
    return zip(*[(model.infer_vector(doc.words, steps=steps, alpha=alpha,
                                     min_alpha=min_alpha), doc.tags[0]) for doc in messages])

def build_model(path_to_data='./data/ProcessedData.csv',
                is_model_saved=True,
                path_to_model_dir='./model/nlp.model',
                test_size=0.2,
                split_data_random_state=None,
                seed=None,
                **params):

    train_tagged, test_tagged = read_and_preprocess(path=path_to_data, test_size=test_size, is_training=True,
                                                    random_state=split_data_random_state)

    train_messages = train_tagged.values
    model_PVDBOW = Doc2Vec(train_messages, dm=0, vector_size=300, window=10, min_count=1, epochs=100, workers=1,
                       alpha=0.025, min_alpha=0.01, seed=seed)
    Xx, yy = infered_vectors(model_PVDBOW, train_messages)
    test_messages = test_tagged.values
    Xt, yt = infered_vectors(model_PVDBOW, test_messages)

    if is_model_saved:
        model_PVDBOW.save(path_to_model_dir)

    return Xx, yy, Xt, yt, model_PVDBOW