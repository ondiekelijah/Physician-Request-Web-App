def deploy():
	"""Run deployment tasks."""
	from main_app import create_app,bcrypt

	main_app = create_app()
	main_app.app_context().push()

	from models import User
	from main_app import db
	from flask_migrate import upgrade,migrate,init,stamp
	db.create_all()
	
	# migrate database to latest revision
	stamp()
	migrate()
	upgrade()
	
deploy()
	