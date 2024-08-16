import serial
import time
import binascii
import logging
import os
import sys

# Configurações básicas
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_PORT_TIMEOUT = 1
INTERVALO_SERIAL = 1  # Intervalo de 1 segundo
UPS_BATERY_LEVEL = 15

# Comando para o nobreak
CMD_QUERY = "51 ff ff ff ff b3 0d"

# Função de inicialização do logger
def iniciaLogger():
    log = logging.getLogger('ups_monitor')
    hdlr = logging.FileHandler('ups_monitor.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    return log

log = iniciaLogger()

# Função para abrir a porta serial
def abre_serial():
    try:
        ser = serial.Serial(SERIAL_PORT,
                            baudrate=2400,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=SERIAL_PORT_TIMEOUT)
        log.info(f"Port {SERIAL_PORT} - is open: {ser.isOpen()}")
        return ser
    except Exception as e:
        log.error(f"Unable to open the serial port {SERIAL_PORT}: {str(e)}")
        return None

# Função para enviar comando e receber resposta
def send_command(ser, cmd):
    try:
        cmd_bytes = bytearray.fromhex(cmd)
        for cmd_byte in cmd_bytes:
            hex_byte = "{0:02x}".format(cmd_byte)
            ser.write(bytearray.fromhex(hex_byte))
            time.sleep(0.100)
        response = ser.read(32)
        return binascii.hexlify(bytearray(response))
    except serial.SerialException as e:
        log.error(f"Serial error: {str(e)}")
        return ""
    except Exception as e:
        log.error(f"Error sending command: {str(e)}")
        return ""

# Função para tratar a resposta do nobreak
def trataRetorno(rawData):
    rData = rawData.lower()
    if len(rData) == 0:
        return None
    if isinstance(rData, str):
        rData = bytearray.fromhex(rData)
        rData = binascii.hexlify(rData)
    tmp = []
    if rData[0:2] != b'3d':
        log.error('String error!')
        return None
    tmp.append(rData[0:2])
    for i in range(2, 36, 4):
        tmp.append(rData[i:i+4])
    return tmp

# Função para extrair dados do nobreak
def dadosNoBreak(lista):
    if lista is None:
        log.error("No UPS Data")
        return {'noData': True}
    noBreak = {
        'noData': False,
        'batterylevel': int(lista[6], 16) / 10
    }
    return noBreak

# Função principal para obter e verificar o nível da bateria
def query_battery_level(ser):
    raw_data = send_command(ser, CMD_QUERY)
    lista_dados = trataRetorno(raw_data)
    ups_data = dadosNoBreak(lista_dados)
    return ups_data

# Função para desligar o computador
def shutdown_computer():
    log.warning("Battery level critical. Shutting down the computer.")
    if os.name == 'nt':  # Windows
        os.system('shutdown /s /t 1')
    elif os.name == 'posix':  # Unix/Linux/Mac
        os.system('sudo shutdown now')

# Loop principal para imprimir o nível da bateria no console a cada segundo
def main():
    ser = abre_serial()
    if ser is None:
        sys.exit(1)
    while True:
        ups_data = query_battery_level(ser)
        if ups_data['noData']:
            print("No UPS Data")
        else:
            print(f"Battery level: {ups_data['batterylevel']}%")
            if ups_data['batterylevel'] < UPS_BATERY_LEVEL:
                shutdown_computer()
        time.sleep(INTERVALO_SERIAL)

if __name__ == "__main__":
    main()