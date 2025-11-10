# Minecraft Instance Setup

A lightweight and user-friendly desktop application to automatically install and configure all required client files for a modded Minecraft server.

## Features

- Choose the location of your `.minecraft` folder easily.
- Detects existing mods and lets the user either back them up or remove them before installation.
- Automatically installs:
  - Mods (`mods_to_install/`)
  - Resourcepacks (`resourcepacks_to_install/`)
  - Shaders (`shaderpacks_to_install/`)
  - Server list (`servers.dat`)
- Optional installation steps for resource packs and shaders.
- Fully standalone `.exe` for Windows (built with PyInstaller).

## Requirements

- Python 3.9+
- Windows OS
- Minecraft installed with Forge or Fabric matching your server version.

## How to Use

1. Download the latest release from the **Releases** section.
2. Run `MinecraftModInstaller.exe`.
3. Select your `.minecraft` folder.
4. Follow the instructions to install mods, resources, and shaders.
5. Launch Minecraft and join your server.

## Build Your Own Version

If you want to build a custom version of this installer for your own Minecraft server:

1. Clone or download this repository.
2. Replace the contents of the following folders with your own files:
   - `mods_to_install/` → all required mod `.jar` files
   - `resourcepacks_to_install/` → your resource pack `.zip` files
   - `shaderpacks_to_install/` → your shaders (any format, zipped or not)
3. Replace `servers.dat` with your own file containing your server list.
4. (Optional) Replace `minecraft_folder.png` with your own image to show in the help window.

Setup the build environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install pyinstaller
```

Then compile your own executable using **PyInstaller**:

```bash
pyinstaller --onefile --windowed --name MinecraftModInstaller --icon=icon.ico --add-data "mods_to_install;mods_to_install" --add-data "resourcepacks_to_install;resourcepacks_to_install" --add-data "shaderpacks_to_install;shaderpacks_to_install" --add-data "minecraft_folder.png;." --add-data "servers.dat;." installer.py
```

After building, your `.exe` will appear in the `dist/` folder.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
