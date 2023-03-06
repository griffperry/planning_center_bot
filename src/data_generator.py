import pandas


class DataGenerator():
    def __init__(self):
        self.valid = False  # default

    def verify_data(self, data):
        print(f"Verify {data}")
        if True:
            self.valid = True

    def submit_data(self, data):
        # data: string (filepath to excel)
        self.verify_data(data)
        return self.valid
