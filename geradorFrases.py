phrases = []
import random
import spacy
from spacy.training import offsets_to_biluo_tags

nlp = spacy.load('pt_core_news_lg')

valores = ["5", "7", "10", "12", "15", "18", "20", "22", "25", "27", "30", "32", "35", "40", "45", "50", "55", "60", "65", "70"]
produtos = ["hamburguer", "pizza", "gasolina", "mercado", "uber", "taxi", "cinema", "café", "lanche", "restaurante",
            "posto de gasolina", "livros", "roupa", "farmácia", "estacionamento", "taxas", "cartão", "hotel", "bar", "sorvete"]

templates = [
    "gastei {v} reais em {p}",
    "usei {v} reais em {p}",
    "paguei {v} reais por {p}",
    "{v} reais gastos em {p}",
    "foram {v} reais em {p}",
    "fix um pix de {v} em {p}",
    "enviei {v} reais para comprar {p}",
    "mandei {v} reais pra fulano trazer {p} pra gente",
    "{p} custou {v} prata",
    "paguei {v} conto em {p}"
]

# generate 200
count = 200
items = []
while len(items) < count:
    v = random.choice(valores)
    p = random.choice(produtos)
    t = random.choice(templates)
    phrase = t.format(v=v, p=p)
    # find spans
    v_start = phrase.find(v)
    v_end = v_start + len(v)
    p_start = phrase.find(p)
    p_end = p_start + len(p)
    items.append((phrase, {"entities":[(v_start, v_end, "VALOR"), (p_start, p_end, "PRODUTO")]}))

for text, ent in items:
    doc = nlp.make_doc(text)
    if '-' in offsets_to_biluo_tags(doc, ent['entities']):
        print('ERROR - FOUND')