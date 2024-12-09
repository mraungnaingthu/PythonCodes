#For Huawei New Installation Sites to configure

import paramiko
import time
import sys

print("\n")
print("   ********** Welcome From Provisioning Automation Team **********")
print("\n")
print("_" * 70)

olt = input("OLT: ")
ip_address = {"olt1": "x.x.x.x", "olt2": "x.x.x.x", "olt3": "x.x.x.x"}
ip = ip_address[olt.lower()]

try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username='oltUsername', password='oltPassword')
    shell = ssh_client.invoke_shell()

    commands = [
        'enable\n',
        'config\n',
        'display ont autofind all\n',
        ' '
        '\n',
    ]

    for command in commands:
        shell.send(command)
        time.sleep(1)  # Adjust sleep time if needed
        while not shell.recv_ready():
            pass
        output = shell.recv(65535).decode('utf-8')
        print(output)


    #Checking the serial OK or Not
    myCheck = input('sn found? (y/n): ')
    if myCheck == 'y':
        pass
    elif myCheck == 'n':
        sys.exit()

    f = int(input("frame: "))
    s = int(input("slot: "))
    p = int(input("port: "))
    vlan = int(input("vlan: "))
    pppoe_id = input("PPPOE ID: ")


    # For Eco, EcoPlus, ATS users
    if vlan == 1116:
        commands = [
            ' \n'
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 1 ont-srvprofile-id 10\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [  # 'quit\n',
            f'service-port vlan 1116 gpon {f}/{s}/{p} ont {ont_id} gemport 2 multi-service user-vlan 1116 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")


    # For Eco, EcoPlus, ATS users
    elif vlan == 1113:
        commands = [
            f'\n',
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 14 ont-srvprofile-id 14\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [  f'\n',
            f'service-port vlan 1113 gpon {f}/{s}/{p} ont {ont_id} gemport 1 multi-service user-vlan 1113 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")


    #For Eco, EcoPlus, ATS users
    elif vlan == 1103:
        commands = [
            f'\n',
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 10 ont-srvprofile-id 10\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [  # 'quit\n',
            f'service-port vlan 1103 gpon {f}/{s}/{p} ont {ont_id} gemport 1 multi-service user-vlan 1103 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")


    #For XSplus to XL Users
    elif vlan == 1114:
        commands = [
            f'\n',
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 2 ont-srvprofile-id 10\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [  # 'quit\n',
            f'service-port vlan 1114 gpon {f}/{s}/{p} ont {ont_id} gemport 2 multi-service user-vlan 1114 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")


    #For XS Plan
    elif vlan ==1117:
        commands = [
            f'\n',
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 1 ont-srvprofile-id 10\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [  f'\n',
            f'service-port vlan 1117 gpon {f}/{s}/{p} ont {ont_id} gemport 3 multi-service user-vlan 1117 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")


    #For XXSplus Plan
    elif vlan == 1115:
        commands = [
            f'\n',
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 1 ont-srvprofile-id 10\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [#'quit\n',
                        f'service-port vlan 1115 gpon {f}/{s}/{p} ont {ont_id} gemport 1 multi-service user-vlan 1115 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
                        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")


    elif vlan == 1112:
        answer = input("route mode? (y/n) : ")
        if answer == 'y':
            #Business Plan >> Route Mode to configure onu
            commands = [
                f'\n',
                f'int gpon {f}/{s}\n',
                f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 2 ont-srvprofile-id 10\n\n',
                'quit\n',
            ]

            for command in commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            ont_id = int(input("ont id: "))
            new_commands = [  f'\n',
                f'service-port vlan 1112 gpon {f}/{s}/{p} ont {ont_id} gemport 1 multi-service user-vlan 1112 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
            ]
            for command in new_commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            print(">>> Configuration Done! <<<")
            print("\n")

        #Business Plan >> Bridge Mode to configure onu
        elif answer == 'n':
            commands = [
                f'\n',
                f'int gpon {f}/{s}\n',
                f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 2 ont-srvprofile-id 10\n\n',
                'quit\n',
            ]

            for command in commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            ont_id = int(input("ont id: "))
            new_commands = [  # 'quit\n',
                f'service-port vlan 1112 gpon {f}/{s}/{p} ont {ont_id} gemport 1 multi-service user-vlan 1112 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
                f'int gpon {f}/{s}\n',
                f'ont port native-vlan {p} {ont_id} eth 1 vlan 1112 priority 0\n',
            ]
            for command in new_commands:
                shell.send(command)
                time.sleep(1)  # Adjust sleep time if needed
                while not shell.recv_ready():
                    pass
                output = shell.recv(65535).decode('utf-8')
                print(output)

            print(">>> Configuration Done! <<<")
            print("\n")

    #For Prepaid Plan
    elif vlan == 1118:
        commands = [
            f'\n',
            f'int gpon {f}/{s}\n',
            f'ont add {p} password-auth {pppoe_id} always-on omci ont-lineprofile-id 2 ont-srvprofile-id 10\n\n',
            'quit\n',
        ]

        for command in commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        ont_id = int(input("ont id: "))
        new_commands = [  # 'quit\n',
            f'service-port vlan 1118 gpon {f}/{s}/{p} ont {ont_id} gemport 3 multi-service user-vlan 1118 tag-transform translate inbound traffic-table index 6 outbound traffic-table index 6\n',
        ]
        for command in new_commands:
            shell.send(command)
            time.sleep(1)  # Adjust sleep time if needed
            while not shell.recv_ready():
                pass
            output = shell.recv(65535).decode('utf-8')
            print(output)

        print(">>> Configuration Done! <<<")
        print("\n")

    else:
        print(">>> You typed the wrong vlan! Please try again... <<<")

    while True:
        print('\n')
        ipCheck = input('Want to check IP? (y/n): ')
        if ipCheck == 'y':
            ipcheck_commands = [
                ' \n'
                f'display ont wan-info {f}/{s} {p} {ont_id}\n',
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