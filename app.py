from flask import Flask,request, jsonify
import mysq.connector

app= FLask(__name__)

db = mysql.connector.connect(
    host = "localhost",
    user='root',
    password="",
    database='flip_db'
)
@app.route('/register_user', methods=['POST'])

def register_user():
    data = request.json
    cursor=db.cursor()
    cursor.execute("INSERT INTO users (username,email,skills,positions) VALUES(%s,%s,%s,%s)",(data['username'],data['email'],data['skills'],data['positions']))
    db.commit()
    return jsonify({"message": "User registered successfully!"}),201

@app.route('/post_vacancy',methods=['POST'])

def post_vacancy():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO vacancies (company_id, title, description, skills_required) VALUES (%s, %s, %s, %s)", (data['company_id'], data['title'], data['description'], data['skills_required']))
    db.commit()
    return jsonify("message":"Vacancy posted successfully!"}),201

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT skills, positions FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    cursor.execute("""
        SELECT v.id, v.title, v.description, v.skills_required
        FROM vacancies v
        WHERE MATCH(v.skills_required) AGAINST (%s IN NATURAL LANGUAGE MODE)
    """, (user['skills'],))
    
    recommendations = cursor.fetchall()
    
    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(debug=True)