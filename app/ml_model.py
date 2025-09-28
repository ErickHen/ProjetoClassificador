import os
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB  
from sklearn.preprocessing import LabelEncoder
from openai import OpenAI
from dotenv import load_dotenv

# Baixar recursos do NLTK
nltk.download("stopwords", quiet=True)
nltk.download("rslp", quiet=True)

MODEL_PATH = "email_model.pkl"

# Configuração OpenRouter + DeepSeek
load_dotenv()
AI_KEY = os.getenv('AI_KEY')

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_KEY  
)

MODEL_NAME = "deepseek/deepseek-r1:free"

# Dados de treino
TRAIN_TEXTS = [
    "Preciso de suporte para minha conta",
    "Estou com dúvida sobre o sistema",
    "Erro no cadastro, preciso de ajuda",
    "Atualização do status do chamado",
    "Promoção exclusiva, clique aqui",
    "Ganhe prêmios grátis agora",
    "Convite para evento social",
    "Você foi sorteado, parabéns"
]
TRAIN_LABELS = [
    "Produtivo", "Produtivo", "Produtivo", "Produtivo",
    "Improdutivo", "Improdutivo", "Improdutivo", "Improdutivo"
]

# Funções de NLP
def remove_stopwords(text):
    stop_words = set(stopwords.words("portuguese"))
    tokens = text.lower().split()
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

def apply_stemming(text):
    stemmer = RSLPStemmer()
    tokens = text.lower().split()
    stemmed = [stemmer.stem(word) for word in tokens]
    return " ".join(stemmed)

# Pré-processar textos de treino
PROCESSED_TEXTS = [apply_stemming(remove_stopwords(t)) for t in TRAIN_TEXTS]

# LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(TRAIN_LABELS)

# Treinar / salvar modelo
def train_and_save_model():
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(PROCESSED_TEXTS)
    clf = MultinomialNB()
    clf.fit(X, y_encoded)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, clf, label_encoder), f)

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    with open(MODEL_PATH, "rb") as f:
        vectorizer, clf, le = pickle.load(f)
    return vectorizer, clf, le

VECTORIZER, CLASSIFIER, LABEL_ENCODER = load_model()

def classify_email(text: str):
    # Pré-processamento
    processed = apply_stemming(remove_stopwords(text))
    X = VECTORIZER.transform([processed])
    pred = CLASSIFIER.predict(X)[0]
    category = LABEL_ENCODER.inverse_transform([pred])[0]

    # Prompt para a IA
    prompt = f"""
        Você é um assistente que responde emails.
        Categoria detectada: {category}.
        Email recebido: "{text}"

        Gere uma resposta educada e apropriada ao remetente com base nisso.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = completion.choices[0].message.content.strip()
    except Exception:
        if category == "Produtivo":
            answer = "Obrigado pelo contato! Nossa equipe retornará em breve."
        else:
            answer = "Recebemos sua mensagem. Não é necessária nenhuma ação."

    return category, answer
