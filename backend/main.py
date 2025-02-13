from sazonAI import create_app

app = create_app()

@app.route("/")
def test():
    return "hola mundo"

if __name__ == "__main__":
    app.run()
