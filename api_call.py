import requests

from config import PD_API_TOKEN

SERVICES_ENDPOINT = "https://api.pagerduty.com/services"


def get_all_services():
    headers = {
        "Authorization": f"Token token={PD_API_TOKEN}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    services = []
    more = True
    offset = 0

    while more:
        params = {"limit": 100, "offset": offset}
        response = requests.get(SERVICES_ENDPOINT, headers=headers, params=params)
        data = response.json()
        services.extend(data["services"])
        more = data["more"]
        offset += len(data["services"])

    return services


def get_integration_key(service_id, integration_id):
    headers = {
        "Authorization": f"Token token={PD_API_TOKEN}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    url = f"{SERVICES_ENDPOINT}/{service_id}/integrations/{integration_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["integration"]["integration_key"]