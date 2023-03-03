#	/subscriptions/aa1792c8-2080-4570-9e12-a13c30464c9f/resourceGroups/acinew/providers/Microsoft.ContainerInstance/containerGroups/acitest


import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import jinja2

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

options = [
    "AKS",
    "ACI",
    "ACR",
    "ARO",
    "AzurePortal",
    "Custom"
]
variable = tk.StringVar(root)
variable.set(options[0]) # default value


def aci_handler():
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    containerGroup = resURI[8]
    print(resourceGroup)
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    ACI_TEMPLATE_FILE = "aci.kqt"
    template = templateEnv.get_template(ACI_TEMPLATE_FILE)
    aci_outputText = template.render(subscription=subscription, containerGroup=containerGroup, resourceGroupName=resourceGroup, fromTime=fromt, toTime=tot, resUri = rawId)   # this is where to put args to the template renderer
    file_name = containerGroup + ".kql"
    new_file = open(file_name,"w")
    new_file.write(aci_outputText)
    new_file.close()
    

def acr_handler():
    #/subscriptions/bb420665-908d-4789-8bb4-51568e8bede0/resourceGroups/k8s-bi-prod-rg/providers/Microsoft.ContainerRegistry/registries/biprod01acr
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    registryName = resURI[9]
    print(registryName)

def aks_handler():
    fromt = fromTimeEntry.get()
    tot = toTimeEntry.get()
    rawId = resId.get()
    resURI =  rawId.split("/")
    subscription = resURI[2]
    resourceGroup = resURI[4]
    clusterName = resURI[8]
    print(clusterName)
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "aks.kqt"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(subscription=subscription, clusterName=clusterName, resourceGroupName=resourceGroup, fromTime=fromt, toTime=tot)   # this is where to put args to the template renderer
    file_name = clusterName + ".kql"
    new_file = open(file_name,"w")
    new_file.write(outputText)
    new_file.close()
    if variable.get() == "ARO":
        print("Ai ales ARO")
    #int(resId.get())
    #msg = f'You entered email: {email.get()} and password: {password.get()}'
    #showinfo(
    #    title='Information',
    #    message=msg
    #)

def general_handler():
    if variable.get() == "AKS":
        print("Ai ales AKS")
        aks_handler()
    elif variable.get() == "ACI":
        print("Ai ales ACI")
        aci_handler()
    elif variable.get() == "ACR":
        print("Ai ales ACR")
        acr_handler()
    elif variable.get() == "ARO":
        print( "Ai ales ARO")
    elif variable.get() == "AzurePortal":
        print( "Ai ales AzurePortal")
    elif variable.get() == "Custom":
        print( "Ai ales Custom")

if __name__ == "__main__":

    main = ttk.Frame(root)
    main.pack(padx=10, pady=10, fill='x', expand=True)
    second = ttk.Frame(root)
    second.pack(padx=15, pady=15, fill='x', expand=True)
    #title = ttk.Label(main, text="KustoBuddy v0.20230227",  anchor="e", font=("Helvetica", 10))
    #title.pack(ipadx=10, ipady=10)
    w = OptionMenu(main, variable, *options)
    w.pack()


    # Resource Id
    resource = ttk.Label(main, text="AKS Resource Id:")
    resource.pack(fill='x', expand=True)
    resource_entry = ttk.Entry(main, textvariable=resId)
    resource_entry.pack(fill='x', expand=True, pady=15)
    resource_entry.focus()

    # From Time
    fromTime = ttk.Label(main, text="FromTime")
    fromTime.pack(side=tk.LEFT, fill=tk.X, padx=5)
    fromtime_entry = ttk.Entry(main, textvariable=fromTimeEntry)
    #fromtime_entry.pack(fill='x', expand=True)
    fromtime_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)

    # to Time
    toTime = ttk.Label(main, text="ToTime")
    toTime.pack(side=tk.RIGHT, fill=tk.X, padx=5)
    toTime_entry = ttk.Entry(main, textvariable=toTimeEntry)
    #fromtime_entry.pack(fill='x', expand=True)
    toTime_entry.pack(side=tk.RIGHT, fill=tk.X, padx=5)
    
    
    # namespace
    #namespace = ttk.Label(main, text="Namespace")
    #namespace.pack(fill='x', expand=True)
    #namespace.pack(side=tk.BOTTOM, fill=tk.X, padx=5)
    namespace_entry = ttk.Entry(main, textvariable=nsEntry)
    #namespace_entry.pack(fill='x', expand=True)
    namespace_entry.insert(0, "CCP Namespace")
    namespace_entry.pack(side=tk.TOP, fill=tk.X, padx=25)
    #namespace = ttk.Label(main, text="Namespace")
    #namespace.pack(side=tk.RIGHT, padx=15)
    
    # login button

    login_button = ttk.Button(second, text="Generate", command=general_handler)
    #login_button.pack(fill='x', expand=True, pady=20)
    login_button.pack(side=tk.LEFT, fill=tk.X, padx=5)

    quit_button = ttk.Button(second, text="Quit", command=general_handler)
    quit_button.pack(side=tk.LEFT, fill=tk.X, padx=5)

    #title = ttk.Label(second, text="KustoBuddy v0.20230227",  anchor="e", font=("Helvetica", 10))
    #title.pack(ipadx=3, ipady=3, side=tk.TOP)
    
    C1 = Checkbutton(second, text = "Open in Kusto Explorer", variable = checkvar, onvalue = 1, offvalue = 0, height=2, width = 20).pack()
    title = ttk.Label(second, text="KustoBuddy v0.20230227", font=("Helvetica", 8))
    title.pack(ipadx=1, ipady=1, side=tk.RIGHT)
    root.mainloop()