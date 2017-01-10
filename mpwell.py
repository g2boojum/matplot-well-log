#! /bin/env python

import matplotlib.pyplot as plt

default_color='b'
def make_log(tracks, title=None, mindepth=None, maxdepth=None, tagged_depths=None):
    """Create a well log using matplotlib.

       tracks: list of tracks. Each track is a dictionary with a 'traces'
       key (required), and possibly keys that describe the scale (log or linear)
       and appearance of the track. The 'traces' key points to a list of traces.
       Each trace is a dictionary containing a 'data' key that points to a Pandas
       DataFrame that contains the data to be plotted. The DataFrame must have
       a column named 'depth' that contains the depth in the desired units, and 
       also a column named the same as value of the 'curve' key in the trace. The
       trace dictionary may also have a 'label' key that provides the log mnemonic 
       for the trace, and additional keys that describe the appearance of the trace.

       title: Display title for the log.

       mindepth: minimum depth to be plotted. Optional. Determined from the first trace
       of the first track, if not specified.

       maxdepth: maximum depth to be plotted. Optional. Determined from the first trace
       of the first track, if not specified.

       tagged_depths: List of depths which should be marked on the logs with a horizontal
       line.
    """
    f, axs = plt.subplots(nrows=1, ncols=len(tracks), figsize=(8, 10))
    if title:
        f.suptitle(title, fontsize=22)
    # reserve space at the top and between subplots
    f.subplots_adjust(top=.85,wspace=0.25)
    first_trace_data = tracks[0]['traces'][0]['data']
    if mindepth is None:
        mindepth = min(first_trace_data['depth'])
    if maxdepth is None:
        maxdepth = max(first_trace_data['depth'])
    # set up each track
    for ax in axs:
        ax.set_ylim (mindepth,maxdepth)
        ax.invert_yaxis()
        ax.get_xaxis().set_visible(False)
        ax.grid(False)
    # plot each trace in each track
    for i, track in enumerate(tracks):
        for num_trace, trace in enumerate(track['traces']):
            color = trace.get('color', default_color)
            label = trace.get('label', trace['curve'])
            ls = trace.get('ls', '-')
            marker = trace.get('marker', 'None')
            axi = axs[i].twiny()
            axi.set_xlim(*trace['range'])
            axi.set_ylim(mindepth, maxdepth)
            axi.spines['top'].set_position(('outward', 5+30*num_trace))
            axi.spines['top'].set_color(color)
            axi.xaxis.set_ticks(trace['range'])
            axi.set_xlabel(label, color=color, labelpad=-5)
            data = trace['data']
            axi.plot(data[trace['curve']], data['depth'], ls=ls, marker=marker, color=color)
            axi.tick_params(axis='x', color=color, length=0)
            axi.yaxis.grid(False)
            axi.invert_yaxis()
            if tagged_depths is not None:
                for depth in tagged_depths:
                      axi.axhline(depth, color='grey', lw=1)
            if i>0:
                axi.set_yticklabels([])
            else:
                # Turn off the "offset" in the y-axis labeling
                y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
                axi.yaxis.set_major_formatter(y_formatter)
    return f


