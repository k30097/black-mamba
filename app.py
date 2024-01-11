from aph import create_app

app = create_app()

# the app starts when this file is run
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)