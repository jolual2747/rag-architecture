PYTHON := python3
CURRENT_DIR := $(shell pwd)

.PHONY: build_gradio_app

build_gradio_app:
	export PYTHONPATH=$(shell pwd):$$PYTHONPATH && poetry run python src/frontend/gradio_app.py

.PHONY: build_streamlit_app

build_streamlit_app:
	export PYTHONPATH=$(CURRENT_DIR):$$PYTHONPATH && poetry run streamlit run src/frontend/st_app.py