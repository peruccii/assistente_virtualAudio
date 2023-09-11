import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import os
import webbrowser
import openai
from decouple import config
import pyautogui
import time
from selenium import webdriver
from pynput.keyboard import Key, Controller
import threading

keyboard = Controller()

audio = sr.Recognizer()
maquina = pyttsx3.init()

openai.api_key = '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'
model_engine = "text-davinci-003"
prompt = 'Hello, how are you today?'

eu = config('EU_NUMBER')
rose = config('MOM_NUMBER')


audio.energy_threshold = 4000

dormindo = False



def executa_comando():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio.pause_threshold = 1
            voz = audio.listen(source, timeout=1,phrase_time_limit=5)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            return comando
    except sr.UnknownValueError:
        print("Não foi possível entender o comando.")
        return ""
    except sr.RequestError:
        print("Não foi possível acessar o serviço de reconhecimento de fala.")
        return ""
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return ""

def comando_horas():
    hora = datetime.datetime.now().strftime('%H:%M')
    maquina.say('Agora são ' + hora)
    maquina.runAndWait()

def comando_toque(comando):
    musica = comando.replace('toque', '')
    resultado = pywhatkit.playonyt(musica)
    maquina.say('Tocando Música')
    maquina.runAndWait()
        
def pesquisa_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)
    
def youtube():
    url = "https://www.youtube.com/"
    webbrowser.open_new_tab(url)
    
def comando_spotify():
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('Spotify')
    time.sleep(1)
    pyautogui.press('enter')
    maquina.runAndWait()

def comando_fortnite():
    webbrowser.open("com.epicgames.launcher://apps/fn%3A4fe75bbc5a674f4f9b356b5c90567da5%3AFortnite?action=launch&silent=true")
    maquina.say('Abrindo Fortnite')
    maquina.runAndWait()

def comando_abra(comando):
    app = comando.replace('abra', '').strip()
    app = app.replace(' ', '')
    url = "https://www.{}.com".format(app)
    webbrowser.open_new_tab(url)
    maquina.say('Abrindo {}'.format(app))
    maquina.runAndWait()
    
def chatgpt():
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    response = completion.choices[0].text
    print(response)
    
def desligar():
    maquina.say("Deseja desligar o computador ?")
    maquina.runAndWait()
    comando = executa_comando()
    if 'sim' in comando:
        maquina.say("Desligando o computador")
        maquina.runAndWait()
        os.system('shutdown /s /f /t 0')
    if 'nao' in comando:
        maquina.say("Ok")
        maquina.runAndWait()
        
        
def enviar_mensagem(numero, mensagem):
    pywhatkit.sendwhatmsg_instantly(numero, mensagem, tab_close=True)
    time.sleep(5)
    pyautogui.press('enter')
    maquina.say(f'Mensagem para {numero} enviada com sucesso.')
    maquina.runAndWait()
    
def comando_envia_mensagem(comando): 
    eu = config('EU_NUMBER')  
    rose = config('MOM_NUMBER')
    if 'mensagem para eu' in comando:
        numero = eu
        mensagem = comando.split(' ', 3)[-1].strip()
        enviar_mensagem(numero, mensagem)
    elif 'mensagem para rose' in comando:
        numero = rose
        mensagem = comando.split(' ', 3)[-1].strip()
        enviar_mensagem(numero, mensagem)
        


while True:
    comando = executa_comando()
    
    if dormindo:
        if 'acorde java' in comando:
            dormindo = False
            maquina.say('Java acordou. Estou ouvindo novamente.')
            maquina.runAndWait()
    else:
        if comando:
            if 'horas' in comando:
                comando_horas()
            elif 'toque' in comando:
                comando_toque(comando)
            elif 'pesquisar' in comando or 'Google' in comando:
               
                query = comando.replace('pesquisar', '').replace('Google', '').strip()
                pesquisa_google(query)
            elif 'spotify' in comando:
                comando_spotify()
            elif 'abra' in comando:
                comando_abra(comando)
            elif 'desligue' in comando:
                desligar()
            elif 'ligue o fortnite' in comando:
                comando_fortnite()
            elif 'carro' in comando:
                chatgpt()
            elif 'mensagem para' in comando:
                comando_envia_mensagem(comando)
            elif 'durma java' in comando:
                dormindo = True
                maquina.say('Java está dormindo. Não vou ouvir comandos.')
                maquina.runAndWait()
            elif 'desligue java' in comando:
                print("Encerrando o programa...")
                break
