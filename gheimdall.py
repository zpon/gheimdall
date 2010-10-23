#!/usr/bin/env python
# -*- coding: UTF8 -*-

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

class Gheimdall:

	currentPath = ""
	params = []
	# found files
	# Not recognized
	foundpda = []
	nrpda = []
	foundphone = []
	nrphone = []
	foundcsc = []
	nrcsc = []
	# Files accepted in pda, phone and csc
	pdafiles = ["zImage", "dbdata.rfs", "param.lfs", "factoryfs.rfs", "boot.bin", "cache.rfs", "Sbl.bin"]
	phonefiles = ["modem.bin"]
	cscfiles = ["dbdata.rfs", "cache.rfs"]
	
	parameters = {"zImage":"--kernel", "dbdata.rfs":"--dbdata", "param.lfs":"--param", "factoryfs.rfs":"--factoryfs", "boot.bin":"--boot", "cache.rfs":"--cache", "modem.bin":"--modem", "Sbl.bin":"--secondary"}

	def generateCode(self, widget, data=None):
		# Check Pda
		try:
			if tarfile.is_tarfile(self.etrPda.get_text()):
				pdatar = tarfile.open(self.etrPda.get_text())
				members = pdatar.getnames()
				for name in members:
					if name in self.pdafiles and name not in self.params:
						self.params.append(name)
						self.foundpda.append(name)
					elif name not in self.pdafiles:
						self.nrpda.append(name)
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
					if name in self.phonefiles and name not in self.params:
						self.params.append(name)
						self.foundphone.append(name)
					elif name not in self.phonefiles:
						self.nrphone.append(name)
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
					if name in self.cscfiles:
						if name not in self.params:
							self.params.append(name)
						self.foundcsc.append(name)
					elif name not in self.cscfiles:
						self.nrcsc.append(name)
			else:
				print "TODO handle csc not tar file"
		except(ValueError):
			print "TODO handle csc no file"

		print self.params
		print self.nrpda
		print self.nrphone
		print self.nrcsc

		

		txtbuffer = gtk.TextBuffer()
		self.txtResult.set_buffer(txtbuffer)
		
		tmp = "EXTRACTING FROM PDA\n"
		for name in self.foundpda:
			tmp += "Extracting " + name + ".."
			txtbuffer.set_text(tmp)
			while gtk.events_pending():
				gtk.main_iteration_do(False)

			# Do the ectual extraction
			pdatar.extract(name, ".")
			
			tmp += " DONE\n"
			txtbuffer.set_text(tmp)
			while gtk.events_pending():
				gtk.main_iteration_do(False)
		
		tmp += "\nEXTRACTING FROM PHONE\n"
		for name in self.foundphone:
			tmp += "Extracting " + name + ".."
			txtbuffer.set_text(tmp)
			while gtk.events_pending():
				gtk.main_iteration_do(False)

			# Do the ectual extraction
			phonetar.extract(name, ".")
			
			tmp += " DONE\n"
			txtbuffer.set_text(tmp)
			while gtk.events_pending():
				gtk.main_iteration_do(False)
		
		tmp += "\nEXTRATING FROM CSC\n"
		for name in self.foundcsc:
			tmp += "Extracting " + name + ".."
			txtbuffer.set_text(tmp)
			while gtk.events_pending():
				gtk.main_iteration_do(False)

			# Do the ectual extraction
			csctar.extract(name, ".")
			
			tmp += " DONE\n"
			txtbuffer.set_text(tmp)
			while gtk.events_pending():
				gtk.main_iteration_do(False)

		tmp += "\nEXTRACTIONS FINISHED\nNow run the following command:\n"
		tmp += "\nheimdall flash --pit " + self.etrPit.get_text()
		for element in self.params:
			tmp += " " + self.parameters[element] + " " + element
		txtbuffer.set_text(tmp)
		
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
			if len(self.currentPath) > 0:
				dialog.set_current_folder_uri(self.currentPath)
			if len(data[1].get_text()) > 0:
				dialog.select_filename(data[1].get_text())

			if data[2] == 1:
				filter = gtk.FileFilter()
				filter.set_name("Tar archives")
				filter.add_mime_type("application/x-tar")
				dialog.add_filter(filter)
			elif data[2] == 2:
				filter = gtk.FileFilter()
				filter.set_name("PIT files")
				filter.add_pattern("*.pit")
				filter.add_pattern("*.PIT")
				filter.add_pattern("*.Pit")
				dialog.add_filter(filter)
			
			filter = gtk.FileFilter()
			filter.set_name("All files")
			filter.add_pattern("*")
			dialog.add_filter(filter)


			response = dialog.run()
			if response == gtk.RESPONSE_OK:
				data[1].set_text(dialog.get_filename())
				self.currentPath = dialog.get_current_folder_uri()
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
		self.window.set_title("gheimdall")

		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		# Sets the border width of the window.
		self.window.set_border_width(5)

		self.vbox = gtk.VBox(False,4)

		# Pit file
		self.lblPit = gtk.Label("Choose PIT file")
		self.lblPit.set_alignment(0, 0)
		self.hboxPit = gtk.HBox(False,0)
		self.etrPit = gtk.Entry()
		self.etrPit.set_editable(False)
		self.etrPit.set_sensitive(False)
		self.btnPit = gtk.Button("Browse")
		self.btnPitclear = gtk.Button("Clear")

		self.btnPit.connect("clicked", self.showDialog, ["Choose PIT file..", self.etrPit, 2])
		self.btnPitclear.connect("clicked", self.clear, self.etrPit)

		self.vbox.add(self.lblPit)
		self.vbox.add(self.hboxPit)
		self.hboxPit.add(self.etrPit)
		self.hboxPit.add(self.btnPit)
		self.hboxPit.add(self.btnPitclear)
		self.lblPit.show()
		self.btnPit.show()
		self.btnPitclear.show()
		self.etrPit.show()
		self.hboxPit.show()

		# PDA box
		self.lblPda = gtk.Label("Choose PDA (CODE) file")
		self.lblPda.set_alignment(0, 0)
		self.hboxPda = gtk.HBox(False,0)
		self.etrPda = gtk.Entry()
		self.etrPda.set_editable(False)
		self.etrPda.set_sensitive(False)
		self.btnPda = gtk.Button("Browse")
		self.btnPdaclear = gtk.Button("Clear")

		self.btnPda.connect("clicked", self.showDialog, ["Choose PDA (CODE) file..", self.etrPda, 1])
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

		self.btnPhone.connect("clicked", self.showDialog, ["Choose PHONE (MODEM) file..", self.etrPhone, 1])
		self.btnPhoneclear.connect("clicked", self.clear, self.etrPhone)

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

		self.btnCsc.connect("clicked", self.showDialog, ["Choose CSC file..", self.etrCsc, 1])
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

		self.sw = gtk.ScrolledWindow()
		self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		self.txtResult = gtk.TextView()
		self.txtResult.set_size_request(500, 100)
		self.txtResult.set_editable(False)
		self.sw.add(self.txtResult)
		self.vbox.add(self.sw)
		self.sw.show()
		self.txtResult.show()


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
	gh = Gheimdall()
	gh.main()
