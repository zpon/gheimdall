#!/usr/bin/env python

"""
gheimdall a GTK frontend for heimdall

Copyright (c) Søren Juul (2010) <zpon.dk@gmail.com> (zpon at xdadevelopers)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

I TAKE NO RESPONSIBILITY FOR THE USE OF THIS CODE! IT MAY BRICK YOUR PHONE,
VOID YOU WARRANTY, CAUSE FLOODING AND IN MANY OTHER WAYS CAUSE HARM. 
ALWAYS REMEMBER TO CHECK UP ON THE ACTIONS EFFECT AND READ UP ON THEORY BEFORE
DOING ANYTHING YOUR NOT SURE OF.


Big credits to Benjamin Dobell for creating heimdall (http://www.glassechidna.com.au/products/heimdall/)
"""

import tarfile
import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld:

	params = []
	notrecognized = []

	def generateCode(self, widget, data=None):
		# Check Pda
		try:
			if tarfile.is_tarfile(self.etrPda.get_text()):
				pdatar = tarfile.open(self.etrPda.get_text())
				members = pdatar.getnames()
				for name in members:
					if name == "zImage":
						self.params.append("--kernel zImage")
					elif name == "dbdata.rfs":
						self.params.append("--dbdata dbdata.rfs")
					elif name == "factoryfs.rfs":
						self.params.append("--factoryfs factoryfs.rfs")
					elif name == "param.lfs":
						self.params.append("--param param.lfs")
					elif name == "boot.bin":
						self.params.append("--boot boot.bin")
					elif name == "cache.rfs":
						self.params.append("--cache cache.rfs")
					else:
						self.notrecognized.append(name)
				print self.params
				print self.notrecognized
			else:
				print "TODO handle pda not tar file"
		except(ValueError):
			print "TODO handle PDA no file"

		# Check Phone
		try:
			if tarfile.is_tarfile(self.etrPhone.get_text()):
				phonetar = tarfile.open(self.etrPhone.get_text())
				members = phonetar.getnames()
				for name in members:
					if name == "modem.bin":
						self.params.append("--modem modem.bin")
					else:
						self.notrecognized.append(name)
				print self.notrecognized
			else:
				print "TODO handle phone not tar file"
		except(ValueError):
			print "TODO handle phone no file"

		# Check CSC
		try:
			if tarfile.is_tarfile(self.etrCsc.get_text()):
				csctar = tarfile.open(self.etrCsc.get_text())
				members = csctar.getnames()
				for name in members:
					if name == "dbdata.rfs":
						self.params.append("--dbdata dbdata.rfs")
					elif name == "cache.rfs":
						self.params.append("--cache cache.rfs")
					else:
						self.notrecognized.append(name)
			else:
				print "TODO handle csc not tar file"
		except(ValueError):
			print "TODO handle csc no file"

		print self.params
		print self.notrecognized


	# Filechooser dialog
	# data = [title, where-to-write-result]
	def showDialog(self, widget, data=None):
		if data != None:
			dialog = gtk.FileChooserDialog(data[0],
				       self.window,
				       gtk.FILE_CHOOSER_ACTION_OPEN,
				       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
					gtk.STOCK_OPEN, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)

			filter = gtk.FileFilter()
			filter.set_name("Tar archives")
			filter.add_mime_type("application/x-tar")
			dialog.add_filter(filter)
			
			filter = gtk.FileFilter()
			filter.set_name("All files")
			filter.add_pattern("*")
			dialog.add_filter(filter)


			response = dialog.run()
			if response == gtk.RESPONSE_OK:
				data[1].set_text(dialog.get_filename())
			elif response == gtk.RESPONSE_CANCEL:
				print 'Closed, no files selected'
			dialog.destroy()

	def clear(self, widget, data):
		data.set_text("")

	def delete_event(self, widget, event, data=None):
		print "delete event occurred"
		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

	def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		# Sets the border width of the window.
		self.window.set_border_width(10)

		self.vbox = gtk.VBox(False,0)

		# PDA box
		self.lblPda = gtk.Label("Choose PDA (CODE) file")
		self.lblPda.set_alignment(0, 0)
		self.hboxPda = gtk.HBox(False,0)
		self.etrPda = gtk.Entry()
		self.etrPda.set_editable(False)
		self.etrPda.set_sensitive(False)
		self.btnPda = gtk.Button("Browse")
		self.btnPdaclear = gtk.Button("Clear")

		self.btnPda.connect("clicked", self.showDialog, ["Choose PDA (CODE) file..", self.etrPda])
		self.btnPdaclear.connect("clicked", self.clear, self.etrPda)

		self.vbox.add(self.lblPda)
		self.vbox.add(self.hboxPda)
		self.hboxPda.add(self.etrPda)
		self.hboxPda.add(self.btnPda)
		self.hboxPda.add(self.btnPdaclear)
		self.lblPda.show()
		self.btnPda.show()
		self.btnPdaclear.show()
		self.etrPda.show()
		self.hboxPda.show()
		
		# PHONE box
		self.lblPhone = gtk.Label("Choose PHONE (MODEM) file")
		self.lblPhone.set_alignment(0, 0)
		self.hboxPhone = gtk.HBox(False,0)
		self.etrPhone = gtk.Entry()
		self.etrPhone.set_editable(False)
		self.etrPhone.set_sensitive(False)
		self.btnPhone = gtk.Button("Browse")
		self.btnPhoneclear = gtk.Button("Clear")

		self.btnPhone.connect("clicked", self.showDialog, ["Choose PHONE (MODEM) file..", self.etrPhone])
		self.btnPhone.connect("clicked", self.clear, self.etrPhone)

		self.vbox.add(self.lblPhone)
		self.vbox.add(self.hboxPhone)
		self.hboxPhone.add(self.etrPhone)
		self.hboxPhone.add(self.btnPhone)
		self.hboxPhone.add(self.btnPhoneclear)
		self.lblPhone.show()
		self.btnPhone.show()
		self.etrPhone.show()
		self.btnPhoneclear.show()
		self.hboxPhone.show()

		# CSC box
		self.lblCsc = gtk.Label("Choose CSC file")
		self.lblCsc.set_alignment(0, 0)
		self.hboxCsc = gtk.HBox(False,0)
		self.etrCsc = gtk.Entry()
		self.etrCsc.set_editable(False)
		self.etrCsc.set_sensitive(False)
		self.btnCsc = gtk.Button("Browse")
		self.btnCscclear = gtk.Button("Clear")

		self.btnCsc.connect("clicked", self.showDialog, ["Choose CSC file..", self.etrCsc])
		self.btnCscclear.connect("clicked", self.clear, self.etrCsc)

		self.vbox.add(self.lblCsc)
		self.vbox.add(self.hboxCsc)
		self.hboxCsc.add(self.etrCsc)
		self.hboxCsc.add(self.btnCsc)
		self.hboxCsc.add(self.btnCscclear)
		self.lblCsc.show()
		self.btnCsc.show()
		self.etrCsc.show()
		self.btnCscclear.show()
		self.hboxCsc.show()


		self.btnGenerate = gtk.Button("Generate code")
		self.btnGenerate.connect("clicked", self.generateCode, None)
		self.vbox.add(self.btnGenerate)
		self.btnGenerate.show()

		self.window.add(self.vbox)
		self.vbox.show()

		# and the window
		self.window.show()

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()
