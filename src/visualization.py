"""
Visualization utilities for book analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from typing import Dict, List
import pandas as pd
import os


class Visualizer:
    """Handles all visualization operations."""

    def __init__(self, output_dir: str = "results"):
        """
        Initialize visualizer.

        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)

    def create_wordcloud(self, word_frequencies: Dict[str, int],
                        title: str, filename: str):
        """
        Create and save a word cloud.

        Args:
            word_frequencies: Dictionary of words and frequencies
            title: Title for the word cloud
            filename: Filename to save the image
        """
        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            colormap='viridis',
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(word_frequencies)

        plt.figure(figsize=(16, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=20, pad=20)
        plt.tight_layout(pad=0)

        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Word cloud saved to: {filepath}")

    def plot_word_frequencies(self, word_frequencies: Dict[str, int],
                             title: str, filename: str, top_n: int = 20):
        """
        Create a bar plot of word frequencies.

        Args:
            word_frequencies: Dictionary of words and frequencies
            title: Title for the plot
            filename: Filename to save the image
            top_n: Number of top words to display
        """
        # Get top N words
        sorted_words = sorted(word_frequencies.items(),
                            key=lambda x: x[1], reverse=True)[:top_n]
        words, frequencies = zip(*sorted_words)

        plt.figure(figsize=(12, 8))
        plt.barh(range(len(words)), frequencies, color='steelblue')
        plt.yticks(range(len(words)), words)
        plt.xlabel('Frequency', fontsize=12)
        plt.ylabel('Words', fontsize=12)
        plt.title(title, fontsize=14, pad=20)
        plt.gca().invert_yaxis()
        plt.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Frequency plot saved to: {filepath}")

    def compare_statistics(self, books_data: Dict[str, Dict],
                          filename: str = "comparison_statistics.png"):
        """
        Create comparison plots for multiple books.

        Args:
            books_data: Dictionary mapping book names to their statistics
            filename: Filename to save the image
        """
        # Prepare data
        book_names = list(books_data.keys())
        metrics = {
            'Word Count': [books_data[book]['word_count'] for book in book_names],
            'Unique Words': [books_data[book]['unique_words'] for book in book_names],
            'Vocabulary Richness': [books_data[book]['vocabulary_richness'] for book in book_names],
            'Avg Word Length': [books_data[book]['average_word_length'] for book in book_names]
        }

        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Comparative Book Statistics', fontsize=16, y=1.02)

        colors = sns.color_palette("husl", len(book_names))

        for idx, (metric_name, values) in enumerate(metrics.items()):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]

            bars = ax.bar(book_names, values, color=colors)
            ax.set_title(metric_name, fontsize=12, pad=10)
            ax.set_ylabel(metric_name, fontsize=10)

            # Rotate x-axis labels if needed
            if len(book_names) > 3:
                ax.set_xticklabels(book_names, rotation=45, ha='right')

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}' if isinstance(height, float) else f'{height}',
                       ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Comparison plot saved to: {filepath}")

    def plot_vocabulary_overlap(self, books_vocab: Dict[str, set],
                               filename: str = "vocabulary_overlap.png"):
        """
        Create a heatmap showing vocabulary overlap between books.

        Args:
            books_vocab: Dictionary mapping book names to sets of words
            filename: Filename to save the image
        """
        book_names = list(books_vocab.keys())
        n_books = len(book_names)

        # Calculate overlap matrix
        overlap_matrix = []
        for book1 in book_names:
            row = []
            vocab1 = books_vocab[book1]
            for book2 in book_names:
                vocab2 = books_vocab[book2]
                if len(vocab1) > 0 and len(vocab2) > 0:
                    overlap = len(vocab1 & vocab2) / len(vocab1 | vocab2)
                else:
                    overlap = 0
                row.append(overlap)
            overlap_matrix.append(row)

        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(overlap_matrix, annot=True, fmt='.2f',
                   xticklabels=book_names, yticklabels=book_names,
                   cmap='YlOrRd', vmin=0, vmax=1,
                   square=True, linewidths=0.5)
        plt.title('Vocabulary Overlap (Jaccard Similarity)', fontsize=14, pad=20)
        plt.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Vocabulary overlap plot saved to: {filepath}")

    def create_summary_report(self, books_data: Dict[str, Dict],
                            filename: str = "analysis_summary.txt"):
        """
        Create a text summary report of the analysis.

        Args:
            books_data: Dictionary mapping book names to their statistics
            filename: Filename to save the report
        """
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("COMPARATIVE BOOK ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")

            for book_name, data in books_data.items():
                f.write(f"\n{book_name}\n")
                f.write("-" * 80 + "\n")
                f.write(f"Word Count: {data['word_count']:,}\n")
                f.write(f"Unique Words: {data['unique_words']:,}\n")
                f.write(f"Sentence Count: {data['sentence_count']:,}\n")
                f.write(f"Vocabulary Richness: {data['vocabulary_richness']:.4f}\n")
                f.write(f"Average Word Length: {data['average_word_length']:.2f}\n")

                f.write(f"\nTop 10 Words:\n")
                for word, freq in list(data['word_frequencies'].items())[:10]:
                    f.write(f"  {word}: {freq}\n")

                f.write("\n")

            f.write("\n" + "=" * 80 + "\n")

        print(f"Summary report saved to: {filepath}")
