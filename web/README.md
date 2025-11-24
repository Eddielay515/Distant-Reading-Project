# Distant Reading Project - Static Website

This is a static HTML website that showcases the book collection without requiring Python or any server-side processing.

## Features

- **Pure HTML/CSS/JavaScript**: No server required
- **Clickable Tag Filtering**: Filter books by category in real-time
- **Responsive Design**: Works on desktop and mobile devices
- **Direct Gutenberg Links**: Read books instantly on Project Gutenberg
- **100% Open Access**: No authentication or setup needed

## How to Use

### Option 1: Open Directly in Browser

1. Navigate to the `web` directory
2. Open `index.html` in any web browser
3. Click on tags to filter books by category
4. Click "Read on Gutenberg" to read books online

### Option 2: Serve with Any HTTP Server

Using Python:
```bash
cd web
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

Using Node.js:
```bash
cd web
npx http-server
```

Using PHP:
```bash
cd web
php -S localhost:8000
```

## File Structure

```
web/
├── index.html              # Main page with book collection
├── book-*.html            # Individual book detail pages
├── css/
│   └── style.css          # Responsive styling
├── js/
│   ├── books-data.js      # Book metadata
│   └── app.js             # Client-side filtering logic
└── README.md              # This file
```

## Book Collection

All books are from Project Gutenberg and include:

1. **The Coming Race** by Edward Bulwer-Lytton
2. **Dracula** by Bram Stoker
3. **Metamorphosis** by Franz Kafka
4. **Book 4**
5. **Pride and Prejudice** by Jane Austen

## Tag Categories

- Classic (5 books)
- 19th Century (3 books)
- 20th Century (1 book)
- Science Fiction, Horror, Romance, etc.

## Deployment

This static site can be deployed to any web hosting service:

- **GitHub Pages**: Push to a gh-pages branch
- **Netlify**: Drag and drop the `web` folder
- **Vercel**: Connect your repository
- **Any static host**: Upload the `web` directory

No build process or server configuration needed!

## License

All books are in the public domain. The code and design are open source.
