.PHONY: all
all: install data executable

.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: data
data:
	echo "Gen Data"

.PHONY: groups
groups: install data
	python .\small_groups_creator.py create_groups

.PHONY: clean
clean: install data
	python .\small_groups_creator.py delete_groups

.PHONY: executable
executable:
	pyinstaller --onefile .\small_groups_creator.py .\src\main_process.py .\src\group_manager.py .\src\planning_center_bot.py
	echo "Executable located at ./dist/small_groups_creator.exe"
