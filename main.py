import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import os
import webbrowser

audio = sr.Recognizer()
maquina = pyttsx3.init()


dormindo = False

def executa_comando():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voz = audio.listen(source)
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

def comando_navegador():
    os.system('start Chrome.exe')
    maquina.say('Abrindo navegador')
    maquina.runAndWait()

def comando_spotify():
    os.system('start Spotify')
    maquina.say('Abrindo Spotify')
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
            elif 'navegador' in comando:
                comando_navegador()
            elif 'spotify' in comando:
                comando_spotify()
            elif 'abra' in comando:
                comando_abra(comando)
            elif 'ligue o fortnite' in comando:
                comando_fortnite()
            elif 'durma java' in comando:
                dormindo = True
                maquina.say('Java está dormindo. Não vou ouvir comandos.')
                maquina.runAndWait()
            elif 'desligue java' in comando:
                print("Encerrando o programa...")
                break
