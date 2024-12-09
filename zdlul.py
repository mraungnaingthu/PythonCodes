import paramiko
import time
import sys

print("\n")
print("Welcome From Provisioning Automation Team")
print("\n")
print("_" * 70)

print('\n')
print("Check IP, Power and ont reset ?      >>> Press 1: ")
print("Check IP, Remote Access Enable ?     >>> Press 2: ")
print("Check Service Port and Delete ONU ?  >>> Press 3: ")
print("Factory Restore to the ONU ?         >>> Press 4: ")
#print("Check Wifi Username ?                >>> Press 5: ")
print("\n")

condition = int(input("what do you want to do: "))

sn = input("serial number: ")
olt = input("OLT: ")

ip_address = {"olt1": "x.x.x.x", "olt2": "x.x.x.x", "olt3": "x.x.x.x"}
ip = ip_address[olt.lower()]


try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username='oltUsername', password='oltPassword')
    shell = ssh_client.invoke_shell()

    commands = [
        'con t\n',
        f'show gpon onu by sn {sn}\n',
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

s = input("slot: ")
p = input("port: ")
ont_id = input("ont id: ")

if condition == 1:
    commands = [
        f'show gpon remote-onu ip-host gpon-onu_1/{s}/{p}:{ont_id}\n',
        ' '
        ' \n',
        f'show pon power attenuation gpon-onu_1/{s}/{p}:{ont_id}\n',
        ' '
        ' \n',
        f'show gpon onu state gpon-olt_1/{s}/{p} {ont_id}\n',
    ]

    try:
        for command in commands:
            shell.send(command)
            time.sleep(3)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        result = input("ip ok, power ok? (y/n): ")
        if result == 'y':
            first_commands = [
                f'pon-onu-mng gpon-onu_1/{s}/{p}:{ont_id}\n',
                'reboot\n',
                'y\n'
            ]

            for command in first_commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output1 = shell.recv(65535).decode('utf-8')
                print(output1)

            print("onu is successfully rebooted!")

        else:
            print("onu is abnormal!")

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


elif condition == 2:
    commands = [
        f'show gpon remote-onu ip-host gpon-onu_1/{s}/{p}:{ont_id}\n',
        ' '
        ' \n',
        f'show pon power attenuation gpon-onu_1/{s}/{p}:{ont_id}\n',
        f'pon-onu-mng gpon-onu_1/{s}/{p}:{ont_id}\n',
        'security-mgmt 1 state e i w m f\n',
    ]

    try:
        for command in commands:
            shell.send(command)
            time.sleep(3)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print("remote access is already enabled!")

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


elif condition == 3:
    commands = [
        f'int gpon-onu_1/{s}/{p}:{ont_id}\n',
        'show this\n',
        'exit\n'
        f'show onu running config gpon-onu_1/{s}/{p}:{ont_id}\n',
    ]

    try:
        for command in commands:
            shell.send(command)
            time.sleep(3)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()

    double_check = input("do you want to delete onu? (y/n): ")

    if double_check == 'y':
        try:
            second_commands = [
                f'int gpon-olt_1/{s}/{p}\n',
                f'no onu {ont_id}\n',
            ]

            for command in second_commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            print("ont is successfully deleted!")

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            sys.exit()

    else:
        sys.exit()


elif condition == 4:
    commands = [
        f'pon-onu-mng gpon-onu_1/{s}/{p}:{ont_id}\n',
        ' '
        ' \n',
        f'restore factory\n',
    ]

    try:
        for command in commands:
            shell.send(command)
            time.sleep(3)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print("ont is already factory restored!")

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit()


else:
    sys.exit()


ssh_client.close()
