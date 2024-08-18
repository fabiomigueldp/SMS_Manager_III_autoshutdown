
# autoshtdwn.py

## English Version

This project contains a Python script named `autoshtdwn.py`, designed to monitor the battery level of a UPS connected via a serial port (`/dev/ttyUSB0`). If the battery level falls below a specified threshold, the script will automatically shut down the computer to prevent data loss.

### Prerequisites

- Python 3.x
- `pyserial` library: Install with `pip install pyserial`
- Access to the serial device `/dev/ttyUSB0`

### Script Overview

The script performs the following actions:
1. Opens a serial connection to the UPS.
2. Sends a command to the UPS to retrieve the battery status.
3. Parses the response and checks the battery level.
4. If the battery level is below the defined threshold (default: 15%), it triggers a system shutdown.

### Installation and Setup

#### 1. Save the Script

Save the `autoshtdwn.py` script in the desired directory, for example, `/path/to/your/script/`.

#### 2. Create a Systemd Service

To run the script automatically at startup and restart it in case of failure, create a systemd service:
1. Create the service file:
   ```bash
   sudo nano /etc/systemd/system/autoshtdwn.service
   ```
2. Add the following content, replacing placeholders with appropriate values:
   ```ini
   [Unit]
   Description=Script to monitor UPS battery level and shutdown the computer if necessary
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/your/script/autoshtdwn.py
   WorkingDirectory=/path/to/your/script/
   Restart=always
   User=your_user
   Group=your_group
   StandardOutput=syslog
   StandardError=syslog
   SyslogIdentifier=ups_monitor
   Environment=PYTHONUNBUFFERED=1

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and start the service:
   ```bash
   sudo systemctl enable autoshtdwn.service
   sudo systemctl start autoshtdwn.service
   ```

#### 3. Adjust Permissions

Ensure your user is part of the `dialout` group to allow the script to access the serial port (`/dev/ttyUSB0`):
```bash
sudo usermod -aG dialout your_user
```
You may need to log out and log back in for the group change to take effect.

#### 4. Configure Shutdown Command

The default shutdown command in the script uses the system's shutdown utility. To configure this command to run without requiring a password:
1. Open the sudoers file:
   ```bash
   sudo visudo
   ```
2. Add the following line at the end of the file, replacing `your_user` with your actual username:
   ```bash
   your_user ALL=(ALL) NOPASSWD: /sbin/shutdown
   ```
This configuration allows the user to execute the `shutdown` command without a password, enabling the script to initiate a shutdown without user interaction.

#### 5. Check the Service Status

To verify that the service is running correctly:
```bash
sudo systemctl status autoshtdwn.service
```

### Logging

The script logs its activities in two places:
- **Console Output:** Displays real-time battery status.
- **Log File (`ups_monitor.log`):** Stores error and status messages for later review.

### Customization

Adjust these script settings as needed:
- **Battery Threshold:** Modify the `UPS_BATERY_LEVEL` variable to change the shutdown threshold.
- **Serial Port:** Change the `SERIAL_PORT` variable if your UPS is connected to a different port.
- **Shutdown Command:** Adjust the shutdown command if using a non-Unix/Linux/Mac system.

### Useful Commands

Manage and troubleshoot the UPS monitoring script with these commands:
- **Start/Stop/Restart the Service:**
   ```bash
   sudo systemctl start|stop|restart autoshtdwn.service
   ```
- **View Real-Time Logs:**
   ```bash
   journalctl -u autoshtdwn.service -f
   ```
- **Enable/Disable Service at Boot:**
   ```bash
   sudo systemctl enable|disable autoshtdwn.service
   ```

### License

This project is licensed under the MIT License.

---

## Versão em Português

Este projeto contém um script Python chamado `autoshtdwn.py`, projetado para monitorar o nível de bateria de um nobreak conectado via uma porta serial (`/dev/ttyUSB0`). Se o nível da bateria cair abaixo de um limite especificado, o script desligará automaticamente o computador para evitar perda de dados.

### Pré-requisitos

- Python 3.x
- Biblioteca `pyserial`: Instale com `pip install pyserial`
- Acesso ao dispositivo serial `/dev/ttyUSB0`

### Visão Geral do Script

O script executa as seguintes ações:
1. Abre uma conexão serial com o nobreak.
2. Envia um comando ao nobreak para recuperar o status da bateria.
3. Analisa a resposta e verifica o nível da bateria.
4. Se o nível da bateria estiver abaixo do limite definido (padrão: 15%), ele aciona o desligamento do sistema.

### Instalação e Configuração

#### 1. Salve o Script

Salve o script `autoshtdwn.py` no diretório desejado, por exemplo, `/path/to/your/script/`.

#### 2. Crie um Serviço Systemd

Para executar o script automaticamente na inicialização e reiniciá-lo em caso de falha, crie um serviço systemd:
1. Crie o arquivo de serviço:
   ```bash
   sudo nano /etc/systemd/system/autoshtdwn.service
   ```
2. Adicione o seguinte conteúdo, substituindo os marcadores pelos valores apropriados:
   ```ini
   [Unit]
   Description=Script para monitorar o nível da bateria do nobreak e desligar o computador se necessário
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/your/script/autoshtdwn.py
   WorkingDirectory=/path/to/your/script/
   Restart=always
   User=your_user
   Group=your_group
   StandardOutput=syslog
   StandardError=syslog
   SyslogIdentifier=ups_monitor
   Environment=PYTHONUNBUFFERED=1

   [Install]
   WantedBy=multi-user.target
   ```
3. Habilite e inicie o serviço:
   ```bash
   sudo systemctl enable autoshtdwn.service
   sudo systemctl start autoshtdwn.service
   ```

#### 3. Ajuste as Permissões

Certifique-se de que seu usuário faça parte do grupo `dialout` para permitir que o script acesse a porta serial (`/dev/ttyUSB0`):
```bash
sudo usermod -aG dialout your_user
```
Você pode precisar fazer logout e login novamente para que a alteração de grupo tenha efeito.

#### 4. Configure o Comando de Desligamento

O comando de desligamento padrão no script usa a utilidade de desligamento do sistema. Para configurar este comando para ser executado sem exigir uma senha:
1. Abra o arquivo sudoers:
   ```bash
   sudo visudo
   ```
2. Adicione a seguinte linha no final do arquivo, substituindo `your_user` pelo seu nome de usuário real:
   ```bash
   your_user ALL=(ALL) NOPASSWD: /sbin/shutdown
   ```
Essa configuração permite que o usuário execute o comando `shutdown` sem senha, permitindo que o script inicie um desligamento sem interação do usuário.

#### 5. Verifique o Status do Serviço

Para verificar se o serviço está funcionando corretamente:
```bash
sudo systemctl status autoshtdwn.service
```

### Logs

O script registra suas atividades em dois lugares:
- **Saída do Console:** Exibe o status da bateria em tempo real.
- **Arquivo de Log (`ups_monitor.log`):** Armazena mensagens de erro e status para revisão posterior.

### Customização

Ajuste as configurações do script conforme necessário:
- **Limite de Bateria:** Modifique a variável `UPS_BATERY_LEVEL` para alterar o limite de desligamento.
- **Porta Serial:** Altere a variável `SERIAL_PORT` se o seu nobreak estiver conectado a uma porta diferente.
- **Comando de Desligamento:** Ajuste o comando de desligamento se estiver usando um sistema diferente de Unix/Linux/Mac.

### Comandos Úteis

Gerencie e solucione problemas do script de monitoramento do nobreak com esses comandos:
- **Iniciar/Parar/Reiniciar o Serviço:**
   ```bash
   sudo systemctl start|stop|restart autoshtdwn.service
   ```
- **Visualizar Logs em Tempo Real:**
   ```bash
   journalctl -u autoshtdwn.service -f
   ```
- **Habilitar/Desabilitar o Serviço na Inicialização:**
   ```bash
   sudo systemctl enable|disable autoshtdwn.service
   ```

### Licença

Este projeto está licenciado sob a Licença MIT.
