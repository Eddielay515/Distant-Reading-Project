// Global state
let currentFilter = null;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    renderTags();
    renderBooks(booksData);

    // Check for tag filter in URL hash
    const hash = window.location.hash.substring(1);
    if (hash.startsWith('tag=')) {
        const tag = decodeURIComponent(hash.substring(4));
        filterByTag(tag);
    }
});

// Render all tags
function renderTags() {
    const tagsContainer = document.getElementById('tagsContainer');
    const allTags = getAllTags();

    tagsContainer.innerHTML = allTags.map(tag =>
        `<a href="#tag=${encodeURIComponent(tag)}"
            class="tag ${currentFilter === tag ? 'tag-active' : ''}"
            onclick="filterByTag('${tag.replace(/'/g, "\\'")}'); return false;">
            ${tag}
        </a>`
    ).join('');
}

// Render books
function renderBooks(books) {
    const booksGrid = document.getElementById('booksGrid');
    const bookCount = document.getElementById('bookCount');
    const noBooks = document.getElementById('noBooks');

    bookCount.textContent = books.length;

    if (books.length === 0) {
        booksGrid.style.display = 'none';
        noBooks.style.display = 'block';
        return;
    }

    booksGrid.style.display = 'grid';
    noBooks.style.display = 'none';

    booksGrid.innerHTML = books.map(book => `
        <div class="book-card">
            <div class="book-header">
                <h4><a href="book-${book.id}.html">${book.title}</a></h4>
                <p class="book-author">by ${book.author}</p>
            </div>

            <div class="book-tags">
                ${book.tags.map(tag =>
                    `<a href="#tag=${encodeURIComponent(tag)}"
                        class="tag tag-small"
                        onclick="filterByTag('${tag.replace(/'/g, "\\'")}'); return false;">
                        ${tag}
                    </a>`
                ).join('')}
            </div>

            <div class="book-description" style="margin: 1rem 0; color: #6b7280; font-size: 0.875rem;">
                ${book.description}
            </div>

            <div class="book-actions">
                <a href="${book.readUrl}" target="_blank" class="btn btn-primary">Read on Gutenberg</a>
                <a href="book-${book.id}.html" class="btn btn-secondary">Details</a>
            </div>
        </div>
    `).join('');
}

// Filter books by tag
function filterByTag(tag) {
    currentFilter = tag;
    const filteredBooks = getBooksByTag(tag);

    // Update filter info
    const filterInfo = document.getElementById('filterInfo');
    const selectedTag = document.getElementById('selectedTag');
    filterInfo.style.display = 'block';
    selectedTag.textContent = tag;

    // Update URL hash
    window.location.hash = `tag=${encodeURIComponent(tag)}`;

    // Re-render
    renderTags();
    renderBooks(filteredBooks);

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Clear filter
function clearFilter() {
    currentFilter = null;

    // Update filter info
    const filterInfo = document.getElementById('filterInfo');
    filterInfo.style.display = 'none';

    // Clear URL hash
    window.location.hash = '';

    // Re-render
    renderTags();
    renderBooks(booksData);

    return false;
}

// Handle browser back/forward
window.addEventListener('hashchange', function() {
    const hash = window.location.hash.substring(1);
    if (hash.startsWith('tag=')) {
        const tag = decodeURIComponent(hash.substring(4));
        if (tag !== currentFilter) {
            filterByTag(tag);
        }
    } else if (currentFilter !== null) {
        clearFilter();
    }
});
