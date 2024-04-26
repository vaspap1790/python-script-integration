from config import ABSOLUTE_PROJECT_PATH


def update_alertmanager(env, encrypted_key):
    file_path = f"{ABSOLUTE_PROJECT_PATH}/appGroup-config/retailer/platformConfiguration/alertmanager/{env}/alertmanager.yml"

    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        route_written = False
        route_found = False
        match_found = False
        receivers_written = False
        pagerduty_configs_found = False

        for line in lines:
            if "receiver:" in line and not route_written:
                line = line.replace(line.split(":")[1].strip(), f"squids-pd-{env}")
                route_written = True

            if "match:" in line and not route_found:
                route_found = True

            if route_found and not match_found and "receiver:" in line:
                line = f"        receiver: {env.replace('-', '_')}\n"
                match_found = True

            if "name:" in line and not receivers_written:
                line = line.replace(line.split(":")[1].strip(), f"squids-pd-{env}")
                receivers_written = True

            if "routing_key:" in line and not pagerduty_configs_found:
                line = line.replace(line.split(":")[1].strip(), encrypted_key)
                pagerduty_configs_found = True

            file.write(line)


def update_prometheus(env):
    file_path = f"{ABSOLUTE_PROJECT_PATH}/appGroup-config/retailer/platformConfiguration/prometheus/{env}/rules.yml"
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        with open(file_path, "w") as file:
            in_rule = False
            for line in lines:
                if "rules:" in line:
                    in_rule = True
                if in_rule and "receiver:" in line:
                    # Update the receiver label within the labels section without extra space
                    updated_line = line.replace(line.split(":")[1].strip(), f"{env.replace('-', '_')}")
                    file.write(updated_line)
                else:
                    file.write(line)
    except FileNotFoundError:
        print(f"Prometheus rules file not found for environment: {env}")

