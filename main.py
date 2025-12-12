import random
import spacy
from spacy.util import minibatch
from spacy.training.example import Example
nlp = spacy.load("pt_core_news_lg")

if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner')
else:
    ner = nlp.get_pipe('ner')
    


train_data = [
    ('gastei 10 reais em hamburguer no BK', {"entities": [(7,9, 'VALOR'), (22, 32, 'PRODUTO')]}),
    ('usei 15 reais em gasolina', {"entities": [(5,7, 'VALOR'), (17, 25, 'PRODUTO')]})
]



print(ner.labels)

for _, annotations in train_data:
    for ent in annotations:
        if ent[2] not in ner.labels:
            ner.add_label(ent[2]) 

other_pipes=[pipe for pipe in nlp.pipe_names if pipe!='ner']
with nlp.disable_pipes(*other_pipes):
    optimezer = nlp.begin_training()

    epochs = 50
    for epoch in range(epochs):
        random.suffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=2)
        for batch in batches:
            examples = []
            for text, annotation in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            nlp.update(examples, drop=0.5, losses=losses)   
        print(f'Epoch {epoch+1}, Losses: {losses}')