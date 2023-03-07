import ROOT
import numpy as np

class EfficiencyPlot():
    def __init__(self, init_params=None):
        ROOT.gStyle.SetOptStat(0)
        # ROOT.gStyle.SetOptTitle(0)
        self.color1 = 'black'
        self.color2 = 'orange'
        self.title_string = ';p_{T} [GeV];Efficiency'
        self.canvas_size = (800,800)
        self.xrange = (5,50)
        self.yrange = (0.,1.1)
        self.rrange = (.2,3)
        self.text_size='med'
        self.leg_pos = 'upper_right'

        if init_params: self.set_params(init_params)

    def set_params(self, params):
        for key in params:
            setattr(self, key, params[key])

    def format_entry(self, hist, title=None, marker_color='black', marker_style ='', marker_size='small', line_color='black', line_style='-', line_width='med'):
        color_map = {
            'white'   : 0,
            'black'   : 1,
            'red'     : 2,
            'green'   : 3,
            'blue'    : 4,
            'cyan'    : 432,
            'gray'    : 920,
            'magenta' : 616,
            'orange'  : 797,
        }

        linestyle_map = {
            '-'  : 1,
            '..' : 2,
            '--' : 9,
            '-.' : 10,
        }

        linewidth_map = {
            'thin'  : 1,
            'med'   : 2,
            'thick' : 5,
        }

        markerstyle_map = {
            ''     : 0,
            '.'    : 1,
            '+'    : 34,
            'x'    : 5,
            'o'    : 4,
            '*'    : 3,
            '^'    : 22,
            'star' : 29,
        }

        markersize_map = {
            'small'    : 1,
            'med'      : 2,
            'large'    : 3,
            'x-large'  : 4,
            'xx-large' : 5,
        }
        
        if title is not None: hist.SetTitle(title)
        hist.SetMarkerColor(color_map[marker_color])
        hist.SetMarkerStyle(markerstyle_map[marker_style])
        hist.SetMarkerSize(markersize_map[marker_size])
        hist.SetLineColor(color_map[line_color])
        hist.SetLineStyle(linestyle_map[line_style])
        hist.SetLineWidth(linewidth_map[line_width])

    def format_axes(self, hist, option='hist', xrange=None, yrange=None, text_size='small', x_title=None, y_title=None):
        titlesize_map = {
            'small' : .02,
            'med'   : .04,
            'large' : .05,
        }

        labelsize_map = {
            'small' : .025,
            'med'   : .04,
            'large' : .07,
        }

        titleoffset_map = {
            'hist' : {
                'small' : {'x' : 1.5, 'y' : 1.5},
                'med'   : {'x' : 1.5, 'y' : 1.5},
                'large' : {'x' : 1.5, 'y' : 1.5},
            },
            'eff' : {
                'small' : {'x' : 1.2, 'y' : 1.2},
                'med'   : {'x' : 1.2, 'y' : 1.1},
                'large' : {'x' : 1.2, 'y' : 1},
            },
            'ratio' : {
                'small' : {'x' : 1.5, 'y' : .5},
                'med'   : {'x' : 1.2, 'y' : .4},
                'large' : {'x' : 1.2, 'y' : .35},
            }
        }

        if option=='hist':
            padh = padw = padsize = 1
            hist.Draw()
            ROOT.gPad.Update()
            g = hist.GetPaintedGraph()

            # X- & Y-Axis
            if x_title is not None: g.GetXaxis().SetTitle(x_title)
            if y_title is not None: g.GetYaxis().SetTitle(y_title)
            if xrange is not None: g.GetXaxis().SetRangeUser(xrange[0],xrange[1])
            labelsize = labelsize_map[text_size] / padsize
            titlesize = titlesize_map[text_size] / padsize

            g.GetXaxis().SetLabelSize(labelsize)
            g.GetXaxis().SetLabelOffset(.008)
            g.GetXaxis().SetTitleSize(titlesize)
            g.GetXaxis().SetTitleOffset(titleoffset_map['hist'][text_size]['x'])
            g.GetYaxis().SetLabelSize(labelsize)
            g.GetYaxis().SetLabelOffset(.008)
            g.GetYaxis().SetTitleSize(titlesize)
            g.GetYaxis().SetTitleOffset(titleoffset_map['hist'][text_size]['y'])

        if option=='eff':
            padh = .7; padw = 1; padsize=.7
            hist.Draw()
            ROOT.gPad.Update()
            g = hist.GetPaintedGraph()
            labelsize = labelsize_map[text_size] / padsize
            titlesize = titlesize_map[text_size] / padsize

            # X-Axis
            if x_title is not None: g.GetXaxis().SetTitle(x_title)
            if xrange is not None: g.GetXaxis().SetRangeUser(xrange[0],xrange[1])
            g.GetXaxis().SetLabelSize(labelsize)
            g.GetXaxis().SetTitleSize(titlesize)
            g.GetXaxis().SetTitleOffset(titleoffset_map['eff'][text_size]['x'])

            # Y-Axis
            if yrange is not None:
                g.SetMinimum(yrange[0])
                g.SetMaximum(yrange[1])
            g.GetYaxis().SetLabelSize(labelsize)
            g.GetYaxis().SetLabelOffset(.008)
            g.GetYaxis().SetTitleSize(titlesize)
            g.GetYaxis().SetTitleOffset(titleoffset_map['eff'][text_size]['y'])

            ROOT.gPad.Update()

        elif option=='ratio':
            padh = .25; padw = 1; padsize=.25
            hist.SetTitle('')
            labelsize = labelsize_map[text_size] / padsize
            titlesize = titlesize_map[text_size] / padsize
            
            # X-Axis
            if x_title is not None: g.GetXaxis().SetTitle(x_title)
            if xrange is not None: hist.GetXaxis().SetRangeUser(xrange[0],xrange[1])
            hist.GetXaxis().SetLabelSize(labelsize)
            hist.GetXaxis().SetLabelOffset(.008)
            hist.GetXaxis().SetTitleSize(titlesize)
            hist.GetXaxis().SetTitleOffset(titleoffset_map['ratio'][text_size]['x'])

            # Y-Axis
            hist.GetYaxis().SetTitle('Ratio')
            if yrange is not None: hist.GetYaxis().SetRangeUser(yrange[0],yrange[1])
            hist.GetYaxis().SetLabelSize(labelsize)
            hist.GetYaxis().SetLabelOffset(.008)
            hist.GetYaxis().SetTitleSize(titlesize)
            hist.GetYaxis().SetTitleOffset(titleoffset_map['ratio'][text_size]['y'])
            hist.GetYaxis().SetNdivisions(4)

            # Draw Ratio Line at 1
            line = ROOT.TLine(0,0,1,1)
            line.SetLineStyle(2)
            line.DrawLine(xrange[0],1,xrange[1],1) if xrange else line.DrawLine(0,1,hist.GetXaxis().GetXmax(),1)

    def format_legend(self, leg, pos='lower_right', option='hist'):
        pos_map = {
            'hist' : {
                'upper_left'   : [.16,.75,.79,.88],
                'upper_right'  : [.16,.75,.89,.88],
                'center_left'  : [.16,.43,.79,.56],
                'center_right' : [.16,.43,.89,.56],
                'lower_left'   : [.16,.17,.79,.3],
                'lower_right'  : [.16,.17,.89,.3],
            },
            'eff' : {
                'upper_left'   : [.16,.7,.79,.88],
                'upper_right'  : [.16,.7,.89,.88],
                'center_left'  : [.16,.4,.79,.55],
                'center_right' : [.16,.4,.89,.55],
                'lower_left'   : [.16,.03,.79,.2],
                'lower_right'  : [.16,.03,.89,.2],
            },
            'ratio' : {
                'upper_left'   : [.16,.77,.5,.98],
                'upper_right'  : [.5,.77,.89,.98],
                'center_left'  : [.16,.65,.5,.85],
                'center_right' : [.5,.65,.89,.85],
                'lower_left'   : [.16,.52,.5,.73],
                'lower_right'  : [.5,.52,.89,.73],
            },
        }
        
        leg.SetTextSize(.04) if option=='hist' or option=='eff' else leg.SetTextSize(.1)

        leg.SetX1(pos_map[option][pos][0])
        leg.SetX2(pos_map[option][pos][2])
        leg.SetY1(pos_map[option][pos][1])
        leg.SetY2(pos_map[option][pos][3])

        ROOT.gPad.Modified()
        leg.DrawClone()

    def createCanvas(self, option='hist', size=(800,800)):
        c = ROOT.TCanvas('c', 'c', size[0], size[1])

        if option=='hist': 
            c.SetLeftMargin(0.15)
            c.SetBottomMargin(0.15)
            return c

        elif option=='ratio':
            pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1., 1.)
            pad1.SetBottomMargin(0) 
            pad1.SetLeftMargin(0.15)
            pad1.Draw()

            c.cd()  
            pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
            pad2.SetTopMargin(0)  
            pad2.SetBottomMargin(0.5)
            pad2.SetLeftMargin(0.15)    

            pad2.SetFrameFillColor(0)
            pad2.SetFrameBorderMode(0)
            pad2.SetFrameFillColor(0)
            pad2.SetFrameBorderMode(0)
            pad2.Draw()
            return c, pad1, pad2
 
    
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
            self.format_axes(eff1, option='eff', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            eff2.Draw('SAME E')
            # self.format_axes(eff2, option='eff', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)

            # Legend
            leg.Draw()
            self.format_legend(leg, pos=self.leg_pos, option='eff')

            ## Ratio Panel
            ROOT.gPad.Update()
            p2.cd()

            # Efficiency ratio
            r = self.eff_ratio(eff1, eff2)
            r.Draw()
            self.format_entry(r)
            self.format_axes(r, option='ratio', xrange=self.xrange, yrange=self.rrange, text_size=self.text_size)

            # Ratio legend FIXME
            # r_leg = ROOT.TLegend(0, 0, .5, .5)
            # r_leg.AddEntry(r, 'Ratio', 'l')
            # r_leg.Draw()
            # self.format_legend(r_leg, pos='lower_left', option='ratio')

            ROOT.gPad.Update()
            c.cd()
            c.Update()

        # No ratio panel
        else:
            c = self.createCanvas(option='hist', size=self.canvas_size)

            # Primary plot
            eff1.Draw()
            self.format_axes(eff1, option='hist', xrange=self.xrange, yrange=self.yrange, text_size=self.text_size)
            eff2.Draw('SAME')

            # Legend
            self.format_legend(leg, option='hist', pos=self.leg_pos)
            leg.Draw()

            ROOT.gPad.Update()
            c.Update()
        
        if save: c.SaveAs(save)
        del c, p1, p2