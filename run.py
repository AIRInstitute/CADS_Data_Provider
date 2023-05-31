from app import create_app, db
import logging

logging.basicConfig(level=logging.DEBUG)
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
