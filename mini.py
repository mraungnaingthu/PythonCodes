#For ZTE Mini New Installation Sites to configure

import paramiko
import time
import sys

olt = input("OLT: ")
ip_address = {"olt1": "x.x.x.x", "olt2": "x.x.x.x", "olt3": "x.x.x.x"}
ip = ip_address[olt.lower()]

try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username='oltUsername', password='oltPassword')
    shell = ssh_client.invoke_shell()

    commands = [
        # 'enable\n',
        'conf t\n',
        'show pon onu uncfg\n',
    ]

    for command in commands:
        shell.send(command)
        time.sleep(1)  # Adjust sleep time if needed
        while not shell.recv_ready():
            pass
        output = shell.recv(65535).decode('utf-8')
        print(output)

    myCheck = input('sn found? (y/n): ')
    if myCheck == 'y':
        pass

    else:
        sys.exit()

    s = int(input("slot: "))
    p = int(input("port: "))

    second_commands = [
            f'show gpon onu state gpon_olt-1/{s}/{p}\n',
            ' '
            '\n',
            ' '
            '\n'
        ]

    for command in second_commands:
        shell.send(command)
        time.sleep(1)  # Adjust sleep time if needed
        while not shell.recv_ready():
            pass
        output2 = shell.recv(65535).decode('utf-8')
        print(output2)

    sn = input("serial number: ")
    vlan = int(input("vlan: "))
    pppoe_id = input("PPPOE ID: ")
    pppoe_psw = input("PPPOE PSW: ")
    ont_id = int(input("ont id: "))

    third_commands = [
            f'interface gpon_olt-1/{s}/{p}\n',
            f'onu {ont_id} type ZXHN-F600W sn {sn}\n',
            'exit\n\n',
            f'interface gpon_onu-1/{s}/{p}:{ont_id}\n',
            f'name {pppoe_id}\n',
            'tcont 1 name HSI profile HSI-1000M\n',
            'gemport 1 name HSI tcont 1\n',
            'exit\n\n',
            f'int vport-1/{s}/{p}.{ont_id}:1\n',
            f'service-port 1 user-vlan {vlan} vlan {vlan}\n',
            'exit\n\n',
            f'pon-onu-mng gpon_onu-1/{s}/{p}:{ont_id}\n',
            f'service 1 gemport 1 vlan {vlan}\n',
            f'wan-ip 1 ipv4 mode pppoe username {pppoe_id} password {pppoe_psw} vlan-profile HSI-{vlan} host 1\n',
            'wan 1 service internet host 1 pppoe connect always\n',
            'exit\n',
            '\n',
        ]

    for command in third_commands:
        shell.send(command)
        time.sleep(1)  # Adjust sleep time if needed
        while not shell.recv_ready():
            pass
        output3 = shell.recv(65535).decode('utf-8')
        print(output3)

    print('Configuration Done!')

    while True:
        print('\n')
        ipCheck = input('Want to check IP? (y/n): ')
        if ipCheck == 'y':
            ipcheck_commands = [
                ' \n'
                f'show gpon remote-onu ip-host gpon-onu_1/{s}/{p}:{ont_id}\n',
            ]

            try:
                for command in ipcheck_commands:
                    shell.send(command)
                    time.sleep(1)  # Adjust sleep time if needed
                    while not shell.recv_ready():
                        pass
                    output = shell.recv(65535).decode('utf-8')
                    print(output)

            except Exception as e:
                print(f'An error occurred: {str(e)}')

        elif ipCheck == 'n':
            ssh_client.close()
            break


except paramiko.AuthenticationException as auth_err:
    print(f"Authentication failed: {auth_err}")

except paramiko.SSHException as ssh_err:
    print(f"SSH connection failed: {ssh_err}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    ssh_client.close()  # Close the SSH connection