# Vehicle Recommendation Service

This project is a **FastAPI-based microservice** for a vehicle recommendation system that uses **AI embeddings generated from customer reviews**.

It leverages:
- Sentence Transformers (HuggingFace) for NLP embeddings
- PostgreSQL with pgvector for vector storage and similarity search
- FastAPI for high-performance API services

The system allows:
- Generating embeddings from vehicle reviews
- Updating embeddings when new reviews are added
- Ranking vehicles based on user search queries using semantic similarity

---

# Setup Instructions

## 1. Install Python Requirements

Create a virtual environment (recommended):

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Install dependecies:

```bash
pip install -r requirements.txt
```
## 2. Add .env file to the root location of the project. .env file will contain the db url and API Key(Needed for BE communication)

## 3. Run the FastAPI api

```bash
fastapi dev
```

This will run the app.py file

# System Architectures

## This represents how embeddings are saved for each review.
<img width="1800" height="1148" alt="image" src="https://github.com/user-attachments/assets/b2925d12-6181-4740-8ba5-1f49b24ee771" />

## This shows how search query gives best results available from the reviews.
<img width="1800" height="1148" alt="image" src="https://github.com/user-attachments/assets/a0b906b0-5f01-4165-82c8-779b52d42dd9" />


