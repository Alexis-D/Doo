#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import os
import os.path as path
import sys
import textwrap

DOO_PATH = path.join(path.expanduser('~'), '.doo')
FORMAT = '{:4d} - {}'
# PARSE_STRING = '^\s*(\d+) - (.*)$'
MININDEX = 0

class Doo:
    def __init__(self, doo_path=None):
        """doo_path is the path were doo should store the todo list.
           If not specified, DOO_PATH (~/.doo) will be used."""
        self.doo_path = doo_path or DOO_PATH

        if not path.exists(self.doo_path):
            self.conf = {}
            self.save(emptyList=True)

        with open(self.doo_path) as f:
            data = json.loads(f.read())

        self.conf = data['conf']
        self.tasks = data['tasks']

    def save(self, emptyList=False):
        """Save the list to self.doo_path.
           If emptyList == True, then the saved tasklist is []"""
        with open(self.doo_path, 'w+') as f:
            f.write(json.dumps({
                                'conf': self.conf,
                                'tasks': [] if emptyList else self.tasks,
                                }))

    def sort(self):
        """Sort the task list."""
        self.tasks.sort(key=lambda x: int(x[0]))

    def show(self):
        """Show the todo list."""
        self.sort()
        for i, t in self.tasks:
            print(FORMAT.format(i, t))

        return self

    def replace(self, idx, new):
        """Replace the task with id idx of the list by new."""
        self.sort()
        for listid, (i, t) in enumerate(self.tasks):
            if i == idx:
                self.tasks[listid] = [i, new] # don't use tuples
                                              # because they doesn't
                                              # exists in json
                return self

        raise KeyError('Task #{} doesn\'t exist.'.format(idx))

    def rm(self, idx):
        """Remove the task with id idx of the list."""
        self.sort()
        for listid, (i, t) in enumerate(self.tasks):
            if i == idx:
                self.tasks.remove([i, t])
                return self

        raise KeyError('Task #{} doesn\'t exist.'.format(idx))

    def add(self, new):
        """Add the new task to the list."""
        self.sort()
        last = MININDEX - 1

        for listid, (i, t) in enumerate(self.tasks):
            if i != last + 1:
                self.tasks.insert(listid + 1, [last + 1, new])
                return self

            last = i

        self.tasks.append([last + 1, new])
        return self

if __name__ == '__main__':
    doo = Doo(os.getenv('DOO_PATH'))
    l = len(sys.argv)

    if l == 1:
        doo.show()

    elif sys.argv[1] in ['r', 'rm']:
        for i in sys.argv[2:]:
            try:
                idx = int(i)
            except ValueError:
                print('All arguments of rm should be a integer.',
                      file=sys.stderr)
            else:
                try:
                    doo.rm(idx)
                except KeyError as e:
                    print(e, file=sys.stderr)

        doo.save()

    elif sys.argv[1] in ['R', 'rp']:
        try:
            assert l > 3
            doo.replace(int(sys.argv[2]), ' '.join(sys.argv[3:])).save()
        except ValueError:
            print('The first argument of replace should be an integer.',
                  file=sys.stderr)
        except AssertionError:
            print('replace takes at least two args.', file=sys.stderr)

    elif l == 2 and sys.argv[1] in ['h', '-h']:
        print(textwrap.dedent('''\
                doo is a simple tool designed to help you to manage your todo list.

                doo                    : list all tasks.
                doo rm 1               : remove the task #1.
                doo rm 1 3             : remove tasks #1, #3.
                doo rp 1 new task      : replace task #1 to "new task"
                doo cl                 : remove all tasks.
                doo h                  : show this help.
                doo Conquer the world. : add the "Conquer the world."
                                         task to the list.
                
                Want to use one of the command in your task ? Simply use
                the shell quotes :
                    $ doo "cl whatever."

                Aliases:
                    r, rm
                    R, rp
                    h, -h
                    c, cl
                '''),
              file=sys.stderr) 

    elif l == 2 and sys.argv[1] in ['c', 'cl']:
        doo.save(emptyList=True)

    else:
        doo.add(' '.join(sys.argv[1:])).save()

