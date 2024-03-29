from typing import List

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.figure import Figure

from cesm_toolbox.consts import SEASONS
from cesm_toolbox.paleoclimate import plot_land
from cesm_toolbox.utils import cyclitize, central_lon
from cesm_toolbox.pop import regrid


def map_difference_plot(
    datasets: List[xr.DataArray],
    titles: List[str],
    data_label: str,
    land: xr.DataArray,
    data_func=None,
    target_projection=ccrs.PlateCarree,
    input_projection=ccrs.PlateCarree,
    should_cyclitize=True,
    figsize=(30, 5),
    should_regrid=False,
    regrid_size=(1, 1),
    cmap="viridis",
    norm=None,
    diff_cmap="RdBu_r",
    constrained_layout=True,
    should_diff=True,
    levels=20,
    extent=None,
    land_threshold=0.75,
) -> Figure:
    # Data maniupulation here
    if data_func is not None:
        datasets = [data_func(d) for d in datasets]
    base_data = datasets[0]
    if should_diff:
        diffs = [d - base_data for d in datasets[1:]]
    else:
        diffs = datasets[1:]
    if should_cyclitize:
        base_data = cyclitize(base_data)
        diffs = [cyclitize(d) for d in diffs]
    if should_regrid:
        base_data = regrid(base_data, regrid_size)
        diffs = [regrid(d, regrid_size) for d in diffs]

    # Plot stuff here
    target_proj, input_proj = target_projection(), input_projection()
    num_plots = len(datasets)
    subplots = [int(f"1{num_plots}{i + 2}") for i in range(len(datasets) - 1)]

    fig, axes = plt.subplots(
        nrows=1,
        ncols=num_plots,
        subplot_kw={"projection": target_proj},
        figsize=figsize,
        constrained_layout=constrained_layout,
    )
    contour = axes[0].contourf(
        base_data.lon,
        base_data.lat,
        base_data,
        transform=input_proj,
        cmap=cmap,
        norm=norm,
        levels=levels,
    )
    axes[0].gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    plot_land(axes[0], land, threshold=land_threshold)
    axes[0].set_title(titles[0], size=15)
    cbar = fig.colorbar(contour, ax=axes[0], pad=0.15)
    cbar.set_label(data_label)
    if extent:
        axes[0].set_extent(extent, crs=ccrs.PlateCarree())
    else:
        axes[0].set_global()

    vmax = max(np.nanmax(d.values) for d in diffs)
    vmin = min(np.nanmin(d.values) for d in diffs)
    if should_diff:
        vmax = max(abs(vmin), abs(vmax))
        vmin = -vmax

    bounds = np.linspace(vmin, vmax, levels)
    for data, title, subplot, ax in zip(diffs, titles[1:], subplots, axes[1:].flat):
        diff_contour = ax.contourf(
            data.lon,
            data.lat,
            data,
            transform=input_proj,
            cmap=diff_cmap,
            vmin=vmin,
            vmax=vmax,
            levels=bounds,
        )
        ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
        plot_land(ax, land, threshold=land_threshold)
        ax.set_title(f"{title} - {titles[0]}", size=15)
        if extent:
            ax.set_extent(extent, crs=ccrs.PlateCarree())
        else:
            ax.set_global()

    cbar = fig.colorbar(diff_contour, ax=axes[1:].ravel().tolist())
    cbar.set_label(data_label)
    return fig


