import gi
import os
import glob
import json
from datetime import date
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

date = date.today()

class FlatpakWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, title="Package backer")
        self.set_default_size(600, 200)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(mainBox)
        
        self.button_link = Gtk.LinkButton.new_with_label(uri="https://github.com/vikdevelop", label="How to use this app?")
        mainBox.pack_start(self.button_link, True, True, 0)
        
        self.label = Gtk.Label()
        mainBox.pack_start(self.label, True, True, 0)
        self.entry = Gtk.Entry()
        self.entry.set_text("Enter path to packages list or packages, want you install")
        mainBox.pack_start(self.entry, True, True, 0)
        
        
        self.button_create = Gtk.Button(label="Create")
        self.button_create.connect("clicked", self.on_button_create)
        mainBox.pack_start(self.button_create, True, True, 0)
        
        self.button_importb = Gtk.Button(label="Import")
        self.button_importb.connect("clicked", self.on_button_importb)
        mainBox.pack_start(self.button_importb, True, True, 0)

    def on_button_create(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.create()
        
    def on_button_importb(self, widget, *args):
        self.importb()

    def on_SpinnerWindow_destroy(self, widget, *args):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()

    def create(self):
        HOME = os.path.expanduser('~')
        entry1 = self.entry.get_text()
        if not os.path.exists("%s/PKG_LISTS" % HOME):
            os.makedirs('%s/PKG_LISTS' % HOME)
        with open('%s/PKG_LISTS/package_list_%s.json' % (HOME, date), 'w') as f:
            f.write('{\n')
            f.write('"packages": "%s"\n' % entry1)
            f.write('}')
        print("Package list has been created! Is in directory: %s/PKG_LISTS/package_list_%s.json" % (HOME, date))
        self.label.set_markup("<b>Done!</b> Package list is in the directory: <i>%s/PKG_LISTS/package-list_%s.json</i>. \nYou can now use this PKG list to import PKGS on Linux click on Import button!" % (HOME, date))
        
    def importb(self):
        print("IMPORT CLICKED....")
        HOME = os.path.expanduser('~')
        entry1 = self.entry.get_text()
        with open('%s' % entry1) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        
        packages = jsonObject['packages']
        
        if os.path.exists('/usr/bin/dnf'):
            os.system('pkexec dnf install %s' % packages)
            print('\033[1m' + 'Done! All packages is installed. Please ignore prints below, they are related to other package managers and distributions :)' + '\033[0m')
        else:
            print("Sorry. I didn't found DNF (Fedora) package manager. I trying find other package manager...")
            
        if os.path.exists('/usr/bin/apt'):
            os.system('pkexec apt install %s' % packages)
            print('\033[1m' + 'Done! All packages is installed. Please ignore prints below, they are related to other package managers and distributions :)' + '\033[0m')
        else:
            print("Sorry. I didn't found APT (Debian, Ubuntu, Linux Mint etc.) package manager. I trying found other package manager...")
        
        if os.path.exists('/usr/bin/zypper'):
            os.system('%s zypper install' % packages)
            print('\033[1m' + 'Done! All packages is installed. Please ignore prints below, they are related to other package managers and distributions :)' + '\033[0m')
        else: 
            print("Sorry. I didn't found Zypper (openSUSE) package manager. I trying found other package manager...")
            
        if os.path.exists('/usr/bin/pacman'):
            os.system('pkexec pacman -S %s' % packages)
            print('\033[1m' + 'Done! All packages is installed. Please ignore prints below, they are related to other package managers and distributions :)' + '\033[0m')
        else:
            print("Sorry. I didn't found Pacman (Arch Linux, Manjaro, Garuda, Cutefish OS etc.) package manager and other package managers. So, you will try using other distro with supported package managers:")
            print("APT")
            print("DNF")
            print("Zypper")
            print("Pacman")
            
        self.label.set_markup("<b>Done!</b> All packages has been installed!")
win = FlatpakWindow()
win.show_all()
win.connect("delete-event", Gtk.main_quit)
Gtk.main()
