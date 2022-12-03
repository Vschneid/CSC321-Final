from kivy.app import App
from kivy.uix.label import Label
import pyfiglet
import sys
import socket
from datetime import datetime

class App(App):
    def build(self):
        return Label(text="WARNING!\nPort {} was just opened on your machine.\n".format(new_port)
                        + "Did you start this running process?\n"
                        + "{}".format(banner))

def popup():
    app = App()
    app.run()
  

def get_banner(addr, port):
    '''Connect to process and return application banner'''
    print("Getting service information for port: ", port)
    socket.setdefaulttimeout(2)
    bannergrabber = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        bannergrabber.connect((addr, port))
        bannergrabber.send('WhoAreYou\r\n')
        banner = bannergrabber.recv(100)
        bannergrabber.close()
        print(banner, "\n")
    except:
        print("Cannot connect to port ", port)

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)
  
# Defining a target
if len(sys.argv) == 2:
     
    # translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of Argument")
 
# Add Banner
print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)

new_port = ''
banner = ''
init_ports = []
first_pass = True
flg = True
while(flg == True):
    try:
        # will scan ports between 1 to 65,535
        for port in range(1,65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
            # returns an error indicator
            result = s.connect_ex((target,port))
            if result == 0:
                chk = port in init_ports
                if(first_pass == False and chk == False):
                    get_banner(target, port)
                    new_port = port
                    popup()
                get_banner(target, port)
                print("Port {} is open".format(port))
                print("banner: {}".format(banner))
                if(first_pass == True and chk == False):
                    init_ports.append(port)
            s.close()
            
    except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
    except socket.gaierror:
            print("\n Hostname Could Not Be Resolved !!!!")
            sys.exit()
    except socket.error:
            print("\ Server not responding !!!!")
            sys.exit()

    first_pass = False
