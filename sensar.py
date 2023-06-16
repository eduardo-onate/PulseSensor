# Intento Chat GPT

import spidev
import time
import json
from procesar import procesar

# Configuración del ADC MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, dispositivo 0
spi.max_speed_hz = 1000000  # Velocidad de transmisión del SPI (1 MHz)

def read_adc(channel):
    # Lee el valor analógico del ADC MCP3008 en el canal especificado (0-7)
    adc = spi.xfer2([1, 8 + channel << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

pulsos = [-1] * 2000
print('Atención: la medición dura 10 segundos.')
try:
    for i in range(2000):
        # Lee el valor del pulso cardiaco del canal 0 del ADC y se guarda
        # en la lista 'pulsos'
        pulsos[i] = read_adc(0)

        if i % 200 == 0:
            if i != 0:
                print(round(i/200))
        # Espera un tiempo antes de la siguiente lectura
        time.sleep(0.005)

    print('Listo')
    # print(pulsos)

    with open("pulsos.json", "w") as fp:
        json.dump(pulsos, fp)

    procesar(pulsos)


except KeyboardInterrupt:
    spi.close()  # Cierra la conexión SPI al finalizar