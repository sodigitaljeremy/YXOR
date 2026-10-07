# Marché des cartes de bus (2026-10)

**Engendré** par `.venv/bin/python scripts/marche_composants.py --ecrire`. Ne pas éditer à la main. **Données seulement** : aucune intégration à l'explorateur, aucun achat (fiche 0066). Contexte DÉCIDÉ (fiche 0070, Jeremy, 2026-10-07) : « Les deux robots, YXOR Lab et YXOR, fonctionnent entièrement sur batterie. Je préfère NVIDIA Jetson, mais je veux une comparaison chiffrée avec le Raspberry Pi 5 et ses cartes d'IA. » Sources lues le 2026-10-07, téléchargées hors du dépôt, inscrites à `params/fournisseurs.yaml` (non redistribuables) ; une valeur non lue est un trou (—), jamais estimée.

30 produits, 93 sources.

## Protocole CAN des RobStride

- **interface** : CAN 2.0 — même phrase RS02 p. 41, RS05 p. 45 (« The motor communication is the CAN 2.0 communication interface »)
- **debit can defaut** : 1 Mbit/s — tableau driver « CAN bus bit rate 1Mbps » ; RS02 p. 12, RS05 p. 14 ; répété au protocole (RS00 p. 38) et au protocole MIT (RS00 p. 70)
- **debits possibles** : 1 M, 500 k, 250 k, 125 kbit/s — type de communication 23 (0x17), octet F_CMD : 01 = 1M, 02 = 500K, 03 = 250K, 04 = 125K ; effet après remise sous tension. RS02 p. 46, RS05 p. 51. Paramètre 0x2009 motor_baud (RS00 p. 21)
- **format trame protocole prive** : trame étendue, identifiant 29 bits — identifiant : bits 28-24 type de communication, bits 23-8 zone de données 2, bits 7-0 adresse de destination ; RS02 p. 41, RS05 p. 45
- **format trame protocole mit** : trame standard, identifiant 11 bits — protocole MIT, débit par défaut 1 Mbit/s, « baud rate can be modified by switching to the private protocol » ; RS02 p. 72, RS05 p. 79. Un 3e protocole, CANopen (DS402), existe (chapitre 5, RS00 p. 61 et suivantes) ; basc
- **octets donnees commande** : 8 — « 29-bit ID 8Byte data field » pour chaque type ; commande de type 1 (contrôle « opération ») : couple dans l'identifiant (bits 23-8), angle, vitesse, Kp, Kd sur les 8 octets
- **octets donnees reponse** : 8 — trame de retour type 2 : 8 octets ; défauts et mode codés dans l'identifiant 29 bits
- **une reponse par commande** : True — après la commande de type 1 : « Response frame: Response motor feedback frame (see communication type 2) » ; même mention pour les autres types de commande. Il s'agit d'une lecture du texte, pas d'une mesure du bus
- **remontee active** : désactivée par défaut ; type 24 ; intervalle par défaut 10 ms — p. 48 : « Report type: Type 2 (default interval: 10ms) », réglable par EPScan_time (p. 47 : « 1 indicates 10ms. Plus 1 increments by 5ms ») ; l'outil PC indique « a minimum of 10ms » (p. 16). RS02 p. 17 et 47, RS05 p. 18
- **can fd firmware** : — (non lu) — aucune mention de CAN-FD (ni « CAN FD », « CANFD », « flexible data ») dans les trois manuels 260713 ni dans l'arborescence du dépôt ; tous disent « CAN 2.0 ». Absence de mention, pas preuve d'absence : prise en charge n
- **debit donnees fd** : — (non lu) — sans objet tant que le CAN-FD n'est pas documenté
- **frequence commande max** : — (non lu) — non documentée dans les trois manuels ; seules valeurs temporelles publiées : remontée active 10 ms par défaut (p. 44), minimum 10 ms dans l'outil PC (p. 16)
- **temporisation perte can** : CAN_TIMEOUT, 20000 = 1 s ; 0 = désactivé ; au-delà, passage en mode reset — RS02 p. 31, RS05 p. 34 ; aussi p. 47 (« timeout threshold, 20000 is 1s »)
- **adaptateur canhub debit** : 1M configuré dans la procédure — manuel chinois de l'adaptateur USB-CANHUB RobStride (5 voies CAN, p. 11-12)

