from api_call import get_all_services
from mocks import get_all_services_mock
from utils import filter_services_by_name, format_services, print_services, update_files

IS_MOCK = False


def main():
    pd_services = get_all_services_mock() if IS_MOCK else get_all_services()

    filtered_services = filter_services_by_name(pd_services)

    formatted_services = format_services(filtered_services, IS_MOCK)

    print_services(formatted_services)

    update_files(formatted_services)


if __name__ == "__main__":
    main()
