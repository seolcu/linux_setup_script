# Constants

DNF_PACKAGES: list[str] = [
    # GUI
    "gnome-tweaks",
    "steam",  # Not from flatpak but from RPM Fusion, since it allows application shortcuts and seems to be working better
    # CLI
    ## Development
    ### C/C++
    "gcc",
    "g++",
    ### Java
    "java-21-openjdk-devel",
    ### Python
    "python3-pip",
    "python3-ipykernel",
    "black",
    ### Node.js
    "nodejs",
    ## Utilities
    "neovim",
    "htop",
    "neofetch",
    "gh",
    "distrobox",
    # GNOME extensions
    "gnome-shell-extension-appindicator",
    ## GSConnect Dependencies
    "openssl",
    "nautilus-python",
    "nautilus-extensions",
    # Etc
    "google-noto-sans-cjk-fonts",
]

DNF_REMOVE_PACKAGES: list[str] = [
    "firefox",
    "rhythmbox",
    "gnome-shell-extension-background-logo",
]


FLATPAK_PACKAGES: list[str] = [
    # Web Browsers
    "com.brave.Browser",
    # GNOME Apps
    "de.haeckerfelix.Fragments",
    ## Etc
    "com.mattjakeman.ExtensionManager",
    "com.usebottles.bottles",
    # Work
    "org.onlyoffice.desktopeditors",
    "md.obsidian.Obsidian",
    # Communication
    "us.zoom.Zoom",
    "com.discordapp.Discord",
    "com.slack.Slack",
    "org.signal.Signal",
    # Utilities
    "org.raspberrypi.rpi-imager",
    "org.videolan.VLC",
    "com.vixalien.decibels",
    # Etc
    "com.obsproject.Studio",
    "org.gnome.NetworkDisplays",
]
