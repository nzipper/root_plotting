import numpy as np
from ROOT import gROOT, gStyle, gPad, TLegend
from root_plotting.PlotBase import PlotBase
from root_plotting.Utils import clone


class HistPlot(PlotBase):
    def __init__(self, init_params=None):
        gStyle.SetOptStat(0)
        self.color1 = 'black'
        self.color2 = 'orange'
        self.title_string = ';p_{T} [GeV];Events'
        self.canvas_size = (800,800)
        self.xrange = None
        self.yrange = None
        self.rrange = (.5,2)
        self.text_size='med'
        self.leg_pos = 'upper_right'
        self.leg_scale = None
        if init_params: self.set_params(init_params)

    def set_params(self, params):
        for key in params:
            setattr(self, key, params[key])
    
    def hist_ratio(self, h_1, h_2):
        r = clone(h_1)
        r.Divide(h_2)
        return r

    # Core function for plot generation
    def plotHists(self, h1, h2, ratio=False, h1_title=None, h2_title=None, show=False, save=False):
        # Construct plot objects
        self.format_entry(h1, line_color=self.color1, title=None)
        self.format_entry(h2, line_color=self.color2, title=None)

        # Legend object
        leg = TLegend(0, 0, .5, .5)
        entry1 = f'{h1.GetTitle()}' if h1_title is None else h1_title
        entry2 = f'{h2.GetTitle()}' if h2_title is None else h2_title
        leg.AddEntry(h1, entry1, 'le')
        leg.AddEntry(h2, entry2, 'le')

        # Include ratio panel
        if ratio:
            c, p1, p2 = self.createCanvas(option='ratio', size=self.canvas_size)

            # TODO Fix CMS Style
            cms_style = False
            if cms_style:
                gROOT.ProcessLine("setTDRStyle();")
                gROOT.ProcessLine("CMS_lumi(c);")

            ## Top Panel
            p1.cd()

            # Primary plot
            h1.Draw('E')
            self.format_axes(h1, option='upper', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            h2.Draw('SAME E')

            # Legend
            leg.Draw()
            self.format_legend(leg, pos=self.leg_pos, option='upper', scale=self.leg_scale )

            ## Ratio Panel
            gPad.Update()
            p2.cd()

            # Hist ratio
            r = self.hist_ratio(h1, h2)
            r.Draw('E')
            self.format_entry(r)
            self.format_axes(r, option='lower', xrange=self.xrange, yrange=self.rrange, text_size=self.text_size)

            # # TODO Ratio legend 

            gPad.Update()
            c.cd()
            gPad.Update()
            c.Update()

            if show: c.Draw()
            if save: c.SaveAs(save)
            return c, r

        # No ratio panel
        else:
            c = self.createCanvas(option='hist', size=self.canvas_size)

            # Primary plot
            h1.Draw('E')
            self.format_axes(h1, option='full', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            h2.Draw('SAME E')

            # Legend
            self.format_legend(leg, option='full', pos=self.leg_pos, scale=self.leg_scale)
            leg.Draw()

            gPad.Update()
            c.Update()
        
            if show: c.Draw()
            if save: c.SaveAs(save)
            return c