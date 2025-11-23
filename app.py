"""
Web interface for the Distant Reading Project.
Provides a browseable interface with clickable tags to filter books.
"""

from flask import Flask, render_template, request, jsonify
from src.book_analyzer import BookAnalyzer
import os
import re

app = Flask(__name__)

# Initialize the book analyzer
analyzer = BookAnalyzer()


def extract_gutenberg_id(url):
    """Extract Gutenberg book ID from URL."""
    match = re.search(r'/epub/(\d+)/', url)
    return match.group(1) if match else None


def get_gutenberg_read_url(url):
    """Get the Gutenberg reading page URL from raw text URL."""
    book_id = extract_gutenberg_id(url)
    return f"https://www.gutenberg.org/ebooks/{book_id}" if book_id else None

# Add books with metadata and tags
books_data = [
    {
        "url": "https://www.gutenberg.org/cache/epub/8492/pg8492.txt",
        "title": "The Coming Race",
        "author": "Edward Bulwer-Lytton",
        "tags": ["Science Fiction", "Dystopian", "Classic", "19th Century"]
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/345/pg345.txt",
        "title": "Dracula",
        "author": "Bram Stoker",
        "tags": ["Horror", "Gothic", "Classic", "19th Century", "Vampires"]
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/5200/pg5200.txt",
        "title": "Metamorphosis",
        "author": "Franz Kafka",
        "tags": ["Fiction", "Modernist", "Classic", "20th Century", "Existential"]
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/6087/pg6087.txt",
        "title": "Book 4",
        "author": "Unknown",
        "tags": ["Classic"]
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/1342/pg1342.txt",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "tags": ["Romance", "Classic", "19th Century", "Social Commentary"]
    }
]

# Load books into analyzer
for book in books_data:
    analyzer.add_book_from_url(
        book["url"],
        book["title"],
        author=book["author"],
        tags=book["tags"]
    )


@app.route('/')
def index():
    """Main page showing all books and tags."""
    all_tags = analyzer.get_all_tags()

    # Get all books with their metadata
    books = []
    for book_name in analyzer.books.keys():
        metadata = analyzer.get_book_metadata(book_name)
        stats = analyzer.get_book_statistics(book_name)
        raw_url = metadata.get('url', '')

        books.append({
            'title': book_name,
            'author': metadata.get('author', 'Unknown'),
            'tags': metadata.get('tags', []),
            'url': raw_url,
            'read_url': get_gutenberg_read_url(raw_url),
            'processed': book_name in analyzer.processed_books,
            'stats': stats if stats else None
        })

    return render_template('index.html', books=books, all_tags=all_tags)


@app.route('/tag/<tag>')
def filter_by_tag(tag):
    """Page showing books filtered by a specific tag."""
    all_tags = analyzer.get_all_tags()
    book_names = analyzer.get_books_by_tag(tag)

    # Get books with their metadata
    books = []
    for book_name in book_names:
        metadata = analyzer.get_book_metadata(book_name)
        stats = analyzer.get_book_statistics(book_name)
        raw_url = metadata.get('url', '')

        books.append({
            'title': book_name,
            'author': metadata.get('author', 'Unknown'),
            'tags': metadata.get('tags', []),
            'url': raw_url,
            'read_url': get_gutenberg_read_url(raw_url),
            'processed': book_name in analyzer.processed_books,
            'stats': stats if stats else None
        })

    return render_template('index.html', books=books, all_tags=all_tags, selected_tag=tag)


@app.route('/book/<path:title>')
def book_detail(title):
    """Detailed view of a specific book."""
    metadata = analyzer.get_book_metadata(title)
    stats = analyzer.get_book_statistics(title)

    if not metadata:
        return "Book not found", 404

    raw_url = metadata.get('url', '')
    book_info = {
        'title': title,
        'author': metadata.get('author', 'Unknown'),
        'tags': metadata.get('tags', []),
        'url': raw_url,
        'read_url': get_gutenberg_read_url(raw_url),
        'stats': stats
    }

    return render_template('book_detail.html', book=book_info)


@app.route('/process')
def process_books():
    """Process all books for analysis."""
    analyzer.process_all_books(remove_stops=True, use_lemmatization=True)
    return jsonify({'status': 'success', 'message': 'All books processed'})


@app.route('/analyze')
def analyze_books():
    """Generate analysis and visualizations."""
    analyzer.generate_comparison_report()
    return jsonify({'status': 'success', 'message': 'Analysis complete'})


if __name__ == '__main__':
    print("Starting Distant Reading Project Web Interface...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
