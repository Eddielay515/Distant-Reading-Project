# Distant Reading Project

A comprehensive Python-based tool for comparative analysis of literary texts using natural language processing techniques.

## Features

- **Web Interface**: Browse books with clickable tags for easy filtering
- **Tag-Based Navigation**: Filter books by genre, time period, and other categories
- **Text Processing**: Download and process texts from various sources (Project Gutenberg, local files)
- **Tokenization**: Break down texts into words and sentences
- **Lemmatization**: Reduce words to their base forms for better analysis
- **Stopword Filtering**: Remove common words to focus on meaningful content
- **Comparative Analysis**: Compare multiple books across various metrics
- **Visualization**: Generate word clouds, frequency distributions, and comparison charts

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Distant-Reading-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"
```

## Usage

### Static Website (No Installation Required!)

**Easiest option**: Just open the website in your browser - no Python, no installation needed!

1. Navigate to the `web` directory
2. Open `index.html` in any web browser
3. Browse books and click tags to filter by category

The static website includes:
- All 5 books with clickable tag navigation
- Direct links to read books on Project Gutenberg
- Full responsive design
- Works offline (after first load)

See `web/README.md` for deployment options (GitHub Pages, Netlify, etc.)

### Flask Web Interface (Requires Python)

Launch the dynamic Flask interface for processing and analysis:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

Features:
- Browse all books in the collection
- Click on tags to filter books by category (Genre, Time Period, etc.)
- View detailed statistics for each book
- Process and analyze books directly from the web interface

### Command Line Analysis

```python
from src.book_analyzer import BookAnalyzer

# Initialize analyzer
analyzer = BookAnalyzer()

# Add books from URL
analyzer.add_book_from_url(
    "https://www.gutenberg.org/cache/epub/8492/pg8492.txt",
    "Sample Book"
)

# Add books from local file
analyzer.add_book_from_file("path/to/book.txt", "My Book")

# Process all books
analyzer.process_all_books()

# Generate comparative analysis
analyzer.generate_comparison_report()
```

### Running the Example

```bash
python main.py
```

## Project Structure

```
Distant-Reading-Project/
├── src/
│   ├── book_analyzer.py      # Main analysis module
│   ├── text_processor.py     # Text processing utilities
│   └── visualization.py      # Visualization tools
├── books/                    # Storage for downloaded books
├── results/                  # Analysis results and visualizations
├── main.py                   # Example usage script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Analysis Features

### Text Statistics
- Total word count
- Unique word count
- Vocabulary richness (type-token ratio)
- Average word length
- Sentence count

### Linguistic Analysis
- Part-of-speech distribution
- Most common words (with and without stopwords)
- Most common lemmas
- Vocabulary overlap between books

### Visualizations
- Word clouds
- Word frequency distributions
- Comparative bar charts
- Vocabulary richness comparisons

## Examples

The repository includes a sample analysis of texts from Project Gutenberg demonstrating all features.

## License

MIT License
