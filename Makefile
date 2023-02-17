.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: data
data:
	echo "Gen Data"

.PHONY: groups
groups: 
	python main_process.py create_groups

.PHONY: clean
clean:
	python main_process.py delete_groups