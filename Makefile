.PHONY: up resume backend lazyboard

up:
	@echo "Starting services..."
	@make -j2 resume backend

resume:
	@echo "Starting Vite dev server..."
	@cd resume && npm run dev

backend:
	@echo "Starting Flask backend..."
	source ./.venv/bin/activate && cd backend && python app.py

board:
	@echo "Starting lazyboard..."
	source ./.venv/bin/activate && cd lazyboard && PYTHONPATH=. python -m src

db:
	sqlite3 lazyboard/db/jobs.db

rmdb:
	@rm lazyboard/db/jobs.db
