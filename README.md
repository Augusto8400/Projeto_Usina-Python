# Fliperama de Partículas Elementares

App em Python (pygame) para rodar num fliperama caseiro feito com
Raspberry Pi, TV vertical, botões e leitor RFID para os cubos do
modelo padrão.

## Estrutura do projeto

```
fliperama/
  main.py                 # ponto de entrada / loop principal
  config.py                # pinos GPIO, resolução, timings
  requirements.txt
  data/
    particles_data.py      # conteúdo de física (partículas, quiz, etc.)
    rfid_map.json           # UID da tag -> partícula (edite aqui!)
    rfid_map.py              # carrega o json
  hardware/
    input_handler.py        # botões (gpiozero ou teclado)
    rfid_reader.py            # leitor MFRC522 em thread
  ui/
    theme.py                 # cores e fontes
    widgets.py                # desenho: estrelas, painéis, menus, tabelas
  screens/
    home.py, cube_reader.py, leptons_quarks.py, antimatter.py,
    hadron_game.py, forces.py, spin.py, quiz.py
  tools/
    descobrir_uid.py         # descobre o UID de cada cubo
  assets/fonts/               # coloque aqui uma fonte .ttf pixelada (opcional)
```

## 1. Testar no PC (sem hardware nenhum)

```bash
pip install pygame
python3 main.py
```

Controles no teclado (modo desenvolvimento, ativado automaticamente
quando `gpiozero` não está disponível):

- **Setas** = cima/baixo/esquerda/direita
- **ENTER / ESPAÇO** = botão A (confirmar)
- **ESC / BACKSPACE** = botão B (voltar)
- **Teclas 1 a 8** = simulam encostar cada um dos 8 cubos no leitor
- **9** = simula "cubo retirado"
- **Ctrl+Q** = sair

## 2. Montagem na Raspberry Pi

### Ligações sugeridas (BCM)

| Componente                | Pino GPIO (BCM)      | Observação                                    |
|-----------------------------|------------------------|--------------------------------------------------|
| Botão de ação                 | GPIO 26              | outro terminal no GND                             |
| Joystick VCC                    | 3.3V                | **não ligue em 5V**                               |
| Joystick GND                      | GND                |                                                    |
| Joystick VRx (eixo X)                | MCP3008 CH0     |                                                    |
| Joystick VRy (eixo Y)                  | MCP3008 CH1   |                                                    |
| MCP3008 VDD / VREF                        | 3.3V        |                                                    |
| MCP3008 AGND / DGND                          | GND       |                                                    |
| MCP3008 CLK                                     | GPIO 11   | SPI SCLK (compartilhado com o RFID)               |
| MCP3008 DOUT                                      | GPIO 9  | SPI MISO (compartilhado com o RFID)               |
| MCP3008 DIN                                         | GPIO 10 | SPI MOSI (compartilhado com o RFID)               |
| MCP3008 CS/SHDN                                       | GPIO 7 | **CE1** — diferente do RFID, que usa CE0 (GPIO 8) |
| MFRC522 SDA/SS                | GPIO 8 (CE0)         | pino fixo do SPI                                  |
| MFRC522 SCK                     | GPIO 11             | SPI SCLK (compartilhado com o MCP3008)            |
| MFRC522 MOSI                       | GPIO 10          | SPI MOSI (compartilhado com o MCP3008)            |
| MFRC522 MISO                          | GPIO 9        | SPI MISO (compartilhado com o MCP3008)            |
| MFRC522 RST                              | GPIO 25    | qualquer GPIO livre (ajustável)                   |
| MFRC522 GND / 3.3V                          | -       | **use 3.3V, não 5V!**                             |

O joystick e o leitor RFID usam o mesmo barramento SPI (CLK/MOSI/MISO são
compartilhados — isso é normal), mas cada um com seu próprio pino de
**chip-select** (CE0 pro RFID, CE1 pro MCP3008), então não há conflito.

Se as direções saírem trocadas ou invertidas na prática (ex.: cima e
baixo trocados), não precisa mexer na fiação — ajuste
`JOYSTICK_INVERT_X` / `JOYSTICK_INVERT_Y` em `config.py`. Se o stick
disparar direção sozinho (ruído/folga mecânica) ou estiver difícil de
disparar, ajuste `JOYSTICK_DEADZONE` (padrão 0.30).

Os pinos do botão e os canais do joystick estão em `config.py` — mude à
vontade se sua fiação for diferente.

### Habilitar SPI na Raspberry

```bash
sudo raspi-config
# Interface Options -> SPI -> Enable
sudo reboot
```

### Instalar dependências

```bash
cd fliperama
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Cadastrar o UID de cada cubo

1. Cole uma tag RFID em cada cubo impresso.
2. Rode `python3 tools/descobrir_uid.py`, encoste cada cubo um de
   cada vez e anote o UID mostrado no terminal.
3. Edite `data/rfid_map.json`, substituindo os UIDs de exemplo pelos
   UIDs reais, associando cada um à chave da partícula correta
   (as chaves disponíveis estão em `data/particles_data.py`, dict
   `PARTICLES`: `eletron`, `quark_up`, `quark_down`, `foton`,
   `neutrino`, `gluon`, `positron`, `higgs`).

### Tela vertical (TV em pé)

O app detecta a resolução automaticamente e abre em tela cheia
(`config.FULLSCREEN = True`). Gire fisicamente a TV/monitor 90°; se
a saída de vídeo da Raspberry precisar ser rotacionada por software
também, adicione no `/boot/firmware/config.txt`:

```
display_rotate=1   # ou display_hdmi_rotate, dependendo da versão do OS
```
(em Raspberry Pi OS mais novos, use `xrandr` no autostart, ou a opção
de rotação em Configurações de Tela, dependendo do compositor.)

### Rodar automaticamente ao ligar (systemd)

Crie `/etc/systemd/system/fliperama.service`:

```ini
[Unit]
Description=Fliperama Particulas Elementares
After=graphical.target

[Service]
User=pi
WorkingDirectory=/home/pi/fliperama
ExecStart=/home/pi/fliperama/venv/bin/python3 main.py
Restart=on-failure
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
```

```bash
sudo systemctl enable fliperama.service
sudo systemctl start fliperama.service
```

## 3. Fonte pixelada (opcional)

Sem nenhuma fonte extra, o app usa uma fonte monoespaçada do sistema
(ainda com cara retrô). Para o visual 8-bit "de verdade", baixe uma
fonte gratuita tipo **Press Start 2P** ou **VT323** e coloque o
arquivo `.ttf` dentro de `assets/fonts/` — o app detecta e usa
automaticamente, sem precisar mexer no código.

## 4. Correção feita em relação ao app original (React)

O "Jogo dos Hádrons" original tinha um bug: só verificava acerto para
bárions de 3 quarks (próton/nêutron); píon e káon (mésons, 2 quarks
com antiquark) eram impossíveis de acertar, porque nem existiam
antiquarks disponíveis para selecionar. Nesta versão, a paleta inclui
antiquarks (ū, d̄, s̄) e a checagem compara a composição completa —
funciona para todos os 6 hádrons.
