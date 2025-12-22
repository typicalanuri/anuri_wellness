from openai import OpenAI
import pandas as pd
import json
client = OpenAI()

def get_embeddings(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model = model).data[0].embedding

def save_embeddings_to_csv(text):
    data = {
        text: get_embeddings(text, model='text-embedding-3-small'),
        'Bend It Like Beckham': get_embeddings("Bend It Like Beckham", model='text-embedding-3-small'),
        'Pele: Birth of a Legend': get_embeddings("Pele: Birth of a Legend", model='text-embedding-3-small')
    }
    print("Embedding data: ", data)
    df = pd.DataFrame(data)
    df.to_csv('output/3_movies.csv', index=False)
    return df

def cosine_similarity(v1, v2):
    dot_product = sum([a * b for a, b in zip(v1, v2)])
    magnitude = (sum([a**2 for a in v1]) * sum([a**2 for a in v2])) ** 0.5
    return dot_product / magnitude

def exhaustive_search(query_vector, vectors):
    similarities = []
    for title, vector in vectors.items():
        similarity = cosine_similarity(query_vector, vector)
        similarities.append((title, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities

if __name__ == "__main__":
    df = save_embeddings_to_csv("She's the man")
    print("Similarities: ", exhaustive_search(df.loc[0], df))