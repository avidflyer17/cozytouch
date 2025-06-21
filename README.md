# Atlantic Cozytouch

This Home Assistant integration connects to the Atlantic **Cozytouch** cloud. It allows controlling boilers, heat pumps and other appliances that use the Cozytouch service (different from the official Overkiz integration).

## Features

- Cloud polling using Atlantic's API
- Climate entities with HVAC and fan modes
- Sensors for temperatures, power and diagnostic values
- Numbers, selects, time and switch entities
- Away mode scheduling and control
- Optional JSON logging for debugging
- Option to create entities for unknown capabilities

## Supported devices

The integration has been validated with:
- **Atlantic Naema 2 Micro 25** gas boiler with a **Navilink Radio‑Connect 128** thermostat
- **Atlantic Naema 2 Duo 25** gas boiler with a **Navilink Radio‑Connect 128** thermostat
- **Atlantic Naia 2 Micro 25** gas boiler with a **Navilink Radio‑Connect 128** thermostat
- **Atlantic Loria Duo 6006 R32** heat pump with a **Navilink Radio‑Connect 128** thermostat
- **Takao M3** air conditioning unit
- **Kelud 1750W** towel rack
- **Sauter Asama Connecté II Ventilo 1750W** towel rack

Mapping is required for each model. Feel free to open an issue to help support additional devices.

## Installation

You can install the integration via **HACS** or manually.

### HACS

[![Add HACS repository.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=avidflyer17&repository=cozytouch&category=integration)

More information about HACS is available at [hacs.xyz](https://hacs.xyz/).

### Manual

Clone this repository and copy `custom_components/cozytouch` into your Home Assistant configuration directory (for example: `config/custom_components/cozytouch`).

Restart Home Assistant after copying the files.

## Configuration

1. Go to **Settings → Devices & Services → Add integration**.
2. Search for **Cozytouch** and select **Atlantic Cozytouch**.
3. Enter your Cozytouch credentials.
4. Pick the device you want to configure.
5. Optionally enable **Create entities for unknown capabilities** and **Dump a JSON file with received data** for debugging.

If the connection is successful, the selected device will appear with the available entities.

## Contributing

Issues and pull requests are welcome. Please open an issue if your device requires additional mapping.
