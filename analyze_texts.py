"""
Distant Reading Analysis Script
Performs comprehensive text analysis including:
- Text preprocessing and bag of words
- TF-IDF distinctive word extraction
- VADER sentiment analysis
- Style metrics calculation
Outputs results as JSON for web interface
"""

import json
import os
import re
import time
from collections import Counter
import requests
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import textstat

# Download required NLTK data
print("Downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

# Book metadata from main.py
BOOKS = [
    {
        "url": "https://www.gutenberg.org/files/8492/8492-0.txt",
        "title": "The Coming Race",
        "author": "Edward Bulwer-Lytton",
        "tags": ["Science Fiction", "Dystopian", "Classic", "19th Century"]
    },
    {
        "url": "https://www.gutenberg.org/files/345/345-0.txt",
        "title": "Dracula",
        "author": "Bram Stoker",
        "tags": ["Horror", "Gothic", "Classic", "19th Century", "Vampires"]
    },
    {
        "url": "https://www.gutenberg.org/files/5200/5200-0.txt",
        "title": "Metamorphosis",
        "author": "Franz Kafka",
        "tags": ["Fiction", "Modernist", "Classic", "20th Century", "Existential"]
    },
    {
        "url": "https://www.gutenberg.org/files/6087/6087-0.txt",
        "title": "Book 4",
        "author": "Unknown",
        "tags": ["Classic"]
    },
    {
        "url": "https://www.gutenberg.org/files/1342/1342-0.txt",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "tags": ["Romance", "Classic", "19th Century", "Social Commentary"]
    }
]


def download_text(url):
    """Download text from URL"""
    print(f"Downloading from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    time.sleep(2)  # Be polite to Project Gutenberg servers
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def clean_gutenberg_text(text):
    """Remove Project Gutenberg header and footer"""
    # Find start of book (after the header)
    start_match = re.search(r'\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK .+ \*\*\*', text)
    if start_match:
        text = text[start_match.end():]

    # Find end of book (before the footer)
    end_match = re.search(r'\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK .+ \*\*\*', text)
    if end_match:
        text = text[:end_match.start()]

    return text.strip()


def preprocess_text(text):
    """Preprocess text: clean, tokenize, remove stopwords"""
    # Clean text
    text = clean_gutenberg_text(text)

    # Tokenize
    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)

    # Remove non-alphabetic tokens and stopwords
    stop_words = set(stopwords.words('english'))
    words_filtered = [w for w in words if w.isalpha()]
    words_no_stops = [w for w in words_filtered if w not in stop_words]

    return {
        'raw_text': text,
        'words': words_filtered,
        'words_no_stops': words_no_stops,
        'sentences': sentences,
        'all_words': words  # Including non-alpha for some metrics
    }


def calculate_bag_of_words(words):
    """Create bag of words (word frequency dictionary)"""
    return dict(Counter(words).most_common(100))


def calculate_sentiment(text):
    """Calculate VADER sentiment scores"""
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return {
        'compound': scores['compound'],
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu']
    }


def calculate_style_metrics(preprocessed):
    """Calculate comprehensive style metrics"""
    words = preprocessed['words']
    sentences = preprocessed['sentences']
    raw_text = preprocessed['raw_text']

    # Basic counts
    total_words = len(words)
    unique_words = len(set(words))
    total_sentences = len(sentences)

    # Vocabulary richness (type-token ratio)
    vocab_richness = unique_words / total_words if total_words > 0 else 0

    # Average word length
    avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0

    # Average sentence length
    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0

    # Lexical diversity (unique words / total words)
    lexical_diversity = vocab_richness

    # Readability scores using textstat
    flesch_reading_ease = textstat.flesch_reading_ease(raw_text)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(raw_text)

    # Part-of-speech distribution
    # Sample first 5000 words for efficiency
    sample_words = words[:5000] if len(words) > 5000 else words
    pos_tags = pos_tag(sample_words)
    pos_counts = Counter(tag for word, tag in pos_tags)
    total_pos = len(pos_tags)
    pos_distribution = {
        tag: count / total_pos * 100
        for tag, count in pos_counts.most_common(10)
    }

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'total_sentences': total_sentences,
        'vocabulary_richness': round(vocab_richness, 4),
        'average_word_length': round(avg_word_length, 2),
        'average_sentence_length': round(avg_sentence_length, 2),
        'lexical_diversity': round(lexical_diversity, 4),
        'flesch_reading_ease': round(flesch_reading_ease, 2),
        'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
        'pos_distribution': {k: round(v, 2) for k, v in pos_distribution.items()}
    }


