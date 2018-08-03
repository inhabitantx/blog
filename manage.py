import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),  '..')))


from flask_script import Manager, Server
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand



from blogapp.app import create_app, db

app = create_app('dev')

manager = Manager(app)

migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '127.0.0.1'),
    port = int(os.getenv('PORT', 5000))

    )
)

if __name__ == '__main__':
    manager.run()
