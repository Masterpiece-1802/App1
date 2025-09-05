import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('shayari.db')
    c = conn.cursor()

    # Create posts table
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 content TEXT NOT NULL,
                 date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 theme TEXT DEFAULT 'default',
                 tags TEXT)''')

    conn.commit()
    conn.close()

def add_post(content, theme='default', tags=''):
    conn = sqlite3.connect('shayari.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (content, theme, tags) VALUES (?, ?, ?)',
              (content, theme, tags))
    conn.commit()
    conn.close()

def get_all_posts(theme_filter='', tag_filter='', sort_by='date_desc'):
    conn = sqlite3.connect('shayari.db')
    c = conn.cursor()
    
    # Build query with filters
    query = 'SELECT * FROM posts'
    params = []
    
    conditions = []
    if theme_filter:
        conditions.append('theme = ?')
        params.append(theme_filter)
    if tag_filter:
        conditions.append('tags LIKE ?')
        params.append(f'%{tag_filter}%')
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    # Add sorting
    if sort_by == 'date_asc':
        query += ' ORDER BY date_created ASC'
    elif sort_by == 'date_desc':
        query += ' ORDER BY date_created DESC'
    elif sort_by == 'theme':
        query += ' ORDER BY theme, date_created DESC'
    
    c.execute(query, params)
    posts = c.fetchall()
    conn.close()
    return posts

def search_posts(query, theme_filter='', tag_filter='', sort_by='date_desc'):
    conn = sqlite3.connect('shayari.db')
    c = conn.cursor()
    
    # Build query with filters
    sql_query = '''SELECT * FROM posts 
                   WHERE (content LIKE ? OR tags LIKE ?)'''
    params = [f'%{query}%', f'%{query}%']
    
    if theme_filter:
        sql_query += ' AND theme = ?'
        params.append(theme_filter)
    if tag_filter:
        sql_query += ' AND tags LIKE ?'
        params.append(f'%{tag_filter}%')
    
    # Add sorting
    if sort_by == 'date_asc':
        sql_query += ' ORDER BY date_created ASC'
    elif sort_by == 'date_desc':
        sql_query += ' ORDER BY date_created DESC'
    elif sort_by == 'theme':
        sql_query += ' ORDER BY theme, date_created DESC'
    
    c.execute(sql_query, params)
    posts = c.fetchall()
    conn.close()
    return posts

# Initialize the database when this module is imported
init_db()