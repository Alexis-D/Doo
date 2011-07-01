#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import os.path as path
import re
import sys
import textwrap

DOO_PATH = path.join(path.expanduser('~'), '.doo')
FORMAT = '{:4d} - {}'
PARSE_STRING = '^\s*(\d+) - (.*)$'
MININDEX = 0

class Doo:
    def __init__(self, doo_path=None):
        """doo_path is the path were doo should store the todo list.
           If not specified, DOO_PATH (~/.doo) will be used."""
        self.doo_path = doo_path or DOO_PATH

        if not path.exists(self.doo_path):
            self.clear()

    def _tasks(self):
        """Return the task list."""
        tasks = []

        with open(self.doo_path, 'r') as f:
            for t in f.readlines():
                idx, task = re.findall(PARSE_STRING, t)[0]
                tasks.append((int(idx), task))

        return tasks


    def clear(self):
        """Empty the doo file, create it if it doesn't exist."""
        open(self.doo_path, 'w+').close()

    def show(self):
        """Show the todo list."""
        with open(self.doo_path) as f:
            print(f.read(), end='')

    def replace(self, idx, new):
        """Replace the task with id idx of the list by new."""
        tasks = self._tasks()

        with open(self.doo_path, 'w+') as f:
            for i, t in tasks:
                if i == idx:
                    t = new

                print(FORMAT.format(i, t), file=f)

    def rm(self, idx):
        """Remove the task with id idx of the list."""
        tasks = self._tasks()

        with open(self.doo_path, 'w+') as f:
            for i, t in tasks:
                if i != idx:
                    print(FORMAT.format(i, t), file=f)

    def add(self, new):
        """Add the new task to the list."""
        tasks = self._tasks()
        last = MININDEX - 1
        added = False

        with open(self.doo_path, 'w+') as f:
            for i, t in tasks:
                if i != last + 1:
                    print(FORMAT.format(last + 1, new), file=f)
                    added = True

                print(FORMAT.format(i, t), file=f)
                last = i

            if not added:
                print(FORMAT.format(last + 1, new), file=f)


if __name__ == '__main__':
    doo = Doo(os.getenv('DOO_PATH'))
    l = len(sys.argv)

    if l == 1:
        doo.show()

    elif sys.argv[1] in ['r', '-r', 'rm', 'remove']:
        try:
            for i in sys.argv[2:]:
                doo.rm(int(i))
        except ValueError:
            print('All arguments of rm should be a integer.', file=sys.stderr)

    elif sys.argv[1] in ['rp', 'replace']:
        try:
            assert l > 3
            doo.replace(int(sys.argv[2]), ' '.join(sys.argv[3:]))
        except ValueError:
            print('The first argument of replace should be an integer.',
                  file=sys.stderr)
        except AssertionError:
            print('replace takes at least two args.', file=sys.stderr)

    elif l == 2 and sys.argv[1] in ['h', '-h', 'help', '--help']:
        print(textwrap.dedent('''\
                doo is a simple tool to help you tomanage your todo list.

                doo : list all task.
                doo rm 1 : remove the task #1.
                doo rm 1 3 : remove task #1, #3
                doo rp 1 replace task : replace task #1 to "replace task"
                doo clear : remove all tasks.
                doo help : show this help.
                doo Conquer the world. : add the "Conquer the world."
                                         task to the list.
                
                Want to use one of the command in your task ? Simply use
                the shell quotes :
                    $ doo "help myself to stop procrastinating"

                Aliases :
                    r, -r, rm, remove
                    rp, replace
                    h, -h, help, --help
                    c, -c, clear
                '''),
              file=sys.stderr) 

    elif l == 2 and sys.argv[1] in ['c', '-c', 'clear']:
        doo.clear()

    else:
        doo.add(' '.join(sys.argv[1:]))

