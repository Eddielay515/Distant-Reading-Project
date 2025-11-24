// Book collection data
const booksData = [
    {
        id: "the-coming-race",
        title: "The Coming Race",
        author: "Edward Bulwer-Lytton",
        tags: ["Science Fiction", "Dystopian", "Classic", "19th Century"],
        gutenbergId: "8492",
        textUrl: "https://www.gutenberg.org/cache/epub/8492/pg8492.txt",
        readUrl: "https://www.gutenberg.org/ebooks/8492",
        description: "A tale of a subterranean race of superior beings and their advanced civilization."
    },
    {
        id: "dracula",
        title: "Dracula",
        author: "Bram Stoker",
        tags: ["Horror", "Gothic", "Classic", "19th Century", "Vampires"],
        gutenbergId: "345",
        textUrl: "https://www.gutenberg.org/cache/epub/345/pg345.txt",
        readUrl: "https://www.gutenberg.org/ebooks/345",
        description: "The classic vampire tale that defined the genre."
    },
    {
        id: "metamorphosis",
        title: "Metamorphosis",
        author: "Franz Kafka",
        tags: ["Fiction", "Modernist", "Classic", "20th Century", "Existential"],
        gutenbergId: "5200",
        textUrl: "https://www.gutenberg.org/cache/epub/5200/pg5200.txt",
        readUrl: "https://www.gutenberg.org/ebooks/5200",
        description: "A man wakes up to find himself transformed into a giant insect."
    },
    {
        id: "book-4",
        title: "Book 4",
        author: "Unknown",
        tags: ["Classic"],
        gutenbergId: "6087",
        textUrl: "https://www.gutenberg.org/cache/epub/6087/pg6087.txt",
        readUrl: "https://www.gutenberg.org/ebooks/6087",
        description: "Classic literature from Project Gutenberg."
    },
    {
        id: "pride-and-prejudice",
        title: "Pride and Prejudice",
        author: "Jane Austen",
        tags: ["Romance", "Classic", "19th Century", "Social Commentary"],
        gutenbergId: "1342",
        textUrl: "https://www.gutenberg.org/cache/epub/1342/pg1342.txt",
        readUrl: "https://www.gutenberg.org/ebooks/1342",
        description: "A romantic novel of manners set in Georgian England."
    }
];

// Get all unique tags
function getAllTags() {
    const tags = new Set();
    booksData.forEach(book => {
        book.tags.forEach(tag => tags.add(tag));
    });
    return Array.from(tags).sort();
}

// Get books by tag
function getBooksByTag(tag) {
    return booksData.filter(book => book.tags.includes(tag));
}
