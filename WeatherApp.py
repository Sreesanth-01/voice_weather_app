#Importing modules
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import requests
import ttkbootstrap
import pyttsx3
import speech_recognition as sr


#Functions
flag=False
def say():
    global city_name
    global flag
    
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source) 
        audio = recognizer.listen(source, timeout=5)
        try:
            city_name = recognizer.recognize_google(audio)
            n1.config(text="You said:"+city_name)
            print("You said:",city_name)
            flag=True
        except :
            print("Sorry, could not understand audio.")
        #except sr.RequestError as e:
            #print("Could not request results from Google Web Speech API; {0}".format(e))
    

        

def speak(text):
    speaker=pyttsx3.init()
    voice=speaker.getProperty("voices")
    speaker.setProperty("voice",voice[1].id)
    speaker.say(text)
    speaker.runAndWait()
    

def voice():
    v1="You have chosen"+city_name.get()+"!   "+"The temperature in"+city_name.get()+"is"+str(t4)+"degree celcius"
    speak(v1)

    v2="Enter another city to find the weather condition or click the close button to exit"
    speak(v2)

def voice_v():
    v1="You have chosen"+city_name+"!   "+"The temperature in"+city_name+"is"+str(t4)+"degree celcius"
    speak(v1)

    v2="Enter another city to find the weather condition or click the close button to exit"
    speak(v2)
    
    

def weather(city):
    api="https://api.openweathermap.org/data/2.5/weather?q="+str(city)+"&appid=2526059c9de4d50d5da9efd3b1d19da1"
    jdata=requests.get(api).json()


    '''if jdata.status_code==404:
        messagebox.showerror("Error!City Not Found")
        return None'''

    
    temp=int((jdata["main"]["temp"])-273.15)//1
    desc=jdata["weather"][0]['description']
    city=jdata["name"]
    country=jdata["sys"]["country"]
    
   
    return(temp,desc,city,country)

def delete():
	etxt.destroy()
	txt1.destroy()
    


def choosed():
    global city_name
    global voice_butt
    global ref_butt

    if clicked.get() == "Manual":
        voice_butt.destroy()
        ref_butt.destroy()
        city_name = tk.Entry(win, text="Enter City Name Here", justify="center")
        city_name.pack()
        b1 = tk.Button(win, text="Show", font=f4, command=done)
        b1.pack(pady=20)
        voice_butt = tk.Button(win, text="Voice", command=voice)
        voice_butt.pack(pady=20)
    elif clicked.get() == "Speak":
        try:
            city_name.destroy()
            b1.destroy()
        except:
            pass
        ref_butt = tk.Button(win, text='Refresh', command=delete)
        ref_butt.pack(pady=40)
        ref_butt['state'] = DISABLED
        if __name__ == "__main__":
            try:
                say()
                if flag:
                    voice_butt['state'] = NORMAL
                    done_v()
                if not flag:
                    etxt.config(text="Sorry couldn't understand. Click refresh and try again")
                    ref_butt['state'] = NORMAL
            except:
                txt1.config(text="Try again")


                  
                  
def done_v():
    global t4
    city=city_name
    data=weather(city)
    if data is None:
        return
    
    temp,desc,city,country=weather(city)
    t3=city+","+country
    location_l.configure(text=t3)

   

    t4=int(temp)
    temp_l.configure(text="Temperature:"+str(t4)+"°C")

    t5="Weather Condition:"+" "+desc
    desc_l.configure(text=t5)
    
def done():
    global t4
    city=city_name.get()
    data=weather(city)
    if data is None:
        return
    
    temp,desc,city,country=weather(city)
    t3=city+","+country
    location_l.configure(text=t3)

   

    t4=int(temp)
    temp_l.configure(text="Temperature:"+str(t4)+"°C")

    t5="Weather Condition:"+" "+desc
    desc_l.configure(text=t5)

def close():
    if messagebox.askokcancel("Exit","Do you want to close?"):
        speak("Thank you for using our weather forecast application!")
        win.destroy()

   
#Fonts
f1=("Helvetica", "24","bold")
f2=("Helvetica", "20","bold")
f3=("Helvetica", "12")
f4=("Helvetica","10")

                     

#GUI structure

win=ttkbootstrap.Window(themename="vapor")
win.title("Weather Forecast")
win.geometry("900x900")
t1=tk.Label(win,text="Weather Forecast",font=f1)
t1.pack(pady=20)

t2=tk.Label(win,text="Find weather condition of any city!",font=f3)
t2.pack(pady=20)

t3=tk.Label(win,text="Choose method of input:",font=f4)
t3.pack(pady=20)

#widgets
clicked=StringVar()
menu=tk.OptionMenu(win,clicked,"Manual","Speak")
menu.pack()

choose_butt=tk.Button(win,text="Choose",font=f4,command=choosed)
choose_butt.pack(pady=20)

cit_nam_l=tk.Label(win,font=f4)
cit_nam_l.pack()

location_l=tk.Label(win,font=f2)
location_l.pack(pady=30)

desc_l=tk.Label(win,font=f2)
desc_l.pack()

temp_l=tk.Label(win,font=f3)
temp_l.pack()

voice_butt=tk.Button(win,text="Voice",command=voice_v)
voice_butt.pack(pady=20)
voice_butt['state']=DISABLED

ref_butt=tk.Button(win,text='Refresh',command=delete)
ref_butt.pack(pady=40)
ref_butt['state']=DISABLED


etxt=tk.Label(win,font=f4)
etxt.pack(pady=10)
txt1=tk.Label(win,font=f4)
txt1.pack()



#Closing
win.protocol("WM_DELETE_WINDOW",close)







win.mainloop()
