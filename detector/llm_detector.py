import requests
import string
from collections import Counter

# Configuration
API_URL = "http://localhost:8000/chat"
PROMPT_MESSAGE = "Explain the theory of relativity in one sentence."

# 1. Define 'Fingerprints' for different models
# Real LLMs have specific word probability distributions. 
# We mock this by looking for specific keyword densities.
MODEL_SIGNATURES = {
    "GPT-4": {
        "keywords": ["delve", "multifaceted", "crucial", "landscape", "tapestry"],
        "avg_word_length": 6.5
    },
    "Claude-3": {
        "keywords": ["nuance", "perspective", "detailed", "remain", "helpful"],
        "avg_word_length": 6.2
    },
    "Llama-2": {
        "keywords": ["sure", "here", "help", "model", "language"],
        "avg_word_length": 5.8
    },
    "Simple-Bot (Current Docker)": {
        "keywords": ["simple", "always", "bot", "say", "this"],
        "avg_word_length": 3.0
    }
}

def clean_and_tokenize(text):
    """Removes punctuation and splits text into lowercase words."""
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower().split()

def analyze_response(text):
    """Calculates statistics for the received text."""
    tokens = clean_and_tokenize(text)
    
    if not tokens:
        return None

    # Calculate basic stats
    word_counts = Counter(tokens)
    total_words = len(tokens)
    avg_len = sum(len(word) for word in tokens) / total_words
    
    print(f"\n--- Statistical Analysis ---")
    print(f"Total Words: {total_words}")
    print(f"Average Word Length: {avg_len:.2f}")
    print(f"Top 3 Words: {word_counts.most_common(3)}")
    
    return tokens, avg_len

def predict_model(tokens, avg_len):
    """
    Scores the text against known signatures.
    Score = (Keyword Matches * 2) - (Difference in Average Word Length)
    """
    best_score = -float('inf')
    predicted_model = "Unknown"
    
    print(f"\n--- Model Prediction ---")
    
    for model_name, signature in MODEL_SIGNATURES.items():
        score = 0
        
        # Check for signature keywords
        matches = [word for word in tokens if word in signature['keywords']]
        score += len(matches) * 2
        
        # Check word complexity (avg length) proximity
        # We penalize if the complexity is too different
        len_diff = abs(avg_len - signature['avg_word_length'])
        score -= len_diff
        
        print(f"Model: {model_name:<25} | Score: {score:.2f} | Matches: {matches}")
        
        if score > best_score:
            best_score = score
            predicted_model = model_name

    return predicted_model

def main():
    print(f"Connecting to Service at {API_URL}...")
    
    try:
        # 1. Call the Service
        payload = {"message": PROMPT_MESSAGE}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        data = response.json()
        bot_text = data.get("response", "")
        
        print(f"Bot Replied: \"{bot_text}\"")
        
        # 2. Analyze
        analysis_result = analyze_response(bot_text)
        if not analysis_result:
            print("Error: Empty response received.")
            return

        tokens, avg_len = analysis_result
        
        # 3. Predict
        winner = predict_model(tokens, avg_len)
        
        print(f"\n>>> FINAL VERDICT: The service is running '{winner}' <<<")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to localhost:8000. Is your Docker container running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

