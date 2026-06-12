lock:
	cp .env.local .env
dock: 
	cp .env.docker .env
up:
	docker compose up
migrate-test:
	DATABASE_URL=postgresql+psycopg2://todo_user:password@localhost:5433/todo_test_db alembic upgrade head