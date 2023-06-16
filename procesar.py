import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

def media_movil(n, lista):
    # Retorna la media móvil de una lista considerando n elementos.
    nueva_lista = []
    ventana = []

    for i in range(len(lista)):
        ventana.append(lista[i])

        if len(ventana) > n:
            ventana.pop(0)

        suma = sum(ventana)
        promedio = suma / len(ventana)
        nueva_lista.append(promedio)

    return nueva_lista


def procesar(a, d=100):

    # Se filtra la señal usando una media móvil de largo 50.
    avg = media_movil(50, a)
    mx = max(avg)
    mn = min(avg)

    # Nos quedamos con las últimas 1200 muestras (6 segundos) para eliminar el ruido inicial de la medición.
    t = range(1200)
    x = avg[800:]

    # Encontramos los peaks de la señal con la librería scipy.
    # Para evitar ruido, la distancia mínima entre peaks será de 80 muestras.
    # Se muestrea cada 5 milisegundos: 80 muestras <-> 0.4 segundos.
    # Por ende, la máxima frecuencia cardiaca a sensar será de (60 s/min) / 0.4 (s/beat) = 150 BPM.
    p = scipy.signal.find_peaks(x, distance=d)[0]

    # Encontramos mínimo y máximo de la señal para poder escalar el gráfico.
    mx = max(x)
    mn = min(x)
    ax = plt.gca()
    ax.set_ylim([mn-2, mx+2])

    # Asumiendo que los BPM en la medición de 6 segundos fue constante, el número
    # de muestras promedio entre peaks será el índice + 1 del último peak en la
    # muestra, dividido por el total de peaks.
 m_prom = (p[-1]+1)/len(p)
    print(f'Muestras promedio entre latidos: {round(m_prom)}')

    # El tiempo promedio entre peaks (pulsos) es el número de muestras promedio
    # entre pulsos por el periodo de muestreo.
    t_prom = m_prom*0.005 # Ts = 5 ms
    print(f'Tiempo promedio entre latidos: {round(t_prom*1000)} milisegundos')

    # Pulsaciones por minuto.
    bpm = 60/t_prom
    print(f'BPM: {round(bpm)}')

    # Graficamos la señal y sus peaks
    plt.plot(t, x)
    plt.scatter([t[i] for i in p], [x[i] for i in p], c='r')
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200], \
              [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
    plt.title('Pulsaciones')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Pulsaciones')

    import os
    my_path = os.path.abspath(__file__) # Figures out the absolute path for you in case your working directory moves ar>    
    # plt.savefig('/home/pi/var/www/html/img2.png')
    #os.remove('/var/www/html/img.png')
    #plt.savefig('/var/www/html/img.png')
    os.remove("/var/www/html/img4.png")
    plt.savefig("img4.png")
    plt.savefig("/var/www/html/img4.png")
    # plt.show()

    return bpm