from colorama import Fore, Style
from subprocess import run
from simple_term_menu import TerminalMenu
import constants as c


# Classes


class package:
    name: str
    install_command: str
    remove_command: str

    # is_install: 0 is remove, 1 is install
    def process(self, is_install):
        if is_install:
            run(self.install_command, shell=True)
        else:
            run(self.remove_command, shell=True)

    def install(self):
        self.process(True)

    def remove(self):
        self.process(False)


class manual_package(package):
    def __init__(
        self,
        name: str,
        install_command: str,
        remove_command: str,
    ):
        self.name: str = name
        self.install_command: str = install_command
        self.remove_command: str = remove_command


class flathub_package(package):
    def __init__(self, url: str):
        self.url: str = url
        self.name: str = f"Flathub: {url}"
        self.install_command: str = f"flatpak install flathub {url}"
        self.remove_command: str = f"flatpak remove {url}"


class apt_package(package):
    def __init__(self, apt_name: str):
        self.apt_name: str = apt_name
        self.name: str = f"apt: {apt_name}"
        self.install_command: str = f"sudo apt install {apt_name}"
        self.remove_command: str = f"sudo apt remove {apt_name}"


class dnf_package(package):
    def __init__(self, dnf_name: str):
        self.dnf_name: str = dnf_name
        self.name: str = f"dnf: {dnf_name}"
        self.install_command: str = f"sudo dnf install {dnf_name}"
        self.remove_command: str = f"sudo dnf remove {dnf_name}"


class gnome_extension_package(package):
    def __init__(self, url: str):
        self.url: str = url
        self.name: str = f"GNOME Extension: {url}"
        self.install_command: str = f"gext install {url}"
        self.remove_command: str = f"gext uninstall {url}"


class package_list:
    registered_indexes: int | tuple[int] | None

    # selecting packages for process
    def register(self, is_install: bool = True):
        if is_install:
            display_title("Select packages to install")
        else:
            display_title("Select packages to remove")
        self.registered_indexes = TerminalMenu(
            map(lambda a_package: a_package.name, self.raw_package_list),
            multi_select=True,
            show_multi_select_hint=True,
            multi_select_select_on_accept=False,
            multi_select_empty_ok=True,
        ).show()

    def is_registered(self):
        if type(self.registered_indexes) == None:
            return False
        else:
            return True

    def process(self, is_install):
        if self.is_registered():
            if type(self.registered_indexes) == int:
                index = self.registered_indexes
                self.raw_package_list[index].process(is_install)
            elif type(self.registered_indexes) == tuple[int]:
                for index in self.registered_indexes:
                    self.raw_package_list[index].process(is_install)
        else:
            print("No packages registered")

    def install(self):
        self.process(True)

    def remove(self):
        self.process(False)

    def __init__(self, raw_package_list: list[package]):
        self.raw_package_list: list[package] = raw_package_list


class bash_script:
    def execute(self):
        display_title(self.name)
        if self.ask:
            if no_or_yes():
                run(self.command, shell=True)
        else:
            run(self.command, shell=True)

    def __init__(self, name: str, command: str, ask: bool = False):
        self.name: str = name
        self.command: str = command
        self.ask: bool = ask


class bash_script_list:
    def execute(self):
        for a_script in self.raw_script_list:
            a_script.execute()

    def __init__(self, raw_script_list: list[bash_script]):
        self.raw_script_list: list[bash_script] = raw_script_list


# Functions


def display_title(title: str):
    print(Fore.GREEN + f"[!] {title}", end=f"{Style.RESET_ALL}\n")


def no_or_yes():
    ans: int | tuple[int] | None = TerminalMenu(["No", "Yes"]).show()
    if type(ans) == int:
        return ans
    else:
        return 0


def select_one(options: list[str]):
    index: int | tuple[int] | None = TerminalMenu(options).show()
    if type(index) == int:
        return options[index]
    else:
        return ""


# Main


def main():
    display_title("Select your distro")
    distro = select_one(c.DISTRO_LIST)
    display_title("Select your DE")
    de = select_one(c.DE_LIST)

    # register install
    distro_packages["common"]["install"].register()
    distro_packages[distro]["install"].register()
    de_packages[de]["install"].register()

    # register remove
    distro_packages["common"]["remove"].register(is_install=False)
    distro_packages[distro]["remove"].register(is_install=False)
    de_packages[de]["remove"].register(is_install=False)

    # bash scripts - before process
    distro_scripts["common"]["before"].execute()
    distro_scripts[distro]["before"].execute()

    # installation process
    distro_packages["common"]["install"].install()
    distro_packages[distro]["install"].install()
    de_packages[de]["install"].install()

    # removal process
    distro_packages["common"]["remove"].remove()
    distro_packages[distro]["remove"].remove()
    de_packages[de]["remove"].remove()

    # bash scripts - after process
    distro_scripts["common"]["after"].execute()
    distro_scripts[distro]["after"].execute()


# Instances

