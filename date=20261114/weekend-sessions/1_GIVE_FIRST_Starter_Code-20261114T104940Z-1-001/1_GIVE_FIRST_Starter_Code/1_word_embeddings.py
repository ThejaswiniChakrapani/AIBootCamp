# %% [markdown]
# # Exercise 1.1 — Word Embeddings: words as numbers
# **Created by Shivank Agarwal**
# 
# A computer cannot read the word *king*. It can only work with numbers.
# An **embedding** is a list of numbers that stands for a word. Words with a similar meaning get similar lists.
# 
# In this notebook you will:
# 1. Load a ready-made embedding model (GloVe, 50 numbers per word)
# 2. Look at the vector for a word
# 3. Do "word maths" like **king − man + woman ≈ queen**
# 4. Measure how close two words are with **cosine similarity** (the same maths every RAG system uses)
# 
# > The first run downloads the model (about 66 MB). After that it loads from your computer.

# %%
# Libraries:
#   numpy  -> maths on lists of numbers (vectors)
#   gensim -> gives us ready-made word vectors (GloVe)
import numpy as np
import gensim.downloader as api

# "glove-wiki-gigaword-50" = GloVe vectors trained on Wikipedia + news text.
# Every word in its vocabulary (400,000 words) becomes a list of 50 numbers.
model = api.load("glove-wiki-gigaword-50")
print("Words in vocabulary:", len(model.key_to_index))

# %% [markdown]
# ## Step 1 — What does a word look like to the computer?

# %%
# ----- TODO 1: Get the vector for the word "king" and print its shape and first 5 numbers -----
# Hint: The model works like a dictionary: model["some_word"]
# Hint: A numpy array has a .shape attribute
v_king = None  # replace None with your code
print("Shape of the 'king' vector:", v_king.shape)  # expect (50,)
print("First 5 numbers:", v_king[:5])

# %% [markdown]
# ## Step 2 — Which words live close to "king"?
# `most_similar` finds the words whose vectors point in the most similar direction.

# %%
for word, score in model.most_similar("king", topn=5):
    print(f"{word:<10} {score:.3f}")

# %% [markdown]
# ## Step 3 — Word maths (analogies)
# If *king* is to *man* as ? is to *woman*, then **king − man + woman** should land near **queen**.
# 
# ⚠️ Gotcha: if you build the vector yourself and search with it, the closest word is often one of the
# words you started with (for example *king* itself). `most_similar(positive=[...], negative=[...])`
# does the same maths **and** skips the input words. That is why we use it.

# %%
# ----- TODO 2: Use word maths to answer "king - man + woman = ?" -----
# Hint: model.most_similar(positive=[words to add], negative=[words to subtract], topn=1)
answer = None  # replace None with your code
print("king - man + woman =", answer)

# %%
# The same maths done "by hand" with numpy, to see the gotcha for yourself
new_vector = model["king"] - model["man"] + model["woman"]
print("Raw vector search (input words NOT removed):", model.similar_by_vector(new_vector, topn=3))

# %%
# ----- TODO 3: Capital cities: "paris - france + india = ?" -----
# Hint: Same pattern as TODO 2. Words to add: paris, india. Word to subtract: france
answer_2 = None  # replace None with your code
print("paris - france + india =", answer_2)

# %% [markdown]
# ## Step 4 — Cosine similarity by hand
# Cosine similarity tells us how much two vectors point the same way:
# 
# `cosine(a, b) = (a · b) / (|a| × |b|)`
# 
# * close to **1** → very similar meaning
# * close to **0** → unrelated
# 
# You will use this exact formula again in the next exercise to search documents.

# %%
# ----- TODO 4: Write a cosine_similarity(a, b) function using numpy -----
# Hint: np.dot(a, b) gives a · b
# Hint: np.linalg.norm(a) gives |a|
def cosine_similarity(a, b):
    return 0.0  # replace with the formula

pairs = [("king", "queen"), ("cricket", "football"), ("king", "banana")]
for w1, w2 in pairs:
    mine = cosine_similarity(model[w1], model[w2])
    library = model.similarity(w1, w2)  # gensim's own answer, to check yours
    print(f"{w1:>8} vs {w2:<9} -> my answer: {mine:.3f} | gensim: {library:.3f}")


