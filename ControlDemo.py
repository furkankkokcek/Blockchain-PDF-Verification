import hashlib
from tkinter import *
import tkinter.filedialog
from tkinter import ttk
from tkinter import messagebox


window = Tk()

window.wm_minsize(600, 550)
window.title("Blokchain Database Verification Program Demo (Version 1.0.12)")
window.iconbitmap('icon.ico')

def check_pdf(name, pdf_path):
    ledgerFile = open("/Users/cankat/Desktop/chain-ledger.txt", "r+")

    ledgerStr = ledgerFile.readlines()
    ledgerFile.close()

    allHashes = []

    pdf = open(pdf_path, 'rb')
    hashedPdf = hashlib.sha256()
    hashedPdf.update(name.encode('utf-8'))
    hashedPdf.update(pdf.read())
    searchingHash = hashedPdf.hexdigest()

    print(name.encode('utf-8'))
    print(str(searchingHash))


    if not len(ledgerStr) == 0:
        for i in range(0, len(ledgerStr)):
            if ledgerStr[i].startswith("Block Data:"):
                allHashes.append(ledgerStr[i].split("Block Data: ", 1)[1])
    searchingHash = str(searchingHash).rstrip()
    for hash in allHashes:
        print("hash:   " + hash)
        print("search: " + searchingHash)
        if searchingHash == hash.rstrip():
            return True

    return False


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
    pdf_path = list1.get(END)

    if check_pdf(name, pdf_path):
        messagebox.showinfo("Verification Information", "PDF File is Verified.")
    else:
        messagebox.showinfo("Verification Information", "PDF File Could Not Be Verified.")

    name_text.set("")
    surname_text.set("")
    list1.delete(0, 'end')




#define Labels
header = Label(window, text="HOSPITAL RECORD \nVERIFICATION SYSTEM", font=("arial", 20, "bold"), fg="steelblue", anchor=CENTER)
header.place(x=175, y=20)

l1 = Label(window, text='Name')
l1.place(x=150, y=150)

l2 = Label(window, text='Surname')
l2.place(x=150, y=220)

#define Entries
name_text = StringVar()
e1 = Entry(window, textvariable=name_text)
e1.place(x=250, y=150)

surname_text = StringVar()
e2 = Entry(window, textvariable=surname_text)
e2.place(x=250, y=220)

#define Button
b1 = ttk.Button(window, text="SEND", command=send_button)
b1.place(x=170, y=400)

b2 = ttk.Button(window, text="Upload File")
b2.config(command=print_path)
b2.place(x=380, y=400)

#define List
list1 = Listbox(window, height=5, width=45)
list1.place(x=130, y=300)

window.mainloop()


