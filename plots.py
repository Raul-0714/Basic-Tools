import pygmt
import numpy as np


def Plot_faults(faults, fig, projection=None):
    x = []
    y = []
    for fault_index in range(len(faults['index'])):
        x.extend(faults['longitude'][fault_index])
        y.extend(faults['latitude'][fault_index])
        x.append(np.nan)
        y.append(np.nan)

    if projection:
        fig.plot(x=x, y=y, pen="0.8p,black", projection=projection)
    else:
        fig.plot(x=x, y=y, pen="0.8p,black")


def Plot_main_faults(main_faults, fig, projection=None):
    for fault_index in range(len(main_faults['index'])):
        x = main_faults['longitude'][fault_index]
        y = main_faults['latitude'][fault_index]
        linewidth = main_faults['line_width'][fault_index]
        out_linewidth = float(linewidth) + 1.0
        linecolor = main_faults['color'][fault_index]

        if projection:
            fig.plot(x=x, y=y, pen=f"{out_linewidth}p,white", projection=projection)
            fig.plot(x=x, y=y, pen=f"{linewidth}p,{linecolor}", projection=projection)
        else:
            fig.plot(x=x, y=y, pen=f"{out_linewidth}p,white")
            fig.plot(x=x, y=y, pen=f"{linewidth}p,{linecolor}")


def Plot_epicenters(mainshocks, fig):
    for index in range(len(mainshocks['index'])):
        x = mainshocks['epicenter_location'][index][1]
        y = mainshocks['epicenter_location'][index][0]
        style = mainshocks['symbol_style'][index][0]
        fill = mainshocks['symbol_style'][index][1]
        pen = mainshocks['pen_style'][index][0] + "," + mainshocks['pen_style'][index][1]
        fig.plot(x=x, y=y, style=style, fill=fill, pen=pen)

