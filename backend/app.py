from functions.views import create_app # Changed back to absolute import

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
