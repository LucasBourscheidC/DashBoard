from tkinter import filedialog
from tkinter import *
import os
import shutil


class FileSystem():
    def __init__(self):
        self.pixel = PhotoImage(width=1, height=1)

    def draw(self):
        # cria janela
        self.newWindow = Toplevel()
        self.newWindow.geometry("480x150")
        self.newWindow.title("Sistema de Arquivos")
        self.newWindow.config(bg='white')
        # cria os botoes
        creatDirButton = Button(self.newWindow, text="Criar Diretorio", image=self.pixel,
                                command=self.selectDir, width=480, height=50, compound='c')
        creatDirButton.place(x=0, y=0)
        deleteDirButton = Button(self.newWindow, text="Deletar Diretorio", image=self.pixel,
                                 command=self.deleteDir, width=480, height=50, compound='c')
        deleteDirButton.place(x=0, y=50)
        creatTxtButton = Button(self.newWindow, text="Criar txt", image=self.pixel,
                                command=self.textBox, width=480, height=50, compound='c')
        creatTxtButton.place(x=0, y=100)

    # area para escrever texto com opcoes de salvar txt e abrir txt
    def textBox(self):
        self.textWindow = Toplevel()
        self.text = Text(self.textWindow, width=40,
                         height=10, font=('Helvetica', 16))
        self.text.pack()
        openTxtButton = Button(
            self.textWindow, text="Abrir txt", command=self.openTxt)
        openTxtButton.pack(pady=20)
        saveButton = Button(
            self.textWindow, text="Salvar txt", command=self.saveTxt)
        saveButton.pack(pady=20)

    # metodo para abrir o txt
    def openTxt(self):
        txtFile = filedialog.askopenfilename(
            title="Abrir txt", filetypes=(("Text Files", "*.txt"),))
        txtFile = open(txtFile, 'r')
        text = txtFile.read()
        self.text.insert(END, text)
        txtFile.close()

    # metodo para salvar txt
    def saveTxt(self):
        textFile = filedialog.asksaveasfilename(
            title="Abrir txt", filetypes=(("Text Files", "*.txt"),))
        textFile = open(textFile, 'w')
        textFile.write(self.text.get(1.0, END))

    # metodo para selecionar o diretorio
    def selectDir(self):
        # abre uma janela de navegacao dos arquivos do proprio windows
        self.path = filedialog.askdirectory(initialdir="")
        if self.path != "":
            self.dNameWindow = Toplevel()
            self.dNameWindow.geometry("200x80")
            self.dNameWindow.title("Criar Diretorio")
            nameLabel = Label(self.dNameWindow,
                              text="Nome do Diretorio", font=("Arial", 12))
            nameLabel.pack()
            self.dName = Entry(self.dNameWindow, width=50, font=("Arial", 12))
            self.dName.pack()
            createDirButton = Button(self.dNameWindow, text="Criar", image=self.pixel,
                                     command=self.createDir, width=50, height=20, compound='c')
            createDirButton.place(x=75, y=50)

    #cria o diretorio no ambiente selecionado
    def createDir(self):
        dirName = self.dName.get()
        path = os.path.join(self.path, dirName)
        os.mkdir(path)
        self.dNameWindow.destroy()

    #deleta o diretorio selecionado
    def deleteDir(self):
        path = filedialog.askdirectory(initialdir="")
        if path != "":
            shutil.rmtree(path, ignore_errors=True)
