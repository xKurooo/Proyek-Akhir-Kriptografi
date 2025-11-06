# run.py
from web_kripto_keyvera import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)