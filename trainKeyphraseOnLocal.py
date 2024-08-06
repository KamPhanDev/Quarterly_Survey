# Import the necessary libraries
import spacy
import random
from spacy.training import Example

def load_model():
    """
    Load a blank English model from spaCy.
    This model will be used as the base for our Named Entity Recognition (NER) model.
    """
    return spacy.blank('en')

def add_ner_pipe(nlp):
    """
    Add a Named Entity Recognizer (NER) to the pipeline of the model.
    The NER is responsible for predicting named entities in text.
    """
    nlp.add_pipe('ner', last=True)

def get_ner(nlp):
    """
    Get the NER component from the pipeline.
    """
    return nlp.get_pipe('ner')

def add_labels(ner, train_data):
    """
    Add labels to the NER. These are the entities that the model will be able to predict.
    The labels are extracted from the training data.
    """
    for _, annotations in train_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

def train_model(nlp, train_data):
    """
    Train the model using the training data.
    The model is trained for 10 iterations. In each iteration, the training data is shuffled to ensure randomness.
    The model is updated with each example in the training data.
    """
    optimizer = nlp.begin_training()
    print("Training the model...")
    for itn in range(10):
        random.shuffle(train_data)
        losses = {}
        for text, annotations in train_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer, drop=0.35, losses=losses)
        print(losses)

def save_model(nlp, path):
    """
    Save the trained model to the specified path.
    """
    nlp.to_disk(path)

# Define the training data
TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
]

# Load the model
nlp = load_model()

# Add the NER to the pipeline
add_ner_pipe(nlp)

# Get the NER component
ner = get_ner(nlp)

# Add labels to the NER
add_labels(ner, TRAIN_DATA)

# Train the model
train_model(nlp, TRAIN_DATA)

# Save the model to disk
save_model(nlp, "./training/")
