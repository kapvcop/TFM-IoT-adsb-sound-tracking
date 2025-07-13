# SDR IoT ADS B & Acoustic Aircraft Tracking

This repository contains the source code for the Master's Thesis (TFM) submitted to ETSINF‑UPV entitled
**“Design and development of an embedded SDR‑IoT system for ADS‑B tracking and acoustic aircraft measurement.”**

## Overview

The system combines an ADS‑B receiver based on *dump1090* with a sound‑level meter to characterise aircraft fly‑overs in real time. Collected data are packaged and sent to AWS IoT Core. From this implementation, other data‑analysis projects can be derived.

## Key Features

* **ADSB capture** using an RTL SDR dongle (or any compatible SDR) running *dump1090*.
* **Acoustic measurement** (SPL) with a MEMS microphone via the `sounddevice` library.
* **IoT transmission** to AWS IoT Core over MQTT/HTTPS with certificate‑based authentication.
* **Modular OOP design**: each component (capturer, tracker, sound meter, IoT client) is decoupled.
* **Easily editable JSON configuration** (`utils/config.json`).
* **Rotating logs** for debugging (`log_sistema.log`).

## Project Structure

```text
main.py                       # Entry point
requirements.txt              # Python dependencies
certificados/                 # Place your AWS security certificates here
componentes/
    avion.py                  # Aircraft model & utilities
    capturador_dump1090.py    # ADS‑B frame capture thread
    seguidor_de_avion.py      # Tracking / filtering logic
    nivel_de_sonido.py        # SPL measurements
    cliente_aws_iot.py        # MQTT publishing to AWS
utils/
    config.json               # System parameters
    logger_util.py            # Logging configuration
    calcular_distancia.py     # Geodesic helper
```

## Requirements

* **Raspberry Pi 3 Model B Rev 1.2** running **Raspberry Pi OS 64 bit** (Debian 12 “Bookworm”) with **Linux 6.1.x** kernel.
* **Python 3.11.x** (install dependencies from `requirements.txt`).
* **dump1090** (or equivalent) installed and running.
* **RTL‑SDR** (or HackRF / other compatible SDR).
* **MEMS microphone** connected via I²S/ALSA.
* Access to **AWS IoT Core** with provisioned certificates.

Install the dependencies:

```bash
sudo apt update
sudo apt install python3-pip rtl-sdr build-essential
pip install -r requirements.txt
```

## Configuration

1. Copy your certificates to `certificados/` and update their paths in `main.py`.
2. Adjust SPL thresholds, sampling rate and coordinates in **utils/config.json**.
3. Verify the Raspberry Pi serial in `main.py` if you customise it.
4. Update the exact GPS coordinates of the Raspberry Pi in **utils/config.json**.
5. Set `device_id` in **utils/config.json** (0 or 1 depending on your system).
6. Tune the tracking parameters:

   * `"distancia_inicial": <numeric_value>`
   * `"distancia_final": <numeric_value>`
   * `"altura_det": <numeric_value>`
   * `"altura_fin": <numeric_value>`

## Quick Start

```bash
# 1. Activate the virtual environment (adjust the path if different)
source /home/raspbpi/enviroment_venv/bin/activate

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run the application
/home/raspbpi/enviroment_venv/bin/python3 main.py
```

## Main Python Libraries Used

* **paho‑mqtt** – Secure MQTT communication with AWS IoT.
* **sounddevice** – Audio capture and SPL measurement.
* **numpy** – Numeric processing and filters.
* **logging** – Rotating log system for debugging.
* **json** – Dynamic configuration loading.
* **math / geopy** – Distance and geodesic coordinate calculations.

## Credits / Third‑Party Software

* Robb, M. (2014). *dump1090: Mode S/ADS‑B decoder for RTL‑SDR*.
  [https://github.com/MalcolmRobb/dump1090](https://github.com/MalcolmRobb/dump1090)

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

*© 2025 Kristian Patiño — TFM ETSINF/UPV*

