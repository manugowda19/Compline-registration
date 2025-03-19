from flask import Flask, render_template, request, redirect, url_for

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()

app = Flask(__name__)

# Homepage Route
@app.route('/')
def home():
    return render_template('index.html')

# Complaint Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        name = request.form.get('name')
        email = request.form.get('email')
        complaint = request.form.get('complaint')
        
        # Save complaint to Firestore
        data = {
            "name": name,
            "email": email,
            "complaint": complaint
        }
        db.collection('complaints').add(data)

        return redirect(url_for('home'))  # Redirect back to homepage
    return render_template('register.html')

# View Complaints Route
@app.route('/view_complaints')
def view_complaints():
    # Fetch data from Firestore
    complaints_ref = db.collection('complaints').stream()
    complaints = [complaint.to_dict() for complaint in complaints_ref]

    return render_template('view_complaints.html', complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)