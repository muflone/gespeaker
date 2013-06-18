##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2013 Fabio Castelli
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
# 
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

import gtk

def DialogAbout(name=None, version=None, comment=None,
    copyright=None, license=None, website=None, website_label=None,
    authors=None, translation=None, documentation=None, artists=None,
    logo=None, icon=None):
    "Show an About Dialog with specified arguments"
    about = gtk.AboutDialog()
    if name:
      about.set_name(name)
    if version:
      about.set_version(version)
    if comment:
      about.set_comments(comment)
    if copyright:
      about.set_copyright(copyright)
    if license:
      about.set_license(license)
    if website:
      about.set_website(website)
    if website_label:
      about.set_website_label(website_label)
      gtk.about_dialog_set_url_hook(lambda url, data=None: url)
    if authors:
      about.set_authors(authors)
    if translation:
      about.set_translator_credits(translation)
    if documentation:
      about.set_documenters(documentation)
    if artists:
      about.set_artists(artists)
    if logo:
      if isinstance(logo, gtk.gdk.Pixbuf):
        about.set_logo(logo)
      else:
        about.set_logo(gtk.gdk.pixbuf_new_from_file(logo))
    if icon:
      about.set_icon_from_file(icon)

    about.run()
    about.destroy()
