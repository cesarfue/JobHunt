.PHONY: up resume backend lazyboard

up:
	@echo "Starting services..."
	@make -j2 resume backend

resume:
	@echo "Starting Vite dev server..."
	@cd resume && npm run dev

backend:
	@echo "Starting Flask backend..."
	@cd backend && source ./.venv/bin/activate && python app.py

board:
	@echo "Starting lazyboard..."
	@cd lazyboard && source ./.venv/bin/activate && PYTHONPATH=. python -m app.main

db:
	sqlite3 lazyboard/db/jobs.db

rmdb:
	@rm lazyboard/db/jobs.db
