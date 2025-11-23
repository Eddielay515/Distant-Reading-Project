# Quick Start Guide

Get started with the Distant Reading Project in 3 simple steps!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- nltk (Natural Language Toolkit)
- pandas, matplotlib, seaborn (data analysis and visualization)
- wordcloud (word cloud generation)
- scikit-learn (machine learning utilities)

## 2. Run the Example

```bash
python main.py
```

This will:
- Download "The Coming Race" from Project Gutenberg
- Apply text processing (tokenization, lemmatization, stopword filtering)
- Generate comprehensive analysis and visualizations
- Save results to the `results/` directory

## 3. View Results

Check the `results/` directory for:
- Word clouds showing the most prominent words
- Frequency distribution charts
- Comparative statistics (if multiple books)
- Vocabulary overlap analysis
- Text summary report

## Adding Your Own Books

### From URL (Project Gutenberg or any text URL)

```python
from src.book_analyzer import BookAnalyzer

analyzer = BookAnalyzer()
analyzer.add_book_from_url(
    "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    "Frankenstein"
)
```

### From Local File

```python
analyzer.add_book_from_file("path/to/your/book.txt", "My Book")
```

### Complete Example

```python
from src.book_analyzer import BookAnalyzer

# Initialize
analyzer = BookAnalyzer()

# Add multiple books
analyzer.add_book_from_url(
    "https://www.gutenberg.org/cache/epub/8492/pg8492.txt",
    "The Coming Race"
)
analyzer.add_book_from_url(
    "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    "Frankenstein"
)

# Process and analyze
analyzer.process_all_books()
analyzer.generate_comparison_report()
```

## Key Features

### Text Processing Pipeline
- **Cleaning**: Removes Project Gutenberg headers/footers
- **Tokenization**: Splits text into words and sentences
- **Stopword Filtering**: Removes common words (the, a, an, etc.)
- **Lemmatization**: Converts words to base forms (running → run)

### Analysis Outputs
- Word frequency distributions
- Vocabulary richness metrics
- Part-of-speech analysis
- Comparative statistics across books
- Vocabulary overlap between books

## Customization

Control processing options:

```python
# Keep stopwords
analyzer.process_all_books(remove_stops=False)

# Skip lemmatization
analyzer.process_all_books(use_lemmatization=False)

# Compare specific books
analyzer.compare_books("Book 1", "Book 2")
```

## Troubleshooting

**NLTK Data Error**: If you get NLTK data errors, run:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"
```

**Import Error**: Make sure you're running from the project root directory.

**Network Error**: If downloading from Gutenberg fails, try again or use local files instead.

## Next Steps

- Add more books from [Project Gutenberg](https://www.gutenberg.org/)
- Customize visualizations in `src/visualization.py`
- Extend analysis in `src/text_processor.py`
- Share your findings!

Happy analyzing! 📚
