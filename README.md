# About
This is my first project using python and it is all about getting system informations.
Display informations about system performances, all running process, information of the system like
processor type, windows version, etc...

## Libraries used
- tkinter: for creating the user interface
- matplotlib: for generating performance graphs
- threading: for working with multiple screens
- time: for introducing a delay between updating information on the screen to reduce lag
- subprocess: used to retrieve GPU usage in Windows PowerShell and open a terminal
- psutil: for retrieving CPU usage information and managing processes
- cpuinfo: for obtaining CPU information
- os: for creating directories
- shutil: for removing directory trees

## Interface
This is the main screen, containing 5 buttons. 
When clicked, each button always opens a new screen to display the information.

![image](https://github.com/ValafarL/DashBoard/assets/121062556/804eb3c5-3d9e-4074-92ae-afc506962cc9)

## Performance Visualization
These are 3 graphs that display information about CPU, GPU, and memory usage.
If the box is left unchecked, it will show the average usage of all CPUs.

![image](https://github.com/ValafarL/DashBoard/assets/121062556/b2e5a2e2-6e50-4f84-be9d-8685d011e725)

## Process
This screen displays all running processes. 
By selecting one, you can click the "Matar Processo" button to end the selected process.

![image](https://github.com/ValafarL/DashBoard/assets/121062556/acf8fbbd-50e4-421e-99e1-6413bd0b02db)
