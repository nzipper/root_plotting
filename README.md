# ROOT Plot Wrappers for Python

## Simple Templates
### Histogram Plot (up to 2)
    from root_plotting.HistPlot import HistPlot
    # plot parameters can also be set by dict with set_params() method
    hp = HistPlot(init_params={
        'color1'       : 'black',
        'color2'       : 'orange',
        'title_string' : None,
        'canvas_size'  : (800,800),
        'xrange'       : None,
        'yrange'       : None,
        'rrange'       : (.5,2),
        'text_size'    : 'med',
        'leg_pos'      : 'upper_right',
        'leg_scale'    : None,
    })
    canvas = hp.plotHists(hist_1, hist_2, ratio=False, h1_title=None, h2_title=None, show=False, save=False)
### Multiple Histogram Plot (more than 2)
    from root_plotting.MultiHistPlot import MultiHistPlot
    # plot parameters can also be set by dict with set_params() method
    mhp = MultiHistPlot(init_params={
        'title_string' : None,
        'x_title'      : None,
        'y_title'      : None,
        'colors'       : ['black','orange','blue','red','green','magenta','cyan','gray'],
        'canvas_size'  : (800,800),
        'marker_style' : ['.','+','x','o','*','^','star'],
        'marker_size'  : 'small',
        'xrange'       : None,
        'yrange'       : None,
        'rrange'       : (.5,2),
        'text_size'    : 'med',
        'leg_pos'      : 'upper_right',
        'legtext_size' : 'med',
        'leg_scale'    : None,
        'norm'         : None,
    })
    mhp.plotHists(hist_list, ratio=False, titles=None, show=False, save=False):

### Efficiency Plot
    from root_plotting.EfficiencyPlot import EfficiencyPlot
    ep = EfficiencyPlot(init_params={
        'color1'       : 'black'
        'color2'       : 'orange'
        'title_string' : ';p_{T} [GeV];Efficiency'
        'canvas_size'  : (800,800)
        'xrange'       : (0,100)
        'yrange'       : (0.,1.1)
        'rrange'       : (.5,2)
        'text_size'    : 'med'
        'leg_pos'      : 'upper_right'
    })
    ep.plotEfficiencies(hist_1, hist_2, ratio=True, h1_title=None, h2_title=None, save=False, addIntegral=False, integralRange=None)

## Helper Parameters

The goal of the parameter reformatting is to make it easier to pick simple options. To that end, colors/sizes/styles are rewritten in simpler terms (closer to Matplotlib) instead of the codes used in ROOT.

Examples:
    - 'title_string' : 'plot title ; x-axis title ; y-axis title'
    - 'title_size' : ['small','med','large']
    - 'colors' : ['black','orange','blue','red','green','magenta','cyan','gray']
    - 'marker_size' : ['small','med','large','x-large,'xx-large']
    - 'marker_style' : ['.','+','x','o','*','^','star']
    - 'line_width' : ['thin','med','thick']
    - 'line_style' : ['-','..','--','-.']
    - 'label_size' : ['small','med','large']
    - 'leg_pos'    : ['upper_left','upper_right','center_left','center_right','lower_left','lower_right']
    - 'leg_scale'  : 0-1 # scales length horizontally across canvas