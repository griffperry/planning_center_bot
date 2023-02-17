.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: data
data:
	echo "Gen Data"

.PHONY: groups
groups: 
	python src/main_process.py create_groups

.PHONY: clean
clean:
	python src/main_process.py delete_groups