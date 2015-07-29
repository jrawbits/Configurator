tools=[
    'UrbanSegment',     # Urban street segment
#    'SignalizedInt',    # Signalized Intersection: TODO: requires expandable input parameter structures
#    'TwoWayStop',       # Two-Way Stop Intersection (and mid-block crossing)
                        # Develop summary of inputs required (not in HCM)
#    'AllWayStop',       # All-Way Stop Intersection - Qualitative evaluation only
#    'PedOnly',          # Dedicated Pedestrian Facility (Walkways, stairways) : UNDERWAY
                        # Probably could use dedicated worksheet for "furniture" -- how to link analyses
                        # in the configuration?
#    'SharedUse',        # Shared-Use Non-motorized Facility : UNDERWAY
]

UrbanSegment={
    'info': {
        'name'    : 'HCM2010 Urban Street Segment (Pedestrian)',
        'text'    :
            'This tool evaluates various performance measures including Pedestrian Level of Service '
            'for an Urban Street Segment (with interrupted flow, mid-block access, and other features '
            'of an urban roadway.  The input parameters and their defaults reflect the 2010 version of '
            'the Highway Capacity Manual.',
        'version' : '0.1'
    },
    'sample': {
        },
    'documentation': {
        'links': [
            {
                'title' : 'Highway Capacity Manual 2010',
                'url'   : "http://hcm.trb.org",
            },
        ]
    },
    'input': [
        {
            'type'        : 'ConfigurationPage',
            'name'        : 'traffic',
            'label'       : 'Traffic Characteristics',
            'description' :
                'Enter the traffic characteristics below.  Fields are already completed with their HCM default '
                'values if one is available, but you should supply a more specific local estimate if possible.',
            'elements'    : [
                {
                    'name'        : 'vehicles',
                    'description' : 'Total bidirectional motorized flow (all vehicles) on all lanes (vehicles per hour)',
                    'type'        : 'number',
                    'required'    : True,
                },
                {
                    'name'        : 'pedestrianflow',
                    'description' : 'Pedestrian flow rate',
                    'type'        : 'number',
                    'required'    : False,
                    'default'     : 0.06,
                },
                {
                    'name'        : 'onstreetparking',
                    'description' : 'Fraction of segment with occupied on-street parking (decimal)',
                    'type'        : 'number',
                    'required'    : False,
                    'default'     : 0.00,
                },
                {
                    'name'        : 'runningspeed',
                    'description' : 'Motorized Vehicle Running Speed',
                    'type'        : 'number',
                    'default'     : 4,
                },
            ],
        },
        {
            'type'        : 'ConfigurationPage',
            'name'        : 'geometry',
            'label'       : 'Roadway Geometry',
            'description' :
                'Enter the roadway geometry below.  Fields are already completed with their HCM default '
                'values if one is available, but you should supply a more specific local estimate if possible.',
            'elements'    : [
                {
                    'name'        : 'intersectionwidth',
                    'description' : 'Downstream intersection width',
                    'type'        : 'number',
                    'default'     : 0,
                    'required'    : False,
                },
                {
                    'name'        : 'segmentlength',
                    'description' : 'Length of Segment (miles?)',
                    'type'        : 'number',
                    'required'    : True,
                    
                },
                {
                    'name'        : 'lanes',
                    'description' : 'Number of through lanes in the analyzed direction',
                    'type'        : 'number',
                    'required'    : True,
                    
                },
                {
                    'name'        : 'lanewidth',
                    'description' : 'Width of outermost lane (feet)',
                    'type'        : 'number',
                    'default'     : 12,
                    'required'    : False,
                },
                {
                    'name'        : 'bikelanewidth',
                    'description' : 'Width of bicycle lane, if any (feet)',
                    'type'        : 'number',
                    'default'     : 4,
                    'required'    : False,
                },
                {
                    'name'        : 'shoulderwidth',
                    'description' : 'Width of paved outside shoulder, if any (feet)',
                    'type'        : 'number',
                    'default'     : 0,
                    'required'    : False,
                },
                {
                    'name'        : 'mediancurb',
                    'description' : 'Median type and curb presence',
                    'type'        : 'number',
                    'default'     : 0,
                    'required'    : False,
                },
            ],
        },
        {
            'type'        : 'ConfigurationPage',
            'name'        : 'sidewalk',
            'label'       : 'Sidewalk',
            'description' :
                'Enter information related to sidewalks.  See the Highway Capacity Manual for definitions '
                'of "buffer", "spacing of objects", and "effective width". '
                'Fields are already completed with their HCM default '
                'values if one is available, but you should supply a more specific local estimate if possible.',
            'elements'    : [
                {
                    'name'        : 'sidewalkpresent',
                    'description' : 'Presence of a sidewalk',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'walkwidth',
                    'description' : 'Total walkway width',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'fixedobjectwidth',
                    'description' : 'Effective width of fixed objects',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'bufferwidth',
                    'description' : 'Buffer width',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'bufferspacing',
                    'description' : 'Spacing of objects in buffer',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'blockface',
                    'description' : 'Proportion of sidewalk adjacent to window, building or fence',
                    'type'        : 'number',
                    'default'     : 0,
                    'required'    : False,
                },

            ]
        },
        {
            'type'        : 'ConfigurationPage',
            'name'        : 'crossing',
            'label'       : 'Crossing Parameters',
            'description' :
                'Enter information about where pedestrians can cross this segment.'
                'Fields are already completed with their HCM default '
                'values if one is available, but you should supply a more specific local estimate if possible.',
            'elements'    : [
                {
                    'name'        : 'intersectiondistance',
                    'description' : 'Distance to nearest signal-controlled intersection',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'midblockcrossing',
                    'description' : 'Legality of midsegment pedestrian crossing',
                    'type'        : 'number',
                    'default'     : 4,
                },
            ]
        },
        {
            'type'        : 'ConfigurationPage',
            'name'        : 'performancemeasures',
            'label'       : 'Performance Measures',
            'description' :
                'Enter performance information for the  boundary (downstream) intersection performance.'
                'Fields are already completed with their HCM default '
                'values if one is available, but you should supply a more specific local estimate if possible.',
            'elements'    : [
                {
                    'name'        : 'pedestriandelay',
                    'description' : 'Pedestrian delay at downstream intersection',
                    'type'        : 'number',
                    'default'     : 4,
                },
                {
                    'name'        : 'pedestrianlos',
                    'description' : 'Downstream intersection Pedestrian Level of Service (BLOS)',
                    'type'        : 'number',
                    'default'     : 4,
                },
            ]
        },
    ],
    'output': [
        ]
}

###################### Dump the configuration as JSON>>>>

if __name__ == '__main__':
    import json

    for t in tools:
        print "Loading tool '%s'"%(t,)
        raw = eval(t)
        js = json.dumps(raw,indent=2, separators=(',',':'))
        f = file(t+"config.json","w")
        f.write(js)
        f.close()
