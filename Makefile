.PHONY: all
all: install executable

.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: data
data: install
	echo "Gen Data"

.PHONY: groups
groups: install
	python .\small_groups_creator.py create_groups

.PHONY: clean
clean: install
	python .\small_groups_creator.py delete_groups

.PHONY: executable
executable:
	pyinstaller --onefile --icon=daystar_logo.ico --windowed --clean .\small_groups_creator.py .\src\main_process.py .\src\group_manager.py .\src\planning_center_bot.py
	echo "Executable located at ./dist/small_groups_creator.exe"
