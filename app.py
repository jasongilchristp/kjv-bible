from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load Bible data with uppercase columns
def load_bible_data():
    df = pd.read_csv('data/kjv.csv')
    return df

# Add Testament column manually
def add_testament_column(df):
    # Define Old Testament books (sample, you should adjust according to your data)
    old_testament_books = [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 
        'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
        'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 
        'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 
        'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
        'Haggai', 'Zechariah', 'Malachi'
    ]
    
    # Define New Testament books (sample, you should adjust according to your data)
    new_testament_books = [
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 
        'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', 
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', 
        '1 John', '2 John', '3 John', 'Jude', 'Revelation'
    ]
    
    # Add Testament column based on book names
    df['Testament'] = df['Book'].apply(lambda x: 'Old' if x in old_testament_books else 'New' if x in new_testament_books else None)
    return df

# Get Old Testament books
def get_old_testament_books():
    df = load_bible_data()
    df = add_testament_column(df)  # Add the Testament column
    old_testament = df[df['Testament'] == 'Old']['Book'].unique()
    return old_testament

# Get New Testament books
def get_new_testament_books():
    df = load_bible_data()
    df = add_testament_column(df)  # Add the Testament column
    new_testament = df[df['Testament'] == 'New']['Book'].unique()
    return new_testament

# Get list of unique books
def get_books():
    df = load_bible_data()
    return df['Book'].unique()

# Get chapters for a specific book
def get_chapters(book):
    df = load_bible_data()
    return df[df['Book'] == book]['Chapter'].unique()

# Get verses for a specific book and chapter
def get_verses(book, chapter):
    df = load_bible_data()
    return df[(df['Book'] == book) & (df['Chapter'] == chapter)]

# Search through all verses
def search_verses(query):
    df = load_bible_data()
    return df[df['Text'].str.contains(query, case=False)]

# Route definitions
@app.route('/')
def index():
    old_books = get_old_testament_books()
    new_books = get_new_testament_books()
    return render_template('index.html', old_testament_books=old_books, new_testament_books=new_books)

@app.route('/book/<string:book>/chapters')
def chapters(book):
    chapters_list = get_chapters(book)
    return render_template('chapter.html', book=book, chapters=chapters_list)

@app.route('/book/<string:book>/chapter/<int:chapter>')
def verses(book, chapter):
    verses_df = get_verses(book, chapter)
    if verses_df.empty:
        return render_template('404.html'), 404
    verses = verses_df.to_dict('records')
    return render_template('verses.html', book=book, chapter=chapter, verses=verses)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results_df = search_verses(query)
        results = results_df.to_dict('records')
        return render_template('search.html', results=results, query=query)
    return redirect(url_for('index'))

@app.route('/old-testament')
def old_testament():
    books = get_old_testament_books()
    print(books)  # Check data in the console
    return render_template('old_testament.html', old_testament_books=books)

@app.route('/new-testament')
def new_testament():
    books = get_new_testament_books()
    print(books)  # Check data in the console
    return render_template('new_testament.html', new_testament_books=books)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
