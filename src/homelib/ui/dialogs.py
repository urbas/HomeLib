# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: utils.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 11-Oct-2010, 09:04:13
# 
#  Copyright © 2010 Matej Urbas
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



from homelib.utils import flatten
from homelib.utils import runCmdGetString




"""
The name of the application which provides dialogs.
"""
ZENITY='zenity'

DLG_TYPE_calendar='calendar'
DLG_TYPE_entry='entry'
DLG_TYPE_error='error'
DLG_TYPE_file_selection='file-selection'
DLG_TYPE_info='info'
DLG_TYPE_list='list'
DLG_TYPE_notification='notification'
DLG_TYPE_progress='progress'
DLG_TYPE_question='question'
DLG_TYPE_text_info='text-info'
DLG_TYPE_warning='warning'
DLG_TYPE_scale='scale'



###
### Zenity Dialogs
###

##
#Opens a \c Zenity dialog of the given type with the specified title, text and
#other details.
#
#@param title   The title of the dialog (displayed in the title-bar of its
#               window).
#
#@param text    The text to be displayed as the main message of the dialog. This
#               text is located within the dialog.
#
#@param dialogType  <b>[Optional]</b> The type of dialog to open. Can be one of
#                   the following: \ref DLG_TYPE_calendar, \ref DLG_TYPE_entry,
#                   \ref DLG_TYPE_error, \ref DLG_TYPE_file_selection,
#                   \ref DLG_TYPE_info, \ref DLG_TYPE_list,
#                   \ref DLG_TYPE_notification, \ref DLG_TYPE_progress,
#                   \ref DLG_TYPE_question, \ref DLG_TYPE_text_info,
#                   \ref DLG_TYPE_warning or \ref DLG_TYPE_scale. If not given,
#                   'info' will be used.
#
#@param args    Other arguments to be passed to 'Zenity'. See
#               <b><tt>man zenity</tt></b> for more info.
#
#@returns    A pair-tuple, where the first element is the return code of the
#            finished process and the second element the string contents of
#            the application's output.
def dlg(title, text, dialogType=DLG_TYPE_info, *args):
    """
    Opens a \c Zenity dialog of the given type with the specified title, text and
    other details.

    @param title   The title of the dialog (displayed in the title-bar of its
                   window).

    @param text    The text to be displayed as the main message of the dialog. This
                   text is located within the dialog.

    @param dialogType  <b>[Optional]</b> The type of dialog to open. Can be one of
                       the following: \ref DLG_TYPE_calendar, \ref DLG_TYPE_entry,
                       \ref DLG_TYPE_error, \ref DLG_TYPE_file_selection,
                       \ref DLG_TYPE_info, \ref DLG_TYPE_list,
                       \ref DLG_TYPE_notification, \ref DLG_TYPE_progress,
                       \ref DLG_TYPE_question, \ref DLG_TYPE_text_info,
                       \ref DLG_TYPE_warning or \ref DLG_TYPE_scale. If not given,
                       'info' will be used.

    @param args    Other arguments to be passed to 'Zenity'. See
                   <b><tt>man zenity</tt></b> for more info.

    @returns    A pair-tuple, where the first element is the return code of the
                finished process and the second element the string contents of
                the application's output.
    """
    (retCode, retMsg) = runCmdGetString(ZENITY, '--' + (dialogType or DLG_TYPE_info), '--title', title, '--text', text, flatten(args))
    if retMsg.endswith('\n'):
        retMsg = retMsg[0:-1]
    return (retCode, retMsg)

##
#Shows a dialog with the question specified in \c text and returns \c True
#iff the user confirms.
#
#@param title   The title of the dialog (displayed in the title-bar of its
#               window).
#
#@param text    The text to be displayed as the main message of the dialog. This
#               text represents the actual question.
#
#@returns    \c True iff the user confirms.
def dlgQuestion(title, text):
    """
    Shows a dialog with the question specified in \c text and returns \c True
    iff the user confirms.

    @param title   The title of the dialog (displayed in the title-bar of its
                   window).

    @param text    The text to be displayed as the main message of the dialog. This
                   text represents the actual question.

    @returns    \c True iff the user confirms.
    """
    return dlg(title, text, DLG_TYPE_question)[0] == 0

##
#Shows a list dialog with the given columns and list items.
#
#@param title   The title of the dialog (displayed in the title-bar of its
#               window).
#
#@param text    The text to be displayed as the main message within the dialog.
#
#@param columns The columns of the list.
#
#@param items   The items of the list.
#
#@returns   A pair tuple. The first element of the tuple is the return code (0
#           iff the user pressed OK). The second element is the text of the
#           chosen cell in the list.
def dlgList(title, text, columns = ['Items'], *items):
    """
    Shows a list dialog with the given columns and list items.

    @param title   The title of the dialog (displayed in the title-bar of its
                   window).

    @param text    The text to be displayed as the main message within the dialog.

    @param columns The columns of the list.

    @param items   The items of the list.

    @returns   A pair tuple. The first element of the tuple is the return code (0
               iff the user pressed OK). The second element is the text of the
               chosen cell in the list.
    """
    return dlg(title, text, DLG_TYPE_list, ['--column=' + col for col in columns], items)

##
#Shows a list dialog with the given columns and list items.
#
#@param title   The title of the dialog (displayed in the title-bar of its
#               window).
#
#@param text    The text to be displayed as the main message within the dialog.
#
#@param entryText The pre-set entry text.
#
#@returns   A pair tuple. The first element of the tuple is the return code (0
#           iff the user pressed OK). The second element is the text the user
#           entered.
def dlgEntry(title, text, entryText = None):
    """
    Shows a list dialog with the given columns and list items.

    @param title   The title of the dialog (displayed in the title-bar of its
                   window).

    @param text    The text to be displayed as the main message within the dialog.

    @param entryText The pre-set entry text.

    @returns   A pair tuple. The first element of the tuple is the return code (0
               iff the user pressed OK). The second element is the text the user
               entered.
    """
    return dlg(title, text, DLG_TYPE_entry, ('--entry-text=' + entryText) if entryText else [])