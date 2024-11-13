import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('sample.db')
cursor = conn.cursor()

# Create a table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS sample_table (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   age INTEGER)''')
conn.commit()

# Run a select query based on the given ID and return the result in a list
def select_by_id(id):
    cursor.execute('SELECT * FROM sample_table WHERE id=?', (id,))
    result = cursor.fetchone()
    return result if result else []

# Insert a new record
def insert_record(id, name, age):
    cursor.execute('INSERT INTO sample_table (id, name, age) VALUES (?, ?, ?)', (id, name, age))
    conn.commit()

# Update an existing record
def update_record(id, name, age):
    cursor.execute('UPDATE sample_table SET name=?, age=? WHERE id=?', (name, age, id))
    conn.commit()

# Delete a record
def delete_record(id):
    cursor.execute('DELETE FROM sample_table WHERE id=?', (id,))
    conn.commit()

# Example usage
insert_record(1, 'John Doe', 30)
print(select_by_id(1))
update_record(1, 'John Smith', 31)
print(select_by_id(1))
delete_record(1)
print(select_by_id(1))

# Close the connection
conn.close()