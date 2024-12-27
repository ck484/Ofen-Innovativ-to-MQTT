# Ofen-Innovativ-to-MQTT
Ofen Innovativ Abbrandsteuerung Werte der Webseite aus Canvas auslesen und per MQTT versenden, zur verwendung in Home Assistant

Die Abbrandsteuerung von Ofen Innovativ (ORi wifi/Orex wifi) bietet eine Weboberfläche, die sich über eine IP-Adresse im Browser aufrufen lässt. 
Über die Weboberfläche wird die Brennraumtemperatur, Zuluft, Brenndauer, Türstatus, Wassertaschentemperatur, Puffertemperatur oben und Puffertemperatur unten
Grafisch in einem Canvas Element dargestellt. Um diese Werte nun z.B. im Home Assistant zu verwenden, kann der Python Code verwendet werden.

Ein Webscraper funktioniert nicht und gibt nur die Platzhalter z.B. ---°C aus. Mit dem Python Programm wird ein Java Script im Webbrowser ausgeführt, der die Canvas Texte extrahiert und anschließend an den MQTT-Broker sendet.

Bei mir läuft das Programm auf einem Raspberry-PI.
Für die Ausführung muss eine Virtuelle Umgebung aktiviert werden, sowie einige Python anwendungen installiert werden. 
Außerdem sollte eine Service datei erstellt werden, damit das Programm automatisch gestartet wird.

Chat GPT ist eine gute unterstützung bei der Umsetzung ;)  

Ich hoffe ich konnte weiterhelfen.
