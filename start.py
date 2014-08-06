execfile('init.cfg')
servers = {}
for entry in initservers:
	servers[entry[0]] = entry[1:len(entry)]
print servers