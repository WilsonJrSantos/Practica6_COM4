import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hann, welch, butter, cheby1, convolve, iirnotch, filtfilt
import sounddevice as sd
import wavio
from scipy.signal import stft

import numpy as np 
from scipy.io import wavfile 
import matplotlib.pyplot as plt 
import numpy as np
import scipy.signal as signal   
import scipy.io.wavfile as wav 


# Comprueba si estamos ejecutando en MATLAB o en Octave
if os.getenv('OCTAVE_VERSION') is not None:
    # Estamos en Octave
    from oct2py import Oct2Py
    oc = Oct2Py()
    oc.eval('pkg load signal')

# Menu principal
opcion = 0
while opcion != 10:
    # Menu de opciones
    print('Seleccione una opcion: ')
    print('1. Grabar')
    print('2. Reproducir')
    print('3. Graficar')
    print('4. Graficar Densidad')
    print('5. Practica 4')
    print('6. Practica 5')
    print('7. Reproducir la señal con T Z')
    print('8. práctica 6')
    print('9. audio comprimido')
    print('10. Salir')
    opcion = int(input('Ingrese su selección: '))

    if opcion == 1:
        # Grabación de audio
        try:
            duracion = int(input('Ingrese la duración de la grabación en segundos: '))
            print('Comenzando la grabación.....')
            # Configuración de la grabación
            duracion_grabacion = duracion# duración de la grabación en segundos
            frecuencia_muestreo = 8000 # frecuencia de muestreo en HzS
            num_bits = 16 # número de bits por muestra
            num_canales = 1 # número de canales de grabación (mono)

            # Grabación de la señal de voz
            grabacion = sd.rec(int(duracion_grabacion * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=num_canales, dtype='int16')
            sd.wait()

            # Guardar la señal de voz en un archivo WAV
            
            wavio.write("C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav", grabacion, frecuencia_muestreo, sampwidth=num_bits // 8)
            print('Archivo de audio grabado y guardado correctamente.')

        except:
            print('Error al grabar el audio.')

    elif opcion == 2:
        # Reproducción de audio
        try:
            # Cargar la última señal de voz grabada
            data = wavio.read('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav').data
            senal_grabada = np.array(data, dtype='int16')
            print('Reproduciendo señal de voz...')
            sd.play(senal_grabada, samplerate=frecuencia_muestreo)
            sd.wait()
            print('Reproducción finalizada')
        except:
            print('Error al reproducir el audio.')

    elif opcion == 3:
        # Gráfica de audio en el dominio del tiempo
        try:
            fs, data = wavfile.read('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav')
            tiempo = np.linspace(0, len(data)/fs, len(data))
            plt.plot(tiempo, data)
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud')
            plt.title('Audio')
            plt.show()
        except:
            print('Error al graficar el audio.')

    elif opcion == 4:
        # Gráfica de la densidad espectral de potencia del audio
        try:
            print('graficando espectro de frecuencia')
            fs, audio = wavfile.read('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav')
            N = len(audio)  # numero de muestras de la señal
            f, Sxx = welch(audio, fs, window=hann(N), nperseg=N, scaling='density', detrend=False)
            plt.plot(f, 10*np.log10(Sxx))
            plt.xlabel('Frecuencia (Hz)')
            plt.ylabel('Densidad espectral de potencia (dB/Hz)')
            plt.title('Espectro de frecuencia de la señal grabada')
            plt.show()
        except:
            print('Error al graficar el audio')
    elif opcion ==5:
        #try:
        fs, input_signal = wavfile.read('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav') # cargamos el audio

        # diseño RFI filtro
        fc = 1000 # frecuencia de corte
        bw = 500 # ancho de banda
        #Wn = np.array([fc-bw/2, fc+bw/2])/(fs/2)
        #Wn = [fc-bw/2, fc+bw/2]/(fs/2) #  Frecuencia normalizada
        #Wn = fc/(fs/2)  # Frecuencia crítica normalizada
        #b, a = butter(2, Wn, btype='lowpass')  # Filtro Butterworth de 2° orden pasa bajo 

        #b, a = butter(2, Wn) # filtro Butterworth 2 orden

        Wn = [(fc-bw/2)/(fs/2), (fc+bw/2)/(fs/2)] # frecuencia normalizada

        # Diseñar el filtro Butterworth de segundo orden
        b, a = butter(2, Wn, btype='band')        


        fn = 1200 # frecuencia de interferencia
        Wn_notch = fn/(fs/2) # Frecuencia normalizada
        Q = 0.1 # factor Q
        b_notch, a_notch = iirnotch(Wn_notch, Q) # notch filter
        b_total = convolve(b, b_notch) # combinacion numerador
        a_total = convolve(a, a_notch) # combinacion denominador
        filtered_signal_RFI = filtfilt(b_total, a_total, input_signal) # aplicar filtro

        # diseño  RII filter
        fc = 1000 # frecuencia de corte
        gain = 20 # ganancia
        Wn = fc/(fs/2) # frecuencia normalziada
        b, a = cheby1(3, gain, Wn, 'high') # filtro de 3rd order Chebyshev 
        filtered_signal_RII = filtfilt(b, a, filtered_signal_RFI) # aplicar filtros

        # plot imagen original
        t = np.arange(len(input_signal))/fs
        plt.figure()
        plt.plot(t, input_signal)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitud')
        plt.title('Señal original')

        # Plot señal filtrada RFI
        t = np.arange(len(filtered_signal_RFI))/fs
        plt.figure()
        plt.plot(t, filtered_signal_RFI)
        plt.xlabel('tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title('Serial filtrada con filtro RFI')

        # Plot RII filtered signal
        t = np.arange(len(filtered_signal_RII))/fs
        plt.figure()
        plt.plot(t, filtered_signal_RII)
        plt.xlabel('tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title('Serial filtrada con filtro RII')

        plt.show() # mostrar plots
        #except:
        #    print('Error al graficar el audio')
    elif opcion==6:
#practica 5


        # Leer archivo de audio WAV
        fs, x = wav.read('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav')

        #convertir a señal monoaural
        if len(x.shape) > 1:
            x = np.mean(x, axis=1)

        # Calcular transformada Z
        z = signal.TransferFunction([1.0], [1.0, 0.0], dt=1/fs)

        # Obtener coeficientes de la transformada Z
        b, a = z.num, z.den

        # Aplicar transformada Z al archivo de audio
        y = signal.lfilter(b, a, x)

        # Graficar señal original y señal con transformada Z aplicada
        t = np.arange(len(x))/float(fs)
        plt.subplot(2,1,1)
        plt.plot(t, x)
        plt.xlabel('Tiempo(s)')
        plt.ylabel('Amplitud')
        plt.title('Señal Original')

        plt.subplot(2,1,2)
        plt.plot(t, y)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title('Señal con transformada Z aplicada')

        plt.show()

        # Escribir archivo de audio WAV con transformada Z aplicada
        wav.write('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\archivo_audio_con_Z.wav', fs, y.astype(np.int16))





    elif opcion==7:
       # Reproducción de audio
        try:
            # Cargar la última señal de voz grabada
            dataa = wavio.read('C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\archivo_audio_con_Z.wav').data
            senal_grabadaq = np.array(dataa, dtype='int16')
            print('Reproduciendo señal de voz...')
            sd.play(senal_grabadaq, samplerate=frecuencia_muestreo)
            sd.wait()
            print('Reproducción finalizada')
        except:
            print('Error al reproducir el audio.') 
    elif opcion ==8:
        print("PRACTICA 6")

        # Cargar archivo de audio 
        fs, audio = wavfile.read("C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\audio.wav","r") 
        # Convertir a float entre -1 y 1 
        audio = audio.astype(float)/32768.0 
        # Aplicar la DCT 
        dct = np.fft.rfft(audio) 
        #    Realizar la compresiOn eliminando los coeficientes de menor
        #  magnitud 
        threshold = 0.1*np.max(np.abs(dct)) 
        dct_compressed = dct*(np.abs(dct) >= threshold) 
        # Aplicar la IDCT 
        audio_compressed = np.fft.irfft(dct_compressed) 
        # Graficar archivo de audio inicial y final 
        t = np.arange(len(audio)) / fs 
        plt.subplot(2,1,1) 
        plt.plot(t, audio) 
        plt.title('Archivo de audio inicial') 
        plt.xlabel('Tiempo (seg)') 
        plt.ylabel('Amplitud') 
        plt.subplot(2,1,2) 
        plt.plot(t, audio_compressed) 
        plt.title('Archivo de audio comprimido') 
        plt.xlabel('Tiempo (seg)') 
        plt.ylabel('Amplitud') 
        plt.tight_layout() 
        plt.show() 
        try: 
            wavfile.write("C:\\Users\\santo\\Documents\\Comunicaciones 4 USAC\\Archivo_audio_comprimido.wav", fs, (audio_compressed * 32768.0).astype(np.int16))
            print("Audio gauardado")
        except:
            print("ocurrio un error al guardar el audio")
    elif opcion==9:
               # Reproducción de audio
        try:
            print("Reproduciendo audio comprimido...")
            sd.play(audio_compressed, fs)
            sd.wait()
            print('Reproducción finalizada')
        except:
            print('Error al reproducir el audio.') 
    elif opcion == 8:
        # Salir del programa
        print('Saliendo del programa...')
    else:
        # Opción inválida
        print('Opcion invalida. Intente de nuevo.')
