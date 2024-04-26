import json


def get_all_services_mock():
    try:
        with open("mock-data.json", "r") as file:
            data = json.load(file)
            return data["services"]
    except FileNotFoundError:
        print("Mock file 'mock-data.json' not found.")
        return []


def get_integration_key_mock(service_id, integration_id):
    try:
        with open("mock-data.json", "r") as file:
            data = json.load(file)
            return data["integration"]["integration_key"]
    except FileNotFoundError:
        print("Mock file 'mock-data.json' not found.")
        return []