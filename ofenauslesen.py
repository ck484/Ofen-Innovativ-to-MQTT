import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import paho.mqtt.client as mqtt

# MQTT-Konfiguration (bitte Anpassen)
MQTT_HOST = "HOST IP" 
MQTT_PORT = 1883
MQTT_USER = "USER"
MQTT_PASSWORD = "Passwort"

# Funktion zum Senden der Daten über MQTT
def send_to_mqtt(data):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)

    # Veröffentlichen der Daten in verschiedenen Untertopics
    for label, value in data.items():
        # Entferne das Zeichen "°" und "%" aus dem Wert
        clean_value = value.replace('°', '').replace('%', '')
        
        # Erstelle das Topic und sende den bereinigten Wert als Payload
        topic = f"holzofen/{label}"  # Erstelle das Topic
        client.publish(topic, clean_value)  # Sende den bereinigten Wert als Payload

    client.disconnect()

# Funktion, um die Daten vom Holzofen zu extrahieren
def get_holzofen_data():
    # Selenium-Optionen
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # WebDriver-Setup
    service = Service("/usr/bin/chromedriver")  # Chromedriver-Pfad
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://IP von der Ofensteuerung")  # URL des Holzofens anpassen

    # Warten, bis die Seite vollständig geladen ist
    time.sleep(20)  # Warten auf vollständiges Laden der Seite

    # JavaScript, um Canvas-Text abzufangen
    inject_js = """
    const originalFillText = CanvasRenderingContext2D.prototype.fillText;
    let count = 0; // Zählvariable für die Anzahl der Ausgaben

    // Bezeichner für die Textwerte 1-8
    const labels = [
        'Brennraumtemperatur',
        'Zuluft',
        'Brenndauer',
        'Türstatus',
        'Abluft',
        'Wassertasche',
        'PufferO',
        'PufferU'
    ];

    window.canvasTexts = [];  // Hier speichern wir die abgefangenen Texte

    CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
        // Wenn die Anzahl der Ausgaben 8 erreicht, beenden wir die Funktion
        if (count >= 8) {
            return; // Stoppt die Ausführung des Codes
        }

        // Füge den Text zur window.canvasTexts-Array hinzu
        const label = labels[count];
        window.canvasTexts.push({ label: label, text: text });  // Speichere den Bezeichner und Text

        count++; // Erhöhe den Zähler um 1

        // Führe den ursprünglichen fillText-Befehl aus
        return originalFillText.apply(this, arguments);
    };
    """

    # Führe das JavaScript auf der Seite aus
    driver.execute_script(inject_js)

    # Warten, um sicherzustellen, dass der JavaScript-Code Zeit hat, den Canvas-Text zu extrahieren
    time.sleep(5)  # 5 Sekunden warten, damit die Canvas-Texte protokolliert werden können

    # Lese alle abgefangenen Canvas-Texte aus
    canvas_texts = driver.execute_script("return window.canvasTexts;")
    print(f"Abgefangene Canvas-Texte: {canvas_texts}")

    driver.quit()

    # Wenn Canvas-Texte abgefangen wurden, gib sie als dictionary zurück
    if canvas_texts:
        data = {entry['label']: entry['text'] for entry in canvas_texts}
        return data
    else:
        return None

# Endlosschleife, die alle 30 Sekunden die Daten abruft und an den MQTT Broker sendet
while True:
    data = get_holzofen_data()
    if data:
        print(f"Extrahierte Daten: {data}")
        send_to_mqtt(data)  # Sende die Daten an den MQTT-Broker
    else:
        print("Keine Daten extrahiert.")
    time.sleep(20)  # 20 Sekunden warten, bevor die nächste Abfrage erfolgt
