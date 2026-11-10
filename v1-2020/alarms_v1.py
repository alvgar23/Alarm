# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:41:27 2020

@author: alvar
"""

""" 
Program countdown with alarm. It says how much time is left to the end.
It takes a sound of alarm that it must be in the project and needs to be mp3.
"""


"""
Import some necessary modules, time and pygame. pyautogui para el hover mouse.
"""

from time import perf_counter, sleep
from pygame import mixer #mixer plays sounds
import pyautogui



"""
Define the functions
"""

def menu():
    menu = """    MENÚ
    Tiempos en segundos para cada actividad:
    1. Abdominales.
    2. Flexiones.
    3. Flexibilidad.
    4. Muslos.
    5. Preparación.
    6. Machine Learning.
    7. Python.
    8. Languages.
    9. TFG.
   10. Introducir el tiempo de forma manual.
   11. Hover Mouse antiblock. Suma 10 segundos al tiempo introducido.
   12. Salir
    """
    print(menu)



def to_seconds(h, m, s):
    
    """
    Converts the time given in hours, minutes and seconds to seconds.
    """
    
    print("\n",int(h), "horas", int(m), "minutos", int(s), "segundos son...")
    time = int(h * 60 * 60 + m * 60 + s)
    print("...",time, "segundos\n")
    
    return time



def eleccion():
    
    """
    User chooses an option from menu. The nine first choices are predefined.
    The 10th allows to the user to introduce the time and it will call to the
    function to_seconds(). 11th closes the program.
    """
    
    while True:
        
        try:
            
            menu()
            opt = int(input("Select your choice: "))
        
        except ValueError:
            print("Invalid option. Try again", end="")
            sleep(1)
            print(".", end="")
            sleep(1)
            print(".", end="")
            sleep(1)
            print(".")
            sleep(1)
        
        else:
            
            if opt == 1:
                t_prueba = 1680
            if opt == 2:
                t_prueba = 1200
            if opt == 3:
                t_prueba = 600
            if opt == 4:
                t_prueba = 600
            if opt == 5:
                t_prueba = 240
            if opt == 6:
                t_prueba = 5400
            if opt == 7:
                t_prueba = 5400
            if opt == 8:
                t_prueba = 5400
            if opt == 9:
                t_prueba = 7200
            if opt == 10 or opt == 11:
                t_prueba = user_time()
            if opt >= 12 or opt <= 0:
                t_prueba = -1 #to get -1 when we want to exit
                print("Ending the program", end="")
                sleep(1)
                print(".", end="")
                sleep(1)
                print(".", end="")
                sleep(1)
                print(".", end="")
                sleep(1)
                print("\nTHE PROGRAM WAS CLOSED SUCCESFULLY.")
            
            break #ends the loop
            
    return t_prueba, opt 
    


def user_time():
    
    """
    When the option selected is 10, we introduce manually the time
    """
    
    while True:
        
        try:
            
            h = float(input("Introduce the number of hours: "))
            m = float(input("Introduce the minutes: "))
            s = float(input("Introduce the seconds: "))
        
        except ValueError:
            
            print("Introduce a number.")
        
        else:
            
            while h<0 or m<0 or s<0: #if a negative number is introduced
                
                print("Introduce a positive number.") 
                h = float(input("Introduce the number of hours: "))
                m = float(input("Introduce the minutes: "))
                s = float(input("Introduce the seconds: "))
            
            t_prueba = to_seconds(h,m,s)
            break
        
    return t_prueba



def alarm(t_prueba):
    
    """
    It starts to discount time through the time obtained by parameter.
    From the second 10 the siren starts to sound and once it arrives to 0, the
    sound is played.
    """
    
    t_final = 0 # to show the first time the time
    t_inicial = perf_counter()  #starts the time
    
    while True:
        s = (t_prueba - t_final) % 60 #seconds left
        m = ((t_prueba - t_final) // 60) % 60 #minutes left
        h = ((t_prueba - t_final) // 60) // 60 #hours left
        
        if h != 0 and m!= 0 and s != 0: #111
            print("Quedan",int(h),"horas", int(m),"minutos",int(s),"segundos...")
        elif h != 0 and m != 0 and int(s) == 0: #110
            print("Quedan", int(h),"horas", int(m),"minutos...")
        elif h != 0 and int(m) == 0 and s != 0: #101
            print("Quedan",int(h),"horas", int(m),"minutos",int(s),"segundos...")
        elif h != 0 and int(m) == 0 and int(s) == 0: #100
            print("Quedan",int(h),"horas...")
        elif int(h) == 0 and m != 0 and s != 0: #011
            print("Quedan", int(m),"minutos", int(s), "segundos...")
        elif int(h) == 0 and m != 0 and int(s) == 0:
            print("Quedan", int(m),"minutos...") #010
        elif int(h) == 0 and int(m) == 0: #000 and 001
            print("Quedan", int(s), "segundos...")
        
        t_final = perf_counter() - t_inicial
        sleep(1)
        
        if t_prueba - t_final <= 10: #Empieza a sonar cuando faltan 10 segundos
            mixer.init()
            mixer.music.load("sirena.mp3")
            mixer.music.play()
            
            if t_prueba - t_final <= 0: #cuando llega a 0 reproduce toda
                print("EL TIEMPO HA ACABADO")
                break


def hover_mouse(t_prueba):
    
    """
    Countdown like the alarm, but each 5 seconds it moves the mouse for 
    0.2 seconds to avoid the computer screen is blocked.
    It adds 10 more seconds to sound the alarm.
    """
    
    t_final = 0 # to show the first time the time
    t_inicial = perf_counter()  #starts the time
    
    while t_prueba - t_final > 0:
        t_final = perf_counter() - t_inicial

        # Mover el mouse cada 5 segundos
        if int(t_final) % 5 == 0:
            x, y = pyautogui.position()
            pyautogui.moveTo(x + 10, y + 10, duration=0.2)
            pyautogui.moveTo(x, y, duration=0.2)

        # Mostrar el tiempo restante
        s = (t_prueba - t_final) % 60
        m = ((t_prueba - t_final) // 60) % 60
        h = ((t_prueba - t_final) // 60) // 60
        print(f"Quedan {int(h)} horas, {int(m)} minutos, {int(s)} segundos...")
        sleep(1)

    alarm(10)  # Alarma final

"""
We call the functions to execute the program. First, the menu and then we
obtain the value of t_prueba (time of test) calling to election().
The function alarm() only is executed if the chosen option by the user in 
election is not 11 (exit)
"""

menu()
t_prueba, opt = eleccion()
if t_prueba != -1 and opt != 11:   #if opt=11, t_prueba=-1
    alarm(t_prueba)  #t_prueba as argument

if t_prueba != -1 and opt == 11:   #if opt=11, t_prueba=-1
    hover_mouse(t_prueba)  #t_prueba as argument

