import random
import matplotlib.pyplot as plt


class Draw:
    def __init__(self, b, title=""):
        self.b = b
        self.title = title

    def drawTable(self):
        fig, ax = plt.subplots()
        table_data = list()
        col = ['Job', 'Time', 'Precedenze', 'Vincoli Disgiuntivi']
        table_data.append(col)
        for y in self.b.csp.jobs:
            col_name = y.name
            col_time = y.time
            col_precede = ''
            for k in y.precedence:
                if col_precede == '':
                    col_precede = k.name
                else:
                    col_precede += ', ' + k.name
            col_disjunctive = ''
            for k in y.disjunctive:
                if col_disjunctive == '':
                    col_disjunctive = k.name
                else:
                    col_disjunctive += ', ' + k.name
            col = [col_name, col_time, col_precede, col_disjunctive]
            table_data.append(col)
        table = ax.table(cellText=table_data, colWidths=[0.08, 0.08, 0.64, 0.2], loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1)
        ax.axis('off')
        ax.set_title(self.title)
        fig.set_size_inches(18, 10)
        plt.show()

    def drawSolution(self):
        time = 0
        ticks = []
        label_ticks = []
        labels = []
        start_ticks = 25
        bars = []
        legendLabel = []
        vLine = []
        for x in self.b.solution:
            for i in x:
                if time < x[i][list(x[i].keys())[-1]][1]:
                    time = x[i][list(x[i].keys())[-1]][1]
                ticks.append(start_ticks)
                label_ticks.append(str(i))
                start_ticks += 20
                labels.append(i)
                bars.append([])
                for j in x[i]:
                    legendLabel.append(
                        self.b.csp.X.getVariableName(j) + ' ' + str(i) + ':' + ' (' + str(x[i][j][0]) + ',' + str(
                            x[i][j][1]) + ')')
                    bars[i].append(x[i][j])
        fig1, ax1 = plt.subplots()
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Worker')
        ax1.set_ylim(0, start_ticks + 10)
        ax1.set_xlim(0, time + 10)
        ax1.set_yticks(ticks, labels=label_ticks)
        for i in range(len(bars)):
            for x in bars[i]:
                ax1.broken_barh([(x[0], x[1] - x[0])], (20 * (i + 1), 9),
                                facecolors=self.htmlColor(random.randint(0, 250), random.randint(0, 250),
                                                          random.randint(0, 250)), edgecolors=['black', 'black'])
                vLine.append((x[0], 0, 20 * (i + 1)))
                vLine.append((x[1], 0, 20 * (i + 1)))
        for x in vLine:
            ax1.vlines(x[0], x[1], x[2], alpha=0.2)
        ax1.legend(legendLabel, loc='upper center', bbox_to_anchor=(0.5, 1.15),
                   ncol=3, fancybox=True, shadow=True)
        fig1.set_size_inches(10, 7)
        ax1.set_title(self.title)
        plt.show()

    @staticmethod
    def htmlColor(r, g, b):
        def _chkarg(a):
            if isinstance(a, int):  # clamp to range 0--255
                if a < 0:
                    a = 0
                elif a > 255:
                    a = 255
            elif isinstance(a, float):  # clamp to range 0.0--1.0 and convert to integer 0--255
                if a < 0.0:
                    a = 0
                elif a > 1.0:
                    a = 255
                else:
                    a = int(round(a * 255))
            else:
                raise ValueError('Arguments must be integers or floats.')
            return a

        r = _chkarg(r)
        g = _chkarg(g)
        b = _chkarg(b)
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