def seasonal_difference_plot(
    base_dataset: xr.DataArray,
    dataset: xr.DataArray,
    data_label: str,
    land: xr.DataArray,
    data_func=None,
    input_projection=ccrs.PlateCarree,
    output_projection=ccrs.PlateCarree,
    extent=None,
    diff_cmap="RdBu_r",
    levels=20,
    figsize=(24, 12),
    should_cyclitize=True,
    draw_labels=True,
    time_func=np.mean,
    mask: xr.DataArray = None,
    land_threshold=0.75,
) -> Figure:
    if data_func:
        base_dataset = data_func(base_dataset)
        dataset = data_func(dataset)
    grouped_base = base_dataset.groupby("time.season").reduce(time_func, dim="time")
    grouped_data = dataset.groupby("time.season").reduce(time_func, dim="time")
    diffs = [
        grouped_data.sel(season=season) - grouped_base.sel(season=season)
        for season in SEASONS
    ]
    if should_cyclitize:
        diffs = [cyclitize(d) for d in diffs]
    if mask is not None:
        diffs = [d.where(mask) for d in diffs]

    vmax = max(
        max(abs(float(np.nanmax(d.values))), abs(float(np.nanmin(d.values))))
        for d in diffs
    )

    central_longitude = central_lon(extent) if extent else 0

    fig, axes = plt.subplots(
        nrows=2,
        ncols=2,
        subplot_kw={
            "projection": output_projection(central_longitude=central_longitude)
        },
        figsize=figsize,
    )
    bounds = np.linspace(-vmax, vmax, levels)
    for season, ax, diff in zip(SEASONS, axes.flat, diffs):
        diff_contour = ax.contourf(
            diff.lon,
            diff.lat,
            diff,
            transform=input_projection(),
            cmap=diff_cmap,
            levels=bounds,
            vmin=-vmax,
            vmax=vmax,
        )
        plot_land(ax, land, threshold=land_threshold)
        if extent:
            ax.set_extent(extent)
        else:
            ax.set_global()
        ax.gridlines(draw_labels=draw_labels, alpha=0.5)
        ax.set_title(season, size=20)

    cbar = fig.colorbar(diff_contour, ax=axes.ravel().tolist())
    cbar.set_label(data_label)
    return fig


def seasonal_plot(
    dataset: xr.DataArray,
    data_label: str,
    land: xr.DataArray,
    data_func=None,
    input_projection=ccrs.PlateCarree,
    output_projection=ccrs.PlateCarree,
    extent=None,
    cmap="viridis",
    levels=20,
    figsize=(24, 12),
    should_cyclitize=True,
    should_norm=True,
    draw_labels=True,
    time_func=np.mean,
    mask: xr.DataArray = None,
) -> Figure:
    if data_func:
        dataset = data_func(dataset)
    grouped_data = dataset.groupby("time.season").reduce(time_func, dim="time")
    season_data = [grouped_data.sel(season=season) for season in SEASONS]
    if should_cyclitize:
        season_data = [cyclitize(d) for d in season_data]
    if mask is not None:
        season_data = [d.where(mask) for d in season_data]

    vmax = max(np.nanmax(d.values) for d in season_data)
    vmin = min(np.nanmin(d.values) for d in season_data)
    if should_norm:
        vmax = max(abs(vmin), abs(vmax))
        vmin = -vmax

    central_longitude = central_lon(extent) if extent else 0

    fig, axes = plt.subplots(
        nrows=2,
        ncols=2,
        subplot_kw={
            "projection": output_projection(central_longitude=central_longitude)
        },
        figsize=figsize,
    )
    bounds = np.linspace(vmin, vmax, levels)
    for season, ax, diff in zip(SEASONS, axes.flat, season_data):
        season_contour = ax.contourf(
            diff.lon,
            diff.lat,
            diff,
            transform=input_projection(),
            cmap=cmap,
            levels=bounds,
            vmin=vmin,
            vmax=vmax,
        )
        plot_land(ax, land)
        if extent:
            ax.set_extent(extent)
        else:
            ax.set_global()
        ax.gridlines(draw_labels=draw_labels, alpha=0.5)
        ax.set_title(season, size=20)

    cbar = fig.colorbar(season_contour, ax=axes.ravel().tolist())
    cbar.set_label(data_label)
    return fig


@ticker.FuncFormatter
def lat_formatter(x, pos):
    if x > 0:
        return f"{x:.0f}N"
    elif x < 0:
        return f"{abs(x):.0f}S"
    else:
        return f"{x:.0f}"


def line_plot_style(ax):
    ax.grid(alpha=0.4)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    ax.title.set_size(20)


def zonal_plot_style(ax):
    line_plot_style(ax)
    ax.set_xlim([-90, 90])
    ax.xaxis.set_major_formatter(lat_formatter)


def month_plot_style(ax):
    line_plot_style(ax)
    ax.set_xlim([0, 11])
