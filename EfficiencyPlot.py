import numpy as np
import ROOT
import PlotBase

class EfficiencyPlot(PlotBase):
    def __init__(self, init_params=None):
        ROOT.gStyle.SetOptStat(0)
        self.color1 = 'black'
        self.color2 = 'orange'
        self.title_string = ';p_{T} [GeV];Efficiency'
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
    
    def eff_ratio(self, eff_1, eff_2):
        hnew1 = eff_1.GetCopyPassedHisto()
        hnew2 = eff_1.GetCopyTotalHisto()
        hnew3 = eff_2.GetCopyPassedHisto()
        hnew4 = eff_2.GetCopyTotalHisto()
        hnew1.Divide(hnew1, hnew2, c1=1., c2=1., option='B')
        hnew3.Divide(hnew3, hnew4, c1=1., c2=1., option='B')
        hnew1.Divide(hnew3)
        return hnew1

    def integrate_eff(self, eff_1, int_floor=2., int_ceil=99999., show=False):
        hnew_pass = eff_1.GetCopyPassedHisto()
        hnew_tot = eff_1.GetCopyTotalHisto()

        num_tot = 0
        den_tot = 0
        nbins = hnew_pass.GetNbinsX() - 1
        for i in range(nbins):
            if hnew_pass.GetBinLowEdge(i) < int_floor or hnew_pass.GetBinLowEdge(i) > int_ceil: continue
            num_tot += hnew_pass.GetBinContent(i)
            den_tot += hnew_tot.GetBinContent(i)

        eff = num_tot/den_tot if den_tot else print(num_tot)
        eff = round(eff,3) if num_tot and den_tot else 0.
        err = 0. if eff==0. else '{:0.2e}'.format(np.sqrt((eff*(1-eff))/den_tot),5)
        if show: print(f'Integrated Eff = {num_tot} / {den_tot} = {eff} \pm {err}')
        return eff, err

    # Core function for plot generation
    def plotEfficiencies(self, h1, h2, ratio=True, h1_title=None, h2_title=None, save=False, addIntegral=False, integralRange=None):
        # Construct plot objects
        h1_pass = h1.GetCopyPassedHisto()
        h1_tot = h1.GetCopyTotalHisto()
        h2_pass = h2.GetCopyPassedHisto()
        h2_tot = h2.GetCopyTotalHisto()

        eff1 = ROOT.TEfficiency(h1_pass, h1_tot)
        eff2 = ROOT.TEfficiency(h2_pass, h2_tot)
        self.format_entry(eff1, line_color=self.color1, title=h1_title)
        self.format_entry(eff2, line_color=self.color2, title=h2_title)


        # Legend object
        leg = ROOT.TLegend(0, 0, .5, .5)
        entry1 = f'{eff1.GetTitle()}'
        entry2 = f'{eff2.GetTitle()}'

        # Efficiency integral
        if addIntegral:
            if integralRange: 
                int_floor, int_ceil = integralRange
            else:
                int_floor = h1_pass.GetBinLowEdge(1)
                int_ceil = h1_pass.GetBinLowEdge(h1_pass.GetNbinsX())
            eff1_int = self.integrate_eff(eff1, int_floor=int_floor, int_ceil=int_ceil)
            eff2_int = self.integrate_eff(eff2, int_floor=int_floor, int_ceil=int_ceil)
            entry1 = entry1+f' \\ [ \epsilon = {eff1_int[0]} \pm {eff1_int[1]}]'
            entry2 = entry2+f' \\ [ \epsilon = {eff2_int[0]} \pm {eff2_int[1]}]'

        leg.AddEntry(eff1, entry1, 'le')
        leg.AddEntry(eff2, entry2, 'le')

        # Include ratio panel
        if ratio:
            c, p1, p2 = self.createCanvas(option='ratio', size=self.canvas_size)

            ## Top Panel
            p1.cd()

            # Primary plot
            eff1.SetTitle(self.title_string)
            eff2.SetTitle(self.title_string)
            eff1.Draw()
            self.format_axes(eff1, option='upper', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            eff2.Draw('SAME E')

            # Legend
            leg.Draw()
            self.format_legend(leg, pos=self.leg_pos, option='upper')

            ## Ratio Panel
            ROOT.gPad.Update()
            p2.cd()

            # Efficiency ratio
            r = self.eff_ratio(eff1, eff2)
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
            eff1.Draw()
            self.format_axes(eff1, option='full', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            eff2.Draw('SAME')

            # Legend
            self.format_legend(leg, option='full', pos=self.leg_pos)
            leg.Draw()

            ROOT.gPad.Update()
            c.Update()
        
        if save: c.SaveAs(save)