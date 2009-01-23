# $Id: __init__.py,v 1.1 2009/01/16 23:58:15 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.1  2009/01/16 23:58:15  bruno
# configuring the boot action and writing the boot files (e.g., PXE host config
# files and Xen config files) are now done in exactly the same way.
#
#

import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Set the run action for a list of hosts.
	
	<arg type='string' name='host' repeat='1'>
	One or more host names.
	</arg>

	<arg type='string' name='action'>
	The run action to assign to each host. To get a list of all actions,
	execute: "rocks list host bootaction".
	</arg>

	<param optional='1' type='string' name='action'>
	Can be used in place of the action argument.
	</param>

	<example cmd='set host runaction compute-0-0 os'>
	Sets the run action to "os" for compute-0-0.
	</example>

	<example cmd='set host runaction compute-0-0 compute-0-1 memtest'>
	Sets the run action to "memtest" for compute-0-0 and compute-0-1.
	</example>

	<example cmd='set host runaction compute-0-0 compute-0-1 action=memtest'>
	Same as above.
	</example>
	"""

	def run(self, params, args):
		(args, action) = self.fillPositionalArgs(('action',))
		
		if not len(args):
			self.abort('must supply host')
		if not action:
			self.abort('must supply an action')

		if action.lower() == 'none':
			runaction = 'NULL'
		else:
			rows = self.db.execute("""select * from bootaction where
				action = '%s' """ % action)
			if rows != 1:
				self.abort('action "%s" does not exist' %
					action)
			runaction = "'%s'" % action
			
		for host in self.getHostnames(args):
			self.db.execute("""update nodes set runaction=%s
				where name='%s'""" % (runaction, host))
		