import subprocess

from config import ABSOLUTE_PROJECT_PATH


def encrypt_integration_key(integration_key):
    if integration_key:
        # Run shell command to encrypt integration key
        command = f"make encode_routing_key ROUTING_KEY={integration_key}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=ABSOLUTE_PROJECT_PATH)
        output, error = process.communicate()

        if process.returncode == 0:
            encrypted_key = output.decode().split()[-1]
        else:
            print("Error:", error.decode())
            encrypted_key = None
    else:
        encrypted_key = None
    return encrypted_key
