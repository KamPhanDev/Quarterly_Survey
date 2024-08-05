import spacy
import random

# Training data
TRAIN_DATA = [
    ("I love this product", {"cats": {"POSITIVE": 1, "NEGATIVE": 0, "NEUTRAL": 0}}),
    ("This is the worst product", {"cats": {"POSITIVE": 0, "NEGATIVE": 1, "NEUTRAL": 0}}),
    ("This product is okay", {"cats": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 1}})
]

# Load a spacy model
nlp = spacy.blank('en')

# Add TextCategorizer to the pipeline
textcat = nlp.create_pipe(
              "textcat",
              config={
                "exclusive_classes": True,
                "architecture": "simple_cnn",
              }
            )
nlp.add_pipe(textcat, last=True)

# Add labels to text classifier
textcat.add_label("POSITIVE")
textcat.add_label("NEGATIVE")
textcat.add_label("NEUTRAL")

# Train the model
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
with nlp.disable_pipes(*other_pipes):  # only train textcat
    optimizer = nlp.begin_training()
    print("Training the model...")
    for i in range(10):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update([text], [annotations], sgd=optimizer, drop=0.2, losses=losses)
        print(losses)
