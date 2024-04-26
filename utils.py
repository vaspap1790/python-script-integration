from api_call import get_integration_key
from encrypt import encrypt_integration_key
from manipulate_yml import update_alertmanager, update_prometheus
from mocks import get_integration_key_mock


def filter_services_by_name(services):
    return [service for service in services if "flexibility" in service["name"].lower()]


def extract_environment(service_name):
    words = service_name.split(" - ")
    if len(words) >= 3:
        return "-".join(words[1:3])
    else:
        return "Unknown"


def extract_integration_key(is_mock, service):
    integrations = service["integrations"]
    integration_id = None
    for integration in integrations:
        if integration["summary"] == "Prometheus":
            integration_id = integration["id"]
            break
    if integration_id:
        integration_key = get_integration_key_mock(service["id"], integration_id) \
            if is_mock else get_integration_key(service["id"], integration_id)
    else:
        integration_key = None
    return integration_id, integration_key


def format_services(filtered_services, is_mock):
    formatted_services = []
    for service in filtered_services:

        integration_id, integration_key = extract_integration_key(is_mock, service)

        encrypted_key = encrypt_integration_key(integration_key)

        formatted_service = {
            "serviceId": service["id"],
            "serviceName": service["name"],
            "env": extract_environment(service["name"]),
            "integrationId": integration_id,
            "integrationKey": integration_key,
            "encryptedKey": encrypted_key
        }
        formatted_services.append(formatted_service)
    return formatted_services


def update_files(formatted_services):
    for service in formatted_services:
        if service["encryptedKey"]:
            update_alertmanager(service["env"], service["encryptedKey"])
            update_prometheus(service["env"])


def print_services(services):
    for service in services:
        print("Service ID:", service["serviceId"])
        print("Service Name:", service["serviceName"])
        print("Environment:", service["env"])
        print("Integration ID:", service["integrationId"])
        print("Integration Key:", service["integrationKey"])
        print("Encrypted Key:", service["encryptedKey"])
        print()