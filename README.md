# ROOT Plot Wrappers for Python

## Simple Templates
### Histogram Plot
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
### Multiple Histogram Plot
    # plot parameters can also be set by dict with set_params() method
    mhp = MultiHistPlot(init_params={
        'title_string' : None,
        'x_title'      : None,
        'y_title'      : None,
        'colors'       : ['black','orange','blue','red','green','magenta','cyan','gray'],
        'canvas_size'  : (800,800),
        'marker_style' : None,
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