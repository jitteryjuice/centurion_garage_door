# Centurion Garage Door - Home Assistant Integration

A custom Home Assistant integration for controlling Centurion garage doors.

## Features

- Control garage door open/close operations
- Monitor door status (open, closed, opening, closing)
- Real-time status updates
- Easy configuration through Home Assistant UI

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from the releases page
2. Extract the files to your Home Assistant `custom_components` directory
3. Create a folder named `centurion_garage_door` in `custom_components`
4. Copy all files to this folder
5. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Centurion Garage Door"
4. Follow the configuration prompts

## Usage

Once configured, your garage door will appear as a cover entity in Home Assistant. You can:

- Open/close the door from the UI
- Use it in automations and scripts
- Monitor the door status

## Support

For issues and feature requests, please use the GitHub issue tracker.

## License

This project is licensed under the MIT License.
