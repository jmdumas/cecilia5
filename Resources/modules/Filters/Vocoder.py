class Module(BaseModule):
    """
    Module's documentation
    
    """
    def __init__(self):
        BaseModule.__init__(self)
        self.spec = self.addSampler("spec")
        self.exci = self.addSampler("exci")
        self.proc = Vocoder(self.spec, self.exci, freq=self.freq, spread=self.spread, 
                        q=self.q, slope=self.slope, stages=int(self.stages.get()), 
                        mul=DBToA(self.gain))
        self.out = Mix(self.proc, voices=self.nchnls, mul=self.env)

    def stages_up(self, value):
        self.proc.stages = int(value)

Interface = [
    csampler(name="spec", label="Spectral Envelope"),
    csampler(name="exci", label="Exciter"),
    cgraph(name="env", label="Overall Amplitude", func=[(0,1),(1,1)], col="blue"),
    cslider(name="freq", label="Base Frequency", min=10, max=1000, init=80, rel="log", unit="Hz", col="green"),
    cslider(name="spread", label="Frequency Spread", min=0.25, max=2, init=1.25, rel="log", unit="x", col="forestgreen"),
    cslider(name="q", label="Q Factor", min=0.5, max=200, init=20, rel="log", unit="Q", col="orange"),
    cslider(name="slope", label="Time Response", min=0, max=1, init=0.5, rel="lin", unit="x", col="red"),
    cslider(name="gain", label="Gain", min=-90, max=18, init=0, rel="lin", unit="dB", col="blue"),
    cslider(name="stages", label="Num of bands", min=4, max=64, init=20, rel="lin", res="int", unit="x", up=True),
    cpoly()
]
