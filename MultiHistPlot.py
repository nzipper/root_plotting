import numpy as np
from ROOT import gROOT, gStyle, gPad, TLegend
from root_plotting.PlotBase import PlotBase
from root_plotting.Utils import clone

class MultiHistPlot(PlotBase):
    def __init__(self, init_params=None):
        gStyle.SetOptStat(0)
        self.title_string = None
        self.colors = ['black','orange','blue','red','green','magenta','cyan','gray']
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
        # r.Divide(r, h_2, c1=1., c2=1., option='B')
        r.Divide(h_2)
        return r
    
    def incl_yrange(self,hists):
        return np.min([h.GetMinimum() for h in hists]), np.max([h.GetMaximum() for h in hists])*1.1

    # Core function for plot generation
    def plotHists(self, hists, ratio=False, titles=None, show=False, save=False):
        self.yrange = self.incl_yrange(hists) if self.yrange is None else self.yrange

        # Construct plot objects
        for i, h in enumerate(hists):
            self.format_entry(h, line_color=self.colors[i%len(self.colors)], title=None)

        # Legend object
        leg = TLegend(0, 0, .5, .5)
        if titles is not None: assert len(hists)==len(titles)
        for i, h in enumerate(hists):
            entry = f'{h.GetTitle()}' if titles is None else titles[i]
            leg.AddEntry(h, entry, 'le')

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
            hists[0].Draw('E')
            self.format_axes(hists[0], option='upper', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size, title_string=self.title_string)
            for h in hists[1:]: 
                h.Draw('SAME E')

            # Legend
            leg.Draw()
            self.format_legend(leg, pos=self.leg_pos, option='upper', scale=self.leg_scale, legtext_size=self.legtext_size)

            ## Ratio Panel
            gPad.Update()
            p2.cd()

            # Hist ratio
            r = self.hist_ratio(hists[0], hists[1])
            r.Draw('E')
            self.format_entry(r, title=self.title_string if self.title_string else None)
            self.format_axes(r, option='lower', xrange=self.xrange, yrange=self.rrange, text_size=self.text_size)

            if len(hists)>2:
                for h in hists[2:]:
                    rnew = self.hist_ratio(hists[0], h)
                    self.format_entry(rnew, line_color=self.colors[i%len(self.colors)], title=self.title_string if self.title_string else None)
                    # self.format_entry(h, line_color=self.colors[i%len(self.colors)], title=None)
                    rnew.Draw('SAME E')

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
            hists[0].Draw('E')
            self.format_axes(hists[0], option='full', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            for h in hists[1:]: h.Draw('SAME E')

            # Legend
            self.format_legend(leg, option='full', pos=self.leg_pos, scale=self.leg_scale, legtext_size=self.legtext_size)
            leg.Draw()

            gPad.Update()
            c.Update()
        
            if show: c.Draw()
            if save: c.SaveAs(save)
            return c