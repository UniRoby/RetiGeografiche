
from feel_it import EmotionClassifier, SentimentClassifier

emotion_classifier = EmotionClassifier()

print(emotion_classifier.predict(["Basta ancora con sto fascismo non ne possiamo più di sentire sempre le stesse cose", "si stava parlando del salario minimo, non rigiri la frittata per avere ragione", "va bene ora non piangere vai a lavorare"]))


sentiment_classifier = SentimentClassifier()

sentiment= sentiment_classifier.predict(["muori"])
print(sentiment[0])

from setfit import SetFitModel

# Download from Hub and run inference
model = SetFitModel.from_pretrained("nickprock/setfit-italian-hate-speech")
# Run inference
preds = model(["Lei è una brutta bugiarda!", "Mi piace la pizza"," Non mi piace questa situazione","Non posso ascoltare", "Ti voglio poco bene"])
print(preds[0])

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-classification", model="IMSyPP/hate_speech_it")

hate= pipe("Lei è una brutta bugiarda!")
print(hate[0]['label'])












