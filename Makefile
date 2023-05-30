.PHONY: all
all: install executable

.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: data
data: install
	python .\small_groups_manager.py gen_data

.PHONY: groups
groups: install
	python .\small_groups_manager.py create_groups

.PHONY: clean
clean: install
	python .\small_groups_manager.py delete_groups

.PHONY: executable
executable:
	pyinstaller --onefile --icon=daystar_logo.ico --windowed --clean .\small_groups_manager.py
	echo "Executable located at ./dist/small_groups_manager.exe"
