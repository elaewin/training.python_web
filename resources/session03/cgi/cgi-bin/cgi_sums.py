#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
values = form.getlist('operand')
total = sum(map(int, values))

print("Content-type: text/plain")
print()
print("The total is {}".format(total))