## Combien de canaux CAN pour 27 axes à 500 Hz

Calcul écrit : une commande et une réponse par axe et par cycle (protocole RobStride), 8 octets chacune ; trame au PIRE bourrage (un bit inséré au plus tous les 4 bits, du SOF à la fin du CRC), intertrame la plus longue des deux lues ; débit 1 Mbit/s (défaut RobStride, CAN-FD non documenté) ; charge maximale PROPOSÉE 70 %. Le 27 axes de la fiche 0069 compte 4 petits axes (cou 2, pinces 2) en Feetech sur bus série : 23 axes sur CAN.

| Protocole | Axes | Bits par trame (bourrables + bourrage + fixes) | Débit nécessaire | Canaux à 100 % | Canaux à 70 % |
| --- | ---: | --- | ---: | ---: | ---: |
| protocole privé (trame étendue 29 bits) | 27 | 164.0 (118.0 + 29 + 17.0) | 4,43 Mbit/s | 5 | **7** |
| protocole privé (trame étendue 29 bits) | 23 | 164.0 (118.0 + 29 + 17.0) | 3,77 Mbit/s | 4 | **6** |
| protocole MIT (trame standard 11 bits) | 27 | 139.0 (98.0 + 24 + 17.0) | 3,75 Mbit/s | 4 | **6** |
| protocole MIT (trame standard 11 bits) | 23 | 139.0 (98.0 + 24 + 17.0) | 3,20 Mbit/s | 4 | **5** |

## Les produits

