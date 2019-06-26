import hashlib
import mysql.connector
from tkinter import *
import tkinter.filedialog
from tkinter import ttk
from tkinter import messagebox


class Block:
    data = None
    name = ""
    hash = None
    previous_hash = 0x0

    def __init__(self, data, name, previous_hash):
        self.data = data
        self.name = name
        self.previous_hash = previous_hash

    def hash(self):
        h = hashlib.sha256()

        h.update(
            str(self.data).encode('utf-8') +
            str(self.name).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        )

        return h.hexdigest()

    def __str__(self):
        # print out the value of a block
        return "Block Hash: " + str(self.hash()) + "\nBlock Data: " + str(
            self.data) +"\n--------------"

def main():

    mydb = mysql.connector.connect(user='root', password='clapton!',
                                  host='127.0.0.1', database='demo',
                                  auth_plugin='mysql_native_password')


    window = Tk()

    window.wm_minsize(600, 350)
    window.title("Blokchain Database Program Demo (Version 1.0.12)")
    window.iconbitmap('icon.ico')

    def send_to_chain(name, blood_type, doctor_name, payment, disease, pdf_path):
        # print("disease: " + disease)
        # print("payment: " + str(payment))
        cursorCommand = "INSERT INTO patients(blood_type, doctor, disease, payment, pdf_path) " \
                        "VALUES ('" + blood_type + "', '" + doctor_name + "', '" + disease + "', '" + str(payment) + "', '" + pdf_path + "');"

        mycursor = mydb.cursor()

        mycursor.execute(cursorCommand)

        mydb.commit()

        # for x in mycursor:
        #     print(x)

        ledgerFile = open("/Users/cankat/Desktop/chain-ledger.txt", "r+")

        ledgerStr = ledgerFile.readlines()
        ledgerFile.close()

        previous = ""

        if not len(ledgerStr) == 0:
            for i in range(len(ledgerStr) - 1, -1, -1):
                if ledgerStr[i].startswith("Block Hash:"):
                    previous = ledgerStr[i].split("Block Hash: ", 1)[1]
                    break

        # print("previous: " + str(previous))

        pdf = open(pdf_path, 'rb')
        hashedPdf = hashlib.sha256()
        hashedPdf.update(name.encode('utf-8'))
        hashedPdf.update(pdf.read())
        data = hashedPdf.hexdigest()

        print(name.encode('utf-8'))
        print(str(data))

        newBlock = Block(str(data), name, str(previous).rstrip())

        ledgerFile = open("/Users/cankat/Desktop/chain-ledger.txt", "a+")
        ledgerFile.write(newBlock.__str__() + "\n")
        ledgerFile.close()

    def print_path():
        f = tkinter.filedialog.askopenfilename(
            parent=window, initialdir='C:/Desktop',
            title='Choose file',
            filetypes=[('PDF files', '.pdf'),
                       ('png images', '.png'),
                       ('jpeg images', '.jpeg')]
        )
        list1.insert(END, f)
        # print(f)

    def send_button():

        name = str(name_text.get()) + str(surname_text.get())
        blood_type = str(blood_type_text.get())
        hospital_name = str(hospital_name_text.get())
        doctor_name = str(doctor_name_text.get())
        payment = float(payment_text.get())
        disease = str(disease_text.get())
        pdf_path = list1.get(END)

        send_to_chain(name, blood_type, doctor_name, payment, disease, pdf_path)

        name_text.set("")
        surname_text.set("")
        blood_type_text.set("")
        hospital_name_text.set("")
        doctor_name_text.set("")
        payment_text.set("")
        disease_text.set("")
        list1.delete(0, 'end')

        messagebox.showinfo("Information", "Record Added Successfully.")

    # define Labels
    header = Label(window, text="HOSPITAL SYSTEM", font=("arial", 26, "bold"), fg="steelblue")
    header.grid(row=0, column=1)

    l1 = Label(window, text='Name')
    l1.grid(row=1, column=0)

    l1 = Label(window, text='Surname')
    l1.grid(row=2, column=0)

    l1 = Label(window, text='Blood Type')
    l1.grid(row=3, column=0)

    l1 = Label(window, text='Hospital Name')
    l1.grid(row=1, column=2)

    l1 = Label(window, text='Doctor Name')
    l1.grid(row=2, column=2)

    l1 = Label(window, text='Payment')
    l1.grid(row=3, column=2)

    l1 = Label(window, text='')
    l1.grid(row=4, column=0)

    l1 = Label(window, text='')
    l1.grid(row=6, column=0)

    l1 = Label(window, text='Disease')
    l1.grid(row=5, column=0)

    # define Entries
    name_text = StringVar()
    e1 = Entry(window, textvariable=name_text)
    e1.grid(row=1, column=1)

    surname_text = StringVar()
    e2 = Entry(window, textvariable=surname_text)
    e2.grid(row=2, column=1)

    blood_type_text = StringVar()
    e3 = Entry(window, textvariable=blood_type_text)
    e3.grid(row=3, column=1)

    hospital_name_text = StringVar()
    e4 = Entry(window, textvariable=hospital_name_text)
    e4.grid(row=1, column=3)

    doctor_name_text = StringVar()
    e5 = Entry(window, textvariable=doctor_name_text)
    e5.grid(row=2, column=3)

    payment_text = StringVar()
    e6 = Entry(window, textvariable=payment_text)
    e6.grid(row=3, column=3)

    disease_text = StringVar()
    e7 = Entry(window, width=40, textvariable=disease_text)
    e7.grid(row=5, column=1)

    # define Button
    b1 = ttk.Button(window, text="SEND", command=send_button)
    b1.grid(row=8, column=2)

    b2 = ttk.Button(window, text="Upload File")
    b2.grid(row=8, column=1)
    b2.config(command=print_path)

    # define List
    list1 = Listbox(window, height=5, width=45)
    list1.grid(row=7, column=1)

    window.mainloop()

main()