distro_packages: dict[str, dict[str, package_list]] = {
    "common": {
        "install": package_list(
            [
                flathub_package("in.srev.guiscrcpy"),
                flathub_package("org.gnome.Boxes"),
                flathub_package("com.mojang.Minecraft"),
                flathub_package("io.mrarm.mcpelauncher"),
                flathub_package("com.valvesoftware.Steam"),
                flathub_package("com.rafaelmardojai.Blanket"),
                flathub_package("org.gnome.NetworkDisplays"),
                flathub_package("com.obsproject.Studio"),
                flathub_package("org.videolan.VLC"),
                flathub_package("md.obsidian.Obsidian"),
                flathub_package("org.onlyoffice.desktopeditors"),
                flathub_package("com.usebottles.bottles"),
                flathub_package("de.haeckerfelix.Fragments"),
                flathub_package("com.discordapp.Discord"),
                flathub_package("com.github.ztefn.haguichi"),
                flathub_package("com.microsoft.Edge"),
                flathub_package("org.gabmus.whatip"),
                flathub_package("us.zoom.Zoom"),
                flathub_package("com.github.unrud.VideoDownloader"),
                flathub_package("com.github.tchx84.Flatseal"),
                flathub_package("com.mattjakeman.ExtensionManager"),
                flathub_package("com.spotify.Client"),
                flathub_package("com.protonvpn.www"),
                flathub_package("org.remmina.Remmina"),
            ]
        ),
        "remove": package_list([]),
    },
    "debian": {
        "install": package_list(
            [
                manual_package(
                    "manual: vscode-apt",
                    """
                sudo apt install -y wget gpg
                wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
                sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
                sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
                rm -f packages.microsoft.gpg
                sudo apt install apt-transport-https
                sudo apt update -y
                sudo apt install -y code
            """,
                    "sudo apt remove -y code",
                ),
                apt_package("gnome-software-plugin-flatpak"),
                apt_package("git"),
                apt_package("gcc"),
                apt_package("g++"),
                apt_package("curl"),
                apt_package("wget"),
                apt_package("gpg"),
                apt_package("htop"),
                apt_package("neofetch"),
                apt_package("gh"),
                apt_package("solaar"),
                apt_package("python3-nautilus"),
            ]
        ),
        "remove": package_list(
            [
                apt_package("gnome-games"),
                apt_package("rhythmbox"),
                apt_package("evolution"),
                apt_package("zutty"),
                apt_package("shotwell"),
            ]
        ),
    },
    "fedora": {"install": package_list([]), "remove": package_list([])},
}

de_packages: dict[str, dict[str, package_list]] = {
    "gnome": {
        "install": package_list(
            [
                gnome_extension_package("appindicatorsupport@rgcjonas.gmail.com"),
                gnome_extension_package("caffeine@patapon.info"),
                gnome_extension_package("gsconnect@andyholmes.github.io"),
                gnome_extension_package("gestureImprovements@gestures"),
                gnome_extension_package("Vitals@CoreCoding.com"),
            ]
        ),
        "remove": package_list([]),
    }
}

distro_scripts = {
    "common": {
        "before": bash_script_list(
            [
                bash_script(
                    # [Enable Function Keys On Keychron/Various Mechanical Keyboards Under Linux, with systemd](https://github.com/adam-savard/keyboard-function-keys-linux)
                    "Fixing keyboard Fn issue (https://github.com/adam-savard/keyboard-function-keys-linux)",
                    """
                        sudo cp ./assets/keychron.service /etc/systemd/system/keychron.service
                        sudo systemctl enable keychron
                        sudo systemctl start keychron
                    """,
                    ask=True,
                )
            ]
        ),
        "after": bash_script_list(
            [
                bash_script(
                    "Reboot",
                    """
                        sudo systemctl reboot
                    """,
                    ask=True,
                )
            ]
        ),
    },
    "debian": {
        "before": bash_script_list(
            [
                bash_script(
                    "Switching to Debian sid",
                    """
                        sudo mv /etc/apt/sources.list /etc/apt/sources.list.old
                        sudo cp ./assets/sources.list /etc/apt/sources.list
                    """,
                    ask=True,
                ),
                bash_script(
                    "Updating the system",
                    """
                        sudo apt update -y
                        sudo apt full-upgrade -y
                    """,
                ),
                bash_script(
                    "Setting up flatpak & flathub",
                    """
                        sudo apt install -y flatpak
                        sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
                    """,
                ),
            ]
        ),
        "after": bash_script_list(
            [
                bash_script(
                    "Removing packages",
                    """
                        sudo apt autoremove -y
                    """,
                )
            ]
        ),
    },
    "fedora": {
        "before": bash_script_list(
            [
                bash_script(
                    "Updating the system",
                    """
                        sudo dnf update -y
                    """,
                ),
                bash_script(
                    "Enabling RPM Fusion",
                    """
                        sudo dnf install -y https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
                        sudo dnf groupupdate -y core
                    """,
                ),
                bash_script(
                    "Installing codecs from RPM Fusion",
                    """
                        sudo dnf swap -y ffmpeg-free ffmpeg --allowerasing
                        sudo dnf groupupdate -y multimedia --setop="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin
                        sudo dnf groupupdate -y sound-and-video
                        sudo dnf swap -y mesa-va-drivers mesa-va-drivers-freeworld
                        sudo dnf swap -y mesa-vdpau-drivers mesa-vdpau-drivers-freeworld
                        sudo dnf swap -y mesa-va-drivers.i686 mesa-va-drivers-freeworld.i686
                        sudo dnf swap -y mesa-vdpau-drivers.i686 mesa-vdpau-drivers-freeworld.i686
                    """,
                ),
            ]
        ),
        "after": bash_script_list([]),
    },
}
