import pygmt
import numpy as np
import xarray

def Plot_basemap(region, projection="M6i", title=None):
    fig = pygmt.Figure()
    if title:
        fig.basemap(region=region, projection=projection, frame=['a', f'+t"{title}"'])
    else:
        fig.basemap(region=region, projection=projection, frame=['a'])
    return fig


def Plot_hillshade(region,fig):
    grid = pygmt.datasets.load_earth_relief(resolution="01m", region=region)
    background_grid = xarray.full_like(grid, fill_value=1.0)
    intensity_grid = pygmt.grdgradient(grid=grid, azimuth=0, normalize='10')
    pygmt.makecpt(cmap='gray', series=[0, 1])
    fig.grdimage(grid=background_grid, shading=intensity_grid, transparency=50)


def Plot_topography(region, fig):
    grid = pygmt.datasets.load_earth_relief(resolution="01m", region=region)
    pygmt.makecpt(cmap='gmt/globe', series=[-3000, 3000])
    fig.grdimage(grid=grid, transparency=20)
    fig.colorbar(frame=['xa1000+l"Elevation (m)"'])


def Plot_coast(fig):
    fig.coast(
        water="lightblue",
        area_thresh=1000,
        shorelines="1/0.5p,black",
        resolution="i"
    )


def Plot_faults(faults, fig, projection=None, pen_style="0.8p,black"):
    x = []
    y = []
    for fault_index in range(len(faults['index'])):
        x.extend(faults['longitude'][fault_index])
        y.extend(faults['latitude'][fault_index])
        x.append(np.nan)
        y.append(np.nan)

    if projection:
        fig.plot(x=x, y=y, pen=pen_style, projection=projection)
    else:
        fig.plot(x=x, y=y, pen=pen_style)


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

