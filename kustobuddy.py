#  KustoBuddy v16022023
#  For Installation:
# Install Python 3.10 from Microsoft Store. After this operation please do:
# pip install tkinter
# pip install jinja2

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
import jinja2
import subprocess

root = tk.Tk()
root.geometry("700x250")
root.resizable(False, False)
root.title('KustoBuddy')

resId = tk.StringVar()
fromTimeEntry = tk.StringVar()
toTimeEntry = tk.StringVar()
db = tk.StringVar()
nsEntry = tk.StringVar()
checkvar = tk.StringVar()
openInKusto = IntVar(value=0)

options = [
    "AKS",
    "ACI",
    "ACR",
    "ARO",
    "Custom"
]
variable = tk.StringVar(root)
variable.set(options[0]) # default value


def aro_handler():
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    aroCluster = resURI[8]
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    ARO_TEMPLATE_FILE = "aro.kqt"
    template = templateEnv.get_template(ARO_TEMPLATE_FILE)
    aro_outputText = template.render(subscription=subscription, aroCluster=aroCluster, resourceGroupName=resourceGroup, fromTime=fromt, toTime=tot, resUri = rawId)   # this is where to put args to the template renderer
    file_name = aroCluster + ".kql"
    new_file = open(file_name,"w")
    new_file.write(aro_outputText)
    new_file.close()
    path = "./" + file_name
    if openInKusto.get() == 1:
        subprocess.run(["powershell", path]) 

def aci_handler():
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    containerGroup = resURI[8]
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    ACI_TEMPLATE_FILE = "aci.kqt"
    template = templateEnv.get_template(ACI_TEMPLATE_FILE)
    aci_outputText = template.render(subscription=subscription, containerGroup=containerGroup, resourceGroupName=resourceGroup, fromTime=fromt, toTime=tot, resUri = rawId)   # this is where to put args to the template renderer
    file_name = containerGroup + ".kql"
    new_file = open(file_name,"w")
    new_file.write(aci_outputText)
    new_file.close()
    path = "./" + file_name
    if openInKusto.get() == 1:
        subprocess.run(["powershell", path]) 

def acr_handler():
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    registryName = resURI[8]
    fqdn = registryName + ".azurecr.io"
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    ACR_TEMPLATE_FILE = "acr.kqt"
    template = templateEnv.get_template(ACR_TEMPLATE_FILE)
    acr_outputText = template.render(subscription=subscription, registryName=registryName, resourceGroupName=resourceGroup, fromTime=fromt, toTime=tot, resUri = rawId, fqdn = fqdn)   # this is where to put args to the template renderer
    file_name = registryName + ".kql"
    new_file = open(file_name,"w")
    new_file.write(acr_outputText)
    new_file.close()
    path = "./" + file_name
    if openInKusto.get() == 1:
        subprocess.run(["powershell", path]) 

def aks_handler():
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    clusterName = resURI[8]
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "aks.kqt"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(subscription=subscription, clusterName=clusterName, resourceGroupName=resourceGroup, fromTime=fromt, toTime=tot)   # this is where to put args to the template renderer
    file_name = clusterName + ".kql"
    new_file = open(file_name,"w")
    new_file.write(outputText)
    new_file.close()
    path = "./" + file_name
    if openInKusto.get() == 1:
        subprocess.run(["powershell", path]) 
    
def general_handler():
    if variable.get() == "AKS":
        if "managedClusters" not in resId.get():
            messagebox.showinfo('information', 'No valid Azure Kubernetes Service found in provided Id.')
        aks_handler()
    elif variable.get() == "ACI":
        if "Microsoft.ContainerInstance" not in resId.get():
            messagebox.showinfo('information', 'No valid Azure Container Instance found in provided Id.')
        aci_handler()
    elif variable.get() == "ACR":
        if "Microsoft.ContainerRegistry" not in resId.get():
            messagebox.showinfo('information', 'No valid Azure Container Registry found in provided Id.')
        acr_handler()
    elif variable.get() == "ARO":
        if "RedHat" not in resId.get():
            messagebox.showinfo('information', 'No valid Azure RedHat OpenShift found in provided Id.')
        aro_handler()
    elif variable.get() == "Custom":
        subprocess.run(["notepad", "custom.kqt" ]) 

if __name__ == "__main__":
    main = ttk.Frame(root)
    main.pack(padx=10, pady=10, fill='x', expand=True)
    second = ttk.Frame(root)
    second.pack(padx=15, pady=15, fill='x', expand=True)
    w = OptionMenu(main, variable, *options)
    w.pack()

    # Resource Id
    resource = ttk.Label(main, text="Resource Id:")
    resource.pack(fill='x', expand=True)
    resource_entry = ttk.Entry(main, textvariable=resId)
    resource_entry.pack(fill='x', expand=True, pady=15)
    resource_entry.focus()

    # From Time
    fromTime = ttk.Label(main, text="FromTime")
    fromTime.pack(side=tk.LEFT, fill=tk.X, padx=5)
    fromtime_entry = ttk.Entry(main, textvariable=fromTimeEntry)
    fromtime_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
    # to Time
    toTime = ttk.Label(main, text="ToTime")
    toTime.pack(side=tk.RIGHT, fill=tk.X, padx=5)
    toTime_entry = ttk.Entry(main, textvariable=toTimeEntry)
    #fromtime_entry.pack(fill='x', expand=True)
    toTime_entry.pack(side=tk.RIGHT, fill=tk.X, padx=5)
    # namespace
    namespace_entry = ttk.Entry(main, textvariable=nsEntry)
    namespace_entry.insert(0, "CCP Namespace")
    namespace_entry.pack(side=tk.TOP, fill=tk.X, padx=25)
   
    login_button = ttk.Button(second, text="Generate", command=general_handler)
    login_button.pack(side=tk.LEFT, fill=tk.X, padx=5)
    quit_button = ttk.Button(second, text="Quit", command=general_handler)
    quit_button.pack(side=tk.LEFT, fill=tk.X, padx=5)

    C1 = Checkbutton(second, text = "Open in Kusto Explorer", variable = openInKusto, onvalue = 1, offvalue = 0, height=2, width = 20).pack()
    title = ttk.Label(second, text="KustoBuddy v0.16032023", font=("Helvetica", 8))
    title.pack(ipadx=1, ipady=1, side=tk.RIGHT)
    
    root.mainloop()
