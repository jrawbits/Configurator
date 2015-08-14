# Configurator

The Configurator serves as a demonstration tool and provides helper
functions for the NMTK.

It can be used as a skeleton for new tools, and it also demonstrates all
the currently working tool configuration features, as well as basic tool
functions such as status updates and returning result files of different
types.  It also demonstrates the recommended way of interfacing with R.

The tool itself does nothing useful, but it will return a variety of
results based on the input files.  It shows off what can be accomplished
with a tool configuration, and exercises the status update and file
return functions of the tool.

The initial version computes one power raised to another, using Python
decimal math, and also using R if the Rserve daemon is installed and
running.

R is served from the Rserve package which must be running as
a daemon.  Installation is easy, see the Rserve documentation:
https://www.rforge.net/Rserve/doc.html

For accessing R from the Python harness, the pyRserve package is used.
Install it in the NMTK virtual environment using 'pip install pyRserve'.
Note that pyRserve requires numpy, which the NMTK installs by default
because it is expected most tools will need it.

If Rserve is not running when the tool processes a job, a graceful status
will be reported and the results will only include the Python computation.
The Python results will always be calculated if the tool works at all.

To start Rserve once it has been installed, see its documentation which
says to execute 'R CMD Rserve' -- an R interpreter will be launched and
set running in daemon mode.  To close Rserve cleanly, you can activate
the NMTK virtual environment and then use the included Python script with
'python endRserve.py'.  Note that pyRserve must be installed.
