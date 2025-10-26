.PHONY: up dev backend

up:
	@echo "Starting services..."
	@make -j2 resume backend

resume:
	@echo "Starting Vite dev server..."
	@cd src/resume && npm run dev

backend:
	@echo "Starting Flask backend..."
	@cd src && source ./.venv/bin/activate && cd backend && python app.py

scraper:
	@echo "Starting scraper..."
	@cd src && source ./.venv/bin/activate && PYTHONPATH=. python -m scraper.scrape

app:
	@echo "Starting app..."
	@cd src && source ./.venv/bin/activate && PYTHONPATH=. python -m app.main

db:
	sqlite3 src/db/jobs.db
