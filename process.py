from tkinter import *
from tkinter import ttk
import psutil
import threading

class Process():
    def __init__(self):
        self.currentRecord = None
        self.currentPID = None
    def treeViewTeste(self):
        #add a style
        self.style = ttk.Style()
        #pick a theme
        self.style.theme_use('default')
        #config the treeview
        self.style.configure("Treeview", 
        background='#D3D3D3', 
        foreground="black",
        fieldbackground="#D3D3D3",
        rowheight=25)

        #change the color when selected a row
        self.style.map('Treeview', 
        background=[('selected', "#347083")])

        #treeview frame
        self.tree_frame = Frame(self.newWindow)
        self.tree_frame.pack(pady=10)

        #treeview scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        #create treeview
        self.processTreeView = ttk.Treeview(self.tree_frame, 
            yscrollcommand=self.tree_scroll.set,
            selectmode="extended", height=20)
        self.processTreeView.pack()

        #config scroll bar
        self.tree_scroll.config(command=self.processTreeView.yview)

        #set the columns
        self.processTreeView['columns'] = ("Nome", "PID", "memoria", "status")

        #format the columns
        self.processTreeView.column("#0", width=0, stretch=NO)
        self.processTreeView.column("Nome", anchor=W, width=200)
        self.processTreeView.column("PID", anchor=W, width=50)
        self.processTreeView.column("memoria", anchor=CENTER, width=100)
        self.processTreeView.column("status", anchor=W, width=100)
        
        #create headings
        self.processTreeView.heading("#0", text="", anchor=W)
        self.processTreeView.heading("Nome", text="Nome", anchor=W)
        self.processTreeView.heading("PID", text="PID", anchor=W)
        self.processTreeView.heading("memoria", text="memoria", anchor=CENTER)
        self.processTreeView.heading("status", text="status", anchor=W)

        #cria os botoes e insere os dados
        self.createButtons()
        self.processInsertData()

    def processInsertData(self):
        #insere os dados de processos
            global count
            count = 0
            for process in psutil.process_iter ():
                    self.processTreeView.insert(parent='', index= 'end', iid=count,
                    text='', values=(str(process.name()).replace(" ", ""), 
                    str(process.pid),
                    str(round((float(process.memory_info().rss)/1024**2),1)) + " MB",
                    process.status()))
                    count += 1
    def draw(self):
        #mostra na tela as informacoes
        self.newWindow = Toplevel()
        self.newWindow.geometry("800x640")
        self.newWindow.title("Processos")
        self.newWindow.config(bg='white')
        self.treeViewTeste()
        threadUpdateProcess = threading.Thread(target=self.updateProcess, args=(), daemon=True)
        threadUpdateProcess.start()

    def createButtons(self):
        #cria os botoes
        self.buttonFrame = LabelFrame(self.newWindow, text="Comandos")
        self.buttonFrame.pack(fill="x", expand="yes", padx=20)

        self.killProcessButton = Button(self.buttonFrame, text="Matar Processo", command=self.killProcess)
        self.killProcessButton.grid(row=0, column=0, padx=10,pady=10)

    def killProcess(self):
        #mata o processo selecionado 
        selected = self.processTreeView.focus()
        values = self.processTreeView.item(selected, 'values')
        if psutil.pid_exists(int(values[1])):
            psutil.Process(int(values[1])).terminate()

    def updateProcess(self):
        #atualiza os processos removendo e adicionando
        while(True):
            processInTreeView = []
            recordTreeview = []
            #atualiza os processos que existem ainda
            #caso nao exista mais ele remove da visualizacao
            for record in self.processTreeView.get_children():
                    if(record != None):
                        if(psutil.pid_exists(int(self.processTreeView.set(record, '#2')))):
                            processPid = psutil.Process(int(self.processTreeView.set(record, '#2')))
                            processInTreeView.append(processPid.pid)
                            self.currentRecord = record
                            self.currentPID = processPid
                            self.processTreeView.set(record, '#3', str(round((float(processPid.memory_info().rss)/1024**2),1)) + " MB")
                            self.processTreeView.set(record, '#4', processPid.status())
                        else:
                            self.processTreeView.delete(record)
                    recordTreeview.append(record)
            #adiciona novos processos para visualizar
            for process in psutil.process_iter():
                if process.pid in processInTreeView:
                    pass
                else:
                    self.processTreeView.insert(parent='', index= 'end',
                    text='', values=(str(process.name()).replace(" ", ""), 
                    str(process.pid),
                    0,
                    str(round((float(process.memory_info().rss)/1024**2),1)) + " MB",
                    process.status()))   