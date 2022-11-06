from communere.assignment.core.api import create_flask_app

app = create_flask_app()
app.container.wire(packages=['communere.assignment'])
app.container.db().setup()

if __name__ == '__main__':
    app.run()
