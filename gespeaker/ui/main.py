##
#     Project: Gespeaker
# Description: A GTK frontend for espeak
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2021 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from .about import AboutWindow
from .files_dialog import FilesDialog
from .messages_dialog import MessagesDialog

from gespeaker.constants import (APP_NAME,
                                 FILE_GENDER_MALE,
                                 FILE_GENDER_FEMALE,
                                 FILE_GENDER_UNKNOWN,
                                 FILE_ICON)
from gespeaker.engines.base import KEY_LANGUAGE, KEY_NAME, KEY_GENDER
from gespeaker.functions import _, get_ui_file
from gespeaker.gtkbuilder_loader import GtkBuilderLoader
from gespeaker.ui.models.engines import ModelEngines
from gespeaker.ui.models.languages import ModelLanguages


class MainWindow(object):
    def __init__(self, application, backend):
        self.application = application
        self.ui = GtkBuilderLoader(get_ui_file('main.glade'))
        self.backend = backend
        self.backend.on_play_complete = self.on_backend_play_complete
        self.model_engines = None
        self.model_languages = None
        self.clipboard = None
        self.load_user_interface()
        # Restore the saved size and position
        if self.backend.settings.get_value('width', 0) and \
                self.backend.settings.get_value('height', 0):
            self.ui.window_main.set_default_size(
                self.backend.settings.get_value('width', -1),
                self.backend.settings.get_value('height', -1))
        if self.backend.settings.get_value('left', 0) and \
                self.backend.settings.get_value('top', 0):
            self.ui.window_main.move(
                self.backend.settings.get_value('left', 0),
                self.backend.settings.get_value('top', 0))

    def run(self):
        """
        Show the UI
        """
        self.ui.window_main.show_all()

    def load_user_interface(self):
        """
        Load the interface UI
        """
        # Load available engines
        self.model_engines = ModelEngines(self.ui.model_engines)
        for engine_name, obj_engine in self.backend.engines.items():
            # Add a new CheckMenuItem for each engine
            menu_engine = Gtk.CheckMenuItem(engine_name)
            # Load the engine status from the settings
            obj_engine.enabled = self.backend.settings.get_engine_status(
                engine_name)
            menu_engine.set_active(obj_engine.enabled)
            menu_engine.connect('toggled',
                                self.on_action_enable_engine_toggled,
                                obj_engine)
            self.ui.menu_engines.append(menu_engine)
        # Load available languages
        self.model_languages = ModelLanguages(
            model=self.ui.model_languages,
            icon_male=GdkPixbuf.Pixbuf.new_from_file_at_size(
                FILE_GENDER_MALE, 24, 24),
            icon_female=GdkPixbuf.Pixbuf.new_from_file_at_size(
                FILE_GENDER_FEMALE, 24, 24),
            icon_unknown=GdkPixbuf.Pixbuf.new_from_file_at_size(
                FILE_GENDER_UNKNOWN, 24, 24))
        self.ui.treemodelsort_languages.set_sort_column_id(
            self.model_languages.COL_DESCRIPTION, Gtk.SortType.ASCENDING)
        self.on_action_reload_activate(None)
        self.on_combobox_engines_changed(None)
        # Set various properties
        self.ui.window_main.set_title(APP_NAME)
        self.ui.window_main.set_icon_from_file(FILE_ICON)
        self.ui.window_main.set_application(self.application)
        # Set the actions accelerator group
        for group_name in ('actions_application',
                           'actions_edit',
                           'actions_file',
                           'actions_media'):
            if isinstance(self.ui.get_object(group_name), Gtk.ActionGroup):
                for action in self.ui.get_object(group_name).list_actions():
                    action.set_accel_group(self.ui.accelerators)
        # Define the clipboard object for cut/copy/paste actions
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        # Connect signals from the glade file to the functions with the
        # same name
        self.ui.connect_signals(self)

    def on_window_main_delete_event(self, widget, event):
        """
        Close the application
        """
        self.on_action_quit_activate(widget)

    def on_action_about_activate(self, action):
        """
        Show the about dialog
        """
        dialog = AboutWindow(self.ui.window_main, False)
        dialog.show()
        dialog.destroy()

    def on_action_quit_activate(self, action):
        """
        Quit the application
        """
        # Stop any previous play
        self.ui.action_play_stop.set_active(False)
        # Save settings for window size
        self.backend.settings.set_sizes(self.ui.window_main)
        self.backend.settings.save()
        self.ui.window_main.destroy()
        self.application.quit()

    def _get_current_engine(self):
        """
        Return the currently selected engine
        """
        if self.ui.combobox_engines.get_active_iter():
            return self.model_engines.get_engine(
                self.ui.combobox_engines.get_active_iter())
        else:
            return None

    def _get_current_language_engine(self):
        """
        Return the engine used for the currently selected language
        """
        return self.model_languages.get_engine(
            self.ui.treemodelsort_languages.convert_iter_to_child_iter(
                self.ui.combobox_languages.get_active_iter()))

    def _get_current_language_name(self):
        """
        Return the name for the currently selected language
        """
        return self.model_languages.get_name(
            self.ui.treemodelsort_languages.convert_iter_to_child_iter(
                self.ui.combobox_languages.get_active_iter()))

    def on_combobox_engines_changed(self, widget):
        """
        Update languages list after engine change
        """
        self.model_languages.clear()
        current_engine = self._get_current_engine()
        for obj_engine in self.backend.engines.values():
            # Load languages only for selected engine
            if obj_engine.name == current_engine and obj_engine.enabled:
                for language in obj_engine.get_languages():
                    self.model_languages.add(
                        engine=obj_engine.name,
                        description='{LANGUAGE} {GENDER} ({NAME})'.format(
                            LANGUAGE=language[KEY_LANGUAGE],
                            GENDER={'male': _('Male'),
                                    'female': _('Female'),
                                    'other': _('Unknown')}.get(
                                        language[KEY_GENDER],
                                        'other'),
                            NAME=language[KEY_NAME]),
                        name=language[KEY_NAME],
                        gender=language[KEY_GENDER]
                    )
        self.on_buffer_text_changed(None)
        self.ui.combobox_languages.set_tooltip_text(
            '%d languages available' % self.model_languages.count())
        self.ui.combobox_languages.set_active(0)

    def on_action_clipboard_activate(self, action):
        """
        Cut and copy the selected text or paste it
        """
        editable = self.ui.text_text.get_editable()
        if action is self.ui.action_cut:
            self.ui.buffer_text.cut_clipboard(self.clipboard, editable)
        elif action is self.ui.action_copy:
            self.ui.buffer_text.copy_clipboard(self.clipboard)
        elif action is self.ui.action_paste:
            self.ui.buffer_text.paste_clipboard(self.clipboard, None, editable)

    def on_action_play_stop_toggled(self, action):
        """
        Play or stop play
        """
        if self.ui.action_play_stop.get_active():
            self.ui.action_play_stop.set_label(self.ui.action_stop.get_label())
            self.ui.button_play.set_image(self.ui.image_stop)
            # Play the text
            self.backend.set_current_engine(
                self._get_current_language_engine())
            self.backend.play(
                text=self.ui.buffer_text.get_text(
                    self.ui.buffer_text.get_start_iter(),
                    self.ui.buffer_text.get_end_iter(), False),
                language=self._get_current_language_name())
            self.ui.action_pause.set_active(False)
            self.ui.action_pause.set_sensitive(True)
            self.ui.action_record.set_sensitive(False)
        else:
            # Stop any previous play
            self.ui.button_play.set_image(self.ui.image_play)
            self.ui.action_play_stop.set_label(self.ui.action_play.get_label())
            self.ui.action_record.set_sensitive(True)
            self.backend.stop()

    def on_action_pause_toggled(self, action):
        """
        Pause or resume
        """
        if self.ui.action_play_stop.get_active():
            # Pause or resume
            self.backend.pause(self.ui.action_pause.get_active())
        else:
            # Uncheck the Pause button if no playing is active
            self.ui.action_pause.set_active(False)

    def on_action_reload_activate(self, action):
        """
        Reload the available voices list
        """
        self.model_engines.clear()
        self.model_languages.clear()
        for obj_engine in self.backend.engines.values():
            # Load languages only for enabled engines
            if obj_engine.enabled:
                self.model_engines.add(obj_engine.name, obj_engine.name)
        # Select the first item
        self.ui.combobox_engines.set_active(0)
        self.ui.combobox_languages.set_active(0)

    def on_action_enable_engine_toggled(self, action, engine):
        """
        Enable or disable an engine
        """
        engine.enabled = action.get_active()
        self.backend.settings.set_engine_status(engine.name, engine.enabled)
        self.on_action_reload_activate(action)

    def on_backend_play_complete(self):
        """
        Whenever a playing is completed uncheck the Play button and
        disable the Pause button
        """
        self.ui.action_play_stop.set_active(False)
        self.ui.action_pause.set_active(False)
        self.ui.action_pause.set_sensitive(False)

    def on_action_open_activate(self, action):
        """
        Load an external text file
        """
        dialog = FilesDialog(self.ui.window_main)
        dialog.add_filter(_('Text files'), ('text/*',), ('*.txt',))
        dialog.add_filter(_('All files'), None, ('*',))
        dialog.title = _('Please select the text file to open')
        filename = dialog.show_open()
        if filename:
            try:
                # Open the selected text file
                with open(filename, 'r') as f:
                    self.backend.settings.debug_line(
                        'loading text from {FILE}'.format(FILE=filename))
                    self.ui.buffer_text.set_text(f.read())
            except Exception as error:
                # Handle any exception
                self.backend.settings.debug_line(
                    'Error loading {FILE} (Error: {ERROR})'.format(
                        FILE=filename,
                        ERROR=error))
                dialog = MessagesDialog(self.ui.window_main)
                dialog.primary_text = _('Error opening the file')
                dialog.secondary_text = error
                dialog.show_error()

    def on_action_save_as_activate(self, action):
        """
        Save the text to an external text file
        """
        dialog = FilesDialog(self.ui.window_main)
        dialog.add_filter(_('Text files'), ('text/*',), ('*.txt',))
        dialog.add_filter(_('All files'), None, ('*',))
        dialog.title = _('Please select where to save the text file')
        filename = dialog.show_save()
        if filename:
            try:
                # Save to the selected text file
                with open(filename, 'w') as f:
                    self.backend.settings.debug_line(
                        'saving text in {FILE}'.format(FILE=filename))
                    f.write(self.ui.buffer_text.get_text(
                        start=self.ui.buffer_text.get_start_iter(),
                        end=self.ui.buffer_text.get_end_iter(),
                        include_hidden_chars=False))
            except Exception as error:
                # Handle any exception
                self.backend.settings.debug_line(
                    'Error saving to {FILE} (Error: {ERROR})'.format(
                        FILE=filename,
                        ERROR=error))
                dialog = MessagesDialog(self.ui.window_main)
                dialog.primary_text = _('Error saving the file')
                dialog.secondary_text = error
                dialog.show_error()

    def on_action_new_activate(self, action):
        """
        Clear the text buffer
        """
        if len(self.ui.buffer_text.get_text(
                start=self.ui.buffer_text.get_start_iter(),
                end=self.ui.buffer_text.get_end_iter(),
                include_hidden_chars=False)) > 0:
            dialog = MessagesDialog(self.ui.window_main)
            dialog.title = ''
            dialog.primary_text = _('Do you want to delete the current text?')
            if dialog.show_question() == Gtk.ResponseType.OK:
                self.backend.settings.debug_line('text cleared')
                self.ui.buffer_text.set_text('')

    def on_action_record_activate(self, action):
        """
        Record the text to play
        """
        dialog = MessagesDialog(self.ui.window_main)
        dialog.primary_text = _('Not implemented yet!')
        dialog.show_warning()
        self.ui.action_play_stop.activate()

    def on_action_preferences_activate(self, action):
        """
        Show the preferences dialog
        """
        dialog = MessagesDialog(self.ui.window_main)
        dialog.primary_text = _('Not implemented yet!')
        dialog.show_warning()

    def on_buffer_text_changed(self, widget):
        """
        Enable or disable the New and Save actions on text change
        """
        text = self.ui.buffer_text.get_text(
            self.ui.buffer_text.get_start_iter(),
            self.ui.buffer_text.get_end_iter(),
            True)
        has_text = len(text) > 0
        # New and Save actions depend on the written text
        self.ui.action_new.set_sensitive(has_text)
        self.ui.action_save_as.set_sensitive(has_text)
        # For voices settings and Play action check the number of languages
        has_languages = self.model_languages.count() > 0
        self.ui.label_engine.set_sensitive(has_languages)
        self.ui.combobox_languages.set_sensitive(has_languages)
        self.ui.label_language.set_sensitive(has_languages)
        self.ui.action_play_stop.set_sensitive(has_text and has_languages)
        self.ui.action_record.set_sensitive(has_text and has_languages)
