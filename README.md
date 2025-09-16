# Home Assistant Yuya Pet Feeder Integration

This Home Assistant integration allows you to connect to your Tuya Pet Feeder. This integration is still in development, and it's unknown which kind of Petfeeders are supported.

## Features

- Check connection status
- Toggle LED light
- Dispense portion(s)
- Track dispense history (still in development, at this moment only HA dispensed portions)

## Installation

### Manual Installation

1. Download the integration files and place them in your Home Assistant `custom_components/tuyapetfeeder` directory.
2. Restart Home Assistant.

### HACS (Recommended)

1. Add this repository as a custom repository in HACS.
2. Install the integration via HACS.
3. Restart Home Assistant.

## Configuration

1. Find the Device ID and Local Key of the petfeeder. Check this blog for instructions.
2. Navigate in HA to **Settings → Devices & Services → Add Integration**.
3. Search for **Tuya Pet Feeder**.
4. Enter the details:
   - **Name**: A name for the device
   - **Host**: IP address of the device
   - **Device ID**: As found in step 1
   - **Local Key** As found in step 1
5. Click **Submit**.

## Contributing

Contributions and feature requests are welcome! Feel free to open an issue or submit a pull request.

The following features needs to be implemented:

- A
- B

## License

This project is licensed under the MIT License.
