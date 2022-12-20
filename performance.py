from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import psutil
import threading
import time
import subprocess

class Performance():
    def __init__(self):
        self.frame_len = 60
        self.cpu_usage_list = []
        self.perCpu_usage_dict = {}
        self.gpu_usage_list = []
        self.mem_usage_list = []
        self.lastCpuPercent = 0.0
        self.lastPerCpuPercent = []
        self.lastGpuPercent = 0.0
        self.lastMemPercent = 0.0
        self.perCpu = True
        self.cpu = True
        #threads para atualizar os dados dos graficos
        threadPerformanceData = threading.Thread(target=self.managePerformance, args=(), daemon=True)
        threadPerformanceData.start()
        threadGpuData = threading.Thread(target=self.gpuData, args=(), daemon=True)
        threadGpuData.start()
        threadPercpuData = threading.Thread(target=self.perCpuData, args=(), daemon=True)
        threadPercpuData.start()
    def createGraphs(self):
        #cria os graficos
        self.createCpuGraph()
        self.createGpuGraph()
        self.createMemGraph()

    def draw(self):
        #mostra na tela os graficos
        time.sleep(1)
        self.newWindow = Toplevel()
        self.newWindow.geometry("1280x768")
        self.newWindow.title("System Information")
        self.newWindow.config(bg='white')
        self.createGraphs()
        self.cpuCheckBox()
        self.cpuCanvas.get_tk_widget().place(x=0, y=58)
        self.gpuCanvas.get_tk_widget().place(x=640, y=58)
        self.memCanvas.get_tk_widget().place(x=0, y=400)
    
    def animate(self, i):
        #atualiza as informacoes representadas nos graficos
        #a cada 1 seg
        self.cpuGraphUpdate()
        self.gpuGraphUpdate()
        self.memGraphUpdate()

    def managePerformance(self):
        while (True):
            self.data()
            time.sleep(1)

    def data(self):
        #atualiza os dados da cpu e memoria ram
        self.cpuData()
        self.memData()
        
    def createCpuGraph(self):
        #cria o grafico da cpu
        self.cpuGraph = plt.Figure(figsize=(9, 4), dpi=75)
        self.cpuSubplot = self.cpuGraph.add_subplot(111)
        self.cpuCanvas = FigureCanvasTkAgg(self.cpuGraph, master=self.newWindow)
        self.cpuAnimation = animation.FuncAnimation(self.cpuGraph, self.animate, interval=1000)
    
    def createGpuGraph(self):
        #cria o grafico da gpu
        self.gpuGraph = plt.Figure(figsize=(9, 4), dpi=75)
        self.gpuSubplot = self.gpuGraph.add_subplot(111)
        self.gpuCanvas = FigureCanvasTkAgg(self.gpuGraph, master=self.newWindow)
        self.gpuAnimation = animation.FuncAnimation(self.gpuGraph, self.animate, interval=1000)
    
    def createMemGraph(self):
        #cria o grafico da memoria ram
        self.memGraph = plt.Figure(figsize=(9, 4), dpi=75)
        self.memSubplot = self.memGraph.add_subplot(111)
        self.memCanvas = FigureCanvasTkAgg(self.memGraph, master=self.newWindow)
        self.memAnimation = animation.FuncAnimation(self.memGraph, self.animate, interval=1000)
    
    def cpuGraphUpdate(self):
        #atualiza o grafico da cpu
        self.cpuSubplot.clear()
        if self.cpu == True:
            self.cpuSubplot.plot(self.cpu_usage_list, '#00C957', label='CPU : ' + str(self.lastCpuPercent) + '%')
        if self.perCpu == True:
            for i in range (psutil.cpu_count()):
                self.cpuSubplot.plot(self.perCpu_usage_dict.get("cpu{0}".format(i)), label='CPU '+ str(i) + ': ' + 
                str(int(self.lastPerCpuPercent[0][i])) + '%')
        if self.cpu == False and self.perCpu == False:
            pass
        else:
            self.cpuSubplot.set_title("CPU - USAGE")
            self.cpuSubplot.set_xlabel("segundos")
            self.cpuSubplot.set_ylabel("CPU%")
            self.cpuSubplot.set_ylim(0, 100)
            self.cpuSubplot.set_xlim(0, 60)
            self.cpuSubplot.legend() 

    def gpuGraphUpdate(self):
        #atualiza o grafico da gpu
        self.gpuSubplot.clear()
        self.gpuSubplot.plot(self.gpu_usage_list, '#00C957', label='GPU : ' + str(self.lastGpuPercent) + '%')
        self.gpuSubplot.set_title("GPU - USAGE")
        self.gpuSubplot.set_xlabel("segundos")
        self.gpuSubplot.set_ylabel("GPU%")
        self.gpuSubplot.set_ylim(0, 100)
        self.gpuSubplot.set_xlim(0, 60)
        self.gpuSubplot.legend()

    def memGraphUpdate(self):
        #atualiza o grafico da ram
        self.memSubplot.clear()
        self.memSubplot.plot(self.mem_usage_list, '#00C957', label='MEM : ' + str(self.lastMemPercent) + '%')
        self.memSubplot.set_title("MEM - USAGE")
        self.memSubplot.set_xlabel("segundos")
        self.memSubplot.set_ylabel("MEM%")
        self.memSubplot.set_ylim(0, 100)
        self.memSubplot.set_xlim(0, 60)
        self.memSubplot.legend()          

    def cpuData(self):
        #pega a porcentagem de uso da cpu
        self.lastCpuPercent =  int(psutil.cpu_percent())
        self.cpu_usage_list.append(self.lastCpuPercent)
        if len(self.cpu_usage_list) >= self.frame_len:
            self.cpu_usage_list = self.cpu_usage_list[-self.frame_len:]

    def perCpuData(self):
        #pega a porcentagem de uso de cada cpu
        for i in range(psutil.cpu_count()):
            self.perCpu_usage_dict["cpu{0}".format(i)] = []
        self.length = 0
        while True:
            self.lastPerCpuPercent.append(psutil.cpu_percent(interval=1, percpu=True))
            self.lastPerCpuPercent = self.lastPerCpuPercent[-1:]
            for i in range(psutil.cpu_count()):
                self.perCpu_usage_dict["cpu{0}".format(i)].append(self.lastPerCpuPercent[0][i])
                if self.length >= self.frame_len:
                    self.perCpu_usage_dict["cpu{0}".format(i)] = self.perCpu_usage_dict.get("cpu{0}".format(i))[-self.frame_len:]
            if i != 0:
                self.length = self.length + 1
        
    
    def memData(self):
        #pega a porcentagem de uso da memoria ram
        self.lastMemPercent =  int(psutil.virtual_memory()[2])
        self.mem_usage_list.append(self.lastMemPercent)
        if len(self.mem_usage_list) >= self.frame_len:
            self.mem_usage_list = self.mem_usage_list[-self.frame_len:]

    def gpuData(self):
        #pega os dados de uso da gpu atravez do powershell
        powershell = r"C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
        execPW = "(((Get-Counter '\\GPU Engine(*engtype_3D)\\Utilization Percentage').CounterSamples | where CookedValue).CookedValue | measure -sum).sum"
        while (True):
            p = subprocess.Popen([powershell, execPW], stdout=subprocess.PIPE)
            GpuUseTotal = p.communicate()[0]
            caractere2 = ""
            for caractere in str(GpuUseTotal):
                if caractere in "0123456789":
                    caractere2 += caractere
                elif caractere == ",":
                    self.gpu_usage_list.append(int(caractere2))
                    break
            self.lastGpuPercent = int(caractere2)
            if len(self.gpu_usage_list) >= self.frame_len:
                self.gpu_usage_list = self.gpu_usage_list[-self.frame_len:]
            time.sleep(0.1)
    
    def cpuCheckBox(self):
        #cria checkbox para dar opcao ver todas as cpus ou somente uma
        self.x = IntVar()
        self.y = IntVar()
        self.percpuBox = Checkbutton(self.newWindow, text="Mostrar Todas CPUs", variable=self.x, onvalue=1, offvalue=0,
        command=self.display, font=('Arial', 20))
        self.cpuBox = Checkbutton(self.newWindow, text="Mostrar CPU            ", variable=self.y, onvalue=1, offvalue=0,
        command=self.display, font=('Arial', 20))
        self.percpuBox.select()
        self.cpuBox.select()
        self.percpuBox.place(x=710, y= 434)
        self.cpuBox.place(x=710, y= 484)

    def display(self):
        #verifica se deve mostrar todas cpus ou somente uma
        if self.y.get() == 1:
            self.cpu = True
        else:
            self.cpu = False
        if self.x.get() == 1:
            self.perCpu = True
        else:
            self.perCpu = False