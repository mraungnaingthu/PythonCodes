import paramiko
import time
import sys

olt = input("OLT: ")
print("\n")
ip_address = {"olt1": "x.x.x.x", "olt2": "x.x.x.x", "olt3": "x.x.x.x"}
ip = ip_address[olt.lower()]

print("Check IP, Power and ont reset ?      >>> Press 1: ")
print("Check IP, Remote Access Enable ?     >>> Press 2: ")
print("Check Configuration and Delete ONU ? >>> Press 3: ")
print("Factory Restore to the ONU ?         >>> Press 4: ")
print("Check Wifi Username ?                >>> Press 5: ")
print("\n")
condition = int(input("what do you want to do: "))
sn = input("serial number: ")

try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username='oltUsername', password='oltPassword')
    shell = ssh_client.invoke_shell()

    commands = [
        'enable\n',
        'config\n',
        f'display ont info by-sn {sn}\n',
        f'\n\n\n\n\n\n',
        f'\n',
        f'\n',
    ]

    for command in commands:
        shell.send(command)
        time.sleep(1)  # Adjust sleep time if needed
        while not shell.recv_ready():
            pass
        output = shell.recv(65535).decode('utf-8')
        print(output)

except paramiko.SSHException as e:
    print(f"SSH Connection failed: {e}")

myCheck = input('info found? (y/n): ')
if myCheck == 'y':
    pass
elif myCheck == 'n':
    sys.exit()

f = input("frame: ")
s = input("slot: ")
p = input("port: ")
ont_id = input("ont id: ")

if condition == 1:
    first_commands = [
        'config\n',
        ' \n'
        f'interface gpon {f}/{s}\n',
        f'display ont wan-info {p} {ont_id}\n',
        'config\n'
        f'display ont optical-info {p} {ont_id}\n',
        ' \n'
        f'display ont alarm-state {p} {ont_id}\n',
        ' \n'
        'quit\n'
        f'display current-configuration ont {f}/{s}/{p} {ont_id}\n',
    ]

    try:
        for command in first_commands:
            shell.send(command)
            time.sleep(3)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        result = input("ip ok, power ok? (y/n): ")
        if result == 'y':
            second_commands = [
                f'int gpon {f}/{s}\n',
                ' '
                '\n',
                f'ont reset {p} {ont_id}\n',
                'y\n'
            ]

            for command in second_commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            print("onu is successfully rebooted!")

        else:
            print("onu is abnormal")

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


elif condition == 2:
    first_commands = [
        'config\n',
        ' '
        ' \n',
        f'display ont wan-info {f}/{s} {p} {ont_id}\n',
        ' '
        ' \n',
        'diagnose\n',
        f'ont wan-access http {f}/{s}/{p} {ont_id} enable\n',
    ]

    try:
        for command in first_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print("remote access is already enabled!")

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


elif condition == 3:
    first_commands = [
        'config\n',
        ' '
        '\n',
        f'display service-port port {f}/{s}/{p} ont {ont_id}\n\n\n',
    ]

    try:
        for command in first_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        srv_port = int(input("service port: "))
        double_check = input("do you want to delete onu? (y/n): ")

        if double_check == 'y':
            second_commands = [
                f'undo service-port {srv_port}\n',
                f'int gpon {f}/{s}\n',
                f'ont delete {p} {ont_id}\n',
            ]

            for command in second_commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            print("ont is successfully deleted!")

        else:
            sys.exit()

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


elif condition == 4:
    first_commands = [
        f'int gpon {f}/{s}',
        f'ont factory-setting-restore {p} {ont_id}',
    ]

    try:
        for command in first_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print("ont is already factory restored!")

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


elif condition == 5:
    first_commands = [
        'config',
        ' '
        '\n',
        f'int gpon {f}/{s}',
        ' '
        '\n',
        f'display ont wlan-info {p} {ont_id}',
        ' '
        '\n',
    ]

    try:
        for command in first_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()

ssh_client.close()
