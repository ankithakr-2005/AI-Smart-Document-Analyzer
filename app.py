import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from database import init_db, get_db
from ai_pipeline import process_and_vectorize_pdf, query_rag_pipeline

app = Flask(__name__)
app.secret_key = "super_secret_ai_analyzer_key"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

init_db()

@app.route('/')
def index():
    conn = get_db()
    documents = conn.execute("SELECT * FROM documents ORDER BY upload_date DESC").fetchall()
    conn.close()
    return render_template('index.html', documents=documents)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['pdf_file']
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO documents (filename) VALUES (?)", (filename,))
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()

        process_and_vectorize_pdf(file_path, doc_id)
        return redirect(url_for('chat', doc_id=doc_id))
    
    return redirect(url_for('index'))

@app.route('/chat/<int:doc_id>', methods=['GET', 'POST'])
def chat(doc_id):
    conn = get_db()
    document = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    
    if not document:
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_question = request.form.get('question')
        if user_question:
            ai_answer = query_rag_pipeline(doc_id, user_question)
            conn.execute(
                "INSERT INTO chat_history (document_id, question, answer) VALUES (?, ?, ?)",
                (doc_id, user_question, ai_answer)
            )
            conn.commit()
            return redirect(url_for('chat', doc_id=doc_id))

    history = conn.execute(
        "SELECT * FROM chat_history WHERE document_id = ? ORDER BY timestamp ASC", 
        (doc_id,)
    ).fetchall()
    conn.close()
    
    return render_template('chat.html', document=document, history=history)

if __name__ == '__main__':
    app.run(debug=True)