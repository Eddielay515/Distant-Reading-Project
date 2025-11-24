// Global state
let booksData = [];
let activeTags = new Set();
let selectedBooksForComparison = new Set();

// Load and initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    initializeNavigation();
    renderTags();
    renderBooks();
    initializeComparison();
});

// Load JSON data
async function loadData() {
    try {
        const response = await fetch('analysis.json');
        const data = await response.json();
        booksData = data.books;
    } catch (error) {
        console.error('Error loading data:', error);
        document.body.innerHTML = '<div style="padding:40px;text-align:center;"><h2>Error loading analysis data</h2><p>Please ensure analysis.json exists in the same directory.</p></div>';
    }
}

// Navigation
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.view');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetView = btn.dataset.view;

            // Update active nav button
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update active view
            views.forEach(v => v.classList.remove('active'));
            document.getElementById(`${targetView}-view`).classList.add('active');

            // Reset comparison selections when switching views
            if (targetView === 'comparison') {
                renderComparisonBookList();
            }
        });
    });

    // Back to home button
    document.getElementById('back-to-home').addEventListener('click', () => {
        document.getElementById('home-view').classList.add('active');
        document.getElementById('book-detail-view').classList.remove('active');
    });
}

// Render tags
function renderTags() {
    const tagsContainer = document.getElementById('tags-container');
    const allTags = {};

    // Count books per tag
    booksData.forEach(book => {
        book.tags.forEach(tag => {
            allTags[tag] = (allTags[tag] || 0) + 1;
        });
    });

    // Create tag elements
    tagsContainer.innerHTML = '';
    Object.entries(allTags)
        .sort(([a], [b]) => a.localeCompare(b))
        .forEach(([tag, count]) => {
            const tagEl = document.createElement('div');
            tagEl.className = 'tag';
            tagEl.innerHTML = `${tag} <span class="tag-count">(${count})</span>`;
            tagEl.addEventListener('click', () => toggleTag(tag, tagEl));
            tagsContainer.appendChild(tagEl);
        });

    // Clear filters button
    const clearBtn = document.getElementById('clear-filters');
    clearBtn.addEventListener('click', () => {
        activeTags.clear();
        document.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
        clearBtn.style.display = 'none';
        document.getElementById('books-heading').textContent = 'All Books';
        renderBooks();
    });
}

// Toggle tag filter
function toggleTag(tag, tagElement) {
    if (activeTags.has(tag)) {
        activeTags.delete(tag);
        tagElement.classList.remove('active');
    } else {
        activeTags.add(tag);
        tagElement.classList.add('active');
    }

    // Update UI
    const clearBtn = document.getElementById('clear-filters');
    clearBtn.style.display = activeTags.size > 0 ? 'block' : 'none';

    const heading = document.getElementById('books-heading');
    heading.textContent = activeTags.size > 0
        ? `Books tagged: ${Array.from(activeTags).join(', ')}`
        : 'All Books';

    renderBooks();
}

// Render books grid
function renderBooks() {
    const booksGrid = document.getElementById('books-grid');
    const filteredBooks = getFilteredBooks();

    if (filteredBooks.length === 0) {
        booksGrid.innerHTML = '<p style="grid-column: 1/-1; text-align:center; color:#666;">No books match the selected tags.</p>';
        return;
    }

    booksGrid.innerHTML = '';
    filteredBooks.forEach(book => {
        const bookCard = createBookCard(book);
        booksGrid.appendChild(bookCard);
    });
}

// Get filtered books based on active tags
function getFilteredBooks() {
    if (activeTags.size === 0) {
        return booksData;
    }

    return booksData.filter(book => {
        return Array.from(activeTags).some(tag => book.tags.includes(tag));
    });
}

// Create book card element
function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'book-card';

    const sentimentClass = getSentimentClass(book.sentiment.compound);
    const sentimentLabel = getSentimentLabel(book.sentiment.compound);

    card.innerHTML = `
        <h3>${book.title}</h3>
        <p class="author">by ${book.author}</p>
        <div class="book-tags">
            ${book.tags.map(tag => `<span class="book-tag" data-tag="${tag}">${tag}</span>`).join('')}
        </div>
        <div class="book-stats">
            <strong>${book.style_metrics.total_words.toLocaleString()}</strong> words<br>
            <strong>${book.style_metrics.unique_words.toLocaleString()}</strong> unique words
        </div>
        <span class="sentiment-badge sentiment-${sentimentClass}">${sentimentLabel}</span>
    `;

    // Click on card to view details
    card.addEventListener('click', (e) => {
        if (!e.target.classList.contains('book-tag')) {
            showBookDetail(book);
        }
    });

    // Click on tag to filter
    card.querySelectorAll('.book-tag').forEach(tagEl => {
        tagEl.addEventListener('click', (e) => {
            e.stopPropagation();
            const tag = tagEl.dataset.tag;
            const mainTagEl = Array.from(document.querySelectorAll('.tags-container .tag'))
                .find(t => t.textContent.includes(tag));
            if (mainTagEl) {
                toggleTag(tag, mainTagEl);
            }
        });
    });

    return card;
}

