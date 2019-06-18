#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin passwd.py
#       
#       Copyright 2011 Pablo Adolfo Cuyeu <mateman@Terra>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import getpass, sys, hashlib

def main():
    if(len(sys.argv) > 1):
       user = sys.argv[1]
    else:
       user = raw_input('Ingrese el nuevo usuario: ')
    while True:
        pwd = getpass.getpass('Ingrese una password: ')
        npwd = getpass.getpass('Ingrese nuevamente la password: ')
        if pwd == npwd:
           break
        else: print 'Las passwords no coinciden!\n'
    arch = open('claves.txt', 'a')
    arch.write(user+':'+hashlib.md5(pwd).hexdigest()+'\n')
    arch.close()
    print 'Nuevo usuario: '+user
    return 0

if __name__ == '__main__':
      main()

