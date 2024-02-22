import torch
from transformers import BertForSequenceClassification, BertTokenizer

# Directory modello locale
# (Per averlo in locale è sufficiente clonare il repository da huggingface)
model_path = "hate_speech_it"

# Carica il tokenizer
tokenizer = BertTokenizer.from_pretrained(model_path)

# Carica il modello da un file locale
model = BertForSequenceClassification.from_pretrained(model_path)

# Imposta il modello in evalutation mode
model.eval()

# Utilizza il tokenizer e il modello per fare predizioni
input_text = "Lei è una brutta bugiarda!"
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Fai predizioni
with torch.no_grad():
    output = model(input_ids)

# Estrai le probabilità delle classi usando la funzione softmax
probabilities = torch.nn.functional.softmax(output.logits, dim=-1)

# Stampa le probabilità
print("Probabilità delle Classi:", probabilities)