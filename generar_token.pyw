from tkinter import *
from ttkbootstrap import Style
from tkinter import ttk
from requests import post
from config import *

style = Style(theme='cosmo')

raiz = style.master
raiz.title("GENEAR TOKEN")
raiz.resizable(False, False)

frame = Frame(raiz)
frame.pack()

ambiente = IntVar()
text = StringVar()

usuario = StringVar()
password = StringVar()

def generar():
    cuadro_texto.config(state="normal")
    cuadro_texto.delete("1.0", END)

    if ambiente.get() == 1:
        endpoint = ENDPOINT_PROD

    if ambiente.get() == 2:
        endpoint = ENDPOINT_HML

    usr = usuario.get()
    pssw = password.get()       

    response = post(endpoint, auth=(usr, pssw))
    token = response.content.decode('UTF-8')
    cuadro_texto.insert(INSERT, token)
    cuadro_texto.config(state="disabled")
    text.set("")


def copiar():
    token = cuadro_texto.get("1.0", END)
    raiz.clipboard_clear()
    raiz.clipboard_append(token)
    text.set("Copiado al portapapeles")


label_ambiente = Label(frame, text="AMBIENTE")
label_ambiente.config(justify=LEFT)
label_ambiente.grid(row=1, column=1, padx=3, pady=3)

radio_1 = Radiobutton(frame, text="PROD", variable=ambiente, value=1)
radio_1.grid(row=1, column=2, padx=3, pady=3, sticky='W')

radio_2 = Radiobutton(frame, text="HML", variable=ambiente, value=2)
radio_2.grid(row=1, column=2, padx=3, pady=3, sticky='E')

label_user = Label(frame, text="USUARIO")
label_user.config(justify=LEFT)
label_user.grid(row=2, column=1, padx=3, pady=3)

user = Entry(frame, textvariable=usuario)
user.config(justify=LEFT)
user.grid(row=2, column=2, padx=3, pady=3)

label_pssw = Label(frame, text="PASSWORD")
label_pssw.config(justify=LEFT)
label_pssw.grid(row=3, column=1, padx=3, pady=3)

pssw = Entry(frame, textvariable=password, show="*")
pssw.config(justify=LEFT)
pssw.grid(row=3, column=2, padx=3, pady=3)


boton_generar = Button(frame, text="Generar", width=8, command=generar)
boton_generar.grid(row=4, column=1, padx=3, pady=3)

boton_copiar = Button(frame, text="Copiar", width=8, command=copiar)
boton_copiar.grid(row=4, column=2, padx=3, pady=3, sticky='W')

copiado = Entry(frame, textvariable=text)
copiado.config(justify=RIGHT, state="readonly")
copiado.grid(row=4, column=8, padx=3, pady=3)

cuadro_texto = Text(frame, width=60, height=22)
cuadro_texto.config(state="disabled")
cuadro_texto.grid(row=5, column=1, columnspan=8, padx=3, pady=3)

raiz.mainloop()