def calculate_tfidf_words(books_data, top_n=30):
    """Calculate TF-IDF scores and extract distinctive words for each book"""
    # Prepare documents
    documents = [' '.join(book['preprocessed']['words_no_stops']) for book in books_data]
    titles = [book['title'] for book in books_data]

    # Calculate TF-IDF
    vectorizer = TfidfVectorizer(max_features=500)
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    # Extract top words for each book
    tfidf_words = {}
    for idx, title in enumerate(titles):
        # Get TF-IDF scores for this document
        scores = tfidf_matrix[idx].toarray()[0]
        # Get indices of top N scores
        top_indices = scores.argsort()[-top_n:][::-1]
        # Get words and scores
        top_words = [
            {'word': feature_names[i], 'score': round(float(scores[i]), 4)}
            for i in top_indices if scores[i] > 0
        ]
        tfidf_words[title] = top_words

    return tfidf_words


def main():
    """Main analysis pipeline"""
    print("="*80)
    print("DISTANT READING ANALYSIS")
    print("="*80)

    # Create results directory
    os.makedirs('results', exist_ok=True)
    os.makedirs('books', exist_ok=True)

    # Process all books
    books_data = []

    for book_info in BOOKS:
        print(f"\nProcessing: {book_info['title']}")

        # Try to download, if fails try local file
        try:
            raw_text = download_text(book_info['url'])
        except Exception as e:
            print(f"  Download failed: {e}")
            # Check if local file exists
            local_file = f"books/{book_info['title'].replace(' ', '_')}.txt"
            if os.path.exists(local_file):
                print(f"  Using local file: {local_file}")
                with open(local_file, 'r', encoding='utf-8') as f:
                    raw_text = f.read()
            else:
                print(f"  Skipping {book_info['title']}")
                continue

        preprocessed = preprocess_text(raw_text)

        # Calculate metrics
        print(f"  - Building bag of words...")
        bag_of_words = calculate_bag_of_words(preprocessed['words_no_stops'])

        print(f"  - Calculating sentiment...")
        sentiment = calculate_sentiment(preprocessed['raw_text'])

        print(f"  - Calculating style metrics...")
        style_metrics = calculate_style_metrics(preprocessed)

        # Store data
        books_data.append({
            'title': book_info['title'],
            'author': book_info['author'],
            'tags': book_info['tags'],
            'preprocessed': preprocessed,
            'bag_of_words': bag_of_words,
            'sentiment': sentiment,
            'style_metrics': style_metrics
        })

    # Calculate TF-IDF distinctive words
    print("\n" + "="*80)
    print("Calculating TF-IDF distinctive words...")
    print("="*80)
    tfidf_words = calculate_tfidf_words(books_data)

    # Prepare output JSON
    output_data = {
        'books': []
    }

    for book in books_data:
        output_data['books'].append({
            'title': book['title'],
            'author': book['author'],
            'tags': book['tags'],
            'bag_of_words': book['bag_of_words'],
            'tfidf_descriptive_words': tfidf_words[book['title']],
            'sentiment': book['sentiment'],
            'style_metrics': book['style_metrics']
        })

    # Save JSON
    output_path = 'results/analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"Analysis complete! Results saved to: {output_path}")
    print(f"{'='*80}")

    # Print summary
    print("\nSummary:")
    for book in output_data['books']:
        print(f"\n{book['title']} by {book['author']}")
        print(f"  Tags: {', '.join(book['tags'])}")
        print(f"  Words: {book['style_metrics']['total_words']:,}")
        print(f"  Sentiment (compound): {book['sentiment']['compound']:.3f}")
        print(f"  Top 5 distinctive words: {', '.join([w['word'] for w in book['tfidf_descriptive_words'][:5]])}")


if __name__ == "__main__":
    main()
