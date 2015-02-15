#!/usr/bin/env python

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# Andrei Vacariu wrote this code. As long as you retain this notice you can 
# do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. <andrei@avacriu.me>
# ----------------------------------------------------------------------------

# This is a script to be used for switching between dual screen and single 
# screen using an AppIndicator. The output names and positions are specific to 
# my setup.

# Note: To set the position, consider the top-left corner of your primary 
#       display as 0x0, and use the --pos XxY parameter on your other displays
#       to set their relative positions.

import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import subprocess

class AppIndicatorExample:
    def __init__(self):
        self.ind = appindicator.Indicator ("switch_screens_indicator", "gsd-xrandr.svg", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_icon("/usr/share/icons/ubuntu-mono-dark/apps/22/gsd-xrandr.svg")

        self.menu = gtk.Menu()

        dual_screen_radio = gtk.RadioMenuItem(None, "Dual Screen")
        dual_screen_radio.show()
        self.menu.append(dual_screen_radio)

        single_screen_radio = gtk.RadioMenuItem(dual_screen_radio, "Single Screen")
        single_screen_radio.show()
        self.menu.append(single_screen_radio)

        dual_screen_radio.connect("activate", self.dual_screen)
        single_screen_radio.connect("activate", self.single_screen)
        
        self.menu.show()
        
        self.ind.set_menu(self.menu)

    def dual_screen(self, widget, data=None):
        subprocess.call(["/usr/bin/xrandr", "--output", "VGA-0", "--auto",
                         "--left-of", "LVDS-0", "--primary"])
        subprocess.call(["/usr/bin/xrandr", "--output", "LVDS-0",
                         "--pos", "1920x312", "--screen", "0"])

    def single_screen(self, widget, data=None):
        subprocess.call(["/usr/bin/xrandr", "--output", "VGA-0", "--off", 
                         "--screen", "0"])


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    indicator = AppIndicatorExample()
    main()
