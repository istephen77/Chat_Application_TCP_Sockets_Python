import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        msg = tkinter.Tk()  #Implementation of the window dialog box for the chat App
        msg.withdraw() # withdraw() Removes the window from the screen (without destroying it). To redraw the window, use deiconify. When the window has been withdrawn, the state method returns “withdrawn”

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent = msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target= self.gui_loop)
        receive_thread = threading.Thread(target= self.receive)

        gui_thread.start()
        receive_thread.start()

    # Implementation of main-thread function to show the GUI (front-end) -- contains code implementation for text-box, button, padding and background color
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg = "lightgray")

        self.chat_label = tkinter.Label(self.win, text = "Chat:", bg = "lightgray")
        self.chat_label.config(font = ("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text = "Message:", bg = "lightgray")
        self.msg_label.config(font = ("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font = ("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)  #To close the GUI window
        self.win.mainloop()  ##window.mainloop() tells Python to run the Tkinter event loop. This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until you close the window where you called the method

    # Implementation of function to get the text from the message box and send it to the server and clear the message box
    def write(self):
        message = f"{self.nickname} : {self.input_area.get('1.0','end')}"  #1.0 --> To start from the beginning and go up untill the end
        self.sock.send(message.encode("utf-8"))  #To send the message to the server from the client
        self.input_area.delete()  #To clear the textbox


    #Implementation of function to terminate the main thread (gui_loop)
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):  #Daemon/receiver thread which works in the background
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.sock.send(self.nickname.encode("utf-8"))
                else:
                    if self.gui_done:  #Before changing the GUI we wait for it to be finished
                        self.text_area.config(state='normal') #To change it to insert some new text fetched from the server and then set the state back to disabled
                        self.text_area.insert('end',message) #Insert message at end becase we want to append the message at the end
                        self.text_area.yview('end')     #To always scrolll down at the end
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)


