import pandas


class DataGenerator():

    def verify_data(self, data):
        print(f"Verify {data}")
        return True

    def submit_data(self, data):
        success = self.verify_data(data)
        return success
