# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: referencer.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 24-Oct-2010, 11:33:34
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


def getReferencerDevelopmentDependencies():
    """
    @returns    A list of packages one needs to successfully build Referencer
                from sources.
    """
    return [
        'gconfmm26-devel',
        'gtkmm24-devel',
        'libglademm24-devel',
        'gnome-vfsmm26-devel',
        'poppler-glib-devel',
        'libxml2-devel',
        'boost-devel',
        'gettext',
        'gettext-devel',
        'python-devel',
        'gnome-common',
        'libgnomeuimm26-devel',
        'gnome-doc-utils'
    ]