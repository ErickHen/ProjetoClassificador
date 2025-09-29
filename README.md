# 📧 Classificador de E-mails com IA

Este projeto consiste em uma aplicação web que classifica e-mails em Produtivos ou Improdutivos e gera uma resposta automática sugerida utilizando inteligência artificial.
A aplicação é dividida em frontend e backend, com deploy no Vercel e Render, respectivamente.

#🚀 Demonstração

🔹 O usuário pode:

Inserir um texto de e-mail manualmente.
Fazer upload de arquivos .txt ou .pdf contendo o e-mail.
Receber instantaneamente a classificação e uma resposta automática.

#🖼️ Interface

Upload box com efeito vidro preto fosco.
Resultados exibidos em destaque logo após o envio.
Formulário é limpo automaticamente após cada envio.

#🛠️ Tecnologias Utilizadas

Frontend (Vercel)
HTML, CSS e JavaScript
Fetch API para comunicação com o backend
Backend (Render)
Python + Flask
Flask-CORS para comunicação segura
PyPDF2 para leitura de PDFs
Scikit-learn (Naive Bayes) para classificação
NLTK para pré-processamento de texto
TF-IDF para vetorização
Integração com API DeepSeek (OpenRouter) para geração de respostas inteligentes

#⚙️ Como Funciona

O usuário envia um e-mail (texto, .txt ou .pdf).
O backend processa o texto, aplica pré-processamento e classifica com Naive Bayes.
O modelo retorna se o e-mail é Produtivo ou Improdutivo.
Uma chamada à API DeepSeek gera a resposta automática recomendada.
O frontend exibe o resultado na interface.

📂 Estrutura do Projeto
├── backend/
│   ├── app.py          # API Flask
│   ├── ml_model.py     # Modelo de IA treinado
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md

▶️ Executando Localmente
Backend
cd backend
pip install -r requirements.txt
python app.py

Frontend

Abra o index.html no navegador ou utilize Live Server no VSCode.

🌍 Deploy

Backend: Render
Frontend: Vercel
Comunicação via endpoint:

👨‍💻 Autor

Desenvolvido por Erik Henrique 🚀
