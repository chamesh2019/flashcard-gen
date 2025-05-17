from functions.views import create_app # Changed back to absolute import

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # Nginx will handle SSL and external port
