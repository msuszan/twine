"""
Extension functions for parsing sys.argv.

Commands:

   get_args -- load all command-line arguments after the last --
      into $arg1...$argN.
   
"""

import twine.utils

def get_args(require=0):
    """
    >> get_args [<require>]

    Load the command line arguments after the last '--' into $arg1...$argN,
    optionally requiring at least 'require' such arguments.
    """
    from twine import commands, namespaces, shell, errors

    global_dict, local_dict = namespaces.get_twine_glocals()

    require = int(require)

    if len(shell.twineargs) < require:
        from twine.errors import TwineAssertionError
        raise TwineAssertionError("too few arguments; %d rather than %d" % \
                                    (len(shell.twineargs), require,))

    if shell.twineargs:
        for i, arg in enumerate(shell.twineargs):
            global_dict["arg%d" % (i + 1,)] = arg

        print>>commands.OUT, "get_args: loaded %d args as $arg1..$arg%d." % \
                             (i + 1, i + 1)
    else:
        print>>commands.OUT, "no arguments to parse!"
