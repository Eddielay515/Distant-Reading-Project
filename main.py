"""
Example usage of the Distant Reading Project book analyzer.
Demonstrates text processing, tokenization, lemmatization, and comparative analysis.
"""

from src.book_analyzer import BookAnalyzer


def main():
    """Run the book analysis example."""

    print("="*80)
    print("DISTANT READING PROJECT - BOOK ANALYSIS")
    print("="*80)

    # Initialize the analyzer
    analyzer = BookAnalyzer()

    # Add books from Project Gutenberg
    # Book 1: "The Coming Race" by Edward Bulwer-Lytton
    analyzer.add_book_from_url(
        "https://www.gutenberg.org/cache/epub/8492/pg8492.txt",
        "The Coming Race"
    )

    # Book 2: "Dracula" by Bram Stoker
    analyzer.add_book_from_url(
        "https://www.gutenberg.org/cache/epub/345/pg345.txt",
        "Dracula"
    )

    # Or add books from local files
    # analyzer.add_book_from_file("path/to/your/book.txt", "My Book")

    # Process all books with:
    # - Tokenization: Breaking text into words and sentences
    # - Stopword filtering: Removing common words (the, a, an, etc.)
    # - Lemmatization: Converting words to their base forms
    print("\n" + "="*80)
    print("PROCESSING BOOKS")
    print("="*80)

    analyzer.process_all_books(
        remove_stops=True,      # Remove stopwords
        use_lemmatization=True  # Apply lemmatization
    )

    # Generate comprehensive analysis and visualizations
    print("\n" + "="*80)
    print("GENERATING ANALYSIS")
    print("="*80)

    analyzer.generate_comparison_report()

    # Display individual book statistics
    print("\n" + "="*80)
    print("DETAILED STATISTICS")
    print("="*80)

    for book_name in analyzer.processed_books.keys():
        stats = analyzer.get_book_statistics(book_name)
        if stats:
            print(f"\n{book_name}:")
            print(f"  Total words: {stats['word_count']:,}")
            print(f"  Unique words: {stats['unique_words']:,}")
            print(f"  Sentences: {stats['sentence_count']:,}")
            print(f"  Vocabulary richness: {stats['vocabulary_richness']:.4f}")
            print(f"  Average word length: {stats['average_word_length']:.2f} characters")

            print(f"\n  Top 15 most common words:")
            for i, (word, freq) in enumerate(list(stats['word_frequencies'].items())[:15], 1):
                print(f"    {i:2d}. {word:15s} - {freq:5d} occurrences")

    # Compare the two books directly
    if len(analyzer.processed_books) >= 2:
        print("\n" + "="*80)
        print("DIRECT COMPARISON")
        print("="*80)
        book_names = list(analyzer.processed_books.keys())
        analyzer.compare_books(book_names[0], book_names[1])

    print("\n" + "="*80)
    print("Analysis complete! Check the 'results/' directory for visualizations.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