// Show book detail view
function showBookDetail(book) {
    const detailView = document.getElementById('book-detail-view');
    const contentDiv = document.getElementById('book-detail-content');

    const sentimentClass = getSentimentClass(book.sentiment.compound);

    contentDiv.innerHTML = `
        <div class="book-detail">
            <div class="book-header">
                <h2>${book.title}</h2>
                <p class="author">by ${book.author}</p>
                <div class="book-tags">
                    ${book.tags.map(tag => `<span class="book-tag">${tag}</span>`).join('')}
                </div>
            </div>

            <div class="detail-section">
                <h3>Distinctive Words (TF-IDF)</h3>
                <p style="color:#666;font-size:0.9rem;margin-bottom:15px;">These words are most characteristic of this text compared to others in the corpus.</p>
                <div class="tfidf-words">
                    ${book.tfidf_descriptive_words.slice(0, 20).map(item =>
                        `<div class="tfidf-word">
                            ${item.word}
                            <span class="score">${item.score.toFixed(3)}</span>
                        </div>`
                    ).join('')}
                </div>
            </div>

            <div class="detail-section">
                <h3>Sentiment Analysis (VADER)</h3>
                <div class="sentiment-display">
                    <div class="sentiment-item">
                        <div class="sentiment-label">Compound</div>
                        <div class="sentiment-value">${book.sentiment.compound.toFixed(3)}</div>
                    </div>
                    <div class="sentiment-item">
                        <div class="sentiment-label">Positive</div>
                        <div class="sentiment-value" style="color:#28a745;">${(book.sentiment.positive * 100).toFixed(1)}%</div>
                    </div>
                    <div class="sentiment-item">
                        <div class="sentiment-label">Negative</div>
                        <div class="sentiment-value" style="color:#dc3545;">${(book.sentiment.negative * 100).toFixed(1)}%</div>
                    </div>
                    <div class="sentiment-item">
                        <div class="sentiment-label">Neutral</div>
                        <div class="sentiment-value" style="color:#6c757d;">${(book.sentiment.neutral * 100).toFixed(1)}%</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Style Metrics</h3>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-label">Total Words</div>
                        <div class="metric-value">${book.style_metrics.total_words.toLocaleString()}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Unique Words</div>
                        <div class="metric-value">${book.style_metrics.unique_words.toLocaleString()}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Vocabulary Richness</div>
                        <div class="metric-value">${book.style_metrics.vocabulary_richness.toFixed(3)}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Avg Word Length</div>
                        <div class="metric-value">${book.style_metrics.average_word_length.toFixed(1)}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Avg Sentence Length</div>
                        <div class="metric-value">${book.style_metrics.average_sentence_length.toFixed(1)}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Lexical Diversity</div>
                        <div class="metric-value">${book.style_metrics.lexical_diversity.toFixed(3)}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Reading Ease</div>
                        <div class="metric-value">${book.style_metrics.flesch_reading_ease.toFixed(1)}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Grade Level</div>
                        <div class="metric-value">${book.style_metrics.flesch_kincaid_grade.toFixed(1)}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Top 20 Most Frequent Words</h3>
                <div class="tfidf-words">
                    ${Object.entries(book.bag_of_words).slice(0, 20).map(([word, count]) =>
                        `<div class="tfidf-word">${word} <span class="score">${count}</span></div>`
                    ).join('')}
                </div>
            </div>

            <div class="detail-section">
                <h3>Part of Speech Distribution</h3>
                <canvas id="pos-chart" class="pos-chart"></canvas>
            </div>
        </div>
    `;

    // Show detail view
    document.getElementById('home-view').classList.remove('active');
    detailView.classList.add('active');

    // Render POS chart
    renderPOSChart(book.style_metrics.pos_distribution);
}

// Render POS chart
function renderPOSChart(posData) {
    const ctx = document.getElementById('pos-chart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(posData),
            datasets: [{
                label: 'Percentage',
                data: Object.values(posData),
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top 10 Part-of-Speech Tags'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Percentage (%)'
                    }
                }
            }
        }
    });
}

// Comparison functionality
function initializeComparison() {
    renderComparisonBookList();

    document.getElementById('compare-btn').addEventListener('click', () => {
        if (selectedBooksForComparison.size >= 2) {
            showComparison();
        }
    });
}

