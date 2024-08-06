import spacy
import random
from spacy.training import Example  # Import the Example class

# Training data
TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
]

# Load a spacy model
nlp = spacy.blank('en')

# Add NER to the pipeline
nlp.add_pipe('ner', last=True)

# Get the NER component
ner = nlp.get_pipe('ner')

# Add labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

# Train the model
optimizer = nlp.begin_training()

for itn in range(len(TRAIN_DATA)+1):
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        # Create a Doc object from the text
        doc = nlp.make_doc(text)
        # Create an Example object from the Doc and the annotations
        example = Example.from_dict(doc, annotations)
        # Update the model with the Example
        nlp.update([example], sgd=optimizer, drop=0.35, losses=losses)
    print(losses)