| Produit | Famille | Canaux | CAN-FD | Interface | Pilote Linux | g | CHF HT |
| --- | --- | --- | --- | --- | --- | ---: | ---: |
| PCAN-M.2 (IPEH-004083 / 004084 / 004085) | can_m2_pcie | 1, 2 ou 4 | True | M.2 2280/2260-B-M, une ligne PCIe, DMA b | peak_pci (SocketCAN, pilote peak_pciefd selon le n | 6 | 259 |
| PCAN-miniPCIe FD (IPEH-004045 / 004046 / 004047) | can_m2_pcie | 1, 2 ou 4 | True | PCI Express Mini (ligne PCIe), DMA bus m | peak_pci (SocketCAN) ; ou paquet chardev PEAK | 8 | 259 |
| 2-CH CAN FD HAT | can_spi | 2 | True | SPI (GPIO 40 broches Raspberry Pi), SPI  | mcp251xfd (dtoverlay=mcp251xfd) | 40 | 39 |
| PiCAN FD Duo (avec RTC) | can_spi | 2 | True | SPI (HAT Raspberry Pi), interruptions GP | SocketCAN (can0) ; module non nommé | — | 96 |
| 2-Channel CAN-BUS(FD) Shield for Raspberry Pi (SKU 103030296) | can_spi | 2 | True | SPI (HAT Raspberry Pi) | overlay seeed-can-fd-hat-v2 (dépôt seeed-linux-dto | — | 25 |
| Pilote noyau mcp251xfd (référence, pas un produit) | can_spi | — | — | — | CAN_MCP251XFD, « Microchip MCP251xFD SPI CAN contr | — | — |
| RobStride USB_CANHUB (USB-CAN-HUB) | can_usb | 5 | — | USB 2.0 (Type-C), ou connecteur MX1.25-4 | interfaces SocketCAN natives canX (can0, can1…), o | — | 63 |
| PCAN-USB (IPEH-002021) / PCAN-USB opto-decoupled (IPEH-002022) | can_usb | 1 | False | USB Full-Speed (compatible USB 1.1, 2.0, | peak_usb (SocketCAN) ; ou paquet chardev PEAK | 78 | 232 |
| PCAN-USB FD (IPEH-004022 USB-A / IPEH-004023 USB-C) | can_usb | 1 | True | USB 2.0 High-Speed (USB-A ou USB-C) | peak_usb (SocketCAN) ; ou paquet chardev PEAK | 68 | 263 |
| PCAN-USB Pro FD | can_usb | 2 CAN FD + 2 LIN | True | USB 2.0 High-Speed | peak_usb (SocketCAN) ; ou paquet chardev PEAK | 220 | 536 |
| Kvaser Leaf Light v2 | can_usb | 1 | False | USB 2.0 | kvaser_usb (SocketCAN) | 112 | 386 |
| Kvaser U100 | can_usb | 1 | True | USB | kvaser_usb (SocketCAN) | 167 | 447 |
| CANable 2.0 | can_usb | 1 | True | USB-C, port série virtuel (slcan) | slcan (slcand) ; firmware candleLight/gs_usb possi | — | 29 |
| candleLight FD | can_usb | 1 | True | USB 2.0, USB-C | gs_usb (SocketCAN) | — | — |
| candleLight (CAN 2.0) | can_usb | 1 | False | Micro USB 2.0 | gs_usb (SocketCAN) | — | — |
| InnoMaker USB2CAN (module, -C, -X2) | can_usb | 1 (USB2CAN, -C) ; 2 (USB2CAN-X2) | False | USB 2.0 Full-Speed | gs_usb (SocketCAN) | 16 | — |
| Seeed USB-CAN Analyzer (SKU 114991193) | can_usb | 1 | False | USB, port COM virtuel (protocole série p | pas de SocketCAN natif : port série (ttyUSB), inte | — | 23 |
| Korlan USB2CAN | can_usb | 1 | False | USB 2.0 Full speed (12 Mbit/s) | usb_8dev (SocketCAN) | — | 58 |
| Interfaces Geschwister Schneider UG (origine du protocole gs_usb) | can_usb | — | — | USB | gs_usb (SocketCAN) | — | — |
| Contrôleur CAN intégré du Jetson Orin NX/Nano (carte porteuse du kit, connecteur J17) | can_usb | 1 | True | intégré au SoC (bloc Always-On), J17 : C | mttcan (SocketCAN) | — | — |
| U2D2 | serie_dynamixel | 1 bus ; ports TTL 3 broches, RS-485 4 broches, UART 4 broches | — | USB | — | 9 | 31 |
| U2D2 Power Hub Board | serie_dynamixel | connecteurs TTL (JST EHR-03) et RS-485 (JST EHR-04) | — | aucune : carte d’alimentation associée à | — | — | 18 |
| OpenRB-150 | serie_dynamixel | 4 ports DYNAMIXEL TTL | — | USB-C (SAMD21 Cortex-M0+ ; micrologiciel | — | — | 24 |
| FE-URT-1 (URT-1), convertisseur USB/UART vers SMS (RS-485) et SCS (TTL) | serie_feetech | 1 bus, deux connecteurs : SCS TTL 3 broches (5264-3AW) et SMS RS-485 4 broches (5264-4AW) | — | USB 2.0 pleine vitesse | — | 12 | 16 |
| Bus Servo Adapter (A) (SKU 25514) | serie_feetech | 1 bus (servos ST/SC) | — | UART, ou USB (mode B par cavalier) | — | 16 | 4 |
| Serial Bus Servo Driver Board | serie_feetech | — | — | — | — | — | — |
| Bus Servo Driver Board for Seeed Studio XIAO (SKU 105990190) | serie_feetech | 1 bus (servos ST/SC, dont Feetech SCS) | — | UART direct, ou USB via un adaptateur US | — | — | 5 |
| USB-RS485-WE (câble) | serie_generique | — | — | — | — | — | — |
| USB TO RS485 (SKU 17286) | serie_generique | 1 | — | USB-A | — | 67 | 9 |
| USB TO TTL | serie_generique | 1 | — | USB | pilote FT232 inclus dans les distributions (/dev/t | — | — |
