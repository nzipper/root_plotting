import numpy as np
import ROOT
import PlotBase

class HistPlot(PlotBase):
    def __init__(self, init_params=None):
        ROOT.gStyle.SetOptStat(0)
        self.color1 = 'black'
        self.color2 = 'orange'
        self.title_string = ';p_{T} [GeV];Events'
        self.canvas_size = (800,800)
        self.xrange = (0,100)
        self.yrange = (0.,1.1)
        self.rrange = (.5,2)
        self.text_size='med'
        self.leg_pos = 'upper_right'
        if init_params: self.set_params(init_params)

    def set_params(self, params):
        for key in params:
            setattr(self, key, params[key])
    
    def hist_ratio(self, h_1, h_2):
        hnew1 = h_1.Clone('hnew1')
        hnew2 = h_2.Clone('hnew2')
        hnew1.Divide(hnew2)
        return hnew1

    # Core function for plot generation
    def plotHists(self, h1, h2, ratio=True, h1_title=None, h2_title=None, save=False):
        # Construct plot objects
        self.format_entry(h1, line_color=self.color1, title=h1_title)
        self.format_entry(h2, line_color=self.color2, title=h2_title)

        # Legend object
        leg = ROOT.TLegend(0, 0, .5, .5)
        entry1 = f'{h1.GetTitle()}'
        entry2 = f'{h2.GetTitle()}'
        leg.AddEntry(eff1, entry1, 'le')
        leg.AddEntry(eff2, entry2, 'le')

        # Include ratio panel
        if ratio:
            c, p1, p2 = self.createCanvas(option='ratio', size=self.canvas_size)

            ## Top Panel
            p1.cd()

            # Primary plot
            h1.SetTitle(self.title_string)
            h2.SetTitle(self.title_string)
            h1.Draw()
            self.format_axes(h1, option='upper', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            h2.Draw('SAME E')

            # Legend
            leg.Draw()
            self.format_legend(leg, pos=self.leg_pos, option='upper')

            ## Ratio Panel
            ROOT.gPad.Update()
            p2.cd()

            # Hist ratio
            r = self.eff_ratio(h1, h2)
            r.Draw()
            self.format_entry(r)
            self.format_axes(r, option='lower', xrange=self.xrange, yrange=self.rrange, text_size=self.text_size)

            # TODO Ratio legend 

            ROOT.gPad.Update()
            c.cd()
            c.Update()

        # No ratio panel
        else:
            c = self.createCanvas(option='hist', size=self.canvas_size)

            # Primary plot
            h1.Draw()
            self.format_axes(h1, option='full', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            h2.Draw('SAME E')

            # Legend
            self.format_legend(leg, option='full', pos=self.leg_pos)
            leg.Draw()

            ROOT.gPad.Update()
            c.Update()
        
        if save: c.SaveAs(save)