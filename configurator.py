#!/usr/bin/env python
"""

This python file runs standalone and will build a configuration file
from the Python dictionary contained within.  It looks at the containing
folder name and places the JSON configuration file in the templates
folder as required by the NMTK architecture.

"""
import json

tools = ["tool_config"]

tool_config = {
    "info" : {
        "name" : "Tool Configurator",
        "text" : """
<p>The "Configurator" is the place to begin if you're trying to figure
out how to build an interface description for a Non-Motorized Toolkit
(NMTK) tool(what we call a "tool configuration" or just a "tool
config").</p>

<p>This "do-nothing" tool demonstrates the essential properties of an
NMTK tool configuration file.  While it does nothing useful (though
some might find it amusing), it does exercise all the Tool API
elements, including status updates and multiple result files.  Behind
the scenes, it also gives you a skeleton for a tool and some helper
functions that will make tool development easier.</p>

<p>Speaking of easy, building an NMTK tool is just easy.  We knocked out
this Configurator tool in just a couple of days.  Writing an NMTK tool
is way easier than writing a spreadsheet (nobody should ever use
spreadsheets again).</p>

<p>The hardest part of building a tool is constructing the configuration
file so the user can present you with the data you need.  But even a
configuration file is not especially hard, and you can use the
Configurator to learn all you need to know about it.</p>

<p>Configurations have five main parts, which broadly track with what you
would expect to find in a reproducible research repository (q.v.).</p>

<ol>
<li>The <strong>"info"</strong> section contains an overview of the
tool: its name, a block of HTML marked-up text that describes it --
that's what you're reading now -- and version information.</li>

<li>The <strong>"sample"</strong> section describes sample data and a sample
job configuration.  You can use that for testing your tool while you're
developing it so you don't have to repeatedly build job setups by hand,
and it will allow your users to experience your tool to decide if it might
work for them, without having to go through an extensive data preparation
step of their own.</li>

<li>The <strong>"documentation"</strong> section provides links or files
that the user can open to learn more about the tool.  This tool has a
link to its "home base" in Github, so you can download any of the tool
code to look at up close.  You can also retrieve the configuration
file for this tool itself just the way an NMTK server would by
clicking the "Configuration" link.  Finally, you can also download a
couple of PDF files:  the latest version of the Tool Configuration
specification, and the introductory document on how to write a tool.
In short, the Configurator is your gateway to doing cool stuff with
the Non-Motorized Toolkit!</li>
</ol>

The real action happens in the remaining two sections:

<ol start="4">
<li>The <strong>"input"</strong> section describes what the user has to
provide to the tool in order to make it work: input files, fields
within those files, parameters and coefficients, or even literal data
to analyze (put a number into the Configurator's "Nth root" field and
see what comes back!). It says what kinds of files it expects and knows
how to work with.  It ways what is required and what is optional.  The
help text that goes with each of the input elements tells the user
concisely what they need to put into that element; here in the Configurator,
the text focuses on explaining the user interface properties.</li>

<li>The <strong>"output"</strong> section describes what the tool is going
to return.  This section is not exactly optional because it gives
useful information to the NMTK explaining what it is going to return.
And it lets you give the user some ability to shape how the results
are presented, for example by specifying alternate names for the
result fields returned.</li>
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
            {
                "name" : "Tool Interface Specification (.docx)",
                "url" : "/static/Configurator/docs/ToolSpec_2015-07-31.docx",
                "mimetype" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }
        ]
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
            "description" :
"""
Data elements that will be transformed using the factors
""",
            "elements" : [
              {
                  "description" : "The data that will be raised to a power.",
                  "default" : 3,
                  "required" : True,
                  "label" : "Data to Empower",
                  "type" : "number",
                  "name" : "raiseme"
              },
            ],
            "type" : "File",
            "name" : "data",
            "namespace" : "data",
            "primary" : True,
            "label" : "Input data",
            "spatial_types" : ["POLYGON","POINT","LINE"]
        },
        {
            "description" :
"""
Factors that will transform the supplied data
""",
            "elements" : [
              {
                  "description" : "The data will be raised to this power.",
                  "default" : 2,
                  "required" : True,
                  "label" : "Power to Raise",
                  "type" : "number",
                  "name" : "power"
              },
            ],
            "type" : "ConfigurationPage",
            "name" : "factors",
            "namespace" : "factors",
            "label" : "Factors",
            "expanded" : True,
            }
    ], 
    "output" : [
      {
        "description":"""
You may override the default field name in which results from this
tool are reported by entering a different name here.  The name you
enter may be adjusted so it is not the same as any fields already in
your input data.
""",
        "elements":[
          {
            "description":"Field name that will contain the computed result",
            "default":"Root",
            "required":True,
            "label":"Result Field",
            "type":"string",
            "name":"result"
          }
        ],
        "type":"ConfigurationPage",
        "name":"perfeature",
        "namespace":"perfeature",
        "label":"Individual Results"
      }
    ],
}

for tool_name in tools:
    print "Configurating tool %s"%(tool_name,)
    tool_data = eval(tool_name)
    js = json.dumps(tool_data,indent=2, separators=(',',':'))
    f = file("templates/Configurator/%s.json"%(tool_name,),"w")
    f.write(js)
    f.close()
