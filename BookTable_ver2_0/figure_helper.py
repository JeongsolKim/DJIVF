import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Figure_helper():
    def __init__(self, layout):

        mpl.rc('font', family='맑은 고딕 Semilight')
        mpl.rc('axes', unicode_minus=False)

        self.layout = layout
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.max_h = -99
        self.rects = []

    def draw_group_bar_graph(self, ind, value_list, xlabel, width=0.27):
        if len(value_list[0]) == 0 and len(value_list[1]) == 0:
            return 0

        self.ax.clear()
        for value_num in range(len(value_list)):
            temp_rect = self.ax.bar(ind+width*value_num, value_list[value_num], width)
            self.rects.append(temp_rect)
            self.autolabel(temp_rect)

        self.ax.set_xticks(ind + width/2)
        self.ax.set_xticklabels(tuple(xlabel))
        self.ax.set_ylim([0, self.max_h*1.5])
        #self.ax.set_ylabel('판매 권수')
        #self.ax.set_xlabel('판매 일자')
        self.ax.legend(tuple([x[0] for x in self.rects]), ('cash', 'account'))

        self.canvas.draw()
        self.canvas.show()

    def autolabel(self, rect_list):
        for rect in rect_list:
            h = rect.get_height()
            if h > self.max_h: self.max_h = h
            self.ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h), ha='center', va='bottom')
