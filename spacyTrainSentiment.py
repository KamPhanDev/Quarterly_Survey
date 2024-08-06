import spacy
import random
from spacy.training import Example

def load_model():
    """
    Load a blank English model from spaCy.
    """
    return spacy.blank('en')

def add_textcat_pipe(nlp):
    """
    Add a TextCategorizer to the pipeline of the model.
    """
    return nlp.add_pipe("textcat", last=True)

def add_labels(textcat):
    """
    Add labels to the text categorizer. These are the categories that the model will be able to predict.
    """
    textcat.add_label("POSITIVE")
    textcat.add_label("NEGATIVE")
    textcat.add_label("NEUTRAL")

def train_model(nlp, textcat, train_data):
    """
    Train the model using the training data.
    """
    # Get the names of the other pipes in the pipeline, so they can be disabled during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    # Only train the text categorizer (disable the other pipes)
    with nlp.disable_pipes(*other_pipes):
        # Begin training
        optimizer = nlp.begin_training()
        print("Training the model...")
        # Perform 10 iterations of training
        for i in range(10):
            # Shuffle the training data
            random.shuffle(train_data)
            # Initialize a dictionary to hold the training losses
            losses = {}
            # Update the model with each example
            for text, annotations in train_data:
                # Create a Doc object from the text
                doc = nlp.make_doc(text)
                # Create an Example object from the Doc and the annotations
                example = Example.from_dict(doc, annotations)
                # Update the model with the Example
                # The 'sgd' argument is the optimizer
                # The 'drop' argument is the dropout rate
                nlp.update([example], sgd=optimizer, drop=0.2, losses=losses)
            # Print the training losses for each iteration
            print(losses)

# Define the training data
TRAIN_DATA = [
    ("I love this product", {"cats": {"POSITIVE": 1, "NEGATIVE": 0, "NEUTRAL": 0}}),
    ("This is the worst product", {"cats": {"POSITIVE": 0, "NEGATIVE": 1, "NEUTRAL": 0}}),
    ("This product is okay", {"cats": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 1}})
]

# Load the model
nlp = load_model()

# Add the TextCategorizer to the pipeline
textcat = add_textcat_pipe(nlp)

# Add labels to the TextCategorizer
add_labels(textcat)

# Train the model
train_model(nlp, textcat, TRAIN_DATA)
