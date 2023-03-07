from ROOT import TH1F, TH1D

def clone(hist):
    newhist = TH1F(hist.GetName(),hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXmin(),  hist.GetXaxis().GetXmax())
    newhist.Sumw2()

    for ibin in range(hist.GetNbinsX()):
        newhist.SetBinContent(ibin, hist.GetBinContent(ibin))
        newhist.SetBinError(ibin, hist.GetBinError(ibin))

    return newhist

