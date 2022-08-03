from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig = Figure(dpi=100)
        self.fig.set_tight_layout(True) # to properly scale all elements on canvas
        self.axs = self.fig.add_subplot(1, 1, 1)
        self.axs.set_title("Real time Andor spectrum")
        self.axs.set_xlabel("Wavelength, nm", fontweight="bold")
        self.axs.set_ylabel("Intensity, a.u.", fontweight="bold")
        self.axs.grid()
        

        super(MplCanvas, self).__init__(self.fig)