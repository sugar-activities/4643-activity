# Copyright 2013 Paolo Monsalvo - Willian Martinez
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA



import gtk
import logging
import gobject
import random
from ConfigParser import SafeConfigParser
from subprocess import Popen


from gettext import gettext as _

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton

class JugandoAprendesActivity(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        
        self.load_data()
        self.cargar_ui()
        

        # label with the text, make the string translatable
    def cargar_ui(self):
        vbox = gtk.VBox()
        self.set_canvas(vbox)
        self.hbox = gtk.HBox()
        label = gtk.Label()
        self.connect('key-press-event', self.__key_press_cb, label)
        vbox.add(self.hbox)

        self.cargar_imagen()

        vbox.show_all()
            
    def load_data(self):
        self.cadenaPrevia = 'bienvenido al juego................'
        self.indice = 0
        
    def remover_imagen(self):
        self.cadenaPatron = ''
        self.hbox.remove(self.image1)
        self.hbox.remove(self.image2)
        self.hbox.remove(self.image3)
        self.hbox.remove(self.image4)
        
    def cargar_imagen(self):
        self.patron=['arriba','abajo','izquierda', 'derecha']

        self.listaAux = ['','','','']
        pos = random.randint(0, 3)
        self.listaAux[0] = self.patron[pos]
        pos = random.randint(0, 3)
        self.listaAux[1] = self.patron[pos]
        pos = random.randint(0, 3)
        self.listaAux[2] = self.patron[pos]
        pos = random.randint(0, 3)
        self.listaAux[3] = self.patron[pos]
        self.patron = self.listaAux

        self.cadenaPatronAux = ' '.join(self.patron)
        self.cadenaPatron = self.cadenaPrevia + self.cadenaPatronAux
        self.say(self.cadenaPatron)

        self.image1=gtk.Image()
        self.image1.set_from_file('imagenes/'+self.patron[0]+'.png')
        self.image1.show()
        self.hbox.pack_start(self.image1)

        self.image2=gtk.Image()
        self.image2.set_from_file('imagenes/'+self.patron[1]+'.png')
        self.image2.show()
        self.hbox.pack_start(self.image2)

        self.image3=gtk.Image()
        self.image3.set_from_file('imagenes/'+self.patron[2]+'.png')
        self.image3.show()
        self.hbox.pack_start(self.image3)

        self.image4=gtk.Image()
        self.image4.set_from_file('imagenes/'+self.patron[3]+'.png')
        self.image4.show()
        self.hbox.pack_start(self.image4)
        
    def controlar_patron(self, key_name):
        self.cadenaPrevia = ''
        if(self.indice < 4 and self.key_name == self.patron[self.indice]):
            self.cadenaPrevia = 'correcto'
            self.indice = self.indice + 1
            if(self.indice == 4):
                self.cadenaPrevia += '...Felicitaciones'
                self.cadenaPrevia += '...Empecemos con el siguiente juego...'
                self.remover_imagen()
                self.cargar_imagen()
                self.indice = 0
        else:
            self.say('fallaste vuelve a intentar'+self.cadenaPatronAux)
            self.indice = 0

        self.say(self.cadenaPrevia)
        
    def leer_patrones(self):
        self.say(self.patron_nuevo)    
        self.id=0  
        self.flag=1
        
    def generar_patrones(self):
        
        if (self.flag==0):
            self.patron=['arriba','abajo','izquierda', 'derecha']
            random.shuffle(self.patron)
            self.patron_nuevo="    ".join(self.patron)
            self.hbox.remove(self.image1)
            self.hbox.remove(self.image2)
            self.hbox.remove(self.image3)
            self.hbox.remove(self.image4)
            
            self.image1=gtk.Image()
            self.image1.set_from_file('imagenes/'+self.patron[0]+'.png')
            self.image1.show()
            self.hbox.pack_start(self.image1)
            
            self.image2=gtk.Image()
            self.image2.set_from_file('imagenes/'+self.patron[1]+'.png')
            self.image2.show()
            self.hbox.pack_start(self.image2)
            
            self.image3=gtk.Image()
            self.image3.set_from_file('imagenes/'+self.patron[2]+'.png')
            self.image3.show()
            self.hbox.pack_start(self.image3)
            
            self.image4=gtk.Image()
            self.image4.set_from_file('imagenes/'+self.patron[3]+'.png')
            self.image4.show()
            self.hbox.pack_start(self.image4)
            self.leer_patrones()    
              
            
    def __key_press_cb(self, window, event, label):
        self.key_name = gtk.gdk.keyval_name(event.keyval)
        if (self.key_name=='Up'):
            self.key_name='arriba'
            self.controlar_patron(self.key_name)
        elif (self.key_name=='Down'):
            self.key_name='abajo'
            self.controlar_patron(self.key_name)
        elif (self.key_name=='Left'):
            self.key_name='izquierda'
            self.controlar_patron(self.key_name)
        elif (self.key_name=='Right'):
            self.key_name='derecha'
            self.controlar_patron(self.key_name)
        elif (self.key_name == 'space'):
            self.say(self.cadenaPatronAux)
            self.indice = 0
        else:
            self.say('Tecla incorrecta')

                       
    def say(self, text):
        Popen(['espeak', '-v', 'es', text])
        
    def read_file(self, file_name):
        self.patron=self.metadata['juego']
        
    def write_file(self, file_name):
        self.metadata['juego']=self.patron
    
    
