#!/usr/bin/env python
"""

This python file runs standalone and will build a configuration file
from the Python dictionary contained within.  It looks at the containing
folder name and places the JSON configuration file in the templates
folder as required by the NMTK architecture.

"""
import json

configuration = {
    "info" : {
        "name" : ""
        "text" : ""
        "version" : ""
    },
    "sample" : {
        "files" : {
        },
        "config" : {
        }
        "descripti nn tools:
        print "Loading tool '%s'"%(t,)
        raw = eval(t)
        js = json.dumps(raw,indent=2, separators=(',',':'))
        f = file(t+"config.json","w")
        f.write(js)
        f.close()
" : {
        }
    },
    "documentation" : {
        "links" : [
        ],
    },
    "input" : [
    ] 
    "output" : [
    ]
}

js = json.dumps(configuration,indent=2, separators=(',',':'))
f = file("templates/Configurator/tool_config.json","w")
f.write(js)
f.close()
