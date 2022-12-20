from tkinter import *
import platform
import psutil
import cpuinfo
import subprocess


class SystemIformation():
    def __init__(self):
        pass

    def draw(self):
        #cria a janela para exibir as informacoes
        self.newWindow = Toplevel()
        self.newWindow.geometry("1024x768")
        self.newWindow.title("System Information")
        self.newWindow.config(bg='white')
        #chama os metodos para exibir as informacoes 
        self.systemInformation()
        self.ramInformation()
        self.cpuInformation()
        #self.gpuInformation()
        self.diskInformation()

    def systemInformation(self):
        #pega informacoes do sistema com a biblioteca platform
        #e depois separa cada informacao
        self.uname = platform.uname()
        self.frame1 = LabelFrame(self.newWindow, text="Informacoes Do Sistema", font=("helvetica", 12))
        self.frame1.place(x=0, y=0)
        self.sysMessage = Message(self.frame1, text="Sistema Operacional: " + self.uname.system
        + "\nNome: " + self.uname.node +
        "\nVersao: " + self.uname.version+
        "\nArquitetura: " + self.uname.machine+
        "\nProcessador: " + self.uname.processor, 
            font=('helvetica', 18),
            aspect=1500,
            justify=LEFT)
        self.sysMessage.pack(pady=10, padx=10)

    def cpuInformation(self):
        #pega informacoes da cpu com a biblioteca psutil e cpuinfo
        #e depois separa cada informacao
        self.frame2 = LabelFrame(self.newWindow, text="PROCESSADOR", font=("helvetica", 12))
        self.frame2.place(x=0, y=200)
        self.cpuInfo = str(cpuinfo.get_cpu_info()['brand_raw'])
        self.cores = psutil.cpu_count(logical=False)
        self.total = psutil.cpu_count()
        self.cpuMessage = Message(self.frame2, text=str(self.cpuInfo) + "\nNucleos: " + str(self.cores) +
        "\nLogicos: " + str(self.total) +
        "\nFrequencia Maxima: " + str(psutil.cpu_freq().current), 
            font=('helvetica', 18),
            aspect=1500,
            justify=LEFT)
        self.cpuMessage.pack(pady=10, padx=10)

    def ramInformation(self):
        #pega informacoes da ram com a biblioteca psutil
        #e depois separa cada informacao
        total = str(int(int(psutil.virtual_memory().total)/1000/1024/1024))
        free = str(int(int(psutil.virtual_memory().available)/1000/1024/1024))
        used =  str(int(int(psutil.virtual_memory().used)/1000/1024/1024))
        percent = str(psutil.virtual_memory().percent)
        self.frame3 = LabelFrame(self.newWindow, text="MEMORIA RAM", font=("helvetica", 12))
        self.frame3.place(x=0, y=380)
        self.ramMessage = Message(self.frame3, text="Total: " + total +'GBs' +
        "\nDisponivel: " + free +'GBs' +
        "\nUsados: " + used +'GBs' +
        "\nPorcentagem: " + percent, 
            font=('helvetica', 18),
            aspect=1500,
            justify=LEFT)
        self.ramMessage.pack(pady=10, padx=10)

    def gpuInformation(self):
        gpuInfo = subprocess.getoutput(
            'cmd /c "wmic path win32_videocontroller get name"')
        self.gpuInfo = str(gpuInfo[25:48])
        self.gpuLabel = Label(self.newWindow, text="Placa de Video: " + str(
            self.gpuInfo), font=('Arial', 18, 'bold'), bd=5, bg='white', height=1)
        self.gpuLabel.place(x=0, y=120)

    def diskInformation(self):
        #pega informacoes da ram com a biblioteca psutil
        #e depois separa cada informacao
        #a lista armazena a quantidade de HDs ou SSDs
        diskList = []
        partitions = psutil.disk_partitions()
        #separa cada informacao
        for partition in partitions:
            device = str(partition.device)
            fileSystem = str(partition.fstype)
            try:
                partitionUsage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            total = str(int((partitionUsage.total)/1024**3))
            used = str(int((partitionUsage.used)/1024**3))
            free = str(int((partitionUsage.free)/1024**3))
            disk = "Caminho: " + device + "\nSistema de Arquivos: " + fileSystem + \
            "\nTamanho Total: " + total + "GBs" + "\nUsado: " + used + "GBs" + "\nDisponivel: " + free + "GBs"
            diskList.append(disk)
        text = ""
        #junta as informacoes de todos os armazenamentos
        for disk in diskList:
            text =  text + disk + "\n"
        self.frame4 = LabelFrame(self.newWindow, text="Armazenamento", font=("helvetica", 12))
        self.frame4.place(x=0, y=530)
        self.diskMessage = Message(self.frame4,
            text=text, 
            font=('helvetica', 18),
            aspect=1500,
            justify=LEFT)
        self.diskMessage.pack(pady=10, padx=10)

