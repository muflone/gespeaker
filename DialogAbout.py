##
# Project: gespeaker - A GTK frontend for espeak  
#  Author: Muflone Ubuntu Trucchi <muflone@vbsimple.net>
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
      about.set_logo(gtk.gdk.pixbuf_new_from_file(logo))
    if icon:
      about.set_icon_from_file(icon)

    about.run()
    about.destroy()
