"""
Text processing utilities for book analysis.
Includes tokenization, lemmatization, and stopword filtering.
"""

import re
from typing import List, Dict, Set
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from collections import Counter


class TextProcessor:
    """Handles all text processing operations."""

    def __init__(self):
        """Initialize the text processor and download required NLTK data."""
        self.lemmatizer = WordNetLemmatizer()
        self._ensure_nltk_data()
        self.stop_words = set(stopwords.words('english'))

    def _ensure_nltk_data(self):
        """Download required NLTK data if not already present."""
        required_data = [
            'punkt',
            'stopwords',
            'wordnet',
            'averaged_perceptron_tagger',
            'punkt_tab'
        ]

        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                try:
                    nltk.data.find(f'corpora/{data}')
                except LookupError:
                    try:
                        nltk.data.find(f'taggers/{data}')
                    except LookupError:
                        print(f"Downloading {data}...")
                        nltk.download(data, quiet=True)

    def clean_text(self, text: str) -> str:
        """
        Clean raw text by removing Project Gutenberg headers/footers
        and extra whitespace.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        # Remove Project Gutenberg header
        start_markers = [
            "*** START OF THIS PROJECT GUTENBERG",
            "*** START OF THE PROJECT GUTENBERG",
            "*END*THE SMALL PRINT"
        ]

        for marker in start_markers:
            if marker in text:
                text = text.split(marker, 1)[1]
                break

        # Remove Project Gutenberg footer
        end_markers = [
            "*** END OF THIS PROJECT GUTENBERG",
            "*** END OF THE PROJECT GUTENBERG",
            "End of the Project Gutenberg"
        ]

        for marker in end_markers:
            if marker in text:
                text = text.split(marker, 1)[0]
                break

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text

    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words.

        Args:
            text: Text to tokenize

        Returns:
            List of word tokens
        """
        tokens = word_tokenize(text)
        # Keep only alphabetic tokens and convert to lowercase
        tokens = [token.lower() for token in tokens if token.isalpha()]
        return tokens

    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize text into sentences.

        Args:
            text: Text to tokenize

        Returns:
            List of sentences
        """
        return sent_tokenize(text)

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from token list.

        Args:
            tokens: List of word tokens

        Returns:
            List of tokens without stopwords
        """
        return [token for token in tokens if token not in self.stop_words]

    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens to their base forms.

        Args:
            tokens: List of word tokens

        Returns:
            List of lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def lemmatize_with_pos(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens using part-of-speech tags for better accuracy.

        Args:
            tokens: List of word tokens

        Returns:
            List of lemmatized tokens
        """
        pos_tags = pos_tag(tokens)
        lemmatized = []

        for token, pos in pos_tags:
            # Convert POS tag to WordNet format
            pos_wordnet = self._get_wordnet_pos(pos)
            if pos_wordnet:
                lemmatized.append(self.lemmatizer.lemmatize(token, pos=pos_wordnet))
            else:
                lemmatized.append(self.lemmatizer.lemmatize(token))

        return lemmatized

    def _get_wordnet_pos(self, treebank_tag: str) -> str:
        """
        Convert treebank POS tags to WordNet POS tags.

        Args:
            treebank_tag: POS tag from nltk.pos_tag

        Returns:
            WordNet POS tag or None
        """
        if treebank_tag.startswith('J'):
            return 'a'  # Adjective
        elif treebank_tag.startswith('V'):
            return 'v'  # Verb
        elif treebank_tag.startswith('N'):
            return 'n'  # Noun
        elif treebank_tag.startswith('R'):
            return 'r'  # Adverb
        else:
            return None

    def get_word_frequencies(self, tokens: List[str], top_n: int = 50) -> Dict[str, int]:
        """
        Get word frequency distribution.

        Args:
            tokens: List of word tokens
            top_n: Number of top words to return

        Returns:
            Dictionary of words and their frequencies
        """
        counter = Counter(tokens)
        return dict(counter.most_common(top_n))

    def get_pos_distribution(self, tokens: List[str]) -> Dict[str, int]:
        """
        Get part-of-speech distribution.

        Args:
            tokens: List of word tokens

        Returns:
            Dictionary of POS tags and their counts
        """
        pos_tags = pos_tag(tokens)
        pos_counter = Counter(tag for _, tag in pos_tags)
        return dict(pos_counter)

    def calculate_vocabulary_richness(self, tokens: List[str]) -> float:
        """
        Calculate type-token ratio (vocabulary richness).

        Args:
            tokens: List of word tokens

        Returns:
            Type-token ratio (0-1)
        """
        if not tokens:
            return 0.0
        return len(set(tokens)) / len(tokens)

    def process_text(self, text: str, remove_stops: bool = True,
                    use_lemmatization: bool = True) -> Dict:
        """
        Complete text processing pipeline.

        Args:
            text: Raw text to process
            remove_stops: Whether to remove stopwords
            use_lemmatization: Whether to apply lemmatization

        Returns:
            Dictionary containing processed text and statistics
        """
        # Clean text
        cleaned_text = self.clean_text(text)

        # Tokenize
        tokens = self.tokenize_words(cleaned_text)
        sentences = self.tokenize_sentences(cleaned_text)

        # Store original tokens
        original_tokens = tokens.copy()

        # Remove stopwords if requested
        if remove_stops:
            tokens = self.remove_stopwords(tokens)

        # Lemmatize if requested
        if use_lemmatization:
            tokens = self.lemmatize_with_pos(tokens)

        # Calculate statistics
        word_lengths = [len(word) for word in original_tokens]

        return {
            'cleaned_text': cleaned_text,
            'tokens': tokens,
            'original_tokens': original_tokens,
            'sentences': sentences,
            'word_count': len(original_tokens),
            'unique_words': len(set(original_tokens)),
            'sentence_count': len(sentences),
            'vocabulary_richness': self.calculate_vocabulary_richness(original_tokens),
            'average_word_length': sum(word_lengths) / len(word_lengths) if word_lengths else 0,
            'word_frequencies': self.get_word_frequencies(tokens),
            'pos_distribution': self.get_pos_distribution(original_tokens)
        }
