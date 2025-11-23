"""
Main book analyzer module for comparative analysis.
"""

import os
import requests
from typing import Dict, List, Optional
from .text_processor import TextProcessor
from .visualization import Visualizer


class BookAnalyzer:
    """Main class for analyzing and comparing books."""

    def __init__(self, books_dir: str = "books", results_dir: str = "results"):
        """
        Initialize the book analyzer.

        Args:
            books_dir: Directory to store downloaded books
            results_dir: Directory to store analysis results
        """
        self.books_dir = books_dir
        self.results_dir = results_dir
        self.processor = TextProcessor()
        self.visualizer = Visualizer(results_dir)

        # Create directories
        os.makedirs(books_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        # Storage for books
        self.books = {}  # {book_name: raw_text}
        self.processed_books = {}  # {book_name: processed_data}
        self.book_metadata = {}  # {book_name: {author, tags, url}}

    def add_book_from_url(self, url: str, book_name: str, author: str = "Unknown",
                         tags: List[str] = None) -> bool:
        """
        Download and add a book from a URL.

        Args:
            url: URL to download the book from
            book_name: Name to assign to the book
            author: Author of the book
            tags: List of tags/categories for the book

        Returns:
            True if successful, False otherwise
        """
        if tags is None:
            tags = []

        try:
            print(f"Downloading {book_name} from {url}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            text = response.text

            # Save to file
            filename = f"{book_name.replace(' ', '_')}.txt"
            filepath = os.path.join(self.books_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)

            self.books[book_name] = text
            self.book_metadata[book_name] = {
                'author': author,
                'tags': tags,
                'url': url
            }
            print(f"✓ Successfully downloaded {book_name}")
            return True

        except Exception as e:
            print(f"✗ Error downloading {book_name}: {e}")
            return False

    def add_book_from_file(self, filepath: str, book_name: Optional[str] = None) -> bool:
        """
        Add a book from a local file.

        Args:
            filepath: Path to the book file
            book_name: Name to assign to the book (uses filename if not provided)

        Returns:
            True if successful, False otherwise
        """
        try:
            if not book_name:
                book_name = os.path.splitext(os.path.basename(filepath))[0]

            print(f"Loading {book_name} from {filepath}...")

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            self.books[book_name] = text
            print(f"✓ Successfully loaded {book_name}")
            return True

        except Exception as e:
            print(f"✗ Error loading {book_name}: {e}")
            return False

    def process_book(self, book_name: str, remove_stops: bool = True,
                    use_lemmatization: bool = True) -> bool:
        """
        Process a single book.

        Args:
            book_name: Name of the book to process
            remove_stops: Whether to remove stopwords
            use_lemmatization: Whether to apply lemmatization

        Returns:
            True if successful, False otherwise
        """
        if book_name not in self.books:
            print(f"✗ Book '{book_name}' not found")
            return False

        try:
            print(f"Processing {book_name}...")
            text = self.books[book_name]

            processed_data = self.processor.process_text(
                text,
                remove_stops=remove_stops,
                use_lemmatization=use_lemmatization
            )

            self.processed_books[book_name] = processed_data
            print(f"✓ Successfully processed {book_name}")
            print(f"  - Words: {processed_data['word_count']:,}")
            print(f"  - Unique words: {processed_data['unique_words']:,}")
            print(f"  - Sentences: {processed_data['sentence_count']:,}")
            return True

        except Exception as e:
            print(f"✗ Error processing {book_name}: {e}")
            return False

    def process_all_books(self, remove_stops: bool = True,
                         use_lemmatization: bool = True):
        """
        Process all added books.

        Args:
            remove_stops: Whether to remove stopwords
            use_lemmatization: Whether to apply lemmatization
        """
        print(f"\nProcessing {len(self.books)} book(s)...\n")

        for book_name in self.books.keys():
            self.process_book(book_name, remove_stops, use_lemmatization)
            print()

    def analyze_book(self, book_name: str):
        """
        Generate detailed analysis for a single book.

        Args:
            book_name: Name of the book to analyze
        """
        if book_name not in self.processed_books:
            print(f"✗ Book '{book_name}' has not been processed yet")
            return

        print(f"\nAnalyzing {book_name}...\n")
        data = self.processed_books[book_name]

        # Generate word cloud
        self.visualizer.create_wordcloud(
            data['word_frequencies'],
            f"Word Cloud - {book_name}",
            f"{book_name.replace(' ', '_')}_wordcloud.png"
        )

        # Generate frequency plot
        self.visualizer.plot_word_frequencies(
            data['word_frequencies'],
            f"Top Words - {book_name}",
            f"{book_name.replace(' ', '_')}_frequencies.png"
        )

    def analyze_all_books(self):
        """Generate analysis for all processed books."""
        print(f"\nGenerating individual analyses for {len(self.processed_books)} book(s)...\n")

        for book_name in self.processed_books.keys():
            self.analyze_book(book_name)

    def generate_comparison_report(self):
        """Generate a comprehensive comparison report for all books."""
        if len(self.processed_books) < 2:
            print("Need at least 2 books for comparison")
            if len(self.processed_books) == 1:
                # Still generate individual analysis
                self.analyze_all_books()
                self.visualizer.create_summary_report(self.processed_books)
            return

        print("\nGenerating comparative analysis...\n")

        # Generate individual analyses
        self.analyze_all_books()

        # Generate comparison statistics
        self.visualizer.compare_statistics(self.processed_books)

        # Generate vocabulary overlap
        books_vocab = {
            name: set(data['tokens'])
            for name, data in self.processed_books.items()
        }
        self.visualizer.plot_vocabulary_overlap(books_vocab)

        # Generate summary report
        self.visualizer.create_summary_report(self.processed_books)

        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nResults saved to: {self.results_dir}/")
        print("\nGenerated files:")
        print("  - Individual word clouds for each book")
        print("  - Word frequency plots for each book")
        print("  - Comparative statistics chart")
        print("  - Vocabulary overlap heatmap")
        print("  - Text summary report")

    def get_book_statistics(self, book_name: str) -> Optional[Dict]:
        """
        Get statistics for a specific book.

        Args:
            book_name: Name of the book

        Returns:
            Dictionary of statistics or None if book not found
        """
        return self.processed_books.get(book_name)

    def compare_books(self, book1: str, book2: str):
        """
        Print a comparison of two specific books.

        Args:
            book1: Name of first book
            book2: Name of second book
        """
        if book1 not in self.processed_books or book2 not in self.processed_books:
            print("✗ One or both books not found")
            return

        data1 = self.processed_books[book1]
        data2 = self.processed_books[book2]

        vocab1 = set(data1['tokens'])
        vocab2 = set(data2['tokens'])

        overlap = vocab1 & vocab2
        unique_to_1 = vocab1 - vocab2
        unique_to_2 = vocab2 - vocab1

        print(f"\nComparison: {book1} vs {book2}")
        print("="*80)
        print(f"\n{book1}:")
        print(f"  Words: {data1['word_count']:,}")
        print(f"  Unique words: {data1['unique_words']:,}")
        print(f"  Vocabulary richness: {data1['vocabulary_richness']:.4f}")

        print(f"\n{book2}:")
        print(f"  Words: {data2['word_count']:,}")
        print(f"  Unique words: {data2['unique_words']:,}")
        print(f"  Vocabulary richness: {data2['vocabulary_richness']:.4f}")

        print(f"\nVocabulary Overlap:")
        print(f"  Shared words: {len(overlap):,}")
        print(f"  Unique to {book1}: {len(unique_to_1):,}")
        print(f"  Unique to {book2}: {len(unique_to_2):,}")
        print(f"  Jaccard similarity: {len(overlap) / len(vocab1 | vocab2):.4f}")

    def get_all_tags(self) -> List[str]:
        """
        Get all unique tags from all books.

        Returns:
            List of unique tags
        """
        all_tags = set()
        for metadata in self.book_metadata.values():
            all_tags.update(metadata.get('tags', []))
        return sorted(list(all_tags))

    def get_books_by_tag(self, tag: str) -> List[str]:
        """
        Get all books that have a specific tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of book names with that tag
        """
        books = []
        for book_name, metadata in self.book_metadata.items():
            if tag in metadata.get('tags', []):
                books.append(book_name)
        return books

    def get_book_metadata(self, book_name: str) -> Optional[Dict]:
        """
        Get metadata for a specific book.

        Args:
            book_name: Name of the book

        Returns:
            Dictionary of metadata or None if book not found
        """
        return self.book_metadata.get(book_name)
