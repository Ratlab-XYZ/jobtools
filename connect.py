import subprocess




def ssh_connect(username: str, password):
    # Extract cluster name (everything before the first underscore)
    cluster = username.split('_')[0]

    #print(f"Username: {username}")
    #print(f"Cluster: {cluster}")
    ssh_command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@ssh.{cluster}.service.one"
    #print(f"SSH Command: {ssh_command}")

    # Run SSH command
    subprocess.run(ssh_command, shell=True)