function renderComparisonBookList() {
    const container = document.getElementById('comparison-book-list');
    container.innerHTML = '';

    booksData.forEach(book => {
        const div = document.createElement('div');
        div.className = 'book-checkbox';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `compare-${book.title}`;
        checkbox.value = book.title;

        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                selectedBooksForComparison.add(book.title);
                div.classList.add('selected');
            } else {
                selectedBooksForComparison.delete(book.title);
                div.classList.remove('selected');
            }
            updateCompareButton();
        });

        const label = document.createElement('label');
        label.htmlFor = `compare-${book.title}`;
        label.style.cursor = 'pointer';
        label.innerHTML = `<strong>${book.title}</strong><br><small>${book.author}</small>`;

        div.appendChild(checkbox);
        div.appendChild(label);
        container.appendChild(div);
    });

    selectedBooksForComparison.clear();
    updateCompareButton();
}

function updateCompareButton() {
    const btn = document.getElementById('compare-btn');
    btn.disabled = selectedBooksForComparison.size < 2;
    btn.textContent = `Compare Selected Books (${selectedBooksForComparison.size})`;
}

function showComparison() {
    const selectedBooks = booksData.filter(b => selectedBooksForComparison.has(b.title));
    const resultsDiv = document.getElementById('comparison-results');

    // Sentiment Comparison
    let html = `
        <div class="comparison-section">
            <h3>Sentiment Comparison</h3>
            <canvas id="sentiment-comparison-chart" style="max-height:300px;"></canvas>
        </div>

        <div class="comparison-section">
            <h3>Style Metrics Comparison</h3>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        ${selectedBooks.map(b => `<th>${b.title}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Total Words</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.total_words.toLocaleString()}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Unique Words</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.unique_words.toLocaleString()}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Vocabulary Richness</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.vocabulary_richness.toFixed(3)}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Avg Word Length</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.average_word_length.toFixed(2)}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Avg Sentence Length</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.average_sentence_length.toFixed(2)}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Reading Ease</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.flesch_reading_ease.toFixed(1)}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Grade Level</strong></td>
                        ${selectedBooks.map(b => `<td>${b.style_metrics.flesch_kincaid_grade.toFixed(1)}</td>`).join('')}
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="comparison-section">
            <h3>Vocabulary Overlap</h3>
            <p style="color:#666;margin-bottom:15px;">Common words appearing in all selected texts</p>
            ${calculateVocabularyOverlap(selectedBooks)}
        </div>
    `;

    resultsDiv.innerHTML = html;

    // Render sentiment comparison chart
    renderSentimentComparisonChart(selectedBooks);
}

function renderSentimentComparisonChart(books) {
    const ctx = document.getElementById('sentiment-comparison-chart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: books.map(b => b.title),
            datasets: [
                {
                    label: 'Compound',
                    data: books.map(b => b.sentiment.compound),
                    backgroundColor: 'rgba(102, 126, 234, 0.8)'
                },
                {
                    label: 'Positive',
                    data: books.map(b => b.sentiment.positive),
                    backgroundColor: 'rgba(40, 167, 69, 0.8)'
                },
                {
                    label: 'Negative',
                    data: books.map(b => b.sentiment.negative),
                    backgroundColor: 'rgba(220, 53, 69, 0.8)'
                },
                {
                    label: 'Neutral',
                    data: books.map(b => b.sentiment.neutral),
                    backgroundColor: 'rgba(108, 117, 125, 0.8)'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

function calculateVocabularyOverlap(books) {
    const wordSets = books.map(book =>
        new Set(Object.keys(book.bag_of_words))
    );

    // Find intersection of all sets
    const commonWords = wordSets.reduce((acc, set) => {
        return new Set([...acc].filter(word => set.has(word)));
    });

    if (commonWords.size === 0) {
        return '<p style="color:#666;">No common words found in all selected texts.</p>';
    }

    // Get frequency of common words across all books
    const commonWordsList = Array.from(commonWords).map(word => {
        const totalFreq = books.reduce((sum, book) =>
            sum + (book.bag_of_words[word] || 0), 0
        );
        return { word, totalFreq };
    }).sort((a, b) => b.totalFreq - a.totalFreq).slice(0, 30);

    return `
        <p style="color:#666;margin-bottom:10px;">
            <strong>${commonWords.size}</strong> common words found.
            Top 30 by combined frequency:
        </p>
        <div class="tfidf-words">
            ${commonWordsList.map(item =>
                `<div class="tfidf-word">${item.word} <span class="score">${item.totalFreq}</span></div>`
            ).join('')}
        </div>
    `;
}

// Helper functions
function getSentimentClass(compound) {
    if (compound >= 0.05) return 'positive';
    if (compound <= -0.05) return 'negative';
    return 'neutral';
}

function getSentimentLabel(compound) {
    if (compound >= 0.05) return 'Positive';
    if (compound <= -0.05) return 'Negative';
    return 'Neutral';
}
