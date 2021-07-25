import pandas as pd


def get_questions(hash=None, n=10):
    """
    We want to take an equal amount of questions from the tfidf, simple and intell baseline
    topic labels.
    """
    df = pd.read_pickle("./static/data/mturk_final_reduced.pickle")
    intell_baseline = df[df['strategy'] == "intelligent baseline"].sample(n, random_state=hash)
    simple = df[df['strategy'] == "simple"].sample(n, random_state=hash)
    tfidf = df[df['strategy'] == "tfidf"].sample(n, random_state=hash)
    return pd.concat([intell_baseline, simple, tfidf]).sample(frac=1, random_state=hash)