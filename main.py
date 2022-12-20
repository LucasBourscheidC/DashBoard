from tkinter import *
from performance import Performance
from systemInformation import SystemIformation
from process import Process
from terminal import Terminal
from filesSystem import FileSystem


class main():
    def __init__(self):
        # Cria listas para os respectivos classe
        # em que serao armazenados os objetos criado para abrir
        # varias janelas corretamente
        self.performanceList = []
        self.processList = []

        # cria uma janela pelo tkinter e suas configuracoes
        self.window = Tk()
        self.window.geometry("480x250")
        self.window.title("Dashboard")
        self.window.config(background="white")
        self.window.resizable(False, False)

        # cria objetos das classes mais simples
        self.systemInformation = SystemIformation()
        self.fileSystem = FileSystem()
        self.terminal = Terminal()

        # cria um pixel 1x1 para facilitar o posicionamento na tela
        self.pixel = PhotoImage(width=1, height=1)

        # cria os botoes para cada classe
        performanceButton = Button(self.window, text="Desempenho", image=self.pixel,
                                   command=self.execPerformance, width=480, height=50, compound='c')
        performanceButton.place(x=0, y=0)
        processButton = Button(self.window, text="Processos", image=self.pixel,
                               command=self.execProcess, width=480, height=50, compound='c')
        processButton.place(x=0, y=50)

        systemButton = Button(self.window, text="Informações do Sistema", image=self.pixel,
                              command=self.execSystemInformation, width=480, height=50, compound='c')
        systemButton.place(x=0, y=100)

        filesButton = Button(self.window, text="Sistema de Arquivos", image=self.pixel,
                             command=self.execFileSystem, width=480, height=50, compound='c')
        filesButton.place(x=0, y=150)

        TerminalButton = Button(self.window, text="Terminal", image=self.pixel,
                                command=self.execTerm, width=480, height=50, compound='c')
        TerminalButton.place(x=0, y=200)

        self.window.mainloop()  # a janela fica esperando por eventos em um loop

    # executa os comandos das classes ao clicar em cada botao
    def execPerformance(self):
        currentPerformance = Performance()
        self.performanceList.append(currentPerformance)
        currentPerformance.draw()

    def execProcess(self):
        currentProcess = Process()
        self.processList.append(currentProcess)
        currentProcess.draw()

    def execSystemInformation(self):
        self.systemInformation.draw()

    def execFileSystem(self):
        self.fileSystem.draw()

    def execTerm(self):
        self.terminal.execTerminal()


main()
