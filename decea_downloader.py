import urllib.request
import xml.etree.ElementTree as ET
from time import sleep
import os, errno
import tkinter
from tkinter import *
import tkinter.messagebox
import sys

top = tkinter.Tk()

def download():

    global aeroportos
    global CartasIFR
    global CartasEmrotaIFR
    global CartasVFR
    global tipos

    # Tratar Variáveis
    aeroportos = aeroportos.get()
    arrayAeroportos = aeroportos.split(',')
    lenAeroportos = len(arrayAeroportos)

    CartasIFR = CartasIFR.get()
    CartasEmrotaIFR = CartasEmrotaIFR.get()
    CartasVFR = CartasVFR.get()
    
    tipos = tipos.get()
    arrayTipos = tipos.split(',')
    
    # CARTAS IFR

    if CartasIFR:

        urllib.request.urlretrieve('http://www.aisweb.aer.mil.br/api/?apiKey=1697016245&apiPass=3199c002-755b-1033-a49b-72567f175e3a&area=cartas', 'cycle.xml')
        sleep(5)

        tree = ET.parse('cycle.xml')
        root = tree.getroot()

        if lenAeroportos > 0 and aeroportos != '':

            for x in root.iter('item'):

                if x.find('IcaoCode').text in arrayAeroportos:

                    if x.find('tipo').text in arrayTipos:

                        directory = 'cartas/' + x.find('IcaoCode').text + '/' + x.find('tipo').text + '';
                        
                        try:
                            os.makedirs(directory)
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
                                
                        filename = x.find('nome').text;
                        filename = filename.replace("/", "-")

                        print ('Baixando.. ' + x.find('IcaoCode').text + ' - ' + filename + '')
                        
                        urllib.request.urlretrieve(x.find('link').text, '' + directory + '/' + filename + '.pdf')

        else:

            for x in root.iter('item'):

                if x.find('tipo').text in arrayTipos:

                    directory = 'cartas/' + x.find('IcaoCode').text + '/' + x.find('tipo').text + '';
                        
                    try:
                        os.makedirs(directory)
                    except OSError as e:
                        if e.errno != errno.EEXIST:
                            raise
                                
                    filename = x.find('nome').text;
                    filename = filename.replace("/", "-")

                    print ('Baixando.. ' + x.find('IcaoCode').text + ' - ' + filename + '')
                        
                    urllib.request.urlretrieve(x.find('link').text, '' + directory + '/' + filename + '.pdf')

    else:

        print("Pular Cartas IFR")


    # CARTAS EM ROTA IFR

    if CartasEmrotaIFR:

        urllib.request.urlretrieve('http://www.aisweb.aer.mil.br/api/?apiKey=1697016245&apiPass=3199c002-755b-1033-a49b-72567f175e3a&area=cartas&especie=rota', 'cycle_rota.xml')
        sleep(5)

        tree = ET.parse('cycle_rota.xml')
        root = tree.getroot()

        for x in root.iter('item'):
        
            directory = 'cartas_emrota/';
        
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise


            filename = x.find('nome').text;

            try:
            
                filename = filename.replace("/", "-")
            
            except (TypeError, AttributeError):
            
                filename = x.find('IcaoCode').text;
                filename = filename.replace("/", "-")

            print ('Baixando.. ' + filename + '')
        
            urllib.request.urlretrieve(x.find('link').text, '' + directory + '/' + filename + '.pdf')
            
    else:

        print("Pular Cartas Em Rota")

    # CARTAS VFR

    if CartasVFR:

        urllib.request.urlretrieve('http://www.aisweb.aer.mil.br/api/?apiKey=1697016245&apiPass=3199c002-755b-1033-a49b-72567f175e3a&area=cartas&especie=VFR', 'cycle_vfr.xml')
        sleep(5)

        tree = ET.parse('cycle_vfr.xml')
        root = tree.getroot()

        for x in root.iter('item'):
        
            directory = 'cartas_vfr/' + x.find('tipo').text + '';
        
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise


            filename = x.find('nome').text;

            try:
            
                filename = filename.replace("/", "-")
            
            except (TypeError, AttributeError):
            
                filename = x.find('IcaoCode').text;
                filename = filename.replace("/", "-")

            print ('Baixando.. ' + filename + '')
        
            urllib.request.urlretrieve(x.find('link').text, '' + directory + '/' + filename + '.pdf')

    else:

        print("Pular Cartas VFR")


    # Mensagem
    tkinter.messagebox.showinfo("DECEA Downloader", "Cartas baixadas com sucesso!")
    sys.exit()


# Objetos tKinter

# Aeroportos
aeroportosLabel = Label(top, text="Aeroportos (Separados por Vírgula):")
aeroportosLabel.grid(row=1,column=0)
aeroportos = Entry(top, bd =5)
aeroportos.grid(row=1,column=1)

# Cartas IFR Desejadas
CartasIFR = IntVar()
C1 = Checkbutton(top, text = "Cartas IFR (SID, STAR, etc)", variable = CartasIFR)
C1.grid(sticky="W",row=0,column=0)

# Tipos de Cartas IFR Desejadas
tiposLabel = Label(top, text="Tipo de Cartas (Separados por Vírgula):")
tiposLabel.grid(row=2,column=0)
tipos = Entry(top, bd =5)
tipos.grid(row=2,column=1)
tipos.insert(END, 'ADC,AOC,GMC,IAC,PATC,PDC,SID,STAR,VAC')

# Cartas Emrota IFR
CartasEmrotaIFR =  IntVar()
C2 = Checkbutton(top, text = "Cartas Em Rota (ENRC H1, ENRC H2)", variable = CartasEmrotaIFR)
C2.grid(sticky="W",row=3,column=0)

# Cartas VFR
CartasVFR = IntVar()
C3 = Checkbutton(top, text = "Cartas VFR (WAC,REA)", variable = CartasVFR)
C3.grid(sticky="W",row=4,column=0)

# Botão de Download
B = tkinter.Button(top, text ="Download", command = download)
B.grid(row=5,column=0)

# Configurações da Janela
top.title("DECEA Downloader")
top.iconbitmap('dom-decea.ico')

# Main Loop
top.mainloop()
