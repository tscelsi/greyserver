import pandas as pd
from collections import Counter

def get_questions(hash=None, n=10):
    """
    We want to take an equal amount of questions from the tfidf, simple and intell baseline
    topic labels.
    """
    df = pd.read_pickle("./static/data/mturk_final_reduced.pickle")
    top_words_set = []
    intell_baseline = df[df['strategy'] == "intelligent baseline"].sample(n, random_state=hash)
    add_to_set(intell_baseline, top_words_set)
    simple = get_questions_for_subset(df, "simple", n, top_words_set)
    add_to_set(simple, top_words_set)
    # simple = df[df['strategy'] == "simple"].sample(n, random_state=hash)
    tfidf = get_questions_for_subset(df, "tfidf", n, top_words_set)
    return pd.concat([intell_baseline, simple, tfidf]).sample(frac=1, random_state=hash)

def get_questions_for_subset(df, subset, n, _list):
    # shuffle randomly
    data = df[df['strategy'] == subset].sample(frac=1)
    subset_df = []
    i = 0
    for ind, x in data.iterrows():
        if i >= n:
            break
        if x['top_words'] not in _list:
            subset_df.append(x)
            i += 1
    subset_df = pd.DataFrame(subset_df)
    return subset_df

def add_to_set(df, list):
    for x in df.itertuples():
        list.append(x.top_words)