.PHONY: up dev backend

up:
	@echo "Starting services..."
	@make -j2 dev backend

dev:
	@echo "Starting Vite dev server..."
	@cd src/resume && npm run dev

backend:
	@echo "Starting Flask backend..."
	@cd src/backend && source ./.venv/bin/activate && python app.py
