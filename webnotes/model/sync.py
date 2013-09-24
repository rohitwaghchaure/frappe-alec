# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

from __future__ import unicode_literals
"""
	Sync's doctype and docfields from txt files to database
	perms will get synced only if none exist
"""
import webnotes
import os
import conf
from webnotes.modules.import_file import import_file
from webntoes.utils import get_base_path

def sync_all(force=0):
	sync_for("lib", force)
	sync_for("app", force)
	webnotes.clear_cache()

def sync_for(folder, force=0, sync_everything = False):
	return walk_and_sync(os.path.join(get_base_path(),
		folder), force, sync_everything)

def walk_and_sync(start_path, force=0, sync_everything = False):
	"""walk and sync all doctypes and pages"""

	modules = []
	
	document_type = ['doctype', 'page', 'report']

	for path, folders, files in os.walk(start_path):
		# sort folders so that doctypes are synced before pages or reports
		folders.sort()

		if sync_everything or (os.path.basename(os.path.dirname(path)) in document_type):
			for f in files:
				if f.endswith(".txt"):
					doc_name = f.split(".txt")[0]
					if doc_name == os.path.basename(path):

						module_name = path.split(os.sep)[-3]
						doctype = path.split(os.sep)[-2]
						name = path.split(os.sep)[-1]
						
						if import_file(module_name, doctype, name, force):
							print module_name + ' | ' + doctype + ' | ' + name

						webnotes.conn.commit()
					
	return modules
