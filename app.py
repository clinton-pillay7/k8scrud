from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

# Database configuration from environment variables
DB_HOST = os.environ.get('DB_HOST', 'mysql-service')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'contactsdb')
DB_USER = os.environ.get('DB_USER', 'flaskuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'flaskpassword')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }


# Initialize database tables
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"DB init error (will retry): {e}")


# ── UI ──────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ── API ─────────────────────────────────────────────────────────────────────

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([c.to_dict() for c in contacts]), 200


@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact.to_dict()), 200


@app.route('/api/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    required = ['name', 'phone', 'address']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    contact = Contact(
        name=data['name'].strip(),
        phone=data['phone'].strip(),
        address=data['address'].strip()
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact.to_dict()), 201


@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    if 'name' in data:
        contact.name = data['name'].strip()
    if 'phone' in data:
        contact.phone = data['phone'].strip()
    if 'address' in data:
        contact.address = data['address'].strip()

    db.session.commit()
    return jsonify(contact.to_dict()), 200


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': f'Contact {contact_id} deleted'}), 200


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
