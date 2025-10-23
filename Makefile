.PHONY: up down dev backend clean

up:
	@echo "Starting services..."
	@make -j2 dev backend

dev:
	@echo "Starting Vite dev server..."
	@cd src/resume && npm run dev

backend:
	@echo "Starting Flask backend..."
	@cd src/backend && source ./.venv/bin/activate && python app.py

down:
	@echo "Stopping services..."
	@pkill -f "vite" || true
	@pkill -f "flask" || true
	@pkill -f "app.py" || true

clean:
	@echo "Cleaning up..."
	@rm -rf resume/node_modules
	@rm -rf resume/dist
	@rm -rf backend/__pycache__
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
