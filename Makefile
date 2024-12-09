
VENV_DIR=venv
REQUIREMENTS=requirements.txt
BOT_SCRIPT=main.py
PYTHON_BIN=python3.12

.PHONY: help venv install run clean

help:
	@echo "Доступные команды:"
	@echo "  make venv       - Создать виртуальное окружение."
	@echo "  make install    - Установить зависимости в виртуальное окружение."
	@echo "  make run        - Запустить бота."
	@echo "  make clean      - Удалить виртуальное окружение и временные файлы."

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
	    $(PYTHON_BIN) -m venv $(VENV_DIR); \
	    echo "[INFO] Виртуальное окружение создано с использованием $(PYTHON_BIN)"; \
	else \
	    echo "[INFO] Виртуальное окружение уже существует"; \
	fi

install: venv
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)
	@echo "[INFO] Все зависимости установлены"

run: venv
	@$(VENV_DIR)/bin/python $(BOT_SCRIPT)

clean:
	@rm -rf $(VENV_DIR) __pycache__ *.pyc *.pyo
	@echo "[INFO] Виртуальное окружение и временные файлы удалены"
