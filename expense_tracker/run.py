from app import create_app

app = create_app()

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run()
