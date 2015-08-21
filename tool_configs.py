#!/usr/bin/env python
"""
This file manages the NMTK tool configuration.

As written here, it uses the "function-based" mechanism for
delivering the tool configuration.

This python file also runs standalone and will build a configuration file
from the Python dictionary contained within.  It looks at the containing
folder name and places the JSON configuration file in the templates
folder as required by the NMTK architecture.  If you pre-build the
files and put them in the right template directory, you can remove
the function and just load the config as a static JSON file.  The file
will be added to the NMTK when the system is installed, or when you
run the Django command python manage.py collect_static.

This file need not contain anything (then the NMTK will just look for
a pre-built tool_config.json in the app's templates folder).

It can also just contain a single declaration:

tools = []

which is equivalent to the file being empty.

You can put "sub-tool" names into the tools array, and if there
are configurations for those sub-tools, they will added as separate
tools to the NMTK, and they will be located "within" the main tool.

A subtool array would look like this:

tools=['tool1','tool2']

Obviously, you must provide a function or configuration files
for each of the subtools.  If you are providing a function, it
must do something sensible with the subtool parameter.  If you
are serving configurations from the file system, the configuration
files must have names consistent with the subtool names.  So in the
example subtool array above, we would expect to find files named
'tool1.json' and 'tool2.json' in the templates directory for the
tool application.  See the MN_tool sample tool for complete
details.
"""

# If this tool has no subtools, you can leave out the "tools"
# list entirely (or just leave it empty as it is here)
tools = []

# If tool_configs.py contains the generateToolConfiguration function,
# that will be used preferentially to generate a Python dictionary
# containing the tool configuration.  If you want to use a file-based
# configuration (in the templates sub-folder), do not define this
# function.
def generateToolConfiguration(tool,sub_tool=None):
    '''
    Simple function-based approach to returning a tool_config
    In this case, we just return the python dictionary that would
    have been used to make tool_config.json
    '''
    return tool_config

