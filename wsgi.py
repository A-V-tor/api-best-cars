from api_best_cars import create_app


app = create_app()
client = app.test_client()


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
