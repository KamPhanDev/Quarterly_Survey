import spacy
import random

# Training data
TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
]

# Load a spacy model
nlp = spacy.blank('en')

# Add NER to the pipeline
ner = nlp.create_pipe('ner')
nlp.add_pipe(ner, last=True)

# Add labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

# Train the model
optimizer = nlp.begin_training()

for itn in range(10):
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        nlp.update([text], [annotations], sgd=optimizer, drop=0.35, losses=losses)
    print(losses)