# The master configuration for this particular tool that works with
# the implementation of the generateToolConfiguration function
# is defined in the following Pdython dictionary.
tool_config = {
    "info" : {
        "name" : "Tool Configurator",
# The text is HTML-formatted text that describes the tool.  The focus here
# should be the tool implementation itself (i.e. what people have to know to
# make use of the tool).  If you want to get into background or computational
# methods, you should use the Documentation links to direct the user to a paper,
# a website or some other source.
        "text" : """
<p>The "Configurator" is the place to begin if you're trying to figure out how
to build an interface description for a Non-Motorized Toolkit (NMTK) tool(what
we call a "tool configuration" or just a "tool config").</p>

<p>This tool demonstrates the essential properties of an NMTK tool configuration
file.  And the code behind it uses a wide range of NMTK features: working with
different data types, using different computational engines, performing numeric
and spatial analysis.  While it does nothing especially useful (it is left as a
challenge to the reader to figure out how to use it to convert geographic vector
files into geoJSON format without doing anything else), it does exercise all the
Tool API elements, including input files, status updates (including updates from
within running R code) and multiple result files.  Behind the scenes, it also
gives you a skeleton for a tool and some helper functions that will make tool
development easier.</p>

<p>Speaking of easy, building an NMTK tool is just easy.  We knocked out the
basic Configurator tool in an afternoon, and finished the rest of it in a few
more hours (admittedly, some of the computational code like raster conversion
was already written).  Writing an NMTK tool is way easier than writing a
spreadsheet (spreadsheets have no place in responsible scientific research).</p>

<p>The hardest part of building a tool is constructing the configuration file so
the user can present you with the data you need.  But even a configuration file
is not especially hard, and you can use the Configurator to learn all you need
to know about it.</p>

<p>Configurations have five main parts, which broadly track with what you would
expect to find in a reproducible research repository (q.v.).</p>

<ol>

<li>The <strong>"info"</strong> section contains an overview of the tool: its
name, a block of HTML marked-up text that describes it -- that's what you're
reading now -- and version information.</li>

<li>The <strong>"sample"</strong> section describes sample data and a sample job
configuration.  You can use that for testing your tool while you're developing
it so you don't have to repeatedly build job setups by hand, and it will allow
your users to experience your tool to decide if it might work for them, without
having to go through an extensive data preparation step of their own.</li>

<li>The <strong>"documentation"</strong> section provides links or files that
the user can open to learn more about the tool.  This tool has a link to its
"home base" in Github, so you can download any of the tool code to look at up
close.  You can also retrieve the configuration file for this tool itself just
the way an NMTK server would by clicking the "Configuration" link.  Finally, you
can also download a couple of PDF files: the latest version of the Tool
Configuration specification, and the introductory document on how to write a
tool.  In short, the Configurator is your gateway to doing cool stuff with the
Non-Motorized Toolkit!</li> </ol>

<p>The real action happens in the remaining two sections:</p>

<ol start="4">

<li>The <strong>"input"</strong> section describes what the user has to provide
to the tool in order to make it work: input files, fields within those files,
parameters and coefficients, or even literal data to analyze. The input
configuration says what kinds of files it expects and knows how to work with.
It says what is required and what is optional.  The help text that goes with
each of the input elements tells the user concisely what they need to put into
that element; here in the Configurator, the text focuses on explaining the user
interface properties.</li>

<li>The <strong>"output"</strong> section describes what the tool is going
to return.  Though the output section works just like parameter sections in
the input, these parameters should not change what is computed but rather how
the results of the computations are returned to the user.  This section can also
be used (e.g. with readonly result fields) to inform the user of the fixed names
of result fields or what result types they should expect.</li>

</ol>
""",
        "version" : "1.0"
    },
    "documentation" : {
        "links" : [
              {
                "url":"http://github.com/jrawbits/Configurator",
                "title":"Visit the Configurator on Github"
              },
              {
                "url":"http://nmtk.jeremyraw.com/Configurator/config",
                "title":"See the Configurator's raw configuration file"
              }
        ],
        "docs" : [
            "uri" : "ToolSpec_2015-07-31.docx",
            "mimetype" : "",
            "name" : "Tool Configuration Specification",
        ],
    },
# The sample section should be developed after the input and output
# sections
#    "sample" : {
#        "files" : {
#            # just one sample file that can provide the necessary
#             # pieces for a batch job
#         },
#         "config" : {
#             # A config that will use the sample file (or not)
#         }
#         "description" : """
# Sample Configurator job.
#         """
#     },
    "input" : [
        {
            "type" : "File",              # Elements that can be read in multiple rows from a file
            "name" : "computation",       # 'name' and 'namespace' are probably redundant
            "namespace" : "computation",
            "description" :
"""
Data elements that will be transformed using the factors
""",
            "primary" : True,             # True if this input can't be missing
            "label" : "Data used for computation",
            # "spatial_types" : ["POLYGON","POINT","LINE"] # require specific spatial types
            # "required" : True           # if true, an actual file must be provided
            "elements" : [
              {
                  "description" : "The data field that will be subjected to computation.",
                  "default" : 3,
                  "required" : True,
                  "label" : "Data to Empower",
                  "type" : "number",
                  "name" : "raiseme"
              },
              {
                  "description" : "A second data field that will be subjected to computation.",
                  "display_if_filled" : "raiseme2",
                  "default" : 4,
                  "required" : True,
                  "label" : "More Data to Empower",
                  "type" : "number",
                  "name" : "raiseme2"
              },
              {
                  "description" : "A third data field that will be subjected to computation.",
                  "display_if_filled" : "raiseme2",
                  "default" : 5,
                  "required" : True,
                  "label" : "Yet More Data to Empower",
                  "type" : "number",
                  "name" : "raiseme3"
              },
              {
                  "description" : "Sorry, you only get three data fields or we'll be here all day!",
                  "default" : "",
                  "display_if_filled" : "raiseme3",
                  "required" : True,
                  "readonly" : True,
                  "label" : "Out Of Power",
                  "type" : "string",
                  "name" : "backstop"
              },
            ],
        },
        {
            "type" : "File",              # Elements that can be read in multiple rows from a file
            "name" : "computation",       # 'name' and 'namespace' are probably redundant
            "namespace" : "computation",
            "description" :
"""
Data file that will be used for rasterization (must be spatial)
""",
            "primary" : False,            # True if...
            "label" : "Data used for rasterization",
            "spatial_types" : ["POLYGON","POINT","LINE"], # require specific spatial types
            # "required" : True,           # If true, an actual file must be provided
            "elements" : [
              {
                  "description" : """
The value to be assigned to raster cells coinciding with the feature.  May be a constant or a file property.
""",
                  "default" : 10,
                  "required" : True,
                  "label" : "Raster Value",
                  "type" : "number",
                  "name" : "rastervalue"
              },
            ],
        },
        {
            "type" : "ConfigurationPage",  # Elements that are provided as a single instance (global)
            "name" : "computation_params",
            "namespace" : "computation_params",
            "description" :
"""
Parameters that control what will be done with the computation data.
""",
            "label" : "Computation Parameters",
            "expanded" : True,
            "elements" : [
              {
                  "description" : "The computation data will be raised to this power.",
                  "default" : 2,
                  "required" : True,
                  "label" : "Power to Raise",
                  "type" : "number",
                  "name" : "raisetopower"
              },
              {
                  "description" : "Which computation engines will be used.",
                  "default" : "Python",
                  "choices" : [ "Python","R","Both","None" ],
                  "required" : True,
                  "label" : "Computation Engines",
                  "type" : "string",
                  "name" : "computetype"
              },
            ],
        },
        {
            "type" : "ConfigurationPage",  # Elements that are provided as a single instance (global)
            "name" : "rasterization_params",
            "namespace" : "rasterization_params",
            "description" :
"""
Parameters that control how rasterization will be performed.
""",
            "label" : "Rasterization Parameters",
            "expanded" : True,
            "elements" : [
              {
                  "description" : "If true, the rasterization will be attempted.",
                  "default" : 0,
                  "required" : True,
                  "label" : "Rasterize",
                  "type" : "boolean",
                  "name" : "dorasterize"
              },
              {
                  "description" : "Number of X (East-West) cells to construct",
                  "display_if_true" : "dorasterize", # only show this field if rasterizing is non-zero
                  "default" : 300,
                  "required" : True,
                  "label" : "X Cells",
                  "type" : "numeric",
                  "name" : "raster_x"
              },
              {
                  "description" : "Number of Y (North-South) cells to construct",
                  "display_if_true" : "dorasterize", # only show this field if rasterizing is non-zero
                  "default" : 300,
                  "required" : True,
                  "label" : "Y Cells",
                  "type" : "numeric",
                  "name" : "raster_y"
              },
              {
                  "description" : "If rasterizing a polygon file, show fraction of cell covered rather than all or nothing.",
                  "display_if_true" : "dorasterize", # only show this field if rasterizing is non-zero
                  "default" : 0,
                  "required" : True,
                  "label" : "Proportional Area",
                  "type" : "numeric",
                  "name" : "proportional"
              },
              {
                  "description" : "Smooth the rasterized cells into adjacent cells using this parameter",
                  "display_if_true" : "dorasterize", # only show this field if rasterizing is non-zero
                  "required" : False,
                  "label" : "Smoothing",
                  "type" : "numeric",
                  "name" : "smoothing"
              },
            ],
        },
        {
            "type" : "ConfigurationPage",  # Elements that are provided as a single instance (global)
            "name" : "imaging_params",
            "namespace" : "imaging_params",
            "description" :
"""
Parameters that control whether images of the rasters will be generated.
""",
            "label" : "Imaging Parameters",
            "expanded" : True,
            "elements" : [
              {
                  "description" : """
If true, make an image of the input file that will be rasterized.
If this is checked but no rasterization input is provided, a default shapefile will be imaged.
""",
                  "default" : 0,
                  "required" : True,
                  "label" : "Image Input",
                  "type" : "boolean",
                  "name" : "imageinput"
              },
              {
                  "description" : """
If true, make an image of the rasterized file.
If this is checked but no rasterization was attempted (due to missing input or not requested),
a default raster will be imaged.
""",
                  "default" : 0,
                  "required" : True,
                  "label" : "Image Raster",
                  "type" : "boolean",
                  "name" : "imageraster"
              },
            ],
        }
    ], 
    "output" : [
      {
        "type":"ConfigurationPage",
        "name":"computation_output",
        "namespace":"computation_output",
        "label":"Computation Field Names",
        "description":"""
You may supply alternate base names for the result fields used to hold the computations performed.
""",
        "elements":[
          {
            "description":"""
Base field name for results computed by Python (the input field name will be appended after an underscore)
""",
            "default":"PowerOfPython",
            "required":True,
            "label":"Python Result Basename",
            "type":"string",
            "name":"python_result"
          },
          {
            "description":"""
Base field name for results computed by R (the input field name will be appended after an underscore)
""",
            "default":"PowerOfR",
            "required":True,
            "label":"R Result Basename",
            "type":"string",
            "name":"r_result"
          }
        ],
      },
      {
        "type":"ConfigurationPage",
        "name":"rasterization_output",
        "namespace":"rasterization_output",
        "label":"Rasterization Outputs",
        "description":"""
You can force certain rasterization output to occur, regardless of whether you actually attempted rasterization.
The boolean parameters below will control what is returned.
""",
        "elements":[
          {
            "description":"""
Return a raw raster file.  The tool will return either the raster resulting from rasterization,
or if rasterization was not attempted, then a pre-constructed geographic raster.
""",
            "default":0,
            "required":True,
            "label":"Return Raster",
            "type":"boolean",
            "name":"return_raster"
          },
          {
            "description":"""
Mirror (return) the input vector file used for rasterization as a geoJSON file.  If no rasterization input file
was provided, return a pre-determined sample geographic vector file.  NMTK Rubik's cube: can you get this tool
to 
""",
            "default":0,
            "required":True,
            "label":"Mirror Input Vector",
            "type":"boolean",
            "name":"return_vector"
          },
        ],
      },
      {
        "type":"ConfigurationPage",
        "name":"image_output",
        "namespace":"image_output",
        "label":"Image Output",
        "description":"""
If you requested images, you can set the format that will be returned here from a list of supported types (plus
one unsupported type that can be downloaded but not viewed).
""",
        "elements":[
          {
            "description":"""
Select the output format for the image versions of shapefiles or rasters that you may have requested.  All images
will be generated in the same format.
""",
            "default":"PNG",
            "choices" : ["PNG","JPG","GIF","PDF (Download Only)"],
            "required":True,
            "label":"Image Format",
            "type":"string",
            "name":"image_format"
          },
        ],
      },
    ],
}

# Here's a simple function that you can use to dump the tool
# configuration file into a JSON file in the templates folder.
# Run this file as a standalone python script.
# Note that if you define the function generateToolConfiguration,
# then that function will be called to deliver the tool configuration
# to the NMTK, and the file-based configuration will not be used.
if __name__ == "__main__":
    import json
    if not tools:
        tools = ["tool_config"]
    for tool_name in tools:
        print "Configurating tool %s"%(tool_name,)
        tool_data = eval(tool_name)
        js = json.dumps(tool_data,indent=2, separators=(',',':'))
        print js
#        f = file("templates/Configurator/%s.json"%(tool_name,),"w")
#        f.write(js)
#        f.close()
