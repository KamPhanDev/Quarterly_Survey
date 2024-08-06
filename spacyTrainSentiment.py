# Import the necessary libraries
import spacy
import random
from spacy.training import Example  # Import the Example class

# Define the training data
# Each example is a tuple containing a text and a dictionary
# The dictionary has a 'cats' key that maps labels to truth values
TRAIN_DATA = [
    ("I love this product", {"cats": {"POSITIVE": 1, "NEGATIVE": 0, "NEUTRAL": 0}}),
    ("This is the worst product", {"cats": {"POSITIVE": 0, "NEGATIVE": 1, "NEUTRAL": 0}}),
    ("This product is okay", {"cats": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 1}})
]

# Load a blank English model
nlp = spacy.blank('en')

# Add TextCategorizer to the pipeline
# The last=True argument means that the text categorizer will be the last component in the pipeline
textcat = nlp.add_pipe("textcat", last=True)

# Add labels to the text categorizer
# These are the categories that the model will be able to predict
textcat.add_label("POSITIVE")
textcat.add_label("NEGATIVE")
textcat.add_label("NEUTRAL")

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
        random.shuffle(TRAIN_DATA)
        # Initialize a dictionary to hold the training losses
        losses = {}
        # Update the model with each example
        for text, annotations in TRAIN_DATA:
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
