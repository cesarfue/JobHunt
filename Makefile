.PHONY: up resume pdf

resume:
	@echo "Starting Vite dev server..."
	@cd resume && npm run dev

pdf:
	@cd resume && npm run pdf $(if $(OUTPUT),$(OUTPUT),~/Downloads/CV_César_Fuentes.pdf)
