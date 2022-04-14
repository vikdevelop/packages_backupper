import gi
import os
import glob
import json
from datetime import date
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
HOME = os.path.expanduser('~')
date = date.today()

class Dialog_create(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Package list has been created!", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label()
        label.set_markup("<b>Done!</b> Package list is in the directory: <i>%s/PKG_LISTS/package-list_%s.json</i>. \nYou can now use this PKG list to import PKGS on Linux click on Import button!" % (HOME, date))

        box = self.get_content_area()
        box.add(label)
        self.show_all()
        
class Dialog_import(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Package has been installed!", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label()
        label.set_markup("<b>Done!</b> All packages has been installed!")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class PKGBackerWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, title="Package backer")
        self.set_default_size(600, 200)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(mainBox)
        
        self.button_link = Gtk.LinkButton.new_with_label(uri="https://github.com/vikdevelop", label="How to use this app?")
        mainBox.pack_start(self.button_link, True, True, 0)
        
        self.label = Gtk.Label()
        mainBox.pack_start(self.label, True, True, 0)
        
        self.label_h1 = Gtk.Label()
        self.label_h1.set_markup("<b>Creation package list</b>")
        mainBox.pack_start(self.label_h1, True, True, 0)
        
        self.entry = Gtk.Entry()
        self.entry.set_text("Enter name of packages, want you install")
        mainBox.pack_start(self.entry, True, True, 0)
        
        self.button_create = Gtk.Button(label="Create")
        self.button_create.connect("clicked", self.on_button_create)
        mainBox.pack_start(self.button_create, True, True, 0)
        
        self.label_h2 = Gtk.Label()
        self.label_h2.set_markup("<b>Installation packages from package list</b>")
        mainBox.pack_start(self.label_h2, True, True, 0)
        
        self.entry2 = Gtk.Entry()
        self.entry2.set_text("Enter path to package list")
        mainBox.pack_start(self.entry2, True, True, 0)
        
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
        entry1 = self.entry.get_text()
        if not os.path.exists("%s/PKG_LISTS" % HOME):
            os.makedirs('%s/PKG_LISTS' % HOME)
        with open('%s/PKG_LISTS/package_list_%s.json' % (HOME, date), 'w') as f:
            f.write('{\n')
            f.write('"packages": "%s"\n' % entry1)
            f.write('}')
        print("Package list has been created! Is in directory: %s/PKG_LISTS/package_list_%s.json" % (HOME, date))
        # Dialog_create window
        dialog_c = Dialog_create(self)
        response_c = dialog_c.run()

        if response_c == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response_c == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog_c.destroy()
        
    def importb(self):
        entry2 = self.entry2.get_text()
        with open('%s' % entry2) as jsonFile:
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
            
        # Dialog_import window
        dialog_m = Dialog_import(self)
        response_m = dialog_m.run()

        if response_m == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response_m == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog_m.destroy()
win = PKGBackerWindow()
win.show_all()
win.connect("delete-event", Gtk.main_quit)
Gtk.main()
