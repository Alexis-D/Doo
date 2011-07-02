How To Install ?
================

    $ sudo make # pretty easy, huh?

How To Use ?
============

Here is pretty everything you can do with doo:


    $ doo
    $ doo h
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
    
    $ doo Improve doo.
    $ doo Stop procrastinating.
    $ doo
       0 - Improve doo.
       1 - Stop procrastinating.
    $ doo R doo is already awesome, nope?
    $ doo
       0 - doo is already awesome, nope?
       1 - Stop procrastinating.
    $ doo a
    $ doo b
    $ doo d
    $ doo e
    $ doo
       0 - doo is already awesome, nope?
       1 - Stop procrastinating.
       2 - a
       3 - b
       4 - d
       5 - e
    $ doo rm 2
    $ doo
       0 - doo is already awesome, nope?
       1 - Stop procrastinating.
       3 - b
       4 - d
       5 - e
    $ doo rm 2 3 4 5
    $ doo
       0 - doo is already awesome, nope?
       1 - Stop procrastinating.
    $ doo cl
    $ doo

License ?
=========

You like it? Cool, do whatever you want with it!  
You dislike it? Cool, don't use it!

