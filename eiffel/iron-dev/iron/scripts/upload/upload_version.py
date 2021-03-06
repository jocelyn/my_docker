#!/usr/bin/python

import sys;
import os;
import shutil;
from subprocess import call


def trim(s):
	return s.strip()

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def cmd_call (cmd):
	print "CMD=%s" % (cmd)
	call(cmd, shell=True, stdout=sys.stdout)

def iron_command_name():
	return "iron"

def get_package_id (a_name):
	lines = os.popen (iron_command_name() + ' info ' + a_name).readlines ()
	for line in lines:
		s = trim(line)
		if s.startswith("id:"):
			s = s[3:]
			return trim(s)

def package_name_from_iron_package_file (pf):
	import re
	pf_name = None

	# import info data from `pf' if exists
	if os.path.exists (pf):
		f = open (pf, 'r')
		txt = f.read()
		f.close()
		regexp = r"\bpackage\s*([a-zA-Z][a-zA-Z0-9_+-]+)\b"
		p = re.compile (regexp);
		result = p.search (txt,0)
		if result:
			pf_name = result.group(1)
	return pf_name

def process_iron_package (ipfn, a_sources_dir, u,p,repo,v):
	import re;

	print "----"

	dict={}
	p_name = None
	p_description = None
	p_source = None

	p_name = package_name_from_iron_package_file (ipfn)
	if p_name == None:
		print "Unable to find package name from associated data file from: [%s]" % (ipfn)
		return

	if dict.has_key('name'):
		p_name = trim(dict['name'])

	if dict.has_key ('description'):
		p_description = trim(dict['description'])
		if len(p_description) == 0:
			p_description = None

#	if dict.has_key ('source'):
#		p_source = trim(dict['source'])
#		if len(p_source) == 0:
#			p_source = None

	p_source = os.path.normpath(os.path.dirname(ipfn))

	iron_create_cmd = "%s share create -u %s -p \"%s\" --repository %s --batch --package %s " % (iron_command_name(), u, p, repo, ipfn)

	iron_update_cmd = "%s share update -u %s -p \"%s\" --repository %s --batch --package %s " % (iron_command_name(), u, p, repo, ipfn)

	cmd = "%s" % (iron_create_cmd)
	if p_description != None:
		cmd = "%s --package-description \"%s\" " % (cmd, p_description)
		#call([iron_command_name(), 'share', 'create', '-u', u, '-p', p, '--repository', repo, '--batch', '--package-name', p_name, '--package-description', p_description], shell=True, stdout=sys.stdout)
	#else:
		#call([iron_command_name(), 'share', 'create', '-u', u, '-p', p, '--repository', repo, '--batch', '--package-name', p_name], shell=True, stdout=sys.stdout)
	cmd_call (cmd)

	if p_source != None:
		l_src = os.path.dirname(a_sources_dir)
		for seg in p_source.split('/'):
			l_src = os.path.join (l_src, seg)
		l_src = os.path.normpath (l_src)

		is_process_local_archive = False
		if is_process_local_archive:
			l_id = get_package_id (p_name)
			if l_id == None:
				print "No id for %s" % (p_name)
			else:
				if len (l_id) > 0:
					l_folder =  os.path.join (os.path.abspath('archive'), v, "items", l_id)
					if not os.path.exists (l_folder):
						os.makedirs(l_folder)
					cmd_call ("./iron/spec/unix/bin/iron_build_archive  %s %s %s" % (l_src, l_folder, "archive"))
					print ""
		else:
			cmd = "%s --force --package-archive-source \"%s\" " % (iron_update_cmd, l_src)
			cmd_call (cmd)
			print ""

	if not dict.has_key ('maps'):
		if p_source != None:
			p_sources_dir = os.path.normpath(a_sources_dir)
			if p_source.startswith (p_sources_dir):
				p_source = p_source[len(p_sources_dir) + 1:]
			m = p_source.replace ('\\', '/')
			m = "/com.eiffel/%s" % (m)
			print m
			dict['maps'] = [m]
	if dict.has_key ('maps'):
		p_maps = dict['maps']
		if len(p_maps) > 0:
			for m in p_maps:
				cmd = "%s --index \"%s\" " % (iron_update_cmd, m)
				cmd_call (cmd)
				print ""

def process_iron_package_files(a_dir, a_sources_dir, a_login, a_password, a_repo, a_version):
	l_nodes = os.listdir (a_dir)
	l_iron_package_found=False
	l_dirs=[]
	#print (a_dir)
	for f in l_nodes:
		ff = os.path.join (a_dir, f)
		if os.path.isdir(ff):
			if not f.startswith('.'):
				l_dirs.append (ff)
		else:
			if f == 'package.iron':
				l_iron_package_found = True
				process_iron_package (ff, a_sources_dir, a_login, a_password, a_repo, a_version)
				break
			
	if not l_iron_package_found:
		for d in l_dirs:
			process_iron_package_files(d, a_sources_dir, a_login, a_password, a_repo, a_version)

def upload_version(a_sources_dir):
	try:
		import credential;
	except ImportError:
		print "missing 'credential.py'"
		sys.exit()

	try:
		import repository_cfg;
	except ImportError:
		print "missing 'repository_cfg.py'"
		sys.exit()

	l_login = trim(credential.login())
	l_password = trim(credential.password())

	repo = "%s/%s" % (repository_cfg.repository(), repository_cfg.version())
	print "user [%s] on repository [%s]" % (l_login, repo)
	if not os.path.exists (a_sources_dir):
		print "source directory \"%s\" does not exist" % (a_sources_dir)
		sys.exit()

	print "Updating the ecf files for iron packaging ..."
	call([iron_command_name(), "update_ecf", "--save", "-D", "ISE_LIBRARY=%s" % (a_sources_dir), a_sources_dir])
	process_iron_package_files (a_sources_dir, a_sources_dir, l_login, l_password, repo, repository_cfg.version())


def main():
	if len(sys.argv) > 1:
		l_sources_dir = sys.argv[1]
		upload_version(l_sources_dir)
	else:
		print "Usage: prog {source_dir}"
		sys.exit()

if __name__ == '__main__':
	main()
	sys.exit()
