.PHONY: launch backend frontend install test build

launch:
	@echo "Anvil of Taylor baslatiliyor..."
	@$(MAKE) -j2 backend frontend

backend:
	python -m uvicorn server.main:app --reload --port 8000

frontend:
	cd web && npm run dev

install:
	pip install -e ".[dev,viz,latex,notebook]"
	cd web && npm install

test:
	pytest tests/ -v --tb=short

build:
	cd web && npm run build
