% Comprueba si estamos ejecutando en MATLAB o en Octave
if (exist('OCTAVE_VERSION', 'builtin') ~= 0)
  % Estamos en Octave
  pkg load signal;
end

% Menu principal
opcion = 0;
while opcion ~= 10
  % Menu de opciones
  disp('Seleccione una opcion: ')
  disp('1. Grabar ')
  disp('2. Reproducir ')
  disp('3. Graficar ')
  disp('4. Graficar Densidad ')
  disp('5. Ejercicio Practica 4')
  disp('6. Ejercicio practica 5')
  disp('7. escuchar audio con transformada z')
  disp('8. Practica 6')
  disp('9 escuchar 6')
  disp('10. Salir')
  opcion = input('Ingrese su selección: ');

  switch opcion
    case 1
      % Grabación de audio
      try
        duracion = input('Ingrese la duración de la grabación en segundos: ');
        disp('Comenzando la grabación.....');
        recObj=audiorecorder;
        recordblocking(recObj, duracion);
        disp('Grabación finalizada.');
        data =getaudiodata(recObj);
        audiowrite('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav', data, recObj.SampleRate);
        disp('Archivo de audio grabado y guardado correctamente.');
      catch
        disp('Error al grabar el audio.');
      end_try_catch
    case 2
      % Reproducción de audio
      try
        [data,fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav');
        disp('Reproducción de audio......');
        sound(data,fs);
        disp('Reproducción de Finalizada');
      catch
        disp('Error al reproducir el audio.');
      end_try_catch
    case 3
      % Gráfica de audio en el dominio del tiempo
      try
        [data,fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav');
        tiempo=linspace(0,length(data)/fs, length(data));
        plot(tiempo,data);
        xlabel('Tiempo (s)');
        ylabel('Amplitud');
        title('Audio')
      catch
        disp('Error al graficar el audio.');
      end_try_catch
    case 4
      % Gráfica de la densidad espectral de potencia del audio
      try
        disp('graficando espectro de frecuencia');
        [audio,Fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav'); %lee la señal desde el archivo .wav
        N=length(audio); %numero de muestras de la señal
        f=linspace(0,Fs/2,N/2+1); %Vector de frecuencias
        ventana =hann(N);%Ventana de Hann para reducir el efecto de las discontinuidades al calcular la FFT
        Sxx=pwelch(audio,ventana,0,N,Fs); %Densidad espectral de potencia
        plot(f,10*log10(Sxx(1:N/2+1)));%grafica el espectro de frecuencia en dB
        xlabel('Frecuencia (Hz)');
        ylabel('Densidad espectral de potencia (dB/Hz)');
        title('Espectro de frecuencia de la señal grabada');

      catch
        disp('ErrSSor al graficar el audio');
      end_try_catch
    case 5
      try
        % Cargar el archivo de audio
        [input_signal, fs] = audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav');
        % Diseñar el filtro RFI
        fc = 1000; % frecuencia de corte
        bw = 500; %ancho de banda

        % Calcule la frecuencia normalizada
        Wn = [fc-bw/2, fc+bw/2]/(fs/2);

        % Diseñar el filtro Butterworth de segundo orden
        [b, a] = butter(2, Wn);

        % Diseñar el filtro Notch de segundo orden para eliminar interferencias
        fn = 1200; % frecuencia de interferencia
        Wn_notch = fn/(fs/2);
        [b_notch, a_notch] = pei_tseng_notch(Wn_notch, 0.1);

        % Combinar los dos filtros en serie
        b_total = conv(b, b_notch);
        a_total = conv(a, a_notch);

        % Aplicar el filtro RFI a la serial de audio
        filtered_signal_RFI = filter(b_total, a_total, input_signal);

        % Diseñar el filtro RII
        fc = 1000; % frecuencia de corte
        gain = 20; % ganancia en la banda de paso

        % Calcule la frecuencia normalizada
        Wn = fc/(fs/2);

        % Disefiar el filtro Chebyshev de tercer orden con un polo real y dos polos coniplejos conjugados
        [b, a] = cheby1(3, gain, Wn, 'high');

        % Aplicar el filtro RII a la serial de audio
        filtered_signal_RII = filter(b, a, filtered_signal_RFI);

        % Graficar la serial de audio original
        t = 0:1/fs:(length(input_signal)-1)/fs;
        figure();
        plot(t, input_signal);
        xlabel('Tiempo (s)');
        ylabel('Amplitud');
        title('Serial original');


        % Graficar la serial de audio filtrada con el filtro RFI
        t = 0:1/fs:(length(filtered_signal_RFI)-1)/fs;
        figure();
        plot(t, filtered_signal_RFI);
        xlabel('Tiempo (s)');
        ylabel('Amplitud');
        title('Serial filtrada con filtro RFI');

        %graficar la señal de audio filtrada con el filtro RII
        t = 0:1/fs:(length(filtered_signal_RII)-1)/fs;
        figure();
        plot(t, filtered_signal_RII);
        xlabel('Tiempo (s)');
        ylabel('Amplitud');
        title('Serial filtrada con filtro RII');


      catch
    end_try_catch

case 6
    %Leer archivo de audio WAV
[x,fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav');

%Convertir a señal monoaural
x=mean(x,2);

%Calcular la transformada Z
z=tf(x,1);

%Obtener coeficientes de la transformada Z
[b,a]=tfdata(z);

% Asegurar que b y a sean vectores de columna
[b,] = size(b);
[a,] = size(a);
if b<a
b = b';
end
if a<b
a = a';
end

%Aplicar transformada Z al archivo de audio.
y=filter(b,a,x);

%Graficar señal original y señal con transformada z aplicada
t=0:1/fs:(length(x)-1)/fs;
subplot(2,1,1);
plot(t,x);
xlabel("Tiempop(s)");
ylabel("Amplitud");
title("Señal Original");

subplot(2,1,2);
plot(t,y);
xlabel("Tiempo(s)");
ylabel("Amplitud");
title("Señal con transformada Z aplicada");
%Escribir archivo de audio WAV con transformada Z aplicada
audiowrite("C:\Users\santo\Documents\Comunicaciones 4 USAC\Archivo_audio_con_Z.wav",y,fs);


case 7
%Escribir archivo de audio WAV con transformada Z aplicada
#audiowrite("Archivo_audio_con_Z.wav",y,fs);

try
        [data,fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\Archivo_audio_con_Z.wav');
        disp('Reproducción de audio......');
        sound(data,fs);
        disp('Reproducción de Finalizada');
      catch
        disp('Error al reproducir el audio.');
      end_try_catch
case 8
   pkg load signal
  #leer archivo de audio
[y,fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\audio.wav')

#Realizar DCT
dct_y=dct(y);

#establecer el umbral para la compresión
umbral=0.1;

#comprimir DCT
dct_y_comprimido=dct_y.*(abs(dct_y)>umbral);

#realizar la inversa de la DCT para obtener el archivo de audio comprimido

y_comprimido=idct(dct_y_comprimido);

#graficar el archivo inicial y finalizada

t=(0:length(y)-1)/fs;
t_comp=(0:length(y_comprimido)-1)/fs;
subplot(2,1,1);
plot(t,y);
title('Archivo de audio inicial');
xlabel('Tiempo (s)');
ylabel('Amplitud');

subplot(2,1,2);
plot(t_comp,y_comprimido);
title('Archivo de audio comprimido');
xlabel('Tiempo (s)');
ylabel('Amplitud');
audiowrite("C:\Users\santo\Documents\Comunicaciones 4 USAC\Archivo_audio_comprimido.wav",y_comprimido,fs);

case 9
try
        [data,fs]=audioread('C:\Users\santo\Documents\Comunicaciones 4 USAC\Archivo_audio_comprimido.wav');
        disp('Reproducción de audio......');
        sound(data,fs);
        disp('Reproducción de Finalizada');
      catch
        disp('Error al reproducir el audio.');
      end_try_catch
    case 10
      % Salir del programa
      disp('Saliendo del programa...')


    otherwise
      % Opción inválida
      disp('Opcion invalida. Intente de nuevo.')
  endswitch
endwhile

