This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.

<file_summary>
This section contains a summary of this file.

<purpose>
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.
</purpose>

<file_format>
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  - File path as an attribute
  - Full contents of the file
</file_format>

<usage_guidelines>
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.
</usage_guidelines>

<notes>
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: plotnine/geoms/*.py, plotnine/stats/*.py, plotnine/scales/*.py, plotnine/themes/*.py, plotnine/facets/*.py, plotnine/coords/*.py, plotnine/positions/*.py
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)
</notes>

</file_summary>

<directory_structure>
plotnine/
  coords/
    __init__.py
    coord_cartesian.py
    coord_fixed.py
    coord_flip.py
    coord_trans.py
    coord.py
  facets/
    __init__.py
    facet_grid.py
    facet_null.py
    facet_wrap.py
    facet.py
    labelling.py
    layout.py
    strips.py
  geoms/
    __init__.py
    annotate.py
    annotation_logticks.py
    annotation_stripes.py
    geom_abline.py
    geom_area.py
    geom_bar.py
    geom_bin_2d.py
    geom_blank.py
    geom_boxplot.py
    geom_col.py
    geom_count.py
    geom_crossbar.py
    geom_density_2d.py
    geom_density.py
    geom_dotplot.py
    geom_errorbar.py
    geom_errorbarh.py
    geom_freqpoly.py
    geom_histogram.py
    geom_hline.py
    geom_jitter.py
    geom_label.py
    geom_line.py
    geom_linerange.py
    geom_map.py
    geom_path.py
    geom_point.py
    geom_pointdensity.py
    geom_pointrange.py
    geom_polygon.py
    geom_qq_line.py
    geom_qq.py
    geom_quantile.py
    geom_raster.py
    geom_rect.py
    geom_ribbon.py
    geom_rug.py
    geom_segment.py
    geom_sina.py
    geom_smooth.py
    geom_spoke.py
    geom_step.py
    geom_text.py
    geom_tile.py
    geom_violin.py
    geom_vline.py
    geom.py
  positions/
    __init__.py
    position_dodge.py
    position_dodge2.py
    position_fill.py
    position_identity.py
    position_jitter.py
    position_jitterdodge.py
    position_nudge.py
    position_stack.py
    position.py
  scales/
    __init__.py
    _expand.py
    _runtime_typing.py
    limits.py
    range.py
    scale_alpha.py
    scale_color.py
    scale_continuous.py
    scale_datetime.py
    scale_discrete.py
    scale_identity.py
    scale_linetype.py
    scale_manual.py
    scale_shape.py
    scale_size.py
    scale_stroke.py
    scale_xy.py
    scale.py
    scales.py
  stats/
    __init__.py
    binning.py
    density.py
    distributions.py
    smoothers.py
    stat_bin_2d.py
    stat_bin.py
    stat_bindot.py
    stat_boxplot.py
    stat_count.py
    stat_density_2d.py
    stat_density.py
    stat_ecdf.py
    stat_ellipse.py
    stat_function.py
    stat_hull.py
    stat_identity.py
    stat_pointdensity.py
    stat_qq_line.py
    stat_qq.py
    stat_quantile.py
    stat_sina.py
    stat_smooth.py
    stat_sum.py
    stat_summary_bin.py
    stat_summary.py
    stat_unique.py
    stat_ydensity.py
    stat.py
  themes/
    __init__.py
    seaborn_rcmod.py
    targets.py
    theme_538.py
    theme_bw.py
    theme_classic.py
    theme_dark.py
    theme_gray.py
    theme_light.py
    theme_linedraw.py
    theme_matplotlib.py
    theme_minimal.py
    theme_seaborn.py
    theme_tufte.py
    theme_void.py
    theme_xkcd.py
    theme.py
    themeable.py
</directory_structure>

<files>
This section contains the contents of the repository's files.

<file path="plotnine/coords/__init__.py">
"""
Coordinates
"""

from .coord_cartesian import coord_cartesian
from .coord_fixed import coord_equal, coord_fixed
from .coord_flip import coord_flip
from .coord_trans import coord_trans

__all__ = (
    "coord_cartesian",
    "coord_fixed",
    "coord_equal",
    "coord_flip",
    "coord_trans",
)
</file>

<file path="plotnine/coords/coord_cartesian.py">
from __future__ import annotations

import typing
from types import SimpleNamespace

from ..iapi import panel_view
from ..positions.position import transform_position
from .coord import coord, dist_euclidean

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd

    from plotnine.iapi import scale_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatSeries,
    )


class coord_cartesian(coord):
    """
    Cartesian coordinate system

    Parameters
    ----------
    xlim :
        Limits (in data type of the x-aesthetic) for x axis.
        If None, then they are automatically computed.
    ylim :
        Limits (in data type of the x-aesthetic) for y axis.
        If None, then they are automatically computed.
    expand :
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    is_linear = True

    def __init__(
        self,
        xlim: tuple[Any, Any] | None = None,
        ylim: tuple[Any, Any] | None = None,
        expand: bool = True,
    ):
        self.limits = SimpleNamespace(x=xlim, y=ylim)
        self.expand = expand

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        from mizani.bounds import squish_infinite

        def squish_infinite_x(col: FloatSeries) -> FloatArray:
            return squish_infinite(col, range=panel_params.x.range)

        def squish_infinite_y(col: FloatSeries) -> FloatArray:
            return squish_infinite(col, range=panel_params.y.range)

        return transform_position(data, squish_infinite_x, squish_infinite_y)

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        """
        Compute the range and break information for the panel
        """
        from mizani.transforms import identity_trans

        from plotnine.scales.scale_continuous import scale_continuous

        def get_scale_view(
            scale: scale, limits: tuple[Any, Any]
        ) -> scale_view:
            coord_limits = (
                scale.transform(limits)
                if limits and isinstance(scale, scale_continuous)
                else limits
            )
            expansion = scale.default_expansion(expand=self.expand)
            ranges = scale.expand_limits(
                scale.final_limits, expansion, coord_limits, identity_trans()
            )
            sv = scale.view(limits=coord_limits, range=ranges.range)
            return sv

        out = panel_view(
            x=get_scale_view(scale_x, self.limits.x),
            y=get_scale_view(scale_y, self.limits.y),
        )
        return out

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> FloatArray:
        max_dist = dist_euclidean(panel_params.x.range, panel_params.y.range)[
            0
        ]
        return dist_euclidean(x, y) / max_dist
</file>

<file path="plotnine/coords/coord_fixed.py">
from __future__ import annotations

import typing

from .coord_cartesian import coord_cartesian

if typing.TYPE_CHECKING:
    from typing import Optional

    from plotnine.iapi import panel_view


class coord_fixed(coord_cartesian):
    """
    Cartesian coordinates with fixed relationship between x and y scales

    Parameters
    ----------
    ratio : float
        Desired aspect_ratio (:math:`y/x`) of the panel(s).
    xlim : tuple[float, float]
        Limits for x axis. If None, then they are automatically computed.
    ylim : tuple[float, float]
        Limits for y axis. If None, then they are automatically computed.
    expand : bool
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.

    Notes
    -----
    To specify aspect ratio of the visual size for the axes use the
    [](`~plotnine.themes.themeable.aspect_ratio`) themeable.

    ```python
    ggplot(data, aes('x', 'y')) + theme(aspect_ratio=0.5)
    ```

    When changing the `aspect_ratio` in either way, the `width` of the
    panel remains constant (as derived from the
    [](`plotnine.themes.themeable.figure_size`) themeable) and the
    `height` is altered to achieve desired ratio.
    """

    ratio: float

    def __init__(
        self,
        ratio: float = 1,
        xlim: Optional[tuple[float, float]] = None,
        ylim: Optional[tuple[float, float]] = None,
        expand: bool = True,
    ):
        super().__init__(xlim=xlim, ylim=ylim, expand=expand)
        self.ratio = ratio

    def aspect(self, panel_params: panel_view) -> float | None:
        x = panel_params.x.range
        y = panel_params.y.range
        return (y[1] - y[0]) / (x[1] - x[0]) * self.ratio


coord_equal = coord_fixed
</file>

<file path="plotnine/coords/coord_flip.py">
from __future__ import annotations

import typing

import pandas as pd

from ..iapi import labels_view, panel_ranges, panel_view
from .coord_cartesian import coord_cartesian

if typing.TYPE_CHECKING:
    from typing import Sequence, TypeVar

    from plotnine.scales.scale import scale

    THasLabels = TypeVar(
        "THasLabels", bound=pd.DataFrame | labels_view | panel_view
    )


class coord_flip(coord_cartesian):
    """
    Flipped cartesian coordinates

    The horizontal becomes vertical, and vertical becomes horizontal.
    This is primarily useful for converting geoms and statistics which
    display y conditional on x, to x conditional on y.

    Parameters
    ----------
    xlim : tuple[float, float], default=None
        Limits for x axis. If None, then they are automatically computed.
    ylim : tuple[float, float], default=None
        Limits for y axis. If None, then they are automatically computed.
    expand : bool, default=True
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    def labels(self, cur_labels: labels_view) -> labels_view:
        return flip_labels(super().labels(cur_labels))

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        data = flip_labels(data)
        return super().transform(data, panel_params, munch=munch)

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        panel_params = super().setup_panel_params(scale_x, scale_y)
        return flip_labels(panel_params)

    def setup_layout(self, layout: pd.DataFrame) -> pd.DataFrame:
        # switch the scales
        x, y = "SCALE_X", "SCALE_Y"
        layout[x], layout[y] = layout[y].copy(), layout[x].copy()
        return layout

    def range(self, panel_params: panel_view) -> panel_ranges:
        """
        Return the range along the dimensions of the coordinate system
        """
        # Defaults to providing the 2D x-y ranges
        return panel_ranges(x=panel_params.y.range, y=panel_params.x.range)


def flip_labels(obj: THasLabels) -> THasLabels:
    """
    Rename fields x to y and y to x

    Parameters
    ----------
    obj : dict_like | dataclass
        Object with labels to rename
    """

    def sub(a: str, b: str, df: pd.DataFrame):
        """
        Substitute all keys that start with a to b
        """
        columns: Sequence[str] = df.columns.tolist()
        for label in columns:
            if label.startswith(a):
                new_label = b + label[1:]
                df[new_label] = df.pop(label)

    if isinstance(obj, pd.DataFrame):
        sub("x", "z", obj)
        sub("y", "x", obj)
        sub("z", "y", obj)
    elif isinstance(obj, (labels_view, panel_view)):
        obj.x, obj.y = obj.y, obj.x  # type: ignore

    return obj
</file>

<file path="plotnine/coords/coord_trans.py">
from __future__ import annotations

from types import SimpleNamespace as NS
from typing import TYPE_CHECKING, cast
from warnings import warn

from ..exceptions import PlotnineWarning
from ..iapi import panel_ranges, panel_view
from ..positions.position import transform_position
from .coord import coord, dist_euclidean

if TYPE_CHECKING:
    from typing import Optional

    import pandas as pd
    from mizani.transforms import trans

    from plotnine.iapi import scale_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatSeries,
        TFloatArrayLike,
    )


class coord_trans(coord):
    """
    Transformed cartesian coordinate system

    Parameters
    ----------
    x : str | trans
        Name of transform or `trans` class to transform the x axis
    y : str | trans
        Name of transform or `trans` class to transform the y axis
    xlim : tuple[float, float]
        Limits for x axis. If None, then they are automatically computed.
    ylim : tuple[float, float]
        Limits for y axis. If None, then they are automatically computed.
    expand : bool
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    trans_x: trans
    trans_y: trans

    def __init__(
        self,
        x: str | trans = "identity",
        y: str | trans = "identity",
        xlim: Optional[tuple[float, float]] = None,
        ylim: Optional[tuple[float, float]] = None,
        expand: bool = True,
    ):
        from mizani.transforms import gettrans

        self.trans_x = gettrans(x)
        self.trans_y = gettrans(y)
        self.limits = NS(x=xlim, y=ylim)
        self.expand = expand

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        from mizani.bounds import squish_infinite

        if not self.is_linear and munch:
            data = self.munch(data, panel_params)

        def trans_x(col: FloatSeries) -> FloatSeries:
            result = transform_value(self.trans_x, col)
            if any(result.isna()):
                warn(
                    "Coordinate transform of x aesthetic "
                    "created one or more NaN values.",
                    PlotnineWarning,
                )
            return result

        def trans_y(col: FloatSeries) -> FloatSeries:
            result = transform_value(self.trans_y, col)
            if any(result.isna()):
                warn(
                    "Coordinate transform of y aesthetic "
                    "created one or more NaN values.",
                    PlotnineWarning,
                )
            return result

        data = transform_position(data, trans_x, trans_y)
        return transform_position(data, squish_infinite, squish_infinite)

    def backtransform_range(self, panel_params: panel_view) -> panel_ranges:
        return panel_ranges(
            x=self.trans_x.inverse(panel_params.x.range),
            y=self.trans_y.inverse(panel_params.y.range),
        )

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        """
        Compute the range and break information for the panel
        """

        def get_scale_view(
            scale: scale, limits: tuple[float, float], trans: trans
        ) -> scale_view:
            coord_limits = trans.transform(limits) if limits else limits

            expansion = scale.default_expansion(expand=self.expand)
            ranges = scale.expand_limits(
                scale.final_limits, expansion, coord_limits, trans
            )
            sv = scale.view(
                limits=coord_limits,
                range=ranges.range,
            )
            sv.range = tuple(sorted(ranges.range_coord))  # type: ignore
            breaks = cast("tuple[float, float]", sv.breaks)
            sv.breaks = transform_value(trans, breaks)
            sv.minor_breaks = transform_value(trans, sv.minor_breaks)
            return sv

        out = panel_view(
            x=get_scale_view(scale_x, self.limits.x, self.trans_x),
            y=get_scale_view(scale_y, self.limits.y, self.trans_y),
        )
        return out

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> FloatArray:
        max_dist = dist_euclidean(panel_params.x.range, panel_params.y.range)[
            0
        ]
        xt = self.trans_x.transform(x)
        yt = self.trans_y.transform(y)
        return dist_euclidean(xt, yt) / max_dist


def transform_value(trans: trans, value: TFloatArrayLike) -> TFloatArrayLike:
    """
    Transform value
    """
    return trans.transform(value)
</file>

<file path="plotnine/coords/coord.py">
from __future__ import annotations

import typing
from copy import copy

import numpy as np

from ..iapi import panel_ranges

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    import pandas as pd

    from plotnine import ggplot
    from plotnine.iapi import labels_view, panel_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatArrayLike,
        FloatSeries,
    )


class coord:
    """
    Base class for all coordinate systems
    """

    # If the coordinate system is linear
    is_linear = False

    # Additional parameters created acc. to the data,
    # if the coordinate system needs them
    params: dict[str, Any]

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add coordinates to ggplot object
        """
        other.coordinates = copy(self)
        return other

    def setup_data(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        """
        Allow the coordinate system to manipulate the layer data

        Parameters
        ----------
        data :
            Data for all Layer

        Returns
        -------
        :
            Modified layer data
        """
        return data

    def setup_params(self, data: list[pd.DataFrame]):
        """
        Create additional parameters

        A coordinate system may need to create parameters
        depending on the *original* data that the layers get.

        Parameters
        ----------
        data :
            Data for each layer before it is manipulated in
            any way.
        """
        self.params = {}

    def setup_layout(self, layout: pd.DataFrame) -> pd.DataFrame:
        """
        Allow the coordinate system alter the layout dataframe

        Parameters
        ----------
        layout :
            Dataframe in which data is assigned to panels and scales

        Returns
        -------
        :
            layout dataframe altered to according to the requirements
            of the coordinate system.

        Notes
        -----
        The input dataframe may be changed.
        """
        return layout

    def aspect(self, panel_params: panel_view) -> float | None:
        """
        Return desired aspect ratio for the plot

        If not overridden by the subclass, this method
        returns `None`, which means that the coordinate
        system does not influence the aspect ratio.
        """
        return None

    def labels(self, cur_labels: labels_view) -> labels_view:
        """
        Modify labels

        Parameters
        ----------
        cur_labels :
            Current labels. The coord can modify them as necessary.

        Returns
        -------
        :
            Modified labels. Same object as the input.
        """
        return cur_labels

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        """
        Transform data before it is plotted

        This is used to "transform the coordinate axes".
        Subclasses should override this method
        """
        return data

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        """
        Compute the range and break information for the panel
        """
        msg = "The coordinate should implement this method."
        raise NotImplementedError(msg)

    def range(self, panel_params: panel_view) -> panel_ranges:
        """
        Return the range along the dimensions of the coordinate system
        """
        # Defaults to providing the 2D x-y ranges
        return panel_ranges(x=panel_params.x.range, y=panel_params.y.range)

    def backtransform_range(self, panel_params: panel_view) -> panel_ranges:
        """
        Backtransform the panel range in panel_params to data coordinates

        Coordinate systems that do any transformations should override
        this method. e.g. coord_trans has to override this method.
        """
        return self.range(panel_params)

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> npt.NDArray[Any]:
        msg = "The coordinate should implement this method."
        raise NotImplementedError(msg)

    def munch(
        self, data: pd.DataFrame, panel_params: panel_view
    ) -> pd.DataFrame:
        ranges = self.backtransform_range(panel_params)

        x_neginf = np.isneginf(data["x"])
        x_posinf = np.isposinf(data["x"])
        y_neginf = np.isneginf(data["y"])
        y_posinf = np.isposinf(data["y"])
        if x_neginf.any():
            data.loc[x_neginf, "x"] = ranges.x[0]
        if x_posinf.any():
            data.loc[x_posinf, "x"] = ranges.x[1]
        if y_neginf.any():
            data.loc[y_neginf, "y"] = ranges.y[0]
        if y_posinf.any():
            data.loc[y_posinf, "y"] = ranges.y[1]

        dist = self.distance(data["x"], data["y"], panel_params)
        bool_idx = (
            data["group"].to_numpy()[1:] != data["group"].to_numpy()[:-1]
        )
        dist[bool_idx] = np.nan

        # Munch
        munched = munch_data(data, dist)
        return munched


def dist_euclidean(x: FloatArrayLike, y: FloatArrayLike) -> FloatArray:
    """
    Calculate euclidean distance
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    return np.sqrt(
        (x[:-1] - x[1:]) ** 2 + (y[:-1] - y[1:]) ** 2, dtype=np.float64
    )


def interp(start: int, end: int, n: int) -> FloatArray:
    """
    Interpolate
    """
    return np.linspace(start, end, n, endpoint=False)


def munch_data(data: pd.DataFrame, dist: FloatArray) -> pd.DataFrame:
    """
    Breakup path into small segments
    """
    x, y = data["x"], data["y"]
    segment_length = 0.01

    # How many endpoints for each old segment,
    # not counting the last one
    dist[np.isnan(dist)] = 1
    extra = np.maximum(np.floor(dist / segment_length), 1)
    extra = extra.astype(int)

    # Generate extra pieces for x and y values
    # The final point must be manually inserted at the end
    x = [interp(start, end, n) for start, end, n in zip(x[:-1], x[1:], extra)]
    y = [interp(start, end, n) for start, end, n in zip(y[:-1], y[1:], extra)]
    x.append(data["x"].iloc[-1])
    y.append(data["y"].iloc[-1])
    x = np.hstack(x)
    y = np.hstack(y)

    # Replicate other aesthetics: defined by start point
    # but also must include final point
    idx = np.hstack(
        [
            np.repeat(data.index[:-1], extra),
            len(data) - 1,
            # data.index[-1] # TODO: Maybe not
        ]
    )

    munched = data.loc[idx, list(data.columns.difference(["x", "y"]))]
    munched["x"] = x
    munched["y"] = y
    munched.reset_index(drop=True, inplace=True)

    return munched
</file>

<file path="plotnine/facets/__init__.py">
"""
Facets
"""

from .facet_grid import facet_grid
from .facet_null import facet_null
from .facet_wrap import facet_wrap
from .labelling import (
    as_labeller,
    label_both,
    label_context,
    label_value,
    labeller,
)

__all__ = (
    "facet_grid",
    "facet_null",
    "facet_wrap",
    "label_value",
    "label_both",
    "label_context",
    "labeller",
    "as_labeller",
)
</file>

<file path="plotnine/facets/facet_null.py">
from __future__ import annotations

import typing

from .facet import facet, layout_null

if typing.TYPE_CHECKING:
    import pandas as pd


class facet_null(facet):
    """
    A single Panel

    Parameters
    ----------
    shrink : bool, default=True
        Whether to shrink the scales to the output of the
        statistics instead of the raw data.
    """

    def __init__(self, shrink: bool = True):
        facet.__init__(self, shrink=shrink)
        self.nrow = 1
        self.ncol = 1

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        data["PANEL"] = 1
        return data

    def compute_layout(
        self,
        data: list[pd.DataFrame],
    ) -> pd.DataFrame:
        return layout_null()
</file>

<file path="plotnine/facets/labelling.py">
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from ..exceptions import PlotnineError

if TYPE_CHECKING:
    from typing import Callable, Literal, Optional, TypeAlias

    from ..iapi import strip_label_details

    # Function that can facet strips
    StripLabellingFunc: TypeAlias = Callable[
        [strip_label_details], strip_label_details
    ]

    StripLabellingFuncNames: TypeAlias = Literal[
        "label_value", "label_both", "label_context"
    ]

    StripLabellingDict: TypeAlias = (
        dict[str, str] | dict[str, Callable[[str], str]]
    )

    # Can be coerced to a StripLabellingFunc
    CanBeStripLabellingFunc: TypeAlias = (
        StripLabellingFuncNames
        | StripLabellingFunc
        | Callable[[str], str]
        | StripLabellingDict
    )


def label_value(
    label_info: strip_label_details, multi_line: bool = True
) -> strip_label_details:
    """
    Keep value as the label

    Parameters
    ----------
    label_info : strip_label_details
        Label information whose values will be returned
    multi_line : bool
        Whether to place each variable on a separate line

    Returns
    -------
    out : strip_label_details
        Label text strings
    """
    label_info = label_info.copy()

    if not multi_line:
        label_info = label_info.collapse()

    return label_info


def label_both(
    label_info: strip_label_details, multi_line: bool = True, sep: str = ": "
) -> strip_label_details:
    """
    Concatenate the facet variable with the value

    Parameters
    ----------
    label_info : strip_label_details
        Label information to be modified.
    multi_line : bool
        Whether to place each variable on a separate line
    sep : str
        Separation between variable name and value

    Returns
    -------
    out : strip_label_details
        Label information
    """
    label_info = label_info.copy()

    for var, lvalue in label_info.variables.items():
        label_info.variables[var] = f"{var}{sep}{lvalue}"

    if not multi_line:
        label_info = label_info.collapse()

    return label_info


def label_context(
    label_info: strip_label_details, multi_line: bool = True, sep: str = ": "
) -> strip_label_details:
    """
    Create an unabiguous label string

    If facetting over a single variable, `label_value` is
    used, if two or more variables then `label_both` is used.

    Parameters
    ----------
    label_info : strip_label_details
        Label information
    multi_line : bool
        Whether to place each variable on a separate line
    sep : str
        Separation between variable name and value

    Returns
    -------
    out : str
        Concatenated label values (or pairs of variable names
        & values)
    """
    if len(label_info) == 1:
        return label_value(label_info, multi_line)
    else:
        return label_both(label_info, multi_line, sep)


LABELLERS: dict[StripLabellingFuncNames, StripLabellingFunc] = {
    "label_value": label_value,
    "label_both": label_both,
    "label_context": label_context,
}


def as_labeller(
    x: Optional[CanBeStripLabellingFunc] = None,
    default: CanBeStripLabellingFunc = label_value,
    multi_line: bool = True,
) -> labeller:
    """
    Coerse to labeller

    Parameters
    ----------
    x : callable | dict
        Object to coerce
    default : str | callable
        Default labeller. If it is a string,
        it should be the name of one the labelling
        functions provided by plotnine.
    multi_line : bool
        Whether to place each variable on a separate line

    Returns
    -------
    out : labeller
        Labelling function
    """
    if x is None:
        x = default

    if isinstance(x, labeller):
        return x

    x = _as_strip_labelling_func(x)
    return labeller(rows=x, cols=x, multi_line=multi_line)


class labeller:
    """
    Facet Strip Labelling

    When called with strip_label_details knows how to
    alter the strip labels along either dimension.

    Parameters
    ----------
    rows : str | callable
        How to label the rows
    cols : str | callable
        How to label the columns
    multi_line : bool
        Whether to place each variable on a separate line
    default : str | callable
        Fallback labelling function. If it is a string, it should be
        one of `["label_value", "label_both", "label_context"]`{.py}.
    kwargs : dict
        {variable name : function | string} pairs for
        renaming variables. A function to rename the variable
        or a string name.
    """

    def __init__(
        self,
        rows: Optional[CanBeStripLabellingFunc] = None,
        cols: Optional[CanBeStripLabellingFunc] = None,
        multi_line: bool = True,
        default: CanBeStripLabellingFunc = "label_value",
        **kwargs: Callable[[str], str],
    ):
        # Sort out the labellers along each dimension
        self.rows_labeller = _as_strip_labelling_func(rows, default)
        self.cols_labeller = _as_strip_labelling_func(cols, default)
        self.multi_line = multi_line
        self.variable_maps = kwargs

    def __call__(self, label_info: strip_label_details) -> strip_label_details:
        """
        Called to do the labelling
        """
        variable_maps = {
            k: v
            for k, v in self.variable_maps.items()
            if k in label_info.variables
        }

        # No variable specific labeller
        if label_info.meta["dimension"] == "rows":
            result = self.rows_labeller(label_info)
        else:
            result = self.cols_labeller(label_info)

        # Make dict_labeler for the  variable specific labelers
        # do the label and merge
        if variable_maps:
            d = {
                value: variable_maps[var]
                for var, value in label_info.variables.items()
                if var in variable_maps
            }
            func = _as_strip_labelling_func(d)
            result2 = func(label_info)
            result.variables.update(result2.variables)

        if not self.multi_line:
            result = result.collapse()

        return result


def _as_strip_labelling_func(
    fobj: Optional[CanBeStripLabellingFunc],
    default: CanBeStripLabellingFunc = "label_value",
) -> StripLabellingFunc:
    """
    Create a function that can operate on strip_label_details
    """
    if fobj is None:
        fobj = default

    if isinstance(fobj, str) and fobj in LABELLERS:
        return LABELLERS[fobj]

    if isinstance(fobj, _core_labeller):
        return fobj
    elif callable(fobj):
        if fobj.__name__ in LABELLERS:
            return fobj  # type: ignore
        else:
            return _function_labeller(fobj)  # type: ignore
    elif isinstance(fobj, dict):
        return _dict_labeller(fobj)
    else:
        msg = f"Could not create a labelling function for with `{fobj}`."
        raise PlotnineError(msg)


class _core_labeller(metaclass=ABCMeta):
    """
    Per item
    """

    @abstractmethod
    def __call__(self, label_info: strip_label_details) -> strip_label_details:
        pass


class _function_labeller(_core_labeller):
    """
    Use a function turn facet value into a label

    Parameters
    ----------
    func : callable
        Function to label an individual string
    """

    def __init__(self, func: Callable[[str], str]):
        self.func = func

    def __call__(self, label_info: strip_label_details) -> strip_label_details:
        label_info = label_info.copy()
        variables = label_info.variables
        for facet_var, facet_value in variables.items():
            variables[facet_var] = self.func(facet_value)
        return label_info


class _dict_labeller(_core_labeller):
    """
    Use a dict to alter specific facet values

    Parameters
    ----------
    lookup : dict
        A dict of the one of the forms
          - {facet_value: label_value}
          - {facet_value: callable(<label_value>)}
    """

    def __init__(
        self, lookup: dict[str, str] | dict[str, Callable[[str], str]]
    ):
        self.lookup = lookup

    def __call__(self, label_info: strip_label_details) -> strip_label_details:
        label_info = label_info.copy()
        variables = label_info.variables
        # Replace facet_value with values from the lookup table
        # If the value is function, call it  the result of calling function
        for facet_var, facet_value in variables.items():
            target = self.lookup.get(facet_value)
            if target is None:
                continue
            elif callable(target):
                variables[facet_var] = target(facet_value)
            else:
                variables[facet_var] = target
        return label_info
</file>

<file path="plotnine/facets/layout.py">
from __future__ import annotations

import typing
from contextlib import suppress

import numpy as np

from .._utils import match
from ..exceptions import PlotnineError
from ..iapi import labels_view, layout_details, pos_scales

if typing.TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine import ggplot
    from plotnine.coords.coord import coord
    from plotnine.facets.facet import facet
    from plotnine.iapi import panel_view
    from plotnine.layer import Layers
    from plotnine.scales.scales import Scales


class Layout:
    """
    Layout of entire plot
    """

    # facet
    facet: facet

    # coordinate system
    coord: coord

    # A dataframe with the layout information of the plot
    layout: pd.DataFrame

    # List of x scales
    panel_scales_x: Scales

    # List of y scales
    panel_scales_y: Scales

    # Range & breaks information for each panel
    panel_params: list[panel_view]

    axs: list[Axes]  # MPL axes

    def setup(self, layers: Layers, plot: ggplot):
        """
        Create a layout for the panels

        The layout is a dataframe that stores all the
        structural information about the panels that will
        make up the plot. The actual layout depends on
        the type of facet.

        This method ensures that each layer has a copy of the
        data it needs in `layer.data`. That data is also has
        column `PANEL` that indicates the panel onto which each
        data row/item will be plotted.
        """
        data = [l.data for l in layers]

        # setup facets
        self.facet = plot.facet
        self.facet.setup_params(data)
        data = self.facet.setup_data(data)

        # setup coords
        self.coord = plot.coordinates
        self.coord.setup_params(data)
        data = self.coord.setup_data(data)

        # Generate panel layout
        data = self.facet.setup_data(data)
        self.layout = self.facet.compute_layout(data)
        self.layout = self.coord.setup_layout(self.layout)
        self.check_layout()

        # Map the data to the panels
        for layer, ldata in zip(layers, data):
            layer.data = self.facet.map(ldata, self.layout)

    def train_position(self, layers: Layers, scales: Scales):
        """
        Create all the required x & y panel_scales

        And set the ranges for each scale according to the data

        Notes
        -----
        The number of x or y scales depends on the facetting,
        particularly the scales parameter. e.g if `scales="free"`{.py}
        then each panel will have separate x and y scales, and
        if `scales="fixed"`{.py} then all panels will share an x
        scale and a y scale.
        """
        layout = self.layout
        if not hasattr(self, "panel_scales_x") and scales.x:
            result = self.facet.init_scales(layout, scales.x, None)
            self.panel_scales_x = result.x

        if not hasattr(self, "panel_scales_y") and scales.y:
            result = self.facet.init_scales(layout, None, scales.y)
            self.panel_scales_y = result.y

        self.facet.train_position_scales(self, layers)

    def map_position(self, layers: Layers):
        """
        Map x & y (position) aesthetics onto the scales.

        e.g If the x scale is scale_x_log10, after this
        function all x, xmax, xmin, ... columns in data
        will be mapped onto log10 scale (log10 transformed).
        The real mapping is handled by the scale.map
        """
        _layout = self.layout

        for layer in layers:
            data = layer.data
            match_id = match(data["PANEL"], _layout["PANEL"])
            if self.panel_scales_x:
                x_vars = list(
                    set(self.panel_scales_x[0].aesthetics) & set(data.columns)
                )
                SCALE_X = _layout["SCALE_X"].iloc[match_id].tolist()
                self.panel_scales_x.map(data, x_vars, SCALE_X)

            if self.panel_scales_y:
                y_vars = list(
                    set(self.panel_scales_y[0].aesthetics) & set(data.columns)
                )
                SCALE_Y = _layout["SCALE_Y"].iloc[match_id].tolist()
                self.panel_scales_y.map(data, y_vars, SCALE_Y)

    def get_scales(self, i: int) -> pos_scales:
        """
        Return x & y scales for panel i

        Parameters
        ----------
        i : int
          Panel id

        Returns
        -------
        scales : types.SimpleNamespace
          Class attributes *x* for the x scale and *y*
          for the y scale of the panel

        """
        # wrapping with np.asarray prevents an exception
        # on some datasets
        bool_idx = np.asarray(self.layout["PANEL"]) == i

        idx = self.layout["SCALE_X"].loc[bool_idx].iloc[0]
        xsc = self.panel_scales_x[idx - 1]

        idx = self.layout["SCALE_Y"].loc[bool_idx].iloc[0]
        ysc = self.panel_scales_y[idx - 1]

        return pos_scales(x=xsc, y=ysc)

    def reset_position_scales(self):
        """
        Reset x and y scales
        """
        if not self.facet.shrink:
            return

        with suppress(AttributeError):
            self.panel_scales_x.reset()

        with suppress(AttributeError):
            self.panel_scales_y.reset()

    def setup_panel_params(self, coord: coord):
        """
        Calculate the x & y range & breaks information for each panel

        Parameters
        ----------
        coord : coord
            Coordinate
        """
        if not self.panel_scales_x:
            raise PlotnineError("Missing an x scale")

        if not self.panel_scales_y:
            raise PlotnineError("Missing a y scale")

        self.panel_params = []
        cols = ["SCALE_X", "SCALE_Y"]
        for i, j in self.layout[cols].itertuples(index=False):
            i, j = i - 1, j - 1
            params = coord.setup_panel_params(
                self.panel_scales_x[i], self.panel_scales_y[j]
            )
            self.panel_params.append(params)

    def finish_data(self, layers: Layers):
        """
        Modify data before it is drawn out by the geom

        Parameters
        ----------
        layers : list
            List of layers
        """
        for layer in layers:
            layer.data = self.facet.finish_data(layer.data, self)

    def check_layout(self):
        required = {"PANEL", "SCALE_X", "SCALE_Y"}
        common = self.layout.columns.intersection(list(required))
        if len(required) != len(common):
            raise PlotnineError(
                "Facet layout has bad format. It must contain "
                f"the columns '{required}'"
            )

    def xlabel(self, labels: labels_view) -> str:
        """
        Determine x-axis label

        Parameters
        ----------
        labels : labels_view
            Labels as specified by the user through the `labs` or
            `xlab` calls.

        Returns
        -------
        out : str
            x-axis label
        """
        if self.panel_scales_x[0].name is not None:
            return self.panel_scales_x[0].name
        elif labels.x is not None:
            return labels.x
        return ""

    def ylabel(self, labels: labels_view) -> str:
        """
        Determine y-axis label

        Parameters
        ----------
        labels : labels_view
            Labels as specified by the user through the `labs` or
            `ylab` calls.

        Returns
        -------
        out : str
            y-axis label
        """
        if self.panel_scales_y[0].name is not None:
            return self.panel_scales_y[0].name
        elif labels.y is not None:
            return labels.y
        return ""

    def set_xy_labels(self, labels: labels_view) -> labels_view:
        """
        Determine x & y axis labels

        Parameters
        ----------
        labels : labels_view
            Labels as specified by the user through the `labs` or
            `ylab` calls.

        Returns
        -------
        out : labels_view
            Modified labels
        """
        labels.x = self.xlabel(labels)
        labels.y = self.ylabel(labels)
        return labels

    def get_details(self) -> list[layout_details]:
        columns = [
            "PANEL",
            "ROW",
            "COL",
            "SCALE_X",
            "SCALE_Y",
            "AXIS_X",
            "AXIS_Y",
        ]
        vcols = self.layout.columns.difference(columns)
        lst = []
        nrow = self.layout["ROW"].max()
        ncol = self.layout["COL"].max()
        for pidx, row in self.layout.iterrows():
            ld = layout_details(
                panel_index=pidx,  # type: ignore
                nrow=nrow,
                ncol=ncol,
                variables={name: row[name] for name in vcols},
                **{str.lower(k): row[k] for k in columns},
            )
            lst.append(ld)
        return lst
</file>

<file path="plotnine/facets/strips.py">
from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..iapi import strip_draw_info, strip_label_details

if TYPE_CHECKING:
    from typing import Sequence

    from matplotlib.axes import Axes
    from typing_extensions import Self

    from plotnine import theme
    from plotnine.facets.facet import facet
    from plotnine.facets.layout import Layout
    from plotnine.iapi import layout_details
    from plotnine.typing import StripPosition


class strip:
    """
    A strip

    This class exists to have in one place all that is required to draw
    strip text onto an axes. As Matplotlib does not have a layout manager
    that makes it easy to adorn an axes with artists, we have to compute
    the space required for the text and the background strip on which it
    is drawn. This is very finicky and fails once the facets become
    complicated.
    """

    position: StripPosition
    label_info: strip_label_details

    def __init__(
        self,
        vars: Sequence[str],
        layout_info: layout_details,
        facet: facet,
        ax: Axes,
        position: StripPosition,
    ):
        self.vars = vars
        self.ax = ax
        self.position = position
        self.facet = facet
        self.figure = facet.figure
        self.theme = facet.theme
        self.layout_info = layout_info
        label_info = strip_label_details.make(layout_info, vars, position)
        self.label_info = facet.labeller(label_info)

    def get_draw_info(self) -> strip_draw_info:
        """
        Get information required to draw strips

        Returns
        -------
        out :
            A structure with all the coordinates (x, y) required
            to draw the strip text and the background box
            (box_x, box_y, box_width, box_height).
        """
        theme = self.theme
        position = self.position

        if position == "top":
            # The x & y values are just starting locations
            # The final location is determined by the layout manager.
            bg_y = 1
            ha = theme.getp(("strip_text_x", "ha"), "center")
            va = theme.getp(("strip_text_x", "va"), "center")
            rotation = theme.getp(("strip_text_x", "rotation"))
            bg_height = 0  # Determined by the text size
            margin = theme.getp(("strip_text_x", "margin")).to("lines")
            strip_align = theme.getp("strip_align_x")

            # x & width properties of the background slide and
            # shrink the strip horizontally.
            bg_x = theme.getp(("strip_text_x", "x"), 0)
            bg_width = theme.getp(("strip_background_x", "width"), 1)

        elif position == "right":
            # The x & y values are just starting locations
            # The final location is determined by the layout manager.
            bg_x = 1
            ha = theme.getp(("strip_text_y", "ha"), "center")
            va = theme.getp(("strip_text_y", "va"), "center")
            rotation = theme.getp(("strip_text_y", "rotation"))
            bg_width = 0  # Determine by the text height
            margin = theme.getp(("strip_text_y", "margin")).to("lines")
            strip_align = theme.getp("strip_align_y")

            # y & height properties of the background slide and
            # shrink the strip vertically.
            bg_y = theme.getp(("strip_text_y", "y"), 0)
            bg_height = theme.getp(("strip_background_y", "height"), 1)
        else:
            raise ValueError(f"Unknown position for strip text: {position!r}")

        return strip_draw_info(
            bg_x=bg_x,
            bg_y=bg_y,
            ha=ha,
            va=va,
            bg_width=bg_width,
            bg_height=bg_height,
            margin=margin,
            strip_align=strip_align,
            position=position,
            label=self.label_info.text(),
            ax=self.ax,
            rotation=rotation,
            layout=self.layout_info,
        )

    def draw(self):
        """
        Create a background patch and put a label on it
        """

        from .._mpl.text import StripText

        targets = self.theme.targets
        draw_info = self.get_draw_info()

        text = StripText(draw_info)
        rect = text.patch

        self.figure.add_artist(text)

        if draw_info.position == "right":
            targets.strip_background_y.append(rect)
            targets.strip_text_y.append(text)
        else:
            targets.strip_background_x.append(rect)
            targets.strip_text_x.append(text)


class Strips(List[strip]):
    """
    List of strips for a plot
    """

    facet: facet

    @staticmethod
    def from_facet(facet: facet) -> Strips:
        new = Strips()
        new.facet = facet
        new.setup()
        return new

    @property
    def axs(self) -> list[Axes]:
        return self.facet.axs

    @property
    def layout(self) -> Layout:
        return self.facet.layout

    @property
    def theme(self) -> theme:
        return self.facet.theme

    @property
    def top_strips(self) -> Strips:
        return Strips([s for s in self if s.position == "top"])

    @property
    def right_strips(self) -> Strips:
        return Strips([s for s in self if s.position == "right"])

    def draw(self):
        for s in self:
            s.draw()

    def setup(self) -> Self:
        """
        Calculate the box information for all strips

        It is stored in self.strip_info
        """
        for layout_info in self.layout.get_details():
            ax = self.axs[layout_info.panel_index]
            lst = self.facet.make_strips(layout_info, ax)
            self.extend(lst)
        return self
</file>

<file path="plotnine/geoms/__init__.py">
"""
Plotting objects
"""

from .annotate import annotate
from .annotation_logticks import annotation_logticks
from .annotation_stripes import annotation_stripes
from .geom_abline import geom_abline
from .geom_area import geom_area
from .geom_bar import geom_bar
from .geom_bin_2d import geom_bin2d, geom_bin_2d
from .geom_blank import geom_blank
from .geom_boxplot import geom_boxplot
from .geom_col import geom_col
from .geom_count import geom_count
from .geom_crossbar import geom_crossbar
from .geom_density import geom_density
from .geom_density_2d import geom_density_2d
from .geom_dotplot import geom_dotplot
from .geom_errorbar import geom_errorbar
from .geom_errorbarh import geom_errorbarh
from .geom_freqpoly import geom_freqpoly
from .geom_histogram import geom_histogram
from .geom_hline import geom_hline
from .geom_jitter import geom_jitter
from .geom_label import geom_label
from .geom_line import geom_line
from .geom_linerange import geom_linerange
from .geom_map import geom_map
from .geom_path import arrow, geom_path
from .geom_point import geom_point
from .geom_pointdensity import geom_pointdensity
from .geom_pointrange import geom_pointrange
from .geom_polygon import geom_polygon
from .geom_qq import geom_qq
from .geom_qq_line import geom_qq_line
from .geom_quantile import geom_quantile
from .geom_raster import geom_raster
from .geom_rect import geom_rect
from .geom_ribbon import geom_ribbon
from .geom_rug import geom_rug
from .geom_segment import geom_segment
from .geom_sina import geom_sina
from .geom_smooth import geom_smooth
from .geom_spoke import geom_spoke
from .geom_step import geom_step
from .geom_text import geom_text
from .geom_tile import geom_tile
from .geom_violin import geom_violin
from .geom_vline import geom_vline

__all__ = (
    "annotate",
    "annotation_logticks",
    "annotation_stripes",
    "geom_abline",
    "geom_area",
    "geom_bar",
    "geom_bin_2d",
    "geom_bin2d",
    "geom_blank",
    "geom_boxplot",
    "geom_col",
    "geom_count",
    "geom_crossbar",
    "geom_density",
    "geom_density_2d",
    "geom_dotplot",
    "geom_errorbar",
    "geom_errorbarh",
    "geom_freqpoly",
    "geom_histogram",
    "geom_hline",
    "geom_jitter",
    "geom_label",
    "geom_line",
    "geom_linerange",
    "geom_map",
    "arrow",
    "geom_path",
    "geom_point",
    "geom_pointdensity",
    "geom_pointrange",
    "geom_quantile",
    "geom_qq",
    "geom_qq_line",
    "geom_polygon",
    "geom_raster",
    "geom_rect",
    "geom_ribbon",
    "geom_rug",
    "geom_segment",
    "geom_sina",
    "geom_smooth",
    "geom_spoke",
    "geom_step",
    "geom_text",
    "geom_tile",
    "geom_violin",
    "geom_vline",
)
</file>

<file path="plotnine/geoms/geom_line.py">
from __future__ import annotations

import typing

from ..doctools import document
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_line(geom_path):
    """
    Connected points

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_path : For documentation of other parameters.
    """

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.sort_values(["PANEL", "group", "x"])
</file>

<file path="plotnine/positions/__init__.py">
"""
Position Adjustments
"""

from .position_dodge import position_dodge
from .position_dodge2 import position_dodge2
from .position_fill import position_fill
from .position_identity import position_identity
from .position_jitter import position_jitter
from .position_jitterdodge import position_jitterdodge
from .position_nudge import position_nudge
from .position_stack import position_stack

__all__ = (
    "position_dodge",
    "position_dodge2",
    "position_fill",
    "position_identity",
    "position_jitter",
    "position_jitterdodge",
    "position_nudge",
    "position_stack",
)
</file>

<file path="plotnine/positions/position_dodge.py">
from __future__ import annotations

import typing
from contextlib import suppress
from copy import copy

import numpy as np
import pandas as pd

from .._utils import groupby_apply, match
from ..exceptions import PlotnineError
from .position import position

if typing.TYPE_CHECKING:
    from typing import Literal, Optional


class position_dodge(position):
    """
    Dodge overlaps and place objects side-by-side

    Parameters
    ----------
    width :
        Dodging width, when different to the width of the
        individual elements. This is useful when you want
        to align narrow geoms with wider geoms
    preserve :
        Should dodging preserve the total width of all elements
        at a position, or the width of a single element?
    """

    REQUIRED_AES = {"x"}

    def __init__(
        self,
        width: Optional[float] = None,
        preserve: Literal["total", "single"] = "total",
    ):
        self.params = {
            "width": width,
            "preserve": preserve,
        }

    def setup_data(self, data, params):
        # # e.g. geom_segment should be dodgeable
        if "x" in data and "xend" in data:
            if "xmin" not in data:
                data["xmin"] = data.pop("x")
            if "xmax" not in data:
                data["xmax"] = data["xend"]

        if "x" not in data and "xmin" in data and "xmax" in data:
            data["x"] = (data["xmin"] + data["xmax"]) / 2

        return super().setup_data(data, params)

    def setup_params(self, data):
        if (
            ("xmin" not in data)
            and ("xmax" not in data)
            and (self.params["width"] is None)
        ):
            msg = "Width not defined. Set with `position_dodge(width = ?)`"
            raise PlotnineError(msg)

        params = copy(self.params)

        if params["preserve"] == "total":
            params["n"] = None
        else:
            # Count at the xmin values per panel and find the highest
            # overall count
            def max_xmin_values(gdf):
                try:
                    n = gdf["xmin"].value_counts().max()
                except KeyError:
                    n = gdf["x"].value_counts().max()
                return pd.DataFrame({"n": [n]})

            res = groupby_apply(data, "PANEL", max_xmin_values)
            params["n"] = res["n"].max()
        return params

    @classmethod
    def compute_panel(cls, data, scales, params):
        return cls.collide(data, params=params)

    @staticmethod
    def strategy(data, params):
        """
        Dodge overlapping interval

        Assumes that each set has the same horizontal position.
        """
        width = params["width"]
        with suppress(TypeError):
            iter(width)
            width = np.asarray(width)
            width = width[data.index]

        udata_group = data["group"].drop_duplicates()

        n = params.get("n", None)
        if n is None:
            n = len(udata_group)
        if n == 1:
            return data

        if not all(col in data.columns for col in ["xmin", "xmax"]):
            data["xmin"] = data["x"]
            data["xmax"] = data["x"]

        d_width = np.max(data["xmax"] - data["xmin"])

        # Have a new group index from 1 to number of groups.
        # This might be needed if the group numbers in this set don't
        # include all of 1:n
        udata_group = udata_group.sort_values()
        groupidx = match(data["group"], udata_group)
        groupidx = np.asarray(groupidx) + 1

        # Find the center for each group, then use that to
        # calculate xmin and xmax
        data["x"] = data["x"] + width * ((groupidx - 0.5) / n - 0.5)
        data["xmin"] = data["x"] - (d_width / n) / 2
        data["xmax"] = data["x"] + (d_width / n) / 2

        if "x" in data and "xend" in data:
            data["x"] = data["xmin"]
            data["xend"] = data["xmax"]

        return data
</file>

<file path="plotnine/positions/position_dodge2.py">
from __future__ import annotations

import typing
from copy import copy

import numpy as np
import pandas as pd

from .._utils import groupby_apply, pivot_apply
from ..exceptions import PlotnineError
from .position_dodge import position_dodge

if typing.TYPE_CHECKING:
    from typing import Literal, Optional

    from plotnine.typing import IntArray


class position_dodge2(position_dodge):
    """
    Dodge overlaps and place objects side-by-side

    This is an enhanced version of
    [](`~plotnine.positions.position_dodge`) that can deal
    with rectangular overlaps that do not share a lower x border.

    Parameters
    ----------
    width :
        Dodging width, when different to the width of the
        individual elements. This is useful when you want
        to align narrow geoms with wider geoms
    preserve :
        Should dodging preserve the total width of all elements
        at a position, or the width of a single element?
    padding :
        Padding between elements at the same position.
        Elements are shrunk by this proportion to allow space
        between them.
    reverse :
        Reverse the default ordering of the groups. This is
        useful if you're rotating both the plot and legend.
    """

    REQUIRED_AES = {"x"}

    def __init__(
        self,
        width: Optional[float] = None,
        preserve: Literal["total", "single"] = "total",
        padding: float = 0.1,
        reverse: bool = False,
    ):
        self.params = {
            "width": width,
            "preserve": preserve,
            "padding": padding,
            "reverse": reverse,
        }

    def setup_params(self, data):
        if (
            ("xmin" not in data)
            and ("xmax" not in data)
            and (self.params["width"] is None)
        ):
            msg = "Width not defined. Set with `position_dodge2(width = ?)`"
            raise PlotnineError(msg)

        params = copy(self.params)

        if params["preserve"] == "total":
            params["n"] = None
        elif "x" in data:

            def max_x_values(gdf):
                n = gdf["x"].value_counts().max()
                return pd.DataFrame({"n": [n]})

            res = groupby_apply(data, "PANEL", max_x_values)
            params["n"] = res["n"].max()
        else:

            def _find_x_overlaps(gdf):
                return pd.DataFrame({"n": find_x_overlaps(gdf)})

            # interval geoms
            res = groupby_apply(data, "PANEL", _find_x_overlaps)
            params["n"] = res["n"].max()
        return params

    @classmethod
    def compute_panel(cls, data, scales, params):
        return cls.collide2(data, params=params)

    @staticmethod
    def strategy(data, params):
        padding = params["padding"]
        n = params["n"]

        if not all(col in data.columns for col in ["xmin", "xmax"]):
            data["xmin"] = data["x"]
            data["xmax"] = data["x"]

        # Groups of boxes that share the same position
        data["xid"] = find_x_overlaps(data)

        # Find newx using xid, i.e. the center of each group of
        # overlapping elements. for boxes, bars, etc. this should
        # be the same as original x, but for arbitrary rects it
        # may not be
        res1 = pivot_apply(data, "xmin", "xid", np.min)
        res2 = pivot_apply(data, "xmax", "xid", np.max)
        data["newx"] = (res1 + res2)[data["xid"].to_numpy()].to_numpy() / 2

        if n is None:
            # If n is None, preserve total widths of elements at
            # each position by dividing widths by the number of
            # elements at that position
            n = data["xid"].value_counts(sort=False).to_numpy()
            n = n[data.loc[:, "xid"] - 1]
            data["new_width"] = (data["xmax"] - data["xmin"]) / n
        else:
            data["new_width"] = (data["xmax"] - data["xmin"]) / n

        # Find the total width of each group of elements
        def sum_new_width(gdf):
            return pd.DataFrame(
                {
                    "size": [gdf["new_width"].sum()],
                    "newx": gdf["newx"].iloc[0],
                }
            )

        group_sizes = groupby_apply(data, "newx", sum_new_width)

        # Starting xmin for each group of elements
        starts = group_sizes["newx"] - (group_sizes["size"] / 2)

        # Set the elements in place
        for i, start in enumerate(starts, start=1):
            bool_idx = data["xid"] == i
            divisions = np.cumsum(
                np.hstack([start, data.loc[bool_idx, "new_width"]])
            )
            data.loc[bool_idx, "xmin"] = divisions[:-1]
            data.loc[bool_idx, "xmax"] = divisions[1:]

        # x values get moved to between xmin and xmax
        data["x"] = (data["xmin"] + data["xmax"]) / 2

        # Shrink elements to add space between them
        if data["xid"].duplicated().any():
            pad_width = data["new_width"] * (1 - padding)
            data["xmin"] = data["x"] - pad_width / 2
            data["xmax"] = data["x"] + pad_width / 2

        if "x" in data and "xend" in data:
            data["x"] = data["xmin"]
            data["xend"] = data["xmax"]

        data = data.drop(columns=["xid", "newx", "new_width"], errors="ignore")
        return data


def find_x_overlaps(df: pd.DataFrame) -> IntArray:
    """
    Find overlapping regions along the x axis
    """
    n = len(df)
    overlaps = np.zeros(n, dtype=int)
    overlaps[0] = 1
    counter = 1
    for i in range(1, n):
        if df["xmin"].iloc[i] >= df["xmax"].iloc[i - 1]:
            counter += 1
        overlaps[i] = counter
    return overlaps
</file>

<file path="plotnine/positions/position_fill.py">
from .position_stack import position_stack


class position_fill(position_stack):
    """
    Normalise stacked objects to unit height
    """

    fill = True
</file>

<file path="plotnine/positions/position_identity.py">
from .position import position


class position_identity(position):
    """
    Do not adjust the position
    """

    @classmethod
    def compute_layer(cls, data, params, layout):
        return data
</file>

<file path="plotnine/positions/position_jitter.py">
from __future__ import annotations

import typing
from copy import deepcopy

import numpy as np

from .._utils import jitter, resolution
from .position import position

if typing.TYPE_CHECKING:
    from typing import Optional

    from plotnine.typing import FloatArray, FloatArrayLike


class position_jitter(position):
    """
    Jitter points to avoid overplotting

    Parameters
    ----------
    width :
        Proportion to jitter in horizontal direction.
        If `None`, `0.4` of the resolution of the data.
    height :
        Proportion to jitter in vertical direction.
        If `None`, `0.4` of the resolution of the data.
    random_state :
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    """

    REQUIRED_AES = {"x", "y"}

    def __init__(
        self,
        width: Optional[float] = None,
        height: Optional[float] = None,
        random_state: Optional[int | np.random.RandomState] = None,
    ):
        self.params = {
            "width": width,
            "height": height,
            "random_state": random_state,
        }

    def setup_params(self, data):
        params = deepcopy(self.params)
        if params["width"] is None:
            params["width"] = resolution(data["x"]) * 0.4
        if params["height"] is None:
            params["height"] = resolution(data["y"]) * 0.4
        if not params["random_state"]:
            params["random_state"] = np.random
        return params

    @classmethod
    def compute_layer(cls, data, params, layout):
        trans_x = None  # pyright: ignore
        trans_y = None  # pyright: ignore

        if params["width"]:

            def trans_x(x: FloatArrayLike) -> FloatArray:
                return jitter(
                    x,
                    amount=params["width"],
                    random_state=params["random_state"],
                )

        if params["height"]:

            def trans_y(y):
                return jitter(
                    y,
                    amount=params["height"],
                    random_state=params["random_state"],
                )

        return cls.transform_position(data, trans_x, trans_y)
</file>

<file path="plotnine/positions/position_jitterdodge.py">
from __future__ import annotations

import typing
from contextlib import suppress
from copy import copy

from .._utils import jitter, resolution
from ..exceptions import PlotnineError
from ..mapping.aes import SCALED_AESTHETICS
from .position import position
from .position_dodge import position_dodge

if typing.TYPE_CHECKING:
    from typing import Optional

    import numpy as np


# Adjust position by simultaneously dodging and jittering
class position_jitterdodge(position):
    """
    Dodge and jitter to minimise overlap

    Useful when aligning points generated through
    [](`~plotnine.geoms.geom_point`) with dodged a
    [](`~plotnine.geoms.geom_boxplot`).

    Parameters
    ----------
    jitter_width :
        Proportion to jitter in horizontal direction.
        If `None`, `0.4` of the resolution of the data.
    jitter_height :
        Proportion to jitter in vertical direction.
    dodge_width :
        Amount to dodge in horizontal direction.
    random_state :
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    """

    REQUIRED_AES = {"x", "y"}
    strategy = staticmethod(position_dodge.strategy)

    def __init__(
        self,
        jitter_width: Optional[float] = None,
        jitter_height: float = 0,
        dodge_width: float = 0.75,
        random_state: Optional[int | np.random.RandomState] = None,
    ):
        self.params = {
            "jitter_width": jitter_width,
            "jitter_height": jitter_height,
            "dodge_width": dodge_width,
            "random_state": random_state,
        }

    def setup_params(self, data):
        params = copy(self.params)
        width = params["jitter_width"]
        if width is None:
            width = resolution(data["x"]) * 0.4

        # Adjust the x transformation based on the number
        # of dodge variables
        dvars = SCALED_AESTHETICS - self.REQUIRED_AES
        dodge_columns = data.columns.intersection(list(dvars))
        if len(dodge_columns) == 0:
            raise PlotnineError(
                "'position_jitterdodge' requires at least one "
                "aesthetic to dodge by."
            )

        s = set()
        for col in dodge_columns:
            with suppress(AttributeError):
                s.update(data[col].cat.categories)
        ndodge = len(s)

        params["jitter_width"] = width / (ndodge + 2)
        params["width"] = params["dodge_width"]
        return params

    @classmethod
    def compute_panel(cls, data, scales, params):
        trans_x = None  # pyright: ignore
        trans_y = None  # pyright: ignore

        if params["jitter_width"] > 0:

            def trans_x(x):
                return jitter(
                    x,
                    amount=params["jitter_width"],
                    random_state=params["random_state"],
                )

        if params["jitter_height"] > 0:

            def trans_y(y):
                return jitter(
                    y,
                    amount=params["jitter_height"],
                    random_state=params["random_state"],
                )

        # dodge, then jitter
        data = cls.collide(data, params=params)
        data = cls.transform_position(data, trans_x, trans_y)
        return data
</file>

<file path="plotnine/positions/position_nudge.py">
from __future__ import annotations

import typing

from .position import position

if typing.TYPE_CHECKING:
    from plotnine.typing import FloatArray, FloatArrayLike


class position_nudge(position):
    """
    Nudge points

    Useful to nudge labels away from the points
    being labels.

    Parameters
    ----------
    x :
        Horizontal nudge
    y :
        Vertical nudge
    """

    def __init__(self, x: float = 0, y: float = 0):
        self.params = {"x": x, "y": y}

    @classmethod
    def compute_layer(cls, data, params, layout):
        trans_x = None  # pyright: ignore
        trans_y = None  # pyright: ignore

        if params["x"]:

            def trans_x(x: FloatArrayLike) -> FloatArray:
                return x + params["x"]

        if params["y"]:

            def trans_y(y: FloatArrayLike) -> FloatArray:
                return y + params["y"]

        return cls.transform_position(data, trans_x, trans_y)
</file>

<file path="plotnine/positions/position_stack.py">
from __future__ import annotations

from warnings import warn

import numpy as np
import pandas as pd

from .._utils import remove_missing
from ..exceptions import PlotnineWarning
from .position import position


class position_stack(position):
    """
    Stack plotted objects on top of each other

    The objects to stack are those that have
    an overlapping x range.

    Parameters
    ----------
    vjust :
        By what fraction to avoid overlapping the lower object,
        where `0` gives a complete overlap and `1` gives no overlap.
    reverse :
        Reverse the order of the stacked groups if true.
    """

    fill = False

    def __init__(self, vjust: float = 1, reverse: bool = False):
        self.params = {"vjust": vjust, "reverse": reverse}

    def setup_params(self, data):
        """
        Verify, modify & return a copy of the params.
        """
        # Variable for which to do the stacking
        if "ymax" in data:
            if any((data["ymin"] != 0) & (data["ymax"] != 0)):
                warn(
                    "Stacking not well defined when not anchored on the axis.",
                    PlotnineWarning,
                )
            var = "ymax"
        elif "y" in data:
            var = "y"
        else:
            warn(
                "Stacking requires either ymin & ymax or y "
                "aesthetics. Maybe you want position = 'identity'?",
                PlotnineWarning,
            )
            var = None

        params = self.params.copy()
        params["var"] = var
        params["fill"] = self.fill
        return params

    def setup_data(self, data, params):
        if not params["var"]:
            return data

        if params["var"] == "y":
            data["ymax"] = data["y"]
        elif params["var"] == "ymax":
            bool_idx = data["ymax"] == 0
            data.loc[bool_idx, "ymax"] = data.loc[bool_idx, "ymin"]

        data = remove_missing(
            data, vars=("x", "xmin", "xmax", "y"), name="position_stack"
        )

        return data

    @classmethod
    def compute_panel(cls, data, scales, params):
        if not params["var"]:
            return data

        # Positioning happens after scale has transformed the data,
        # and stacking only works well for linear data.
        # If the scale(transformation) is not linear, we undo it,
        # do the "stacking" and redo the transformation.
        from ..scales.scale_continuous import scale_continuous

        if isinstance(scales.y, scale_continuous):
            undo_transform = (
                not scales.y.is_linear_scale and scales.y.domain_is_numerical
            )
        else:
            undo_transform = False

        if undo_transform:
            data = cls.transform_position(data, trans_y=scales.y.inverse)

        negative = data["ymax"] < 0
        neg = data.loc[negative]
        pos = data.loc[~negative]

        if len(neg):
            neg = cls.collide(neg, params=params)

        if len(pos):
            pos = cls.collide(pos, params=params)

        data = pd.concat([neg, pos], axis=0, ignore_index=True, sort=True)

        if undo_transform:
            data = cls.transform_position(data, trans_y=scales.y.transform)

        return data

    @staticmethod
    def strategy(data, params):
        """
        Stack overlapping intervals.

        Assumes that each set has the same horizontal position
        """
        vjust = params["vjust"]

        y = data["y"].copy()
        y[np.isnan(y)] = 0
        heights = np.append(0, y.cumsum())

        if params["fill"]:
            heights = heights / np.abs(heights[-1])

        data["ymin"] = np.min([heights[:-1], heights[1:]], axis=0)
        data["ymax"] = np.max([heights[:-1], heights[1:]], axis=0)
        # less intuitive than (ymin + vjust(ymax-ymin)), but
        # this way avoids subtracting numbers of potentially
        # similar precision
        data["y"] = (1 - vjust) * data["ymin"] + vjust * data["ymax"]
        return data
</file>

<file path="plotnine/scales/_expand.py">
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from mizani.bounds import expand_range_distinct

from .._utils import ignore_warnings
from ..iapi import range_view

if TYPE_CHECKING:
    from mizani.transforms import trans

    from plotnine.typing import CoordRange


def _expand_range_distinct(
    x: tuple[float, float],
    expand: tuple[float, float] | tuple[float, float, float, float],
) -> tuple[float, float]:
    # Expand ascending and descending order range
    a, b = x
    if a > b:
        b, a = expand_range_distinct((b, a), expand)
    else:
        a, b = expand_range_distinct((a, b), expand)
    return (a, b)


def expand_range(
    x: CoordRange,
    expand: tuple[float, float] | tuple[float, float, float, float],
    trans: trans,
) -> range_view:
    """
    Expand Coordinate Range in coordinate space

    Parameters
    ----------
    x:
        (max, min) in data scale
    expand:
        How to expand
    trans:
        Coordinate transformation
    """
    x_coord_space = tuple(trans.transform(x))
    x_coord = _expand_range_distinct(x_coord_space, expand)  # type: ignore

    with ignore_warnings(RuntimeWarning):
        # Consequences of the runtimewarning (NaNs and infs)
        # are dealt with below
        final_x = trans.inverse(x_coord)

    l0, l1 = x
    f0, f1 = final_x
    final_range = (
        f0 if np.isfinite(f0) else l0,
        f1 if np.isfinite(f1) else l1,
    )

    ranges = range_view(range=final_range, range_coord=x_coord)
    return ranges
</file>

<file path="plotnine/scales/_runtime_typing.py">
"""
This module contains type aliases needed in plotnine.scales.* at runtime.
For example as annotations when declaring dataclasses. They are separated
out so that we can refer to them as plotnine.scales._runtime_typing for
the documentation.
"""

from typing import Callable, Sequence, Type, TypeAlias, TypeVar

from mizani.transforms import trans

from .range import Range

# fmt: off

DiscreteBreaksUser: TypeAlias = (
    bool
    | None
    | Sequence[str]
    | Callable[[Sequence[str]], Sequence[str]]
)

DiscreteLimitsUser: TypeAlias = (
    None
    | Sequence[str]
    | Callable[[Sequence[str]], Sequence[str]]
)

ContinuousBreaksUser: TypeAlias = (
    bool
    | None
    | Sequence[float]
    | Callable[[tuple[float, float]], Sequence[float]]
)

MinorBreaksUser: TypeAlias = ContinuousBreaksUser

ContinuousLimitsUser: TypeAlias = (
    None
    | tuple[float, float]
    | Callable[[tuple[float, float]], tuple[float, float]]
)

ScaleLabelsUser: TypeAlias = (
    bool
    | None
    | Sequence[str]
    | Callable[[Sequence[float] | Sequence[str]], Sequence[str]]
    | dict[str, str]
)

TransUser: TypeAlias = trans | str | Type[trans] | None

RangeT = TypeVar("RangeT", bound=Range)
BreaksUserT = TypeVar("BreaksUserT")
LimitsUserT = TypeVar("LimitsUserT")
GuideTypeT = TypeVar("GuideTypeT")
</file>

<file path="plotnine/scales/limits.py">
import sys
from contextlib import suppress

import pandas as pd

from .._utils import array_kind
from ..exceptions import PlotnineError
from ..geoms import geom_blank
from ..mapping.aes import ALL_AESTHETICS, aes
from ..scales.scales import make_scale


# By adding limits, we create a scale of the appropriate type
class _lim:
    aesthetic = None

    def __init__(self, *limits):
        if not limits:
            msg = "{}lim(), is missing limits"
            raise PlotnineError(msg.format(self.aesthetic))
        elif len(limits) == 1:
            limits = limits[0]

        series = pd.Series(limits)

        # Type of transform
        if not any(x is None for x in limits) and limits[0] > limits[1]:
            self.trans = "reverse"
        elif array_kind.continuous(series):
            self.trans = "identity"
        elif array_kind.discrete(series):
            self.trans = None
        elif array_kind.datetime(series):
            self.trans = "datetime"
        elif array_kind.timedelta(series):
            self.trans = "timedelta"
        else:
            msg = f"Unknown type {type(limits[0])} of limits"
            raise TypeError(msg)

        self.limits = limits
        self.limits_series = series

    def get_scale(self, plot):
        """
        Create a scale
        """
        # This method does some introspection to save users from
        # scale mismatch error. This could happen when the
        # aesthetic is mapped to a categorical but the limits
        # are not provided in categorical form. We only handle
        # the case where the mapping uses an expression to
        # convert to categorical e.g `aes(color="factor(cyl)")`.
        # However if `"cyl"` column is a categorical and the
        # mapping is `aes(color="cyl")`, that will result in
        # an error. If later case proves common enough then we
        # could inspect the data and be clever based on that too!!
        ae = self.aesthetic
        series = self.limits_series
        ae_values = []

        # Look through all the mappings for this aesthetic,
        # if we detect any factor stuff then we convert the
        # limits data to categorical so that the right scale
        # can be chosen. This should take care of the most
        # common use cases.
        for layer in plot.layers:
            with suppress(KeyError):
                value = layer.mapping[ae]
                if isinstance(value, str):
                    ae_values.append(value)

        for value in ae_values:
            if "factor(" in value or "Categorical(" in value:
                series = pd.Categorical(self.limits_series)
                break
        return make_scale(
            self.aesthetic, series, limits=self.limits, trans=self.trans
        )

    def __radd__(self, other):
        scale = self.get_scale(other)
        other.scales.append(scale)
        return other


class xlim(_lim):
    """
    Set x-axis limits

    Parameters
    ----------
    *limits :
        Min and max limits. Must be of size 2.
        You can also pass two values e.g
        `xlim(40, 100)`
    """

    aesthetic = "x"


class ylim(_lim):
    """
    Set y-axis limits

    Parameters
    ----------
    *limits :
        Min and max limits. Must be of size 2.
        You can also pass two values e.g
        `ylim(40, 100)`

    Notes
    -----
    If the 2nd value of `limits` is less than
    the first, a reversed scale will be created.
    """

    aesthetic = "y"


class alphalim(_lim):
    """
    Alpha limits
    """

    aesthetic = "alpha"


class colorlim(_lim):
    """
    Color limits
    """

    aesthetic = "color"


class filllim(_lim):
    """
    Fill limits
    """

    aesthetic = "fill"


class linetypelim(_lim):
    """
    Linetype limits
    """

    aesthetic = "linetype"


class shapelim(_lim):
    """
    Shapee limits
    """

    aesthetic = "shape"


class sizelim(_lim):
    """
    Size limits
    """

    aesthetic = "size"


class strokelim(_lim):
    """
    Stroke limits
    """

    aesthetic = "stroke"


class lims:
    """
    Set aesthetic limits

    Parameters
    ----------
    kwargs :
        Aesthetic and the values of the limits.
        e.g `x=(40, 100)`

    Notes
    -----
    If the 2nd value of `limits` is less than
    the first, a reversed scale will be created.
    """

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __radd__(self, other):
        """
        Add limits to ggplot object
        """
        thismodule = sys.modules[__name__]
        for ae, value in self._kwargs.items():
            try:
                klass = getattr(thismodule, f"{ae}lim")
            except AttributeError as e:
                msg = "Cannot change limits for '{}'"
                raise PlotnineError(msg) from e

            other += klass(value)

        return other


def expand_limits(**kwargs):
    """
    Expand the limits any aesthetic using data

    Parameters
    ----------
    kwargs : dict | dataframe
        Data to use in expanding the limits.
        The keys should be aesthetic names
        e.g. *x*, *y*, *colour*, ...
    """

    def as_list(key):
        with suppress(KeyError):
            if isinstance(kwargs[key], (int, float, str)):
                kwargs[key] = [kwargs[key]]

    if isinstance(kwargs, dict):
        as_list("x")
        as_list("y")
        data = pd.DataFrame(kwargs)
    else:
        data = kwargs

    mapping = aes()
    for ae in set(kwargs) & ALL_AESTHETICS:
        mapping[ae] = ae

    return geom_blank(data=data, mapping=mapping, inherit_aes=False)
</file>

<file path="plotnine/scales/range.py">
from __future__ import annotations

import typing

from mizani.scale import scale_continuous, scale_discrete

if typing.TYPE_CHECKING:
    from typing import Any, Sequence

    from plotnine.typing import AnyArrayLike, FloatArrayLike


class Range:
    """
    Base class for all ranges
    """

    # Holds the range information after training
    range: Any

    def reset(self):
        """
        Reset range
        """
        del self.range

    def train(self, x: Sequence[Any]):
        """
        Train range
        """
        raise NotImplementedError("Not Implemented.")

    def is_empty(self) -> bool:
        """
        Whether there is range information
        """
        return not hasattr(self, "range")


class RangeContinuous(Range):
    """
    Continuous Range
    """

    range: tuple[float, float]

    def train(self, x: FloatArrayLike):
        """
        Train continuous range
        """
        rng = None if self.is_empty() else self.range
        self.range = scale_continuous.train(x, rng)


class RangeDiscrete(Range):
    """
    Discrete Range
    """

    range: Sequence[Any]

    def train(self, x: AnyArrayLike, drop: bool = False, na_rm: bool = False):
        """
        Train discrete range
        """
        rng = None if self.is_empty() else self.range
        self.range = scale_discrete.train(x, rng, drop, na_rm=na_rm)
</file>

<file path="plotnine/scales/scale_alpha.py">
from dataclasses import KW_ONLY, InitVar, dataclass
from typing import Literal
from warnings import warn

import numpy as np

from .._utils.registry import alias
from ..exceptions import PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_datetime import scale_datetime
from .scale_discrete import scale_discrete


@dataclass
class scale_alpha(scale_continuous[Literal["legend"]]):
    """
    Continuous Alpha Scale
    """

    _aesthetics = ["alpha"]
    range: InitVar[tuple[float, float]] = (0.1, 1)
    """
    Range ([Minimum, Maximum]) of output alpha values.
    Should be between 0 and 1.
    """

    _: KW_ONLY
    guide: Literal["legend"] = "legend"

    def __post_init__(self, range):
        from mizani.palettes import rescale_pal

        super().__post_init__()
        self.palette = rescale_pal(range)


@alias
class scale_alpha_continuous(scale_alpha):
    pass


@dataclass
class scale_alpha_ordinal(scale_discrete):
    """
    Ordinal Alpha Scale
    """

    _aesthetics = ["alpha"]
    range: InitVar[tuple[float, float]] = (0.1, 1)
    """
    Range ([Minimum, Maximum]) of output alpha values.
    Should be between 0 and 1.
    """

    def __post_init__(self, range):
        super().__post_init__()

        def palette(n):
            return np.linspace(range[0], range[1], n)

        self.palette = palette


@dataclass
class scale_alpha_discrete(scale_alpha_ordinal):
    """
    Discrete Alpha Scale
    """

    def __post_init__(self, range):
        warn(
            "Using alpha for a discrete variable is not advised.",
            PlotnineWarning,
        )
        super().__post_init__(range)


@dataclass
class scale_alpha_datetime(scale_datetime):
    """
    Datetime Alpha Scale
    """

    _aesthetics = ["alpha"]
    range: InitVar[tuple[float, float]] = (0.1, 1)
    """
    Range ([Minimum, Maximum]) of output alpha values.
    Should be between 0 and 1.
    """

    _: KW_ONLY
    guide: Literal["legend"] = "legend"

    def __post_init__(
        self,
        date_breaks: str | None,
        date_labels: str | None,
        date_minor_breaks: str | None,
        range: tuple[float, float],
    ):
        from mizani.palettes import rescale_pal

        self.palette = rescale_pal(range)
        super().__post_init__(date_breaks, date_labels, date_minor_breaks)
</file>

<file path="plotnine/scales/scale_continuous.py">
from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence, cast
from warnings import warn

import numpy as np
import pandas as pd
from mizani.bounds import censor, expand_range_distinct, rescale, zero_range
from mizani.palettes import identity_pal

from .._utils import match
from ..exceptions import PlotnineError, PlotnineWarning
from ..iapi import range_view, scale_view
from ._expand import expand_range
from ._runtime_typing import (
    ContinuousBreaksUser,
    ContinuousLimitsUser,
    GuideTypeT,
    MinorBreaksUser,
    TransUser,
)
from .range import RangeContinuous
from .scale import scale

if TYPE_CHECKING:
    from typing import Optional

    from mizani.transforms import trans
    from mizani.typing import PCensor, PRescale

    from plotnine.typing import (
        CoordRange,
        FloatArrayLike,
        TFloatArrayLike,
    )


@dataclass(kw_only=True)
class scale_continuous(
    scale[
        RangeContinuous,
        ContinuousBreaksUser,
        ContinuousLimitsUser,
        # subclasses are still generic and must specify the
        # type of the guide
        GuideTypeT,
    ]
):
    """
    Base class for all continuous scales

    Notes
    -----
    If using the class directly all arguments must be
    keyword arguments.
    """

    limits: ContinuousLimitsUser = None
    """
    Limits of the scale. Most commonly, these are the minimum & maximum
    values for the scale. If not specified they are derived from the data.
    It may also be a function that takes the derived limits and transforms
    them into the final limits.
    """

    rescaler: PRescale = rescale
    """
    Function to rescale data points so that they can be handled by the
    palette. Default is to rescale them onto the [0, 1] range. Scales
    that inherit from this class may have another default.
    """

    oob: PCensor = censor
    """
    Function to deal with out of bounds (limits) data points. Default
    is to turn them into `np.nan`, which then get dropped.
    """

    breaks: ContinuousBreaksUser = True
    """
    Major breaks
    """

    minor_breaks: MinorBreaksUser = True
    """
    If a list-like, it is the minor breaks points. If an integer, it is the
    number of minor breaks between any set of major breaks.
    If a function, it should have the signature `func(limits)` and return a
    list-like of consisting of the minor break points.
    If `None`, no minor breaks are calculated. The default is to automatically
    calculate them.
    """

    trans: TransUser = None
    """
    The transformation of the scale. Either name of a trans function or
    a trans function. See [](`mizani.transforms`) for possible options.
    """

    def __post_init__(self):
        super().__post_init__()
        self._range = RangeContinuous()
        self._trans = self._make_trans()
        self.limits = self._prep_limits(self.limits)

    def _prep_limits(
        self, value: ContinuousLimitsUser
    ) -> ContinuousLimitsUser:
        """
        Limits for the continuous scale

        Parameters
        ----------
        value : array_like | callable
            Limits in the dataspace.
        """
        # Notes
        # -----
        # The limits are given in original dataspace
        # but they are stored in transformed space since
        # all computations happen on transformed data. The
        # labeling of the plot axis and the guides are in
        # the original dataspace.
        if isinstance(value, bool) or value is None or callable(value):
            return value

        a, b = value
        a = self.transform([a])[0] if a is not None else a
        b = self.transform([b])[0] if b is not None else b

        if a is not None and b is not None and a > b:
            a, b = b, a

        return a, b

    def _make_trans(self) -> trans:
        """
        Return a valid transform object

        When scales specialise on a specific transform (other than
        the identity transform), the user should know when they
        try to change the transform.

        Parameters
        ----------
        t : mizani.transforms.trans
            Transform object
        """
        from mizani.transforms import gettrans

        t = gettrans(self.trans if self.trans else self.__class__.trans)

        orig_trans_name = self.__class__.trans
        new_trans_name = t.__class__.__name__
        if new_trans_name.endswith("_trans"):
            new_trans_name = new_trans_name[:-6]

        if orig_trans_name not in {None, "identity", new_trans_name}:
            warn(
                "You have changed the transform of a specialised scale. "
                "The result may not be what you expect.\n"
                "Original transform: {}\n"
                "New transform: {}".format(orig_trans_name, new_trans_name),
                PlotnineWarning,
                stacklevel=1,
            )

        return t

    @property
    def final_limits(self) -> tuple[float, float]:
        if self.is_empty():
            return (0, 1)

        if self.limits is None:
            return self._range.range
        elif callable(self.limits):
            # Function works in the dataspace, but the limits are
            # stored in transformed space. The range of the scale is
            # in transformed space (i.e. with in the domain of the scale)
            _range = self.inverse(self._range.range)
            return self.transform(self.limits(_range))
        elif (
            self.limits is not None
            and not self._range.is_empty()
            and
            # Fall back to the range if the limits
            # are not set or if any is None or NaN
            len(self.limits) == len(self._range.range)
        ):
            l1, l2 = self.limits
            r1, r2 = self._range.range
            if l1 is None:
                l1 = self.transform([r1])[0]
            if l2 is None:
                l2 = self.transform([r2])[0]
            return l1, l2

        return self.limits

    def train(self, x: FloatArrayLike):
        """
        Train continuous scale
        """
        if not len(x):
            return

        self._range.train(x)

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform dataframe
        """
        if len(df) == 0:
            return df

        aesthetics = set(self.aesthetics) & set(df.columns)
        for ae in aesthetics:
            with suppress(TypeError):
                df[ae] = self.transform(df[ae])

        return df

    def transform(self, x: TFloatArrayLike) -> TFloatArrayLike:
        """
        Transform array|series x
        """
        return self._trans.transform(x)

    def inverse_df(self, df):
        """
        Inverse Transform dataframe
        """
        if len(df) == 0:
            return df

        aesthetics = set(self.aesthetics) & set(df.columns)
        for ae in aesthetics:
            with suppress(TypeError):
                df[ae] = self.inverse(df[ae])

        return df

    def inverse(self, x: TFloatArrayLike) -> TFloatArrayLike:
        """
        Inverse transform array|series x
        """
        return self._trans.inverse(x)

    @property
    def is_linear_scale(self) -> bool:
        """
        Return True if the scale is linear

        Depends on the transformation.
        """
        return self._trans.transform_is_linear

    @property
    def domain_is_numerical(self) -> bool:
        """
        Return True if transformation acts on numerical data.

        Depends on the transformation.
        """
        return self._trans.domain_is_numerical

    @property
    def is_log_scale(self) -> bool:
        """
        Return True if the scale is log transformationed
        """
        return hasattr(
            self._trans, "base"
        ) and self._trans.__class__.__name__.startswith("log")

    def dimension(self, expand=(0, 0, 0, 0), limits=None):
        """
        Get the phyical size of the scale

        Unlike limits, this always returns a numeric vector of length 2
        """
        if limits is None:
            limits = self.final_limits
        return expand_range_distinct(limits, expand)

    def expand_limits(
        self,
        limits: tuple[float, float],
        expand: tuple[float, float] | tuple[float, float, float, float],
        coord_limits: CoordRange | None,
        trans: trans,
    ) -> range_view:
        """
        Calculate the final range in coordinate space
        """
        # - Override None in coord_limits
        # - Expand limits in coordinate space
        # - Remove any computed infinite values &
        if coord_limits is not None:
            c0, c1 = coord_limits
            limits = (
                limits[0] if c0 is None else c0,
                limits[1] if c1 is None else c1,
            )
        return expand_range(limits, expand, trans)

    def view(
        self,
        limits: Optional[CoordRange] = None,
        range: Optional[CoordRange] = None,
    ) -> scale_view:
        """
        Information about the trained scale
        """
        if limits is None:
            limits = self.final_limits

        if range is None:
            range = self.dimension(limits=limits)

        breaks = self.get_bounded_breaks(range)
        labels = self.get_labels(breaks)

        ubreaks = self.get_breaks(range)
        minor_breaks = self.get_minor_breaks(ubreaks, range)

        sv = scale_view(
            scale=self,
            aesthetics=self.aesthetics,
            name=self.name,
            limits=limits,
            range=range,
            breaks=breaks,
            labels=labels,
            minor_breaks=minor_breaks,
        )
        return sv

    def default_expansion(self, mult=0.05, add=0, expand=True):
        """
        Get the default expansion for continuous scale
        """
        # Continuous scales have transforms, some of which may be on
        # domains that are not numeric, and the diffs on these domains
        # are not numeric as well. To do arithmetic (+/-) that uses diff
        # value, we need diff values represented as suitable numerical
        # values.
        if not expand:
            return (0, 0, 0, 0)

        def to_num(x) -> float:
            # For now this function assume that if the user passes in
            # a numeric value (for any kind for scale), they know what
            # they are doing. Usually this will be a 0.
            return (
                x
                if isinstance(x, (float, int))
                else self._trans.diff_type_to_num([x])[0]
            )

        if (exp := self.expand) is None:
            m1, m2 = mult if isinstance(mult, (tuple, list)) else (mult, mult)
            _add = add if isinstance(add, (tuple, list)) else (add, add)
            a1, a2 = to_num(_add[0]), to_num(_add[1])
            exp = (m1, a1, m2, a2)
        elif len(exp) == 2:
            exp = exp[0], to_num(exp[1])
            exp = (*exp, *exp)
        else:  # exp is a tuple with 4 elements
            exp = exp[0], to_num(exp[1]), exp[2], to_num(exp[3])

        return exp

    def palette(self, x):
        """
        Map an data values to values of the scale
        """
        return identity_pal()(x)

    def map(
        self, x: FloatArrayLike, limits: Optional[tuple[float, float]] = None
    ) -> FloatArrayLike:
        if limits is None:
            limits = self.final_limits

        x = self.oob(self.rescaler(x, _from=limits))
        na_value = cast("float", self.na_value)

        uniq = np.unique(x)
        pal = np.asarray(self.palette(uniq))
        scaled = pal[match(x, uniq)]
        if scaled.dtype.kind == "U":
            scaled = [na_value if x == "nan" else x for x in scaled]
        else:
            scaled[pd.isna(scaled)] = na_value
        return scaled

    def get_breaks(
        self, limits: Optional[tuple[float, float]] = None
    ) -> Sequence[float]:
        """
        Generate breaks for the axis or legend

        Parameters
        ----------
        limits : list_like | None
            If None the self.limits are used
            They are expected to be in transformed
            space.

        Returns
        -------
        out : array_like

        Notes
        -----
        Breaks are calculated in data space and
        returned in transformed space since all
        data is plotted in transformed space.
        """
        if limits is None:
            limits = self.final_limits

        # To data space
        _limits = self.inverse(limits)

        if self.is_empty() or self.breaks is False or self.breaks is None:
            breaks = []
        elif self.breaks is True:
            # TODO: Fix this type mismatch in mizani with
            # a typevar so that type-in = type-out
            _tlimits = self._trans.breaks(_limits)
            breaks: Sequence[float] = _tlimits  # pyright: ignore
        elif zero_range(_limits):
            breaks = [_limits[0]]
        elif callable(self.breaks):
            breaks = self.breaks(_limits)
        else:
            breaks = self.breaks

        breaks = self.transform(breaks)
        return breaks

    def get_bounded_breaks(
        self, limits: Optional[tuple[float, float]] = None
    ) -> Sequence[float]:
        """
        Return Breaks that are within limits
        """
        if limits is None:
            limits = self.final_limits
        breaks = self.get_breaks(limits)
        strict_breaks = [b for b in breaks if limits[0] <= b <= limits[1]]
        return strict_breaks

    def get_minor_breaks(
        self,
        major: Sequence[float],
        limits: Optional[tuple[float, float]] = None,
    ) -> Sequence[float]:
        """
        Return minor breaks
        """
        if limits is None:
            limits = self.final_limits

        if self.minor_breaks is False or self.minor_breaks is None:
            minor_breaks = []
        elif self.minor_breaks is True:
            minor_breaks: Sequence[float] = self._trans.minor_breaks(
                major, limits
            )  # pyright: ignore
        elif isinstance(self.minor_breaks, int):
            minor_breaks: Sequence[float] = self._trans.minor_breaks(
                major,
                limits,
                self.minor_breaks,  # pyright: ignore
            )
        elif callable(self.minor_breaks):
            breaks = self.minor_breaks(self.inverse(limits))
            _major = set(major)
            minor = self.transform(breaks)
            minor_breaks = [x for x in minor if x not in _major]
        else:
            minor_breaks = self.transform(self.minor_breaks)

        return minor_breaks

    def get_labels(
        self, breaks: Optional[Sequence[float]] = None
    ) -> Sequence[str]:
        """
        Generate labels for the axis or legend

        Parameters
        ----------
        breaks: None | array_like
            If None, use self.breaks.
        """
        if breaks is None:
            breaks = self.get_breaks()

        breaks = self.inverse(breaks)
        labels: Sequence[str]

        if self.labels is False or self.labels is None:
            labels = []
        elif self.labels is True:
            labels = self._trans.format(breaks)
        elif callable(self.labels):
            labels = self.labels(breaks)
        elif isinstance(self.labels, dict):
            labels = [
                str(self.labels[b]) if b in self.labels else str(b)
                for b in breaks
            ]
        else:
            # When user sets breaks and labels of equal size,
            # but the limits exclude some of the breaks.
            # We remove the corresponding labels
            from collections.abc import Iterable, Sized

            labels = self.labels
            if (
                len(labels) != len(breaks)
                and isinstance(self.breaks, Iterable)
                and isinstance(self.breaks, Sized)
                and len(labels) == len(self.breaks)
            ):
                _wanted_breaks = set(breaks)
                labels = [
                    l
                    for l, b in zip(labels, self.breaks)
                    if b in _wanted_breaks
                ]

        if len(labels) != len(breaks):
            raise PlotnineError("Breaks and labels are different lengths")

        return labels
</file>

<file path="plotnine/scales/scale_datetime.py">
from __future__ import annotations

from dataclasses import KW_ONLY, InitVar, dataclass
from typing import TYPE_CHECKING
from warnings import warn

from ._runtime_typing import TransUser  # noqa: TCH001
from .scale_continuous import scale_continuous

if TYPE_CHECKING:
    from datetime import timedelta


@dataclass
class scale_datetime(scale_continuous):
    """
    Base class for all date/datetime scales
    """

    date_breaks: InitVar[str | None] = None
    """
    A string giving the distance between major breaks.
    For example `'2 weeks'`, `'5 years'`. If specified,
    `date_breaks` takes precedence over `breaks`.
    """

    date_labels: InitVar[str | None] = None
    """
    Format string for the labels.
    See [strftime](:ref:`strftime-strptime-behavior`).
    If specified, `date_labels` takes precedence over `labels`.
    """

    date_minor_breaks: InitVar[str | None] = None
    """
    A string giving the distance between minor breaks.
    For example `'2 weeks'`, `'5 years'`. If specified,
    `date_minor_breaks` takes precedence over `minor_breaks`.
    """

    _: KW_ONLY
    trans: TransUser = "datetime"
    # fmt: off
    expand: ( # pyright: ignore[reportIncompatibleVariableOverride]
        tuple[float, timedelta]
        | tuple[float, timedelta, float, timedelta]
        | None
    ) = None
    # fmt: on
    """
    Multiplicative and additive expansion constants
    that determine how the scale is expanded. If
    specified must be of length 2 or 4. Specifically the
    values are in this order:

    ```
    (mul, add)
    (mul_low, add_low, mul_high, add_high)
    ```

    For example,

    - `(0, timedelta(0))` - Do not expand.
    - `(0, timedelta(days=1))` - Expand lower and upper limits by 1 day.
    - `(1, 0)` - Expand lower and upper limits by 100%.
    - `(0, 0, 0, timedelta(hours=6))` - Expand upper limit by 6 hours.
    - `(0, timedelta(minutes=5), 0.1, timdelta(0))` - Expand lower limit
      by 5 minutes and upper limit by 10%.
    - `(0, 0, 0.1, timedelta(weeks=2))` - Expand upper limit by 10% plus
      2 weeks.

    If not specified, suitable defaults are chosen.
    """

    def __post_init__(
        self,
        date_breaks: str | None,
        date_labels: str | None,
        date_minor_breaks: str | None,
    ):
        from mizani.breaks import breaks_date_width
        from mizani.labels import label_date

        if date_breaks is not None:
            self.breaks = breaks_date_width(date_breaks)  # pyright: ignore[reportAttributeAccessIssue]
        elif isinstance(self.breaks, str):
            warn(
                "Passing a string to `breaks` will not work in "
                f"future versions. Use `date_breaks={self.breaks!r}`",
                FutureWarning,
            )
            self.breaks = breaks_date_width(width=self.breaks)  # pyright: ignore[reportAttributeAccessIssue]

        if date_labels is not None:
            self.labels = label_date(fmt=date_labels)  # pyright: ignore[reportAttributeAccessIssue]
        elif isinstance(self.labels, str):
            warn(
                "Passing a string to `labels` will not work in "
                f"future versions. Use `date_labels={self.labels!r}`",
                FutureWarning,
            )
            self.labels = label_date(fmt=self.labels)  # pyright: ignore[reportAttributeAccessIssue]

        if date_minor_breaks is not None:
            self.minor_breaks = breaks_date_width(date_minor_breaks)  # pyright: ignore[reportAttributeAccessIssue]
        elif isinstance(self.minor_breaks, str):
            warn(
                "Passing a string to `minor_breaks` will not work in "
                "future versions. "
                f"Use `date_minor_breaks={self.minor_breaks!r}`",
                FutureWarning,
            )
            self.minor_breaks = breaks_date_width(width=self.minor_breaks)  # pyright: ignore[reportAttributeAccessIssue]

        scale_continuous.__post_init__(self)
</file>

<file path="plotnine/scales/scale_discrete.py">
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, Sequence

import numpy as np
import pandas as pd
from mizani.bounds import expand_range_distinct
from mizani.palettes import none_pal

from .._utils import match
from ..iapi import range_view, scale_view
from ._expand import expand_range
from ._runtime_typing import DiscreteBreaksUser, DiscreteLimitsUser
from .range import RangeDiscrete
from .scale import scale

if TYPE_CHECKING:
    from typing import Optional

    from mizani.transforms import trans

    from plotnine.typing import AnyArrayLike, CoordRange


@dataclass(kw_only=True)
class scale_discrete(
    scale[
        RangeDiscrete,
        DiscreteBreaksUser,
        DiscreteLimitsUser,
        Literal["legend"] | None,
    ]
):
    """
    Base class for all discrete scales
    """

    limits: DiscreteLimitsUser = None
    """
    Limits of the scale. These are the categories (unique values) of
    the variables. If is only a subset of the values, those that are
    left out will be treated as missing data and represented with a
    `na_value`.
    """

    breaks: DiscreteBreaksUser = True
    """
    List of major break points. Or a callable that takes a tuple of limits
    and returns a list of breaks. If `True`, automatically calculate the
    breaks.
    """

    drop: bool = True
    """
    Whether to drop unused categories from the scale
    """

    na_translate: bool = True
    """
    If `True` translate missing values and show them. If `False` remove
    missing values.
    """

    na_value: Any = np.nan
    """
    If `na_translate=True`, what aesthetic value should be assigned to the
    missing values. This parameter does not apply to position scales where
    `nan` is always placed on the right.
    """

    guide: Literal["legend"] | None = "legend"

    def __post_init__(self):
        super().__post_init__()
        self._range = RangeDiscrete()

    @property
    def final_limits(self) -> Sequence[str]:
        if self.is_empty():
            return ("0", "1")

        if self.limits is None:
            return tuple(self._range.range)
        elif callable(self.limits):
            return tuple(self.limits(self._range.range))
        else:
            return tuple(self.limits)

    def train(self, x: AnyArrayLike, drop=False):
        """
        Train scale

        Parameters
        ----------
        x:
            A column of data to train over
        drop :
            Whether to drop(not include) unused categories

        A discrete range is stored in a list
        """
        if not len(x):
            return

        na_rm = not self.na_translate
        self._range.train(x, drop, na_rm=na_rm)

    def dimension(self, expand=(0, 0, 0, 0), limits=None):
        """
        Get the phyical size of the scale

        Unlike limits, this always returns a numeric vector of length 2
        """
        if limits is None:
            limits = self.final_limits

        return expand_range_distinct((0, len(limits)), expand)

    def expand_limits(
        self,
        limits: Sequence[str],
        expand: tuple[float, float] | tuple[float, float, float, float],
        coord_limits: tuple[float, float],
        trans: trans,
    ) -> range_view:
        """
        Calculate the final range in coordinate space
        """
        # Turn discrete limits into a tuple of continuous limits
        is_empty = self.is_empty() or len(limits) == 0
        climits = (0, 1) if is_empty else (1, len(limits))
        if coord_limits is not None:
            # - Override None in coord_limits
            # - Expand limits in coordinate space
            # - Remove any computed infinite values &
            c0, c1 = coord_limits
            climits = (
                climits[0] if c0 is None else c0,
                climits[1] if c1 is None else c1,
            )
        return expand_range(climits, expand, trans)

    def view(
        self,
        limits: Optional[Sequence[str]] = None,
        range: Optional[CoordRange] = None,
    ) -> scale_view:
        """
        Information about the trained scale
        """
        if limits is None:
            limits = self.final_limits

        if range is None:
            range = self.dimension(limits=limits)

        breaks_d = self.get_breaks(limits)
        breaks = self.map(pd.Categorical(breaks_d))  # pyright: ignore[reportArgumentType]
        minor_breaks = []
        labels = self.get_labels(breaks_d)

        sv = scale_view(
            scale=self,
            aesthetics=self.aesthetics,
            name=self.name,
            limits=limits,
            range=range,
            breaks=breaks,
            labels=labels,
            minor_breaks=minor_breaks,
        )
        return sv

    def default_expansion(self, mult=0, add=0.6, expand=True):
        """
        Get the default expansion for a discrete scale
        """
        return super().default_expansion(mult, add, expand)

    def palette(self, n: int) -> Sequence[Any]:
        """
        Map integer `n` to `n` values of the scale
        """
        return none_pal()(n)

    def map(self, x, limits: Optional[Sequence[str]] = None) -> Sequence[Any]:
        """
        Map values in x to a palette
        """
        if limits is None:
            limits = self.final_limits

        n = sum(~pd.isna(list(limits)))
        pal = self.palette(n)
        if isinstance(pal, dict):
            # manual palette with specific assignments
            pal_match = []
            for val in x:
                try:
                    pal_match.append(pal[val])
                except KeyError:
                    pal_match.append(self.na_value)
        else:
            if not isinstance(pal, np.ndarray):
                pal = np.asarray(pal, dtype=object)
            idx = np.asarray(match(x, limits))
            try:
                pal_match = [pal[i] if i >= 0 else None for i in idx]
            except IndexError:
                # Deal with missing data
                # - Insert NaN where there is no match
                pal = np.hstack((pal.astype(object), np.nan))
                idx = np.clip(idx, 0, len(pal) - 1)
                pal_match = list(pal[idx])

        if self.na_translate:
            bool_pal_match = pd.isna(pal_match)
            if len(bool_pal_match.shape) > 1:
                # linetypes take tuples, these return 2d
                bool_pal_match = bool_pal_match.any(axis=1)
            bool_idx = pd.isna(x) | bool_pal_match
            if bool_idx.any():
                pal_match = [
                    x if i else self.na_value
                    for x, i in zip(pal_match, ~bool_idx)
                ]

        return pal_match

    def get_breaks(
        self, limits: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """
        Return an ordered list of breaks

        The form is suitable for use by the guides e.g.
            ['fair', 'good', 'very good', 'premium', 'ideal']
        """
        if self.is_empty():
            return []

        if limits is None:
            limits = self.final_limits

        if self.breaks in (None, False):
            breaks = []
        elif self.breaks is True:
            breaks = list(limits)
        elif callable(self.breaks):
            breaks = self.breaks(limits)
        else:
            breaks = list(self.breaks)

        return breaks

    def get_bounded_breaks(
        self, limits: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """
        Return Breaks that are within limits
        """
        if limits is None:
            limits = self.final_limits

        lookup_limits = set(limits)
        return [b for b in self.get_breaks() if b in lookup_limits]

    def get_labels(
        self, breaks: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """
        Generate labels for the legend/guide breaks
        """
        if self.is_empty():
            return []

        if breaks is None:
            breaks = self.get_breaks()

        # The labels depend on the breaks if the breaks.
        # No breaks, no labels
        if breaks in (None, False) or self.labels in (None, False):
            return []
        elif self.labels is True:
            return [str(b) for b in breaks]
        elif callable(self.labels):
            return self.labels(breaks)
        # if a dict is used to rename some labels
        elif isinstance(self.labels, dict):
            return [
                str(self.labels[b]) if b in self.labels else str(b)
                for b in breaks
            ]
        else:
            # Return the labels in the order that they match with
            # the breaks.
            label_lookup = dict(zip(self.get_breaks(), self.labels))
            return [label_lookup[b] for b in breaks]

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform dataframe
        """
        # Discrete scales do not do transformations
        return df

    def transform(self, x):
        """
        Transform array|series x
        """
        # Discrete scales do not do transformations
        return x

    def inverse_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Inverse Transform dataframe
        """
        # Discrete scales do not do transformations
        return df
</file>

<file path="plotnine/scales/scale_linetype.py">
from dataclasses import dataclass
from warnings import warn

from .._utils.registry import alias
from ..exceptions import PlotnineError, PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_discrete import scale_discrete

LINETYPES = ["solid", "dashed", "dashdot", "dotted"]


@dataclass
class scale_linetype(scale_discrete):
    """
    Scale for line patterns

    Notes
    -----
    The available linetypes are
    `'solid', 'dashed', 'dashdot', 'dotted'`
    If you need more custom linetypes, use
    [](`~plotnine.scales.scale_linetype_manual`)
    """

    _aesthetics = ["linetype"]

    def __post_init__(self):
        from mizani.palettes import manual_pal

        super().__post_init__()
        self.palette = manual_pal(LINETYPES)


@dataclass
class scale_linetype_ordinal(scale_linetype):
    """
    Scale for line patterns
    """

    _aesthetics = ["linetype"]

    def __post_init__(self):
        super().__post_init__()

        warn(
            "Using linetype for an ordinal variable is not advised.",
            PlotnineWarning,
        )


class scale_linetype_continuous(scale_continuous):
    """
    Linetype scale
    """

    def __init__(self):
        raise PlotnineError(
            "A continuous variable can not be mapped to linetype"
        )


@alias
class scale_linetype_discrete(scale_linetype):
    pass
</file>

<file path="plotnine/scales/scale_manual.py">
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import KW_ONLY, InitVar, dataclass
from typing import Any, Sequence
from warnings import warn

from .._utils.registry import alias
from ..exceptions import PlotnineWarning
from .scale_discrete import scale_discrete


@dataclass
class _scale_manual(scale_discrete):
    """
    Abstract class for manual scales
    """

    values: InitVar[Sequence[Any] | dict[Any, Any]]
    """
    Exact values the scale should map to.
    """

    def __post_init__(self, values):
        from collections.abc import Iterable, Sized

        super().__post_init__()

        if (
            isinstance(self.breaks, Iterable)
            and isinstance(self.breaks, Sized)
            and len(self.breaks) == len(values)
            and not isinstance(values, Mapping)
        ):
            values = dict(zip(self.breaks, values))

        def palette(n):
            max_n = len(values)
            if n > max_n:
                msg = (
                    f"The palette of {self.__class__.__name__} can return "
                    f"a maximum of {max_n} values. {n} were requested "
                    f"from it."
                )
                warn(msg, PlotnineWarning)
            return values

        # manual scales have a unique palette that return
        self.palette = palette  # type: ignore


@dataclass
class scale_color_manual(_scale_manual):
    """
    Custom discrete color scale
    """

    _aesthetics = ["color"]
    values: InitVar[Sequence[Any] | dict[Any, Any]]
    """
    Colors that make up the palette. The values will be matched with
    the `limits` of the scale or the `breaks` if provided.
    If it is a dict then it should map data values to colors.
    """
    _: KW_ONLY
    na_value: str = "#7F7F7F"


@dataclass
class scale_fill_manual(scale_color_manual):
    """
    Custom discrete fill scale
    """

    _aesthetics = ["fill"]


@dataclass
class scale_shape_manual(_scale_manual):
    """
    Custom discrete shape scale

    See Also
    --------
    [](`matplotlib.markers`)
    """

    _aesthetics = ["shape"]
    values: InitVar[Sequence[Any] | dict[Any, Any]]
    """
    Shapes that make up the palette. See [](`matplotlib.markers`) for list
    of all possible shapes. The values will be matched with the `limits`
    of the scale or the `breaks` if provided. If it is a dict then it
    should map data values to shapes.
    """


@dataclass
class scale_linetype_manual(_scale_manual):
    """
    Custom discrete linetype scale

    See Also
    --------
    [](`matplotlib.markers`)
    """

    values: InitVar[Sequence[Any] | dict[Any, Any]]
    """
    Linetypes that make up the palette. Possible values of the list are:

    1. Strings like

    ```python
    'solid'                # solid line
    'dashed'               # dashed line
    'dashdot'              # dash-dotted line
    'dotted'               # dotted line
    'None' or ' ' or ''    # draw nothing
    ```

    2. Tuples of the form (offset, (on, off, on, off, ....))
       e.g. (0, (1, 1)), (1, (2, 2)), (2, (5, 3, 1, 3))

    The values will be matched with the `limits` of the scale or the
    `breaks` if provided. If it is a dict then it should map data
    values to linetypes.
    """

    _aesthetics = ["linetype"]

    def map(self, x, limits=None):
        result = super().map(x, limits)
        # Ensure that custom linetypes are tuples, so that they can
        # be properly inserted and extracted from the dataframe
        if len(result) and hasattr(result[0], "__hash__"):
            result = [x if isinstance(x, str) else tuple(x) for x in result]
        return result


@dataclass
class scale_alpha_manual(_scale_manual):
    """
    Custom discrete alpha scale
    """

    _aesthetics = ["alpha"]
    values: InitVar[Sequence[Any] | dict[Any, Any]]
    """
    Alpha values (in the [0, 1] range) that make up the palette.
    The values will be matched with the `limits` of the scale or
    the `breaks` if provided. If it is a dict then it should map
    data values to alpha values.
    """


@dataclass
class scale_size_manual(_scale_manual):
    """
    Custom discrete size scale
    """

    _aesthetics = ["size"]
    values: InitVar[Sequence[Any] | dict[Any, Any]]
    """
    Sizes that make up the palette. The values will be matched
    with the `limits` of the scale or the `breaks` if provided.
    If it is a dict then it should map data values to sizes.
    """


# American to British spelling
@alias
class scale_colour_manual(scale_color_manual):
    pass
</file>

<file path="plotnine/scales/scale_shape.py">
from dataclasses import InitVar, dataclass
from warnings import warn

from .._utils.registry import alias
from ..exceptions import PlotnineError, PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_discrete import scale_discrete

# All these shapes are filled
shapes = (
    "o",  # circle
    "^",  # triangle up
    "s",  # square
    "D",  # Diamond
    "v",  # triangle down
    "*",  # star
    "p",  # pentagon
    "8",  # octagon
    "<",  # triangle left
    "h",  # hexagon1
    ">",  # triangle right
    "H",  # hexagon1
    "d",  # thin diamond
)

unfilled_shapes = (
    "+",  # plus
    "x",  # x
    ".",  # point
    "1",  # tri_down
    "2",  # tri_up
    "3",  # tri_left
    "4",  # tri_right
    ",",  # pixel
    "_",  # hline
    "|",  # vline
    0,  # tickleft
    1,  # tickright
    2,  # tickup
    3,  # tickdown
    4,  # caretleft
    5,  # caretright
    6,  # caretup
    7,  # caretdown
)

# For quick lookup
FILLED_SHAPES = set(shapes)
UNFILLED_SHAPES = set(unfilled_shapes)


@dataclass
class scale_shape(scale_discrete):
    """
    Scale for shapes
    """

    _aesthetics = ["shape"]
    unfilled: InitVar[bool] = False
    """
    If `True`, then all shapes will have no interiors
    that can be a filled.
    """

    def __post_init__(self, unfilled):
        from mizani.palettes import manual_pal

        super().__post_init__()
        _shapes = unfilled_shapes if unfilled else shapes
        self.palette = manual_pal(_shapes)


@dataclass
class scale_shape_ordinal(scale_shape):
    """
    Scale for shapes
    """

    _aesthetics = ["shape"]

    def __post_init__(self, unfilled):
        warn(
            "Using shapes for an ordinal variable is not advised.",
            PlotnineWarning,
        )
        super().__post_init__(unfilled)


class scale_shape_continuous(scale_continuous):
    """
    Continuous scale for shapes
    """

    def __init__(self):
        raise PlotnineError("A continuous variable can not be mapped to shape")


@alias
class scale_shape_discrete(scale_shape):
    pass
</file>

<file path="plotnine/scales/scale_size.py">
from dataclasses import KW_ONLY, InitVar, dataclass
from typing import Literal
from warnings import warn

import numpy as np
from mizani.bounds import rescale_max

from .._utils.registry import alias
from ..exceptions import PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_datetime import scale_datetime
from .scale_discrete import scale_discrete


@dataclass
class scale_size_ordinal(scale_discrete):
    """
    Discrete area size scale
    """

    _aesthetics = ["size"]
    range: InitVar[tuple[float, float]] = (2, 6)
    """
    Range ([Minimum, Maximum]) of the size.
    """

    def __post_init__(self, range):
        super().__post_init__()

        def palette(value):
            area = np.linspace(range[0] ** 2, range[1] ** 2, value)
            return np.sqrt(area)

        self.palette = palette  # type: ignore


@dataclass
class scale_size_discrete(scale_size_ordinal):
    """
    Discrete area size scale
    """

    _aesthetics = ["size"]

    def __post_init__(self, range):
        warn(
            "Using size for a discrete variable is not advised.",
            PlotnineWarning,
        )
        super().__post_init__(range)


@dataclass
class scale_size_continuous(scale_continuous[Literal["legend"] | None]):
    """
    Continuous area size scale
    """

    _aesthetics = ["size"]
    range: InitVar[tuple[float, float]] = (1, 6)
    """
    Range ([Minimum, Maximum]) of the size.
    """

    _: KW_ONLY
    guide: Literal["legend"] | None = "legend"

    def __post_init__(self, range):
        from mizani.palettes import area_pal

        super().__post_init__()
        self.palette = area_pal(range)


@alias
class scale_size(scale_size_continuous):
    pass


@dataclass
class scale_size_radius(scale_continuous[Literal["legend"] | None]):
    """
    Continuous radius size scale
    """

    _aesthetics = ["size"]
    range: InitVar[tuple[float, float]] = (1, 6)
    """
    Range ([Minimum, Maximum]) of the size.
    """

    _: KW_ONLY
    guide: Literal["legend"] | None = "legend"

    def __post_init__(self, range):
        from mizani.palettes import rescale_pal

        super().__post_init__()
        self.palette = rescale_pal(range)


@dataclass
class scale_size_area(scale_continuous[Literal["legend"] | None]):
    """
    Continuous area size scale
    """

    _aesthetics = ["size"]
    max_size: InitVar[float] = 6
    """
    Maximum size of the plotting symbol.
    """

    _: KW_ONLY
    rescaler = rescale_max
    guide: Literal["legend"] | None = "legend"

    def __post_init__(self, max_size):
        from mizani.palettes import abs_area

        super().__post_init__()
        self.palette = abs_area(max_size)


@dataclass
class scale_size_datetime(scale_datetime):
    """
    Datetime area-size scale
    """

    _aesthetics = ["size"]
    range: InitVar[tuple[float, float]] = (1, 6)
    """
    Range ([Minimum, Maximum]) of the size.
    """

    _: KW_ONLY
    guide: Literal["legend"] | None = "legend"

    def __post_init__(
        self, range, date_breaks, date_labels, date_minor_breaks
    ):
        from mizani.palettes import area_pal

        super().__post_init__(date_breaks, date_labels, date_minor_breaks)
        self.palette = area_pal(range)
</file>

<file path="plotnine/scales/scale_stroke.py">
from dataclasses import KW_ONLY, InitVar, dataclass
from typing import Literal
from warnings import warn

import numpy as np

from .._utils.registry import alias
from ..exceptions import PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_discrete import scale_discrete


@dataclass
class scale_stroke_continuous(scale_continuous[Literal["legend"] | None]):
    """
    Continuous Stroke Scale
    """

    _aesthetics = ["stroke"]
    range: InitVar[tuple[float, float]] = (1, 6)
    """
    Range ([Minimum, Maximum]) of output stroke values.
    Should be between 0 and 1.
    """
    _: KW_ONLY
    guide: Literal["legend"] | None = "legend"

    def __post_init__(self, range):
        from mizani.palettes import rescale_pal

        super().__post_init__()
        self.palette = rescale_pal(range)


@dataclass
class scale_stroke_ordinal(scale_discrete):
    """
    Discrete Stroke Scale
    """

    _aesthetics = ["stroke"]
    range: InitVar[tuple[float, float]] = (1, 6)
    """
    Range ([Minimum, Maximum]) of output stroke values.
    Should be between 0 and 1.
    """

    def __post_init__(self, range):
        super().__post_init__()

        def palette(n: int):
            return np.linspace(range[0], range[1], n)

        self.palette = palette


@dataclass
class scale_stroke_discrete(scale_stroke_ordinal):
    """
    Discrete Stroke Scale
    """

    _aesthetics = ["stroke"]

    def __post_init__(self, range):
        warn(
            "Using stroke for a ordinal variable is not advised.",
            PlotnineWarning,
        )
        super().__post_init__(
            range,
        )


@alias
class scale_stroke(scale_stroke_continuous):
    pass
</file>

<file path="plotnine/scales/scale_xy.py">
from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from .._utils import array_kind, match
from .._utils.registry import alias
from ..exceptions import PlotnineError
from ..iapi import range_view
from ._expand import expand_range
from ._runtime_typing import TransUser  # noqa: TCH001
from .range import RangeContinuous
from .scale_continuous import scale_continuous
from .scale_datetime import scale_datetime
from .scale_discrete import scale_discrete

if TYPE_CHECKING:
    from typing import Sequence

    from mizani.transforms import trans


# positions scales have a couple of differences (quirks) that
# make necessary to override some of the scale_discrete and
# scale_continuous methods
#
# scale_position_discrete and scale_position_continuous
# are intermediate base classes where the required overriding
# is done
@dataclass(kw_only=True)
class scale_position_discrete(scale_discrete):
    """
    Base class for discrete position scales
    """

    def __post_init__(self):
        super().__post_init__()
        # Keeps two ranges, range and range_c
        self._range_c = RangeContinuous()
        if isinstance(self.limits, tuple):
            self.limits = list(self.limits)

        # All positions have no guide
        self.guide = None

    def reset(self):
        # Can't reset discrete scale because
        # no way to recover values
        self._range_c.reset()

    def is_empty(self) -> bool:
        return super().is_empty() and self._range_c.is_empty()

    def train(self, x, drop=False):
        # The discrete position scale is capable of doing
        # training for continuous data.
        # This complicates training and mapping, but makes it
        # possible to place objects at non-integer positions,
        # as is necessary for jittering etc.
        if array_kind.continuous(x):
            self._range_c.train(x)
        else:
            self._range.train(x, drop=self.drop)

    def map(self, x, limits=None):
        # Discrete values are converted into integers starting
        # at 1
        if limits is None:
            limits = self.final_limits
        if array_kind.discrete(x):
            # TODO: Rewrite without using numpy
            seq = np.arange(1, len(limits) + 1)
            idx = np.asarray(match(x, limits, nomatch=len(x)))
            if not len(idx):
                return []
            try:
                seq = seq[idx]
            except IndexError:
                # Deal with missing data
                # - Insert NaN where there is no match
                seq = np.hstack((seq.astype(float), np.nan))
                idx = np.clip(idx, 0, len(seq) - 1)
                seq = seq[idx]
            return list(seq)
        return list(x)

    @property
    def final_limits(self):
        if self.is_empty():
            return (0, 1)
        elif self.limits is not None and not callable(self.limits):
            return self.limits
        elif self.limits is None:
            # discrete range
            return self._range.range
        elif callable(self.limits):
            limits = self.limits(self._range.range)
            # Functions that return iterators e.g. reversed
            if iter(limits) is limits:
                limits = list(limits)
            return limits
        else:
            raise PlotnineError("Lost, do not know what the limits are.")

    def dimension(self, expand=(0, 0, 0, 0), limits=None):
        """
        Get the phyical size of the scale

        Unlike limits, this always returns a numeric vector of length 2
        """
        from mizani.bounds import expand_range_distinct

        if limits is None:
            limits = self.final_limits

        if self.is_empty():
            return (0, 1)

        if self._range.is_empty():  # only continuous
            return expand_range_distinct(self._range_c.range, expand)
        elif self._range_c.is_empty():  # only discrete
            # FIXME: I think this branch should not exist
            return expand_range_distinct((1, len(self.final_limits)), expand)
        else:  # both
            # e.g categorical bar plot have discrete items, but
            # are plot on a continuous x scale
            a = np.hstack(
                [
                    self._range_c.range,
                    expand_range_distinct((1, len(self._range.range)), expand),
                ]
            )
            return a.min(), a.max()

    def expand_limits(
        self,
        limits: Sequence[str],
        expand: tuple[float, float] | tuple[float, float, float, float],
        coord_limits: tuple[float, float],
        trans: trans,
    ) -> range_view:
        # Turn discrete limits into a tuple of continuous limits
        if self.is_empty():
            climits = (0, 1)
        else:
            climits = (1, len(limits))
            self._range_c.range

        if coord_limits is not None:
            # - Override None in coord_limits
            # - Expand limits in coordinate space
            # - Remove any computed infinite values &
            c0, c1 = coord_limits
            climits = (
                climits[0] if c0 is None else c0,
                climits[1] if c1 is None else c1,
            )

        # Expand discrete range
        rv_d = expand_range(climits, expand, trans)

        if self._range_c.is_empty():
            return rv_d

        # Expand continuous range
        no_expand = self.default_expansion(0, 0)
        rv_c = expand_range(self._range_c.range, no_expand, trans)

        # Merge the ranges
        rv = range_view(
            range=(
                min(chain(rv_d.range, rv_c.range)),
                max(chain(rv_d.range, rv_c.range)),
            ),
            range_coord=(
                min(chain(rv_d.range_coord, rv_c.range_coord)),
                max(chain(rv_d.range_coord, rv_c.range_coord)),
            ),
        )
        rv.range = min(rv.range), max(rv.range)
        rv.range_coord = min(rv.range_coord), max(rv.range_coord)
        return rv


@dataclass(kw_only=True)
class scale_position_continuous(scale_continuous[None]):
    """
    Base class for continuous position scales
    """

    guide: None = None

    def map(self, x, limits=None):
        # Position aesthetics don't map, because the coordinate
        # system takes care of it.
        # But the continuous scale has to deal with out of bound points
        if not len(x):
            return x
        if limits is None:
            limits = self.final_limits
        scaled = self.oob(x, limits)  # type: ignore
        scaled[pd.isna(scaled)] = self.na_value
        return scaled


@dataclass(kw_only=True)
class scale_x_discrete(scale_position_discrete):
    """
    Discrete x position
    """

    _aesthetics = ["x", "xmin", "xmax", "xend", "xintercept"]


@dataclass(kw_only=True)
class scale_y_discrete(scale_position_discrete):
    """
    Discrete y position
    """

    _aesthetics = ["y", "ymin", "ymax", "yend", "yintercept"]


# Not part of the user API
@alias
class scale_x_ordinal(scale_x_discrete):
    pass


@alias
class scale_y_ordinal(scale_y_discrete):
    pass


@dataclass(kw_only=True)
class scale_x_continuous(scale_position_continuous):
    """
    Continuous x position
    """

    _aesthetics = ["x", "xmin", "xmax", "xend", "xintercept"]


@dataclass(kw_only=True)
class scale_y_continuous(scale_position_continuous):
    """
    Continuous y position
    """

    _aesthetics = [
        "y",
        "ymin",
        "ymax",
        "yend",
        "yintercept",
        "ymin_final",
        "ymax_final",
        "lower",
        "middle",
        "upper",
    ]


# Transformed scales
@dataclass(kw_only=True)
class scale_x_datetime(scale_datetime, scale_x_continuous):  # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Continuous x position for datetime data points
    """

    guide: None = None


@dataclass(kw_only=True)
class scale_y_datetime(scale_datetime, scale_y_continuous):  # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Continuous y position for datetime data points
    """

    guide: None = None


@alias
class scale_x_date(scale_x_datetime):
    pass


@alias
class scale_y_date(scale_y_datetime):
    pass


@dataclass(kw_only=True)
class scale_x_timedelta(scale_x_continuous):
    """
    Continuous x position for timedelta data points
    """

    trans: TransUser = "pd_timedelta"


@dataclass(kw_only=True)
class scale_y_timedelta(scale_y_continuous):
    """
    Continuous y position for timedelta data points
    """

    trans: TransUser = "pd_timedelta"


@dataclass(kw_only=True)
class scale_x_sqrt(scale_x_continuous):
    """
    Continuous x position sqrt transformed scale
    """

    trans: TransUser = "sqrt"


@dataclass(kw_only=True)
class scale_y_sqrt(scale_y_continuous):
    """
    Continuous y position sqrt transformed scale
    """

    trans: TransUser = "sqrt"


@dataclass(kw_only=True)
class scale_x_log10(scale_x_continuous):
    """
    Continuous x position log10 transformed scale
    """

    trans: TransUser = "log10"


@dataclass(kw_only=True)
class scale_y_log10(scale_y_continuous):
    """
    Continuous y position log10 transformed scale
    """

    trans: TransUser = "log10"


@dataclass(kw_only=True)
class scale_x_reverse(scale_x_continuous):
    """
    Continuous x position reverse transformed scale
    """

    trans: TransUser = "reverse"


@dataclass(kw_only=True)
class scale_y_reverse(scale_y_continuous):
    """
    Continuous y position reverse transformed scale
    """

    trans: TransUser = "reverse"


@dataclass(kw_only=True)
class scale_x_symlog(scale_x_continuous):
    """
    Continuous x position symmetric logarithm transformed scale
    """

    trans: TransUser = "symlog"


@dataclass(kw_only=True)
class scale_y_symlog(scale_y_continuous):
    """
    Continuous y position symmetric logarithm transformed scale
    """

    trans: TransUser = "symlog"
</file>

<file path="plotnine/scales/scales.py">
from __future__ import annotations

import itertools
import typing
from contextlib import suppress
from typing import List
from warnings import warn

import numpy as np
import pandas.api.types as pdtypes

from .._utils import array_kind
from .._utils.registry import Registry
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.aes import aes_to_scale
from .scale import scale

if typing.TYPE_CHECKING:
    import pandas as pd

    from plotnine.typing import ScaledAestheticsName


_TPL_DUPLICATE_SCALE = """\
Scale for '{0}' is already present.
Adding another scale for '{0}',
which will replace the existing scale.
"""


class Scales(List[scale]):
    """
    List of scales

    This class has methods the simplify the handling of
    the ggplot object scales
    """

    def append(self, sc: scale):
        """
        Add / Update scale

        Removes any previous scales that cover the same aesthetics
        """
        ae = sc.aesthetics[0]
        cover_ae = self.find(ae)
        if any(cover_ae):
            warn(_TPL_DUPLICATE_SCALE.format(ae), PlotnineWarning)
            idx = cover_ae.index(True)
            self.pop(idx)
        # super() does not work well with reloads
        list.append(self, sc)

    def find(self, aesthetic: ScaledAestheticsName | str) -> list[bool]:
        """
        Find scales for given aesthetic

        Returns a list[bool] each scale if it covers the aesthetic
        """
        return [aesthetic in s.aesthetics for s in self]

    def input(self):
        """
        Return a list of all the aesthetics covered by the scales
        """
        lst = [s.aesthetics for s in self]
        return list(itertools.chain(*lst))

    def get_scales(
        self, aesthetic: ScaledAestheticsName | str
    ) -> scale | None:
        """
        Return the scale for the aesthetic or None if there isn't one

        These are the scales specified by the user e.g
            `ggplot() + scale_x_continuous()`
        or those added by default during the plot building
        process
        """
        bool_lst = self.find(aesthetic)
        try:
            idx = bool_lst.index(True)
            return self[idx]
        except ValueError:
            return None

    @property
    def x(self) -> scale | None:
        """
        Return x scale
        """
        return self.get_scales("x")

    @property
    def y(self) -> scale | None:
        """
        Return y scale
        """
        return self.get_scales("y")

    def non_position_scales(self) -> Scales:
        """
        Return a list of any non-position scales
        """
        l = [
            s
            for s in self
            if "x" not in s.aesthetics and "y" not in s.aesthetics
        ]
        return Scales(l)

    def position_scales(self) -> Scales:
        """
        Return a list of the position scales that are present
        """
        l = [s for s in self if ("x" in s.aesthetics) or ("y" in s.aesthetics)]
        return Scales(l)

    def train(self, data, vars, idx):
        """
        Train the scales on the data.

        The scales should be for the same aesthetic
        e.g. x scales, y scales, color scales, ...

        Parameters
        ----------
        data : dataframe
            data to use for training
        vars : list | tuple
            columns in data to use for training.
            These should be all the aesthetics of
            a scale type that are present in the
            data. e.g x, xmin, xmax
        idx : array_like
            indices that map the data points to the
            scales. These start at 1, so subtract 1 to
            get the true index into the scales array
        """
        idx = np.asarray(idx)
        for col in vars:
            for i, sc in enumerate(self, start=1):
                bool_idx = i == idx
                sc.train(data.loc[bool_idx, col])

    def map(self, data, vars, idx):
        """
        Map the data onto the scales

        The scales should be for the same aesthetic
        e.g. x scales, y scales, color scales, ...

        Parameters
        ----------
        data : dataframe
            data with columns to map
            This is modified inplace
        vars : list | tuple
            columns to map
        idx : array_like
            indices that link the data points to the
            scales. These start at 1, so subtract 1 to
            get the true index into the scales array
        """
        idx = np.asarray(idx)
        # discrete scales change the dtype
        # from category to int. Use a new dataframe
        # to collect these results.
        # Using `type` preserves the subclass of pd.DataFrame
        discrete_data = type(data)(index=data.index)

        # Loop through each variable, mapping across each scale,
        # then joining back into the copy of the data
        for col in vars:
            use_df = array_kind.discrete(data[col])
            for i, sc in enumerate(self, start=1):
                bool_idx = i == idx
                results = sc.map(data.loc[bool_idx, col])
                if use_df:
                    discrete_data.loc[bool_idx, col] = results
                else:
                    data.loc[bool_idx, col] = results

        for col in discrete_data:
            data[col] = discrete_data[col]

    def reset(self):
        """
        Reset all the scales
        """
        for sc in self:
            sc.reset()

    def train_df(self, data: pd.DataFrame, drop: bool = False):
        """
        Train scales from a dataframe
        """
        if (len(data) == 0) or (len(self) == 0):
            return

        # Each scale trains the columns it understands
        for sc in self:
            sc.train_df(data)

    def map_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Map values from a dataframe.

        Returns dataframe
        """
        if (len(data) == 0) or (len(self) == 0):
            return data

        # Each scale maps the columns it understands
        for sc in self:
            data = sc.map_df(data)
        return data

    def transform_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform values in a dataframe.

        Returns dataframe
        """
        if (len(data) == 0) or (len(self) == 0):
            return data

        # Each scale transforms the columns it understands
        for sc in self:
            data = sc.transform_df(data)
        return data

    def inverse_df(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Inveres transform values in a dataframe.
        Returns dataframe
        """
        if (len(data) == 0) or (len(self) == 0):
            return data

        # Each scale transforms the columns it understands
        for sc in self:
            data = sc.inverse_df(data)
        return data

    def add_defaults(self, data, aesthetics):
        """
        Add default scales for the aesthetics if there is none

        Scales are added only if the aesthetic is mapped to
        a column in the dataframe. This function may have to be
        called separately after evaluating the aesthetics.
        """
        if not aesthetics:
            return

        # aesthetics with scales
        aws = set()
        if self:
            for s in (set(sc.aesthetics) for sc in self):
                aws.update(s)

        # aesthetics that do not have scales present
        # We preserve the order of the aesthetics
        new_aesthetics = [x for x in aesthetics if x not in aws]
        if not new_aesthetics:
            return

        # If a new aesthetic corresponds to a column in the data
        # frame, find a default scale for the type of data in that
        # column
        seen = set()
        for ae in new_aesthetics:
            col = aesthetics[ae]
            if col not in data:
                col = ae
            scale_var = aes_to_scale(ae)

            if self.get_scales(scale_var):
                continue

            seen.add(scale_var)
            try:
                sc = make_scale(scale_var, data[col])
            except PlotnineError:
                # Skip aesthetics with no scales (e.g. group, order, etc)
                continue
            self.append(sc)

    def add_missing(self, aesthetics):
        """
        Add missing but required scales.

        Parameters
        ----------
        aesthetics : list | tuple
            Aesthetic names. Typically, ('x', 'y').
        """
        # Keep only aesthetics that don't have scales
        aesthetics = set(aesthetics) - set(self.input())

        for ae in aesthetics:
            scale_name = f"scale_{ae}_continuous"
            scale_f = Registry[scale_name]
            self.append(scale_f())


def scale_type(series):
    """
    Get a suitable scale for the series
    """
    if array_kind.continuous(series):
        stype = "continuous"
    elif array_kind.ordinal(series):
        stype = "ordinal"
    elif array_kind.discrete(series):
        stype = "discrete"
    elif array_kind.datetime(series):
        stype = "datetime"
    elif array_kind.timedelta(series):
        stype = "timedelta"
    else:
        msg = (
            "Don't know how to automatically pick scale for "
            "object of type {}. Defaulting to 'continuous'"
        )
        warn(msg.format(series.dtype), PlotnineWarning)
        stype = "continuous"
    return stype


def make_scale(ae, series, *args, **kwargs):
    """
    Return a proper scale object for the series

    The scale is for the aesthetic ae, and args & kwargs
    are passed on to the scale creating class
    """
    if pdtypes.is_float_dtype(series) and np.isinf(series).all():
        raise PlotnineError("Cannot create scale for infinite data")

    stype = scale_type(series)

    # filter parameters by scale type
    if stype in ("discrete", "ordinal"):
        with suppress(KeyError):
            del kwargs["trans"]

    scale_name = f"scale_{ae}_{stype}"
    scale_klass = Registry[scale_name]
    return scale_klass(*args, **kwargs)
</file>

<file path="plotnine/stats/__init__.py">
"""
Statistics
"""

from .stat_bin import stat_bin
from .stat_bin_2d import stat_bin2d, stat_bin_2d
from .stat_bindot import stat_bindot
from .stat_boxplot import stat_boxplot
from .stat_count import stat_count
from .stat_density import stat_density
from .stat_density_2d import stat_density_2d
from .stat_ecdf import stat_ecdf
from .stat_ellipse import stat_ellipse
from .stat_function import stat_function
from .stat_hull import stat_hull
from .stat_identity import stat_identity
from .stat_pointdensity import stat_pointdensity
from .stat_qq import stat_qq
from .stat_qq_line import stat_qq_line
from .stat_quantile import stat_quantile
from .stat_sina import stat_sina
from .stat_smooth import stat_smooth
from .stat_sum import stat_sum
from .stat_summary import stat_summary
from .stat_summary_bin import stat_summary_bin
from .stat_unique import stat_unique
from .stat_ydensity import stat_ydensity

__all__ = (
    "stat_count",
    "stat_bin",
    "stat_bin_2d",
    "stat_bin2d",
    "stat_bindot",
    "stat_boxplot",
    "stat_density",
    "stat_ecdf",
    "stat_ellipse",
    "stat_density_2d",
    "stat_function",
    "stat_hull",
    "stat_identity",
    "stat_pointdensity",
    "stat_qq",
    "stat_qq_line",
    "stat_quantile",
    "stat_sina",
    "stat_smooth",
    "stat_sum",
    "stat_summary",
    "stat_summary_bin",
    "stat_unique",
    "stat_ydensity",
)
</file>

<file path="plotnine/stats/density.py">
"""
Kernel Density Functions

These functions make it easy to integrate stats that compute
kernel densities with the wider scientific python ecosystem.

Credit: Jake VanderPlas for the original kde_* functions
https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/
"""

from __future__ import annotations

import typing

import numpy as np

from .._utils import array_kind

if typing.TYPE_CHECKING:
    from typing import Any, Literal

    import pandas as pd

    from plotnine.typing import FloatArray


def kde_scipy(data: FloatArray, grid: FloatArray, **kwargs: Any) -> FloatArray:
    """
    Kernel Density Estimation with Scipy

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out : numpy.array
        Density estimate. Has `m x 1` dimensions
    """
    from scipy.stats import gaussian_kde

    kde = gaussian_kde(data.T, **kwargs)
    return kde.evaluate(grid.T)


def kde_statsmodels_u(
    data: FloatArray, grid: FloatArray, **kwargs: Any
) -> FloatArray:
    """
    Univariate Kernel Density Estimation with Statsmodels

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x 1` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x 1` dimensions, representing m points and p
        variables.

    Returns
    -------
    out : numpy.array
        Density estimate. Has `m x 1` dimensions
    """
    from statsmodels.nonparametric.kde import KDEUnivariate

    kde = KDEUnivariate(data)
    kde.fit(**kwargs)
    return kde.evaluate(grid)  # type: ignore


def kde_statsmodels_m(
    data: FloatArray, grid: FloatArray, **kwargs: Any
) -> FloatArray:
    """
    Multivariate Kernel Density Estimation with Statsmodels

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out :
        Density estimate. Has `m x 1` dimensions
    """
    from statsmodels.nonparametric.kernel_density import KDEMultivariate

    kde = KDEMultivariate(data, **kwargs)
    return kde.pdf(grid)


def kde_sklearn(
    data: FloatArray, grid: FloatArray, **kwargs: Any
) -> FloatArray:
    """
    Kernel Density Estimation with Scikit-learn

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out :
        Density estimate. Has `m x 1` dimensions
    """
    # Not core dependency
    try:
        from sklearn.neighbors import KernelDensity
    except ImportError as err:
        raise ImportError("scikit-learn is not installed") from err
    kde_skl = KernelDensity(**kwargs)
    kde_skl.fit(data)
    # score_samples() returns the log-likelihood of the samples
    log_pdf = kde_skl.score_samples(grid)
    return np.exp(log_pdf)


def kde_count(data: FloatArray, grid: FloatArray, **kwargs: Any) -> FloatArray:
    """
    Kernel Density Estimation via count within radius

    Parameters
    ----------
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out :
        Density estimate. Has `m x 1` dimensions
    """
    r = kwargs.get("radius", np.ptp(data) / 10)

    # Get the number of data points within the radius r of each grid point
    iter = (np.sum(np.linalg.norm(data - g, axis=1) < r) for g in grid)
    count = np.fromiter(iter, float, count=data.shape[0])

    # Get fraction of data within radius
    density = count / data.shape[0]

    return density


KDE_FUNCS = {
    "statsmodels-u": kde_statsmodels_u,
    "statsmodels-m": kde_statsmodels_m,
    "scipy": kde_scipy,
    "scikit-learn": kde_sklearn,
    "sklearn": kde_sklearn,
    "count": kde_count,
}


def kde(
    data: FloatArray, grid: FloatArray, package: str, **kwargs: Any
) -> FloatArray:
    """
    Kernel Density Estimation

    Parameters
    ----------
    package :
        Package whose kernel density estimation to use.
        Should be one of
        `['statsmodels-u', 'statsmodels-m', 'scipy', 'sklearn']`.
    data :
        Data points used to compute a density estimator. It
        has `n x p` dimensions, representing n points and p
        variables.
    grid :
        Data points at which the desity will be estimated. It
        has `m x p` dimensions, representing m points and p
        variables.

    Returns
    -------
    out : numpy.array
        Density estimate. Has `m x 1` dimensions
    """
    if package == "statsmodels":
        package = "statsmodels-m"
    func = KDE_FUNCS[package]
    return func(data, grid, **kwargs)


def get_var_type(col: pd.Series) -> Literal["c", "o", "u"]:
    """
    Return var_type (for KDEMultivariate) of the column

    Parameters
    ----------
    col :
        A dataframe column.

    Returns
    -------
    out :
        Character that denotes the type of column.
        `c` for continuous, `o` for ordered categorical and
        `u` for unordered categorical or if not sure.

    See Also
    --------
    statsmodels.nonparametric.kernel_density.KDEMultivariate : For the origin
        of the character codes.
    """
    if array_kind.continuous(col):
        return "c"
    elif array_kind.discrete(col):
        return "o" if array_kind.ordinal else "u"
    else:
        # unordered if unsure
        return "u"
</file>

<file path="plotnine/stats/distributions.py">
import scipy.stats as stats

from ..exceptions import PlotnineError


def _hasattrs(obj, attrs):
    return all(hasattr(obj, attr) for attr in attrs)


# Continuous univariate
continuous = {
    k for k in dir(stats) if _hasattrs(getattr(stats, k), ("pdf", "cdf"))
}

# Discrete univariate
discrete = {k for k in dir(stats) if hasattr(getattr(stats, k), "pmf")}

univariate = continuous | discrete


def get(name):
    """
    Get any scipy.stats distribution of a given name
    """
    try:
        return getattr(stats, name)
    except AttributeError as e:
        msg = f"Unknown distribution '{name}'"
        raise PlotnineError(msg) from e


def get_continuous_distribution(name):
    """
    Get continuous scipy.stats distribution of a given name
    """
    if name not in continuous:
        msg = "Unknown continuous distribution '{}'"
        raise ValueError(msg.format(name))

    return getattr(stats, name)


def get_univariate(name):
    """
    Get univariate scipy.stats distribution of a given name
    """
    if name not in univariate:
        msg = "Unknown univariate distribution '{}'"
        raise ValueError(msg.format(name))

    return get(name)
</file>

<file path="plotnine/themes/__init__.py">
from .theme import theme, theme_get, theme_set, theme_update
from .theme_538 import theme_538
from .theme_bw import theme_bw
from .theme_classic import theme_classic
from .theme_dark import theme_dark
from .theme_gray import theme_gray, theme_grey
from .theme_light import theme_light
from .theme_linedraw import theme_linedraw
from .theme_matplotlib import theme_matplotlib
from .theme_minimal import theme_minimal
from .theme_seaborn import theme_seaborn
from .theme_tufte import theme_tufte
from .theme_void import theme_void
from .theme_xkcd import theme_xkcd

__all__ = (
    "theme",
    "theme_538",
    "theme_bw",
    "theme_classic",
    "theme_dark",
    "theme_gray",
    "theme_grey",
    "theme_light",
    "theme_linedraw",
    "theme_matplotlib",
    "theme_minimal",
    "theme_seaborn",
    "theme_void",
    "theme_xkcd",
    "theme_tufte",
    "theme_get",
    "theme_set",
    "theme_update",
)
</file>

<file path="plotnine/themes/seaborn_rcmod.py">
# type: ignore

"""Functions that alter the matplotlib rc dictionary on the fly."""

import functools

import matplotlib as _mpl

# https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py
# License: BSD-3-Clause License
#
# Modifications
# ---------------
# modified set_theme()
# removed set_palette(), reset_defaults(), reset_orig()
#
# We (plotnine) do not want to modify the rcParams
# on the matplotlib instance, so we create a dummy object
# The set_* function work on the rcParams dict on that
# object and then set() returns it. Then outside this
# file we only need to call the set() function.


class dummy:
    """
    No Op
    """

    __version__ = _mpl.__version__
    rcParams = {}


mpl = dummy()


_style_keys = [
    "axes.facecolor",
    "axes.edgecolor",
    "axes.grid",
    "axes.axisbelow",
    "axes.labelcolor",
    "figure.facecolor",
    "grid.color",
    "grid.linestyle",
    "text.color",
    "xtick.color",
    "ytick.color",
    "xtick.direction",
    "ytick.direction",
    "lines.solid_capstyle",
    "patch.edgecolor",
    "patch.force_edgecolor",
    "image.cmap",
    "font.family",
    "font.sans-serif",
    "xtick.bottom",
    "xtick.top",
    "ytick.left",
    "ytick.right",
    "axes.spines.left",
    "axes.spines.bottom",
    "axes.spines.right",
    "axes.spines.top",
]

_context_keys = [
    "font.size",
    "axes.labelsize",
    "axes.titlesize",
    "xtick.labelsize",
    "ytick.labelsize",
    "legend.fontsize",
    "legend.title_fontsize",
    "axes.linewidth",
    "grid.linewidth",
    "lines.linewidth",
    "lines.markersize",
    "patch.linewidth",
    "xtick.major.width",
    "ytick.major.width",
    "xtick.minor.width",
    "ytick.minor.width",
    "xtick.major.size",
    "ytick.major.size",
    "xtick.minor.size",
    "ytick.minor.size",
]


def set_theme(
    context="notebook",
    style="darkgrid",
    palette="deep",
    font="sans-serif",
    font_scale=1,
    color_codes=False,
    rc=None,
):
    """
    Set aesthetic parameters in one step

    Each set of parameters can be set directly or temporarily, see the
    referenced functions below for more information.

    Parameters
    ----------
    context : string or dict
        Plotting context parameters, see :func:`plotting_context`
    style : string or dict
        Axes style parameters, see :func:`axes_style`
    palette : string or sequence
        Color palette, see :func:`color_palette`
    font : string
        Font family, see matplotlib font manager.
    font_scale : float
        Separate scaling factor to independently scale the size of the
        font elements.
    color_codes : bool
        If `True` and `palette` is a seaborn palette, remap the shorthand
        color codes (e.g. "b", "g", "r", etc.) to the colors from this palette.
    rc : dict or None
        Dictionary of rc parameter mappings to override the above.

    """
    set_context(context, font_scale)
    set_style(style, rc={"font.family": font})
    if rc is not None:
        mpl.rcParams.update(rc)
    return mpl.rcParams


def set(*args, **kwargs):
    """
    Alias for :func:`set_theme`, which is the preferred interface

    This function may be removed in the future.
    """
    set_theme(*args, **kwargs)


def axes_style(style=None, rc=None):
    """
    Return a parameter dict for the aesthetic style of the plots

    This affects things like the color of the axes, whether a grid is
    enabled by default, and other aesthetic elements.

    This function returns an object that can be used in a `with` statement
    to temporarily change the style parameters.

    Parameters
    ----------
    style : "darkgrid" | "whitegrid" | "dark" | "white" | "ticks" | dict | None
        A dictionary of parameters or the name of a preconfigured set.
    rc : dict
        Parameter mappings to override the values in the preset seaborn
        style dictionaries. This only updates parameters that are
        considered part of the style definition.

    Examples
    --------
    >>> st = axes_style("whitegrid")

    >>> set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

    >>> import matplotlib.pyplot as plt
    >>> with axes_style("white"):
    ...     f, ax = plt.subplots()
    ...     ax.plot(x, y)               # doctest: +SKIP

    See Also
    --------
    set_style : set the matplotlib parameters for a seaborn theme
    plotting_context : return a parameter dict to to scale plot elements
    color_palette : define the color palette for a plot

    """
    if style is None:
        style_dict = {k: mpl.rcParams[k] for k in _style_keys}

    elif isinstance(style, dict):
        style_dict = style

    else:
        styles = ["white", "dark", "whitegrid", "darkgrid", "ticks"]
        if style not in styles:
            raise ValueError(f"style must be one of {', '.join(styles)}")

        # Define colors here
        dark_gray = ".15"
        light_gray = ".8"

        # Common parameters
        style_dict = {
            "figure.facecolor": "white",
            "axes.labelcolor": dark_gray,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.color": dark_gray,
            "ytick.color": dark_gray,
            "axes.axisbelow": True,
            "grid.linestyle": "-",
            "text.color": dark_gray,
            "font.family": ["sans-serif"],
            "font.sans-serif": [
                "Arial",
                "DejaVu Sans",
                "Liberation Sans",
                "Bitstream Vera Sans",
                "sans-serif",
            ],
            "lines.solid_capstyle": "round",
            "patch.edgecolor": "w",
            "patch.force_edgecolor": True,
            "image.cmap": "Greys",
            "xtick.top": False,
            "ytick.right": False,
        }

        # Set grid on or off
        if "grid" in style:
            style_dict.update(
                {
                    "axes.grid": True,
                }
            )
        else:
            style_dict.update(
                {
                    "axes.grid": False,
                }
            )

        # Set the color of the background, spines, and grids
        if style.startswith("dark"):
            style_dict.update(
                {
                    "axes.facecolor": "#EAEAF2",
                    "axes.edgecolor": "white",
                    "grid.color": "white",
                    "axes.spines.left": True,
                    "axes.spines.bottom": True,
                    "axes.spines.right": True,
                    "axes.spines.top": True,
                }
            )

        elif style == "whitegrid":
            style_dict.update(
                {
                    "axes.facecolor": "white",
                    "axes.edgecolor": light_gray,
                    "grid.color": light_gray,
                    "axes.spines.left": True,
                    "axes.spines.bottom": True,
                    "axes.spines.right": True,
                    "axes.spines.top": True,
                }
            )

        elif style in ["white", "ticks"]:
            style_dict.update(
                {
                    "axes.facecolor": "white",
                    "axes.edgecolor": dark_gray,
                    "grid.color": light_gray,
                    "axes.spines.left": True,
                    "axes.spines.bottom": True,
                    "axes.spines.right": True,
                    "axes.spines.top": True,
                }
            )

        # Show or hide the axes ticks
        if style == "ticks":
            style_dict.update(
                {
                    "xtick.bottom": True,
                    "ytick.left": True,
                }
            )
        else:
            style_dict.update(
                {
                    "xtick.bottom": False,
                    "ytick.left": False,
                }
            )

    # Remove entries that are not defined in the base list of valid keys
    # This lets us handle matplotlib <=/> 2.0
    style_dict = {k: v for k, v in style_dict.items() if k in _style_keys}

    # Override these settings with the provided rc dictionary
    if rc is not None:
        rc = {k: v for k, v in rc.items() if k in _style_keys}
        style_dict.update(rc)

    # Wrap in an _AxesStyle object so this can be used in a with statement
    style_object = _AxesStyle(style_dict)

    return style_object


def set_style(style=None, rc=None):
    """
    Set the aesthetic style of the plots

    This affects things like the color of the axes, whether a grid is
    enabled by default, and other aesthetic elements.

    Parameters
    ----------
    style : "darkgrid" | "whitegrid" | "dark" | "white" | "ticks" | dict | None
        A dictionary of parameters or the name of a preconfigured set.
    rc : dict
        Parameter mappings to override the values in the preset seaborn
        style dictionaries. This only updates parameters that are
        considered part of the style definition.

    Examples
    --------
    >>> set_style("whitegrid")

    >>> set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

    See Also
    --------
    axes_style : return a dict of parameters or use in a `with` statement
                 to temporarily set the style.
    set_context : set parameters to scale plot elements
    set_palette : set the default color palette for figures

    """
    style_object = axes_style(style, rc)
    mpl.rcParams.update(style_object)


def plotting_context(context=None, font_scale=1, rc=None):
    """
    Return a parameter dict to scale elements of the figure

    This affects things like the size of the labels, lines, and other
    elements of the plot, but not the overall style. The base context
    is "notebook", and the other contexts are "paper", "talk", and "poster",
    which are version of the notebook parameters scaled by .8, 1.3, and 1.6,
    respectively.

    This function returns an object that can be used in a `with` statement
    to temporarily change the context parameters.

    Parameters
    ----------
    context : dict, None, or one of {paper, notebook, talk, poster}
        A dictionary of parameters or the name of a preconfigured set.
    font_scale : float, optional
        Separate scaling factor to independently scale the size of the
        font elements.
    rc : dict, optional
        Parameter mappings to override the values in the preset seaborn
        context dictionaries. This only updates parameters that are
        considered part of the context definition.

    Examples
    --------
    >>> c = plotting_context("poster")

    >>> c = plotting_context("notebook", font_scale=1.5)

    >>> c = plotting_context("talk", rc={"lines.linewidth": 2})

    >>> import matplotlib.pyplot as plt
    >>> with plotting_context("paper"):
    ...     f, ax = plt.subplots()
    ...     ax.plot(x, y)                 # doctest: +SKIP

    See Also
    --------
    set_context : set the matplotlib parameters to scale plot elements
    axes_style : return a dict of parameters defining a figure style
    color_palette : define the color palette for a plot
    """
    if context is None:
        context_dict = {k: mpl.rcParams[k] for k in _context_keys}

    elif isinstance(context, dict):
        context_dict = context

    else:
        contexts = ["paper", "notebook", "talk", "poster"]
        if context not in contexts:
            raise ValueError(f"context must be in {', '.join(contexts)}")

        # Set up dictionary of default parameters
        texts_base_context = {
            "font.size": 12,
            "axes.labelsize": 12,
            "axes.titlesize": 12,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 11,
            "legend.title_fontsize": 12,
        }

        base_context = {
            "axes.linewidth": 1.25,
            "grid.linewidth": 1,
            "lines.linewidth": 1.5,
            "lines.markersize": 6,
            "patch.linewidth": 1,
            "xtick.major.width": 1.25,
            "ytick.major.width": 1.25,
            "xtick.minor.width": 1,
            "ytick.minor.width": 1,
            "xtick.major.size": 6,
            "ytick.major.size": 6,
            "xtick.minor.size": 4,
            "ytick.minor.size": 4,
        }
        base_context.update(texts_base_context)

        # Scale all the parameters by the same factor depending on the context
        scaling = {"paper": 0.8, "notebook": 1, "talk": 1.5, "poster": 2}[
            context
        ]
        context_dict = {k: v * scaling for k, v in base_context.items()}

        # Now independently scale the fonts
        font_keys = texts_base_context.keys()
        font_dict = {k: context_dict[k] * font_scale for k in font_keys}
        context_dict.update(font_dict)

    # Override these settings with the provided rc dictionary
    if rc is not None:
        rc = {k: v for k, v in rc.items() if k in _context_keys}
        context_dict.update(rc)

    # Wrap in a _PlottingContext object so this can be used in a with statement
    context_object = _PlottingContext(context_dict)

    return context_object


def set_context(context=None, font_scale=1, rc=None):
    """
    Set the plotting context parameters

    This affects things like the size of the labels, lines, and other
    elements of the plot, but not the overall style. The base context
    is "notebook", and the other contexts are "paper", "talk", and "poster",
    which are version of the notebook parameters scaled by .8, 1.3, and 1.6,
    respectively.

    Parameters
    ----------
    context : dict, None, or one of {paper, notebook, talk, poster}
        A dictionary of parameters or the name of a preconfigured set.
    font_scale : float, optional
        Separate scaling factor to independently scale the size of the
        font elements.
    rc : dict, optional
        Parameter mappings to override the values in the preset seaborn
        context dictionaries. This only updates parameters that are
        considered part of the context definition.

    Examples
    --------
    >>> set_context("paper")

    >>> set_context("talk", font_scale=1.4)

    >>> set_context("talk", rc={"lines.linewidth": 2})

    See Also
    --------
    plotting_context : return a dictionary of rc parameters, or use in
                       a `with` statement to temporarily set the context.
    set_style : set the default parameters for figure style
    set_palette : set the default color palette for figures

    """
    context_object = plotting_context(context, font_scale, rc)
    mpl.rcParams.update(context_object)


class _RCAesthetics(dict):
    def __enter__(self):
        rc = mpl.rcParams
        self._orig = {k: rc[k] for k in self._keys}
        self._set(self)

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._set(self._orig)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper


class _AxesStyle(_RCAesthetics):
    """Light wrapper on a dict to set style temporarily."""

    _keys = _style_keys
    _set = staticmethod(set_style)


class _PlottingContext(_RCAesthetics):
    """Light wrapper on a dict to set context temporarily."""

    _keys = _context_keys
    _set = staticmethod(set_context)
</file>

<file path="plotnine/themes/theme_538.py">
from .elements import element_blank, element_line, element_rect, element_text
from .theme import theme
from .theme_gray import theme_gray


class theme_538(theme_gray):
    """
    Theme in the likeness of fivethirtyeight.com plots

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family.
    """

    def __init__(self, base_size=11, base_family="DejaVu Sans"):
        super().__init__(base_size, base_family)
        bgcolor = "#F0F0F0"
        self += theme(
            axis_ticks=element_blank(),
            title=element_text(color="#3C3C3C"),
            legend_background=element_rect(fill="none"),
            panel_background=element_rect(fill=bgcolor),
            panel_border=element_blank(),
            panel_grid_major=element_line(color="#D5D5D5"),
            panel_grid_minor=element_blank(),
            plot_background=element_rect(fill=bgcolor, color=bgcolor, size=1),
            strip_background=element_rect(size=0),
        )
</file>

<file path="plotnine/themes/theme_bw.py">
from .elements import element_line, element_rect, element_text
from .theme import theme
from .theme_gray import theme_gray


class theme_bw(theme_gray):
    """
    White background with black gridlines

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        super().__init__(base_size, base_family)
        self += theme(
            axis_text=element_text(size=0.8 * base_size),
            panel_background=element_rect(fill="white"),
            panel_border=element_rect(fill="none", color="#7f7f7f"),
            panel_grid_major=element_line(color="#E5E5E5"),
            panel_grid_minor=element_line(color="#FAFAFA"),
            strip_background=element_rect(
                fill="#CCCCCC", color="#7F7F7F", size=1
            ),
        )
</file>

<file path="plotnine/themes/theme_classic.py">
from .elements import element_blank, element_line, element_rect
from .theme import theme
from .theme_bw import theme_bw


class theme_classic(theme_bw):
    """
    A classic-looking theme, with x & y axis lines and no gridlines

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        super().__init__(base_size, base_family)
        self += theme(
            panel_border=element_blank(),
            axis_line=element_line(color="black"),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            strip_background=element_rect(colour="black", fill="none", size=1),
            legend_key=element_blank(),
        )
</file>

<file path="plotnine/themes/theme_dark.py">
from .elements import element_blank, element_line, element_rect, element_text
from .theme import theme
from .theme_gray import theme_gray


class theme_dark(theme_gray):
    """
    The dark cousin of [](`~plotnine.themes.theme_light.theme_light`)

    It has  similar line sizes but a dark background. Useful to
    make thin colored lines pop out.

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        super().__init__(base_size, base_family)
        self += theme(
            axis_ticks=element_line(color="#666666", size=0.5),
            axis_ticks_minor=element_blank(),
            panel_background=element_rect(fill="#7F7F7F", color="none"),
            panel_grid_major=element_line(color="#666666", size=0.5),
            panel_grid_minor=element_line(color="#737373", size=0.25),
            strip_background=element_rect(fill="#333333", color="none"),
            strip_text_x=element_text(color="white"),
            strip_text_y=element_text(color="white", angle=-90),
        )
</file>

<file path="plotnine/themes/theme_light.py">
from .elements import element_blank, element_line, element_rect, element_text
from .theme import theme
from .theme_gray import theme_gray


class theme_light(theme_gray):
    """
    A theme similar to [](`~plotnine.themes.theme_linedraw.theme_linedraw`)

    Has light grey lines lines and axes to direct more attention
    towards the data.

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        super().__init__(base_size, base_family)
        self += theme(
            axis_ticks=element_line(color="#B3B3B3", size=0.5),
            axis_ticks_minor=element_blank(),
            legend_key=element_rect(color="#7F7F7F", size=0.72),
            panel_background=element_rect(fill="white"),
            panel_border=element_rect(fill="none", color="#B3B3B3", size=1),
            panel_grid_major=element_line(color="#D9D9D9", size=0.5),
            panel_grid_minor=element_line(color="#EDEDED", size=0.25),
            strip_background=element_rect(
                fill="#B3B3B3", color="#B3B3B3", size=1
            ),
            strip_text_x=element_text(color="white"),
            strip_text_y=element_text(color="white", angle=-90),
        )
</file>

<file path="plotnine/themes/theme_linedraw.py">
from .elements import element_blank, element_line, element_rect, element_text
from .theme import theme
from .theme_bw import theme_bw


class theme_linedraw(theme_bw):
    """
    A theme with only black lines of various widths on white backgrounds

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        super().__init__(base_size, base_family)
        self += theme(
            axis_text=element_text(color="black", size=base_size * 0.8),
            axis_ticks=element_line(color="black", size=0.5),
            axis_ticks_minor=element_blank(),
            legend_key=element_rect(color="black", size=0.72),
            panel_background=element_rect(fill="white"),
            panel_border=element_rect(fill="none", color="black", size=1),
            panel_grid_major=element_line(color="black", size=0.1),
            panel_grid_minor=element_line(color="black", size=0.02),
            strip_background=element_rect(fill="black", color="black", size=1),
            strip_text_x=element_text(color="white"),
            strip_text_y=element_text(color="white", angle=-90),
        )
</file>

<file path="plotnine/themes/theme_minimal.py">
from .elements import element_blank
from .theme import theme
from .theme_bw import theme_bw


class theme_minimal(theme_bw):
    """
    A minimalistic theme with no background annotations

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        super().__init__(base_size, base_family)
        self += theme(
            axis_ticks=element_blank(),
            legend_background=element_blank(),
            legend_key=element_blank(),
            panel_background=element_blank(),
            panel_border=element_blank(),
            plot_background=element_blank(),
            strip_background=element_blank(),
        )
</file>

<file path="plotnine/themes/theme_tufte.py">
from .elements import element_blank
from .theme import theme
from .theme_bw import theme_bw


class theme_tufte(theme_bw):
    """
    Tufte Maximal Data, Minimal Ink Theme

    Theme based on Chapter 6 Data-Ink Maximization and Graphical
    Design of Edward Tufte *The Visual Display of Quantitative
    Information*. No border, no axis lines, no grids. This theme
    works best in combination with
    [](`~plotnine.geoms.geom_rug.geom_rug`).

    The default font family is set to "serif" as he uses serif
    fonts for labels in _The Visual Display of Quantitative
    Information_. The serif font used by Tufte in his books is
    a variant of Bembo, while the sans serif font is Gill Sans.
    If these fonts are installed on your system, consider setting
    them explicitly via the argument `base_family`.

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    ticks: bool
        Whether to show axis ticks.

    References
    ----------
    Tufte, Edward R. (2001) The Visual Display of Quantitative
    Information, Chapter 6.

    Translated from the R ggthemes package by hyiltiz <hyiltiz@gmail.com>.
    Released under GNU GPL v2 license or later.
    """

    def __init__(self, base_size=11, base_family=None, ticks=True):
        theme_bw.__init__(self, base_size, base_family)
        self += theme(
            axis_line=element_blank(),
            axis_ticks=None if ticks else element_blank(),
            legend_background=element_blank(),
            legend_key=element_blank(),
            panel_background=element_blank(),
            panel_border=element_blank(),
            panel_grid=element_blank(),
            plot_background=element_blank(),
            strip_background=element_blank(),
        )
</file>

<file path="plotnine/themes/theme_xkcd.py">
from .elements import element_blank, element_line, element_rect, element_text
from .theme import theme
from .theme_gray import theme_gray


class theme_xkcd(theme_gray):
    """
    xkcd theme

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    scale : float
        The amplitude of the wiggle perpendicular to the line (in pixels)
    length : float
        The length of the wiggle along the line (in pixels).
    randomness : float
        The factor by which the length is randomly scaled. Default is 2.
    stroke_size : float
        Size of the stroke to apply to the lines and text paths.
    stroke_color : str | tuple
        Color of the strokes. Use `"none"` for no color.
    """

    def __init__(
        self,
        base_size=12,
        scale=1,
        length=100,
        randomness=2,
        stroke_size=3,
        stroke_color="white",
    ):
        from matplotlib import patheffects

        super().__init__(base_size)
        sketch_params = (scale, length, randomness)
        path_effects = [
            patheffects.withStroke(
                linewidth=stroke_size, foreground=stroke_color
            )
        ]
        self += theme(
            text=element_text(family=["xkcd", "Humor Sans", "Comic Sans MS"]),
            axis_ticks=element_line(color="black", size=1),
            axis_ticks_minor=element_blank(),
            axis_ticks_length_major=-6,
            legend_background=element_rect(color="black"),
            legend_box_margin=2,
            legend_margin=5,
            panel_border=element_rect(color="black", size=1),
            panel_grid=element_blank(),
            panel_background=element_rect(fill="white"),
            strip_background=element_rect(color="black", fill="white"),
            strip_background_x=element_rect(width=2 / 3),
            strip_background_y=element_rect(height=2 / 3),
            strip_align=-0.5,
        )

        self._rcParams.update(
            {
                "axes.unicode_minus": False,
                "path.sketch": sketch_params,
                "path.effects": path_effects,
            }
        )
</file>

<file path="plotnine/facets/facet_wrap.py">
from __future__ import annotations

import re
import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import join_keys, match
from ..exceptions import PlotnineError, PlotnineWarning
from .facet import (
    add_missing_facets,
    combine_vars,
    eval_facet_vars,
    facet,
    layout_null,
)
from .strips import Strips, strip

if typing.TYPE_CHECKING:
    from typing import Literal, Optional, Sequence

    from matplotlib.axes import Axes

    from plotnine.iapi import layout_details


class facet_wrap(facet):
    """
    Wrap 1D Panels onto 2D surface

    Parameters
    ----------
    facets :
        Variables to groupby and plot on different panels.
        If a string formula is used it should be right sided,
        e.g `"~ a + b"`, `("a", "b")`
    nrow : int, default=None
        Number of rows
    ncol : int, default=None
        Number of columns
    scales :
        Whether `x` or `y` scales should be allowed (free)
        to vary according to the data on each of the panel.
    shrink :
        Whether to shrink the scales to the output of the
        statistics instead of the raw data.
    labeller :
        How to label the facets. A string value if it should be
        one of `["label_value", "label_both", "label_context"]`{.py}.
    as_table :
        If `True`, the facets are laid out like a table with
        the highest values at the bottom-right. If `False`
        the facets are laid out like a plot with the highest
        value a the top-right
    drop :
        If `True`, all factor levels not used in the data
        will automatically be dropped. If `False`, all
        factor levels will be shown, regardless of whether
        or not they appear in the data.
    dir :
        Direction in which to layout the panels. `h` for
        horizontal and `v` for vertical.
    """

    def __init__(
        self,
        facets: Optional[str | Sequence[str]] = None,
        *,
        nrow: Optional[int] = None,
        ncol: Optional[int] = None,
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
        dir: Literal["h", "v"] = "h",
    ):
        super().__init__(
            scales=scales,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
            dir=dir,
        )
        self.vars = parse_wrap_facets(facets)
        self._nrow, self._ncol = check_dimensions(nrow, ncol)

    def compute_layout(
        self,
        data: list[pd.DataFrame],
    ) -> pd.DataFrame:
        if not self.vars:
            self.nrow, self.ncol = 1, 1
            return layout_null()

        base = combine_vars(data, self.environment, self.vars, drop=self.drop)
        n = len(base)
        dims = wrap_dims(n, self._nrow, self._ncol)
        _id = np.arange(1, n + 1)

        if self.dir == "v":
            dims = dims[::-1]

        if self.as_table:
            row = (_id - 1) // dims[1] + 1
        else:
            row = dims[0] - (_id - 1) // dims[1]

        col = (_id - 1) % dims[1] + 1

        layout = pd.DataFrame(
            {
                "PANEL": pd.Categorical(range(1, n + 1)),  # pyright: ignore[reportArgumentType]
                "ROW": row.astype(int),
                "COL": col.astype(int),
            }
        )
        if self.dir == "v":
            layout.rename(columns={"ROW": "COL", "COL": "ROW"}, inplace=True)

        layout = pd.concat([layout, base], axis=1)
        self.nrow = layout["ROW"].nunique()
        self.ncol = layout["COL"].nunique()
        n = layout.shape[0]

        # Add scale identification
        layout["SCALE_X"] = range(1, n + 1) if self.free["x"] else 1
        layout["SCALE_Y"] = range(1, n + 1) if self.free["y"] else 1

        # Figure out where axes should go.
        # The bottom-most row of each column and the left most
        # column of each row
        x_idx = [df["ROW"].idxmax() for _, df in layout.groupby("COL")]
        y_idx = [df["COL"].idxmin() for _, df in layout.groupby("ROW")]
        layout["AXIS_X"] = False
        layout["AXIS_Y"] = False
        _loc = layout.columns.get_loc
        layout.iloc[x_idx, _loc("AXIS_X")] = True  # type: ignore
        layout.iloc[y_idx, _loc("AXIS_Y")] = True  # type: ignore

        if self.free["x"]:
            layout.loc[:, "AXIS_X"] = True

        if self.free["y"]:
            layout.loc[:, "AXIS_Y"] = True

        return layout

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        if not len(data):
            data["PANEL"] = pd.Categorical(
                [], categories=layout["PANEL"].cat.categories, ordered=True
            )
            return data

        facet_vals = eval_facet_vars(data, self.vars, self.environment)
        data, facet_vals = add_missing_facets(
            data, layout, self.vars, facet_vals
        )

        # assign each point to a panel
        if len(facet_vals) and len(facet_vals.columns):
            keys = join_keys(facet_vals, layout, self.vars)
            data["PANEL"] = match(keys["x"], keys["y"], start=1)
        else:
            # Special case of no facetting
            data["PANEL"] = 1

        # matching dtype
        data["PANEL"] = pd.Categorical(
            data["PANEL"],
            categories=layout["PANEL"].cat.categories,
            ordered=True,
        )

        data.reset_index(drop=True, inplace=True)
        return data

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        if not self.vars:
            return Strips([])

        s = strip(self.vars, layout_info, self, ax, "top")
        return Strips([s])


def check_dimensions(
    nrow: Optional[int], ncol: Optional[int]
) -> tuple[int | None, int | None]:
    """
    Verify dimensions of the facet
    """
    if nrow is not None:
        if nrow < 1:
            warn(
                "'nrow' must be greater than 0. Your value has been ignored.",
                PlotnineWarning,
            )
            nrow = None
        else:
            nrow = int(nrow)

    if ncol is not None:
        if ncol < 1:
            warn(
                "'ncol' must be greater than 0. Your value has been ignored.",
                PlotnineWarning,
            )
            ncol = None
        else:
            ncol = int(ncol)

    return nrow, ncol


def parse_wrap_facets(facets: Optional[str | Sequence[str]]) -> Sequence[str]:
    """
    Return list of facetting variables
    """
    if facets is None:
        return []
    elif isinstance(facets, str):
        if "~" in facets:
            return parse_wrap_facets_old(facets)  # formala
        else:
            return [facets]
    return facets


def parse_wrap_facets_old(facets: str | Sequence[str]) -> Sequence[str]:
    """
    Return list of facetting variables

    This handles the old & silently deprecated r-style formulas
    """
    valid_forms = ["~ var1", "~ var1 + var2"]
    error_msg = f"Valid formula for 'facet_wrap' look like {valid_forms}"

    if isinstance(facets, (list, tuple)):
        return facets

    if not isinstance(facets, str):
        raise PlotnineError(error_msg)

    if "~" in facets:
        variables_pattern = r"(\w+(?:\s*\+\s*\w+)*|\.)"
        pattern = rf"\s*~\s*{variables_pattern}\s*"
        match = re.match(pattern, facets)
        if not match:
            raise PlotnineError(error_msg)

        facets = [var.strip() for var in match.group(1).split("+")]
    elif re.match(r"\w+", facets):
        # allow plain string as the variable name
        facets = [facets]
    else:
        raise PlotnineError(error_msg)

    return facets


def wrap_dims(
    n: int, nrow: Optional[int] = None, ncol: Optional[int] = None
) -> tuple[int, int]:
    """
    Wrap dimensions
    """
    if nrow is None:
        if ncol is None:
            return n_to_nrow_ncol(n)
        else:
            nrow = int(np.ceil(n / ncol))

    if ncol is None:
        ncol = int(np.ceil(n / nrow))

    if not nrow * ncol >= n:
        raise PlotnineError(
            "Allocated fewer panels than are required. "
            "Make sure the number of rows and columns can "
            "hold all the plot panels."
        )
    return (nrow, ncol)


def n_to_nrow_ncol(n: int) -> tuple[int, int]:
    """
    Compute the rows and columns given the number of plots.
    """
    if n <= 3:
        nrow, ncol = 1, n
    elif n <= 6:
        nrow, ncol = 2, (n + 1) // 2
    elif n <= 12:
        nrow, ncol = 3, (n + 2) // 3
    else:
        ncol = int(np.ceil(np.sqrt(n)))
        nrow = int(np.ceil(n / ncol))
    return (nrow, ncol)
</file>

<file path="plotnine/geoms/annotate.py">
from __future__ import annotations

import typing

import pandas as pd

from .._utils import is_scalar
from .._utils.registry import Registry
from ..exceptions import PlotnineError
from ..geoms.geom import geom as geom_base_class
from ..mapping import aes
from ..mapping.aes import POSITION_AESTHETICS

if typing.TYPE_CHECKING:
    from typing import Any

    from plotnine import ggplot


class annotate:
    """
    Create an annotation layer

    Parameters
    ----------
    geom :
        geom to use for annotation, or name of geom (e.g. 'point').
    x :
        Position
    y :
        Position
    xmin :
        Position
    ymin :
        Position
    xmax :
        Position
    ymax :
        Position
    xend :
        Position
    yend :
        Position
    xintercept :
        Position
    yintercept :
        Position
    kwargs :
        Other aesthetics or parameters to the geom.

    Notes
    -----
    The positioning aethetics `x, y, xmin, ymin, xmax, ymax, xend, yend,
    xintercept, yintercept` depend on which `geom` is used.

    You should choose or ignore accordingly.

    All `geoms` are created with `stat="identity"`{.py}.
    """

    _annotation_geom: geom_base_class

    def __init__(
        self,
        geom: str | type[geom_base_class],
        x: float | list[float] | None = None,
        y: float | list[float] | None = None,
        xmin: float | list[float] | None = None,
        xmax: float | list[float] | None = None,
        xend: float | list[float] | None = None,
        xintercept: float | list[float] | None = None,
        ymin: float | list[float] | None = None,
        ymax: float | list[float] | None = None,
        yend: float | list[float] | None = None,
        yintercept: float | list[float] | None = None,
        **kwargs: Any,
    ):
        variables = locals()

        # position only, and combined aesthetics
        pos_aesthetics = {
            loc: variables[loc]
            for loc in POSITION_AESTHETICS
            if variables[loc] is not None
        }
        aesthetics = pos_aesthetics.copy()
        aesthetics.update(kwargs)

        # Check if the aesthetics are of compatible lengths
        lengths, info_tokens = [], []
        for ae, val in aesthetics.items():
            if is_scalar(val):
                continue
            lengths.append(len(val))
            info_tokens.append((ae, len(val)))

        if len(set(lengths)) > 1:
            details = ", ".join([f"{n} ({l})" for n, l in info_tokens])
            msg = f"Unequal parameter lengths: {details}"
            raise PlotnineError(msg)

        # Stop pandas from complaining about all scalars
        if all(is_scalar(val) for val in pos_aesthetics.values()):
            for ae in pos_aesthetics:
                pos_aesthetics[ae] = [pos_aesthetics[ae]]
                break

        data = pd.DataFrame(pos_aesthetics)
        if isinstance(geom, str):
            geom_klass: type[geom_base_class] = Registry[f"geom_{geom}"]
        elif isinstance(geom, type) and issubclass(geom, geom_base_class):
            geom_klass = geom
        else:
            raise PlotnineError(
                "geom must either be a plotnine.geom.geom() "
                "descendant (e.g. plotnine.geom_point), or "
                "a string naming a geom (e.g. 'point', 'text', "
                f"...). Got {repr(geom)}"
            )

        mappings = aes(**{str(ae): ae for ae in data.columns})

        # The positions are mapped, the rest are manual settings
        self._annotation_geom = geom_klass(
            mappings,
            data,
            stat="identity",
            inherit_aes=False,
            show_legend=False,
            **kwargs,
        )

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add to ggplot
        """
        from ..layer import layer

        other += layer(geom=self._annotation_geom)
        return other
</file>

<file path="plotnine/geoms/annotation_logticks.py">
from __future__ import annotations

import typing
import warnings

import numpy as np
import pandas as pd

from .._utils import log
from ..coords import coord_flip
from ..exceptions import PlotnineWarning
from ..scales.scale_continuous import scale_continuous as ScaleContinuous
from .annotate import annotate
from .geom_path import geom_path
from .geom_rug import geom_rug

if typing.TYPE_CHECKING:
    from typing import Any, Literal, Optional, Sequence

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.geoms.geom import geom
    from plotnine.iapi import panel_view
    from plotnine.typing import AnyArray


class _geom_logticks(geom_rug):
    """
    Internal geom implementing drawing of annotation_logticks
    """

    DEFAULT_AES = {}
    DEFAULT_PARAMS = {
        "sides": "bl",
        "alpha": 1,
        "color": "black",
        "size": 0.5,
        "linetype": "solid",
        "lengths": (0.036, 0.0225, 0.012),
        "base": 10,
    }
    draw_legend = staticmethod(geom_path.draw_legend)

    def draw_layer(self, data: pd.DataFrame, layout: Layout, coord: coord):
        """
        Draw ticks on every panel
        """
        for pid in layout.layout["PANEL"]:
            ploc = pid - 1
            panel_params = layout.panel_params[ploc]
            ax = layout.axs[ploc]
            self.draw_panel(data, panel_params, coord, ax)

    @staticmethod
    def _check_log_scale(
        base: Optional[float],
        sides: str,
        panel_params: panel_view,
        coord: coord,
    ) -> tuple[float, float]:
        """
        Check the log transforms

        Parameters
        ----------
        base : float | None
            Base of the logarithm in which the ticks will be
            calculated. If `None`, the base of the log transform
            the scale will be used.
        sides : str, default="bl"
            Sides onto which to draw the marks. Any combination
            chosen from the characters `btlr`, for *bottom*, *top*,
            *left* or *right* side marks. If `coord_flip()` is used,
            these are the sides *before* the flip.
        panel_params : panel_view
            `x` and `y` view scale values.
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the geom.

        Returns
        -------
        out : tuple
            The bases (base_x, base_y) to use when generating the ticks.
        """

        def get_base(sc, ubase: Optional[float]) -> float:
            ae = sc.aesthetics[0]

            if not isinstance(sc, ScaleContinuous) or not sc.is_log_scale:
                warnings.warn(
                    f"annotation_logticks for {ae}-axis which does not have "
                    "a log scale. The logticks may not make sense.",
                    PlotnineWarning,
                )
                return 10 if ubase is None else ubase

            base = sc._trans.base  # pyright: ignore
            if ubase is not None and base != ubase:
                warnings.warn(
                    f"The x-axis is log transformed in base={base} ,"
                    "but the annotation_logticks are computed in base="
                    f"{ubase}",
                    PlotnineWarning,
                )
                return ubase
            return base

        base_x, base_y = 10, 10
        x_scale = panel_params.x.scale
        y_scale = panel_params.y.scale

        if isinstance(coord, coord_flip):
            x_scale, y_scale = y_scale, x_scale
            base_x, base_y = base_y, base_x

        if "t" in sides or "b" in sides:
            base_x = get_base(x_scale, base)

        if "l" in sides or "r" in sides:
            base_y = get_base(y_scale, base)

        return base_x, base_y

    @staticmethod
    def _calc_ticks(
        value_range: tuple[float, float], base: float
    ) -> tuple[AnyArray, AnyArray, AnyArray]:
        """
        Calculate tick marks within a range

        Parameters
        ----------
        value_range: tuple
            Range for which to calculate ticks.

        base : number
            Base of logarithm

        Returns
        -------
        out: tuple
            (major, middle, minor) tick locations
        """

        def _minor(x: Sequence[Any], mid_idx: int) -> AnyArray:
            return np.hstack([x[1:mid_idx], x[mid_idx + 1 : -1]])

        # * Calculate the low and high powers,
        # * Generate for all intervals in along the low-high power range
        #   The intervals are in normal space
        # * Calculate evenly spaced breaks in normal space, then convert
        #   them to log space.
        low = np.floor(value_range[0])
        high = np.ceil(value_range[1])
        arr = base ** np.arange(low, float(high + 1))
        n_ticks = int(np.round(base) - 1)
        breaks = [
            log(np.linspace(b1, b2, n_ticks + 1), base)
            for (b1, b2) in list(zip(arr, arr[1:]))
        ]

        # Partition the breaks in the 3 groups
        major = np.array([x[0] for x in breaks] + [breaks[-1][-1]])
        if n_ticks % 2:
            mid_idx = n_ticks // 2
            middle = np.array([x[mid_idx] for x in breaks])
            minor = np.hstack([_minor(x, mid_idx) for x in breaks])
        else:
            middle = np.array([])
            minor = np.hstack([x[1:-1] for x in breaks])

        return major, middle, minor

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        params = self.params
        # Any passed data is ignored, the relevant data is created
        sides = params["sides"]
        lengths = params["lengths"]
        _aesthetics = {
            "size": params["size"],
            "color": params["color"],
            "alpha": params["alpha"],
            "linetype": params["linetype"],
        }

        def _draw(
            geom: geom,
            axis: Literal["x", "y"],
            tick_positions: tuple[AnyArray, AnyArray, AnyArray],
        ):
            for position, length in zip(tick_positions, lengths):
                data = pd.DataFrame({axis: position, **_aesthetics})
                params["length"] = length
                geom.draw_group(data, panel_params, coord, ax, params)

        if isinstance(coord, coord_flip):
            tick_range_x = panel_params.y.range
            tick_range_y = panel_params.x.range
        else:
            tick_range_x = panel_params.x.range
            tick_range_y = panel_params.y.range

        # these are already flipped iff coord_flip
        base_x, base_y = self._check_log_scale(
            params["base"], sides, panel_params, coord
        )

        if "b" in sides or "t" in sides:
            tick_positions = self._calc_ticks(tick_range_x, base_x)
            _draw(self, "x", tick_positions)

        if "l" in sides or "r" in sides:
            tick_positions = self._calc_ticks(tick_range_y, base_y)
            _draw(self, "y", tick_positions)


class annotation_logticks(annotate):
    """
    Marginal log ticks.

    If added to a plot that does not have a log10 axis
    on the respective side, a warning will be issued.

    Parameters
    ----------
    sides :
        Sides onto which to draw the marks. Any combination
        chosen from the characters `btlr`, for *bottom*, *top*,
        *left* or *right* side marks. If `coord_flip()` is used,
        these are the sides *after* the flip.
    alpha :
        Transparency of the ticks
    color :
        Colour of the ticks
    size :
        Thickness of the ticks
    linetype :
        Type of line
    lengths:
        length of the ticks drawn for full / half / tenth
        ticks relative to panel size
    base :
        Base of the logarithm in which the ticks will be
        calculated. If `None`, the base used to log transform
        the scale will be used.
    """

    def __init__(
        self,
        sides: str = "bl",
        alpha: float = 1,
        color: str
        | tuple[float, float, float]
        | tuple[float, float, float, float] = "black",
        size: float = 0.5,
        linetype: Literal["solid", "dashed", "dashdot", "dotted"]
        | Sequence[float] = "solid",
        lengths: tuple[float, float, float] = (0.036, 0.0225, 0.012),
        base: float | None = None,
    ):
        if len(lengths) != 3:
            raise ValueError(
                "length for annotation_logticks must be a tuple of 3 floats"
            )

        self._annotation_geom = _geom_logticks(
            sides=sides,
            alpha=alpha,
            color=color,
            size=size,
            linetype=linetype,
            lengths=lengths,
            base=base,
            inherit_aes=False,
            show_legend=False,
        )
</file>

<file path="plotnine/geoms/annotation_stripes.py">
from __future__ import annotations

import typing
from itertools import cycle, islice

import numpy as np
import pandas as pd

from ..coords import coord_flip
from ..scales.scale_discrete import scale_discrete
from .annotate import annotate
from .geom import geom
from .geom_polygon import geom_polygon
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    from typing import Any, Literal, Sequence

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.iapi import panel_view


class annotation_stripes(annotate):
    """
    Alternating stripes, centered around each label.

    Useful as a background for geom_jitter.

    Parameters
    ----------
    fill :
        List of colors for the strips.
    fill_range :
        How to fill stripes beyond the range of scale:

        ```python
        "cycle"      # keep cycling the colors of the
                     # stripes after the range ends
        "nocycle"    # stop cycling the colors of the
                     # stripes after the range ends
        "auto"       # "cycle" for continuous scales and
                     # "nocycle" for discrete scales.
        "no"         # Do not add stripes passed the range
                     # passed the range of the scales
        ```
    direction :
        Orientation of the stripes
    extend :
        Range of the stripes. The default is (0, 1), top to bottom.
        The values should be in the range [0, 1].
    **kwargs :
        Other aesthetic parameters for the rectangular stripes.
        They include; `alpha`, `color`, `linetype`, and `size`.
    """

    def __init__(
        self,
        fill: Sequence[str] = ("#AAAAAA", "#CCCCCC"),
        fill_range: Literal["auto", "cycle", "no", "nocycle"] = "auto",
        direction: Literal["horizontal", "vertical"] = "vertical",
        extend: tuple[float, float] = (0, 1),
        **kwargs: Any,
    ):
        allowed = ("vertical", "horizontal")
        if direction not in allowed:
            raise ValueError(f"direction must be one of {allowed}")
        self._annotation_geom = _geom_stripes(
            fill=fill,
            fill_range=fill_range,
            extend=extend,
            direction=direction,
            inherit_aes=False,
            show_legend=False,
            **kwargs,
        )


class _geom_stripes(geom):
    DEFAULT_AES = {}
    REQUIRED_AES = set()
    DEFAULT_PARAMS = {
        "color": None,
        "fill": ("#AAAAAA", "#CCCCCC"),
        "linetype": "solid",
        "size": 1,
        "alpha": 0.5,
        "direction": "vertical",
        "extend": (0, 1),
        "fill_range": "auto",
    }
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def draw_layer(self, data: pd.DataFrame, layout: Layout, coord: coord):
        """
        Draw stripes on every panel
        """
        for pid in layout.layout["PANEL"]:
            ploc = pid - 1
            panel_params = layout.panel_params[ploc]
            ax = layout.axs[ploc]
            self.draw_group(data, panel_params, coord, ax, self.params)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        extend = params["extend"]
        fill_range = params["fill_range"]
        direction = params["direction"]

        # Range
        if direction == "vertical":
            axis, other_axis = "x", "y"
        else:
            axis, other_axis = "y", "x"

        if isinstance(coord, coord_flip):
            axis, other_axis = other_axis, axis

        _axis = getattr(panel_params, axis)
        breaks = _axis.breaks
        range = _axis.range
        other_range = getattr(panel_params, other_axis).range

        if fill_range == "auto":
            if isinstance(_axis.scale, scale_discrete):
                fill_range = "nocycle"
            else:
                fill_range = "cycle"

        # Breaks along the width
        n_stripes = len(breaks)
        if n_stripes > 1:
            diff = np.diff(breaks)
            step = diff[0]
            equal_spaces = np.all(diff == step)
            if not equal_spaces:
                raise ValueError(
                    "The major breaks are not equally spaced. "
                    "We cannot create stripes."
                )
        else:
            step = breaks[0]

        deltas = np.array([step / 2] * n_stripes)
        many_stripes = len(breaks) > 1
        xmin = breaks - deltas
        xmax = breaks + deltas
        if fill_range in ("cycle", "nocycle") and many_stripes:
            if range[0] < breaks[0]:
                n_stripes += 1
                xmax = np.insert(xmax, 0, xmin[0])
                xmin = np.insert(xmin, 0, range[0])
            if range[1] > breaks[1]:
                n_stripes += 1
                xmin = np.append(xmin, xmax[-1])
                xmax = np.append(xmax, range[1])

        # Height
        full_height = other_range[1] - other_range[0]
        ymin = other_range[0] + full_height * extend[0]
        ymax = other_range[0] + full_height * extend[1]
        fill = list(islice(cycle(params["fill"]), n_stripes))
        if fill_range == "nocycle" and many_stripes:
            # there are at least two stripes at this point
            fill[0] = fill[1]
            fill[-1] = fill[-2]

        if direction != "vertical":
            xmin, xmax, ymin, ymax = ymin, ymax, xmin, xmax

        data = pd.DataFrame(
            {
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax,
                "fill": fill,
                "alpha": params["alpha"],
                "color": params["color"],
                "linetype": params["linetype"],
                "size": params["size"],
            }
        )

        return geom_rect.draw_group(data, panel_params, coord, ax, params)
</file>

<file path="plotnine/geoms/geom_abline.py">
from __future__ import annotations

import typing
from typing import Sized
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import order_as_data_mapping
from ..doctools import document
from ..exceptions import PlotnineWarning
from ..mapping import aes
from .geom import geom
from .geom_path import geom_path
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import DataLike


@document
class geom_abline(geom):
    """
    Lines specified by slope and intercept

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "color": "black",
        "linetype": "solid",
        "alpha": 1,
        "size": 0.5,
    }
    DEFAULT_PARAMS = {"inherit_aes": False}
    REQUIRED_AES = {"slope", "intercept"}
    draw_legend = staticmethod(geom_path.draw_legend)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        data, mapping = order_as_data_mapping(data, mapping)
        slope = kwargs.pop("slope", None)
        intercept = kwargs.pop("intercept", None)

        # If nothing is set, it defaults to y=x
        if mapping is None and slope is None and intercept is None:
            slope = 1
            intercept = 0

        if slope is not None or intercept is not None:
            if mapping:
                warn(
                    "The 'intercept' and 'slope' when specified override "
                    "the aes() mapping.",
                    PlotnineWarning,
                )

            if isinstance(data, Sized) and len(data):
                warn(
                    "The 'intercept' and 'slope' when specified override "
                    "the data",
                    PlotnineWarning,
                )

            if slope is None:
                slope = 1
            if intercept is None:
                intercept = 0

            data = pd.DataFrame(
                {"intercept": np.repeat(intercept, 1), "slope": slope}
            )

            mapping = aes(intercept="intercept", slope="slope")
            kwargs["show_legend"] = False

        geom.__init__(self, mapping, data, **kwargs)

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        ranges = coord.backtransform_range(panel_params)
        data["x"] = ranges.x[0]
        data["xend"] = ranges.x[1]
        data["y"] = ranges.x[0] * data["slope"] + data["intercept"]
        data["yend"] = ranges.x[1] * data["slope"] + data["intercept"]
        data = data.drop_duplicates()

        for _, gdata in data.groupby("group"):
            gdata.reset_index(inplace=True)
            geom_segment.draw_group(
                gdata, panel_params, coord, ax, self.params
            )
</file>

<file path="plotnine/geoms/geom_area.py">
from __future__ import annotations

import typing

from ..doctools import document
from .geom_ribbon import geom_ribbon

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_area(geom_ribbon):
    """
    Area plot

    {usage}

    An area plot is a special case of geom_ribbon,
    where the minimum of the range is fixed to 0,
    and the position adjustment defaults to 'stack'.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_ribbon
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {"position": "stack", "outline_type": "upper"}

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data["ymin"] = 0
        data["ymax"] = data["y"]
        return data
</file>

<file path="plotnine/geoms/geom_bar.py">
from __future__ import annotations

import typing

from .._utils import resolution
from ..doctools import document
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_bar(geom_rect):
    """
    Bar plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    just : float, default=0.5
        How to align the column with respect to the axis breaks. The default
        `0.5` aligns the center of the column with the break. `0` aligns the
        left of the of the column with the break and `1` aligns the right of
        the column with the break.
    width : float, default=None
        Bar width. If `None`{.py}, the width is set to
        `90%` of the resolution of the data.

    See Also
    --------
    plotnine.geom_histogram
    plotnine.stat_count : The default `stat` for this `geom`.
    """

    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"xmin", "xmax", "ymin", "ymax"}
    DEFAULT_PARAMS = {
        "stat": "count",
        "position": "stack",
        "just": 0.5,
        "width": None,
    }

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "width" not in data:
            if self.params["width"]:
                data["width"] = self.params["width"]
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        just = self.params.get("just", 0.5)

        bool_idx = data["y"] < 0

        data["ymin"] = 0.0
        data.loc[bool_idx, "ymin"] = data.loc[bool_idx, "y"]

        data["ymax"] = data["y"]
        data.loc[bool_idx, "ymax"] = 0.0

        data["xmin"] = data["x"] - data["width"] * just
        data["xmax"] = data["x"] + data["width"] * (1 - just)
        del data["width"]
        return data
</file>

<file path="plotnine/geoms/geom_bin_2d.py">
from ..doctools import document
from .geom_rect import geom_rect


@document
class geom_bin_2d(geom_rect):
    """
    Heatmap of 2d bin counts

    {usage}

    Divides the plane into rectangles, counts the number of
    cases in each rectangle, and then (by default) maps the number
    of cases to the rectangle's fill. This is a useful alternative
    to geom_point in the presence of overplotting.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_bin_2d : The default stat for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "bin_2d"}


geom_bin2d = geom_bin_2d
</file>

<file path="plotnine/geoms/geom_blank.py">
from __future__ import annotations

import typing

from ..doctools import document
from .geom import geom

if typing.TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_blank(geom):
    """
    An empty plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        pass

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
</file>

<file path="plotnine/geoms/geom_boxplot.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import (
    SIZE_FACTOR,
    copy_missing_columns,
    resolution,
    to_rgba,
)
from ..doctools import document
from ..exceptions import PlotnineWarning
from ..positions import position_dodge2
from ..positions.position import position
from .geom import geom
from .geom_crossbar import geom_crossbar
from .geom_point import geom_point
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import DataLike


@document
class geom_boxplot(geom):
    """
    Box and whiskers plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=None
        Box width. If `None`{.py}, the width is set to
        `90%` of the resolution of the data. Note that if the stat
        has a width parameter, that takes precedence over this one.
    outlier_alpha : float, default=1
        Transparency of the outlier points.
    outlier_color : str | tuple, default=None
        Color of the outlier points.
    outlier_shape : str, default="o"
        Shape of the outlier points. An empty string hides the outliers.
    outlier_size : float, default=1.5
        Size of the outlier points.
    outlier_stroke : float, default=0.5
        Stroke-size of the outlier points.
    notch : bool, default=False
        Whether the boxes should have a notch.
    varwidth : bool, default=False
        If `True`{.py}, boxes are drawn with widths proportional to
        the square-roots of the number of observations in the
        groups.
    notchwidth : float, default=0.5
        Width of notch relative to the body width.
    fatten : float, default=2
        A multiplicative factor used to increase the size of the
        middle bar across the box.

    See Also
    --------
    plotnine.stat_boxplot : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "#333333",
        "fill": "white",
        "linetype": "solid",
        "shape": "o",
        "size": 0.5,
        "weight": 1,
    }
    REQUIRED_AES = {"x", "lower", "upper", "middle", "ymin", "ymax"}
    DEFAULT_PARAMS = {
        "stat": "boxplot",
        "position": "dodge2",
        "width": None,
        "outlier_alpha": 1,
        "outlier_color": None,
        "outlier_shape": "o",
        "outlier_size": 1.5,
        "outlier_stroke": 0.5,
        "notch": False,
        "varwidth": False,
        "notchwidth": 0.5,
        "fatten": 2,
    }

    legend_key_size = staticmethod(geom_crossbar.legend_key_size)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        _position = kwargs.get("position", self.DEFAULT_PARAMS["position"])
        varwidth = kwargs.get("varwidth", self.DEFAULT_PARAMS["varwidth"])

        # varwidth = True is not compatible with preserve="total"
        if varwidth:
            if isinstance(_position, str):
                kwargs["position"] = position_dodge2(preserve="single")
            elif (
                isinstance(_position, position)
                and _position.params["preserve"] == "total"
            ):
                warn(
                    "Cannot preserve total widths when varwidth=True",
                    PlotnineWarning,
                    stacklevel=2,
                )
                _position.params["preserve"] = "single"

        super().__init__(mapping, data, **kwargs)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "width" not in data:
            width = self.params.get("width", None)
            if width is not None:
                data["width"] = width
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        if (
            "outliers" not in data
            # Remove outliers if they will not show so that the scale
            # limits do not recognise them.
            or self.params["outlier_shape"] in (None, "")
        ):
            data["outliers"] = [[] for i in range(len(data))]

        # min and max outlier values
        omin = [
            np.min(lst) if len(lst) else +np.inf for lst in data["outliers"]
        ]
        omax = [
            np.max(lst) if len(lst) else -np.inf for lst in data["outliers"]
        ]

        data["ymin_final"] = np.min(
            np.column_stack([data["ymin"], omin]), axis=1
        )
        data["ymax_final"] = np.max(
            np.column_stack([data["ymax"], omax]), axis=1
        )

        # if varwidth not requested or not available, don't use it
        if (
            "varwidth" not in self.params
            or not self.params["varwidth"]
            or "relvarwidth" not in data
        ):
            data["xmin"] = data["x"] - data["width"] / 2
            data["xmax"] = data["x"] + data["width"] / 2
        else:
            # make relvarwidth relative to the size of the
            # largest group
            data["relvarwidth"] /= data["relvarwidth"].max()
            data["xmin"] = data["x"] - data["relvarwidth"] * data["width"] / 2
            data["xmax"] = data["x"] + data["relvarwidth"] * data["width"] / 2
            del data["relvarwidth"]

        del data["width"]

        return data

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        def flat(*args: pd.Series[Any]) -> npt.NDArray[Any]:
            """Flatten list-likes"""
            return np.hstack(args)

        common_columns = [
            "color",
            "size",
            "linetype",
            "fill",
            "group",
            "alpha",
            "shape",
        ]
        # whiskers
        whiskers = pd.DataFrame(
            {
                "x": flat(data["x"], data["x"]),
                "y": flat(data["upper"], data["lower"]),
                "yend": flat(data["ymax"], data["ymin"]),
                "alpha": 1,
            }
        )
        whiskers["xend"] = whiskers["x"]
        copy_missing_columns(whiskers, data[common_columns])

        # box
        box_columns = ["xmin", "xmax", "lower", "middle", "upper"]
        box = data[common_columns + box_columns].copy()
        box.rename(
            columns={"lower": "ymin", "middle": "y", "upper": "ymax"},
            inplace=True,
        )

        # notch
        if params["notch"]:
            box["ynotchlower"] = data["notchlower"]
            box["ynotchupper"] = data["notchupper"]

        # outliers
        num_outliers = len(data["outliers"].iloc[0])
        if num_outliers:

            def outlier_value(param: str) -> Any:
                oparam = f"outlier_{param}"
                if params[oparam] is not None:
                    return params[oparam]
                return data[param].iloc[0]

            outliers = pd.DataFrame(
                {
                    "y": data["outliers"].iloc[0],
                    "x": np.repeat(data["x"].iloc[0], num_outliers),
                    "fill": [None] * num_outliers,
                }
            )
            outliers["alpha"] = outlier_value("alpha")
            outliers["color"] = outlier_value("color")
            outliers["shape"] = outlier_value("shape")
            outliers["size"] = outlier_value("size")
            outliers["stroke"] = outlier_value("stroke")
            geom_point.draw_group(outliers, panel_params, coord, ax, params)

        # plot
        geom_segment.draw_group(whiskers, panel_params, coord, ax, params)
        geom_crossbar.draw_group(box, panel_params, coord, ax, params)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.lines import Line2D
        from matplotlib.patches import Rectangle

        # box
        facecolor = to_rgba(data["fill"], data["alpha"])
        if facecolor is None:
            facecolor = "none"

        kwargs = {"linestyle": data["linetype"]}

        box = Rectangle(
            (da.width * 0.125, da.height * 0.25),
            width=da.width * 0.75,
            height=da.height * 0.5,
            facecolor=facecolor,
            edgecolor=data["color"],
            linewidth=data["size"],
            capstyle="projecting",
            antialiased=False,
            **kwargs,
        )
        da.add_artist(box)

        kwargs["solid_capstyle"] = "butt"
        kwargs["color"] = data["color"]
        kwargs["linewidth"] = data["size"] * SIZE_FACTOR

        # middle strike through
        strike = Line2D(
            [da.width * 0.125, da.width * 0.875],
            [da.height * 0.5, da.height * 0.5],
            **kwargs,
        )
        da.add_artist(strike)

        # whiskers
        top = Line2D(
            [da.width * 0.5, da.width * 0.5],
            [da.height * 0.75, da.height * 0.9],
            **kwargs,
        )
        da.add_artist(top)

        bottom = Line2D(
            [da.width * 0.5, da.width * 0.5],
            [da.height * 0.25, da.height * 0.1],
            **kwargs,
        )
        da.add_artist(bottom)
        return da
</file>

<file path="plotnine/geoms/geom_col.py">
from ..doctools import document
from .geom_bar import geom_bar


@document
class geom_col(geom_bar):
    """
    Bar plot with base on the x-axis

    {usage}

    This is an alternate version of [](`~plotnine.geoms.geom_bar`) that maps
    the height of bars to an existing variable in your data. If
    you want the height of the bar to represent a count of cases,
    use [](`~plotnine.geoms.geom_bar`).

    Parameters
    ----------
    {common_parameters}
    just : float, default=0.5
        How to align the column with respect to the axis breaks. The default
        `0.5` aligns the center of the column with the break. `0` aligns the
        left of the of the column with the break and `1` aligns the right of
        the column with the break.
    width : float, default=None
        Bar width. If `None`{.py}, the width is set to
        `90%` of the resolution of the data.

    See Also
    --------
    plotnine.geom_bar
    """

    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"xmin", "xmax", "ymin", "ymax"}
    DEFAULT_PARAMS = {"position": "stack", "just": 0.5, "width": None}
</file>

<file path="plotnine/geoms/geom_count.py">
from ..doctools import document
from .geom_point import geom_point


@document
class geom_count(geom_point):
    """
    Plot overlapping points

    {usage}

    This is a variant [](`~plotnine.geoms.geom_point`) that counts the number
    of observations at each location, then maps the count to point
    area. It useful when you have discrete data and overplotting.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_sum : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "sum"}
</file>

<file path="plotnine/geoms/geom_crossbar.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, copy_missing_columns, resolution, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from .geom import geom
from .geom_polygon import geom_polygon
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_crossbar(geom):
    """
    Vertical interval represented by a crossbar

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=0.5
        Box width as a fraction of the resolution of the data.
    fatten : float, default=2
        A multiplicative factor used to increase the size of the
        middle bar across the box.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "fill": None,
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y", "ymin", "ymax"}
    DEFAULT_PARAMS = {"width": 0.5, "fatten": 2}

    legend_key_size = staticmethod(geom_segment.legend_key_size)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "width" not in data:
            if self.params["width"]:
                data["width"] = self.params["width"]
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        data["xmin"] = data["x"] - data["width"] / 2
        data["xmax"] = data["x"] + data["width"] / 2
        del data["width"]
        return data

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        y = data["y"]
        xmin = data["xmin"]
        xmax = data["xmax"]
        ymin = data["ymin"]
        ymax = data["ymax"]
        group = data["group"]

        # From violin
        notchwidth = typing.cast("float", params.get("notchwidth"))
        # ynotchupper = data.get('ynotchupper')
        # ynotchlower = data.get('ynotchlower')

        def flat(*args: pd.Series[Any]) -> npt.NDArray[Any]:
            """Flatten list-likes"""
            return np.hstack(args)

        middle = pd.DataFrame(
            {"x": xmin, "y": y, "xend": xmax, "yend": y, "group": group}
        )
        copy_missing_columns(middle, data)
        middle["alpha"] = 1
        middle["size"] *= params["fatten"]

        has_notch = "ynotchupper" in data and "ynotchlower" in data
        if has_notch:  # 10 points + 1 closing
            ynotchupper = data["ynotchupper"]
            ynotchlower = data["ynotchlower"]

            if any(ynotchlower < ymin) or any(ynotchupper > ymax):
                warn(
                    "Notch went outside the hinges. Try setting notch=False.",
                    PlotnineWarning,
                )

            notchindent = (1 - notchwidth) * (xmax - xmin) / 2

            middle["x"] += notchindent
            middle["xend"] -= notchindent
            box = pd.DataFrame(
                {
                    "x": flat(
                        xmin,
                        xmin,
                        xmin + notchindent,
                        xmin,
                        xmin,
                        xmax,
                        xmax,
                        xmax - notchindent,
                        xmax,
                        xmax,
                        xmin,
                    ),
                    "y": flat(
                        ymax,
                        ynotchupper,
                        y,
                        ynotchlower,
                        ymin,
                        ymin,
                        ynotchlower,
                        y,
                        ynotchupper,
                        ymax,
                        ymax,
                    ),
                    "group": np.tile(np.arange(1, len(group) + 1), 11),
                }
            )
        else:
            # No notch, 4 points + 1 closing
            box = pd.DataFrame(
                {
                    "x": flat(xmin, xmin, xmax, xmax, xmin),
                    "y": flat(ymax, ymax, ymax, ymin, ymin),
                    "group": np.tile(np.arange(1, len(group) + 1), 5),
                }
            )

        copy_missing_columns(box, data)
        geom_polygon.draw_group(box, panel_params, coord, ax, params)
        geom_segment.draw_group(middle, panel_params, coord, ax, params)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle with a horizontal strike in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.lines import Line2D
        from matplotlib.patches import Rectangle

        linewidth = data["size"] * SIZE_FACTOR

        # background
        facecolor = to_rgba(data["fill"], data["alpha"])
        if facecolor is None:
            facecolor = "none"

        bg = Rectangle(
            (da.width * 0.125, da.height * 0.25),
            width=da.width * 0.75,
            height=da.height * 0.5,
            linewidth=linewidth,
            facecolor=facecolor,
            edgecolor=data["color"],
            linestyle=data["linetype"],
            capstyle="projecting",
            antialiased=False,
        )
        da.add_artist(bg)

        strike = Line2D(
            [da.width * 0.125, da.width * 0.875],
            [da.height * 0.5, da.height * 0.5],
            linestyle=data["linetype"],
            linewidth=linewidth,
            color=data["color"],
        )
        da.add_artist(strike)
        return da
</file>

<file path="plotnine/geoms/geom_density_2d.py">
from ..doctools import document
from .geom_path import geom_path


@document
class geom_density_2d(geom_path):
    """
    2D density estimate

    {usage}

    This is a 2d version of [](`~plotnine.geoms.geom_density`).

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_density_2d : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "density_2d"}
</file>

<file path="plotnine/geoms/geom_density.py">
from ..doctools import document
from .geom_area import geom_area


@document
class geom_density(geom_area):
    """
    Smooth density estimate

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_ribbon
    """

    DEFAULT_AES = {
        **geom_area.DEFAULT_AES,
        "color": "black",
        "fill": None,
        "weight": 1,
    }

    DEFAULT_PARAMS = {"stat": "density", "outline_type": "upper"}
</file>

<file path="plotnine/geoms/geom_errorbar.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import copy_missing_columns, resolution
from ..doctools import document
from .geom import geom
from .geom_path import geom_path
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_errorbar(geom):
    """
    Vertical interval represented as an errorbar

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=0.5
        Bar width as a fraction of the resolution of the data.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "ymin", "ymax"}
    DEFAULT_PARAMS = {"width": 0.5}

    draw_legend = staticmethod(geom_path.draw_legend)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "width" not in data:
            if self.params["width"]:
                data["width"] = self.params["width"]
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        data["xmin"] = data["x"] - data["width"] / 2
        data["xmax"] = data["x"] + data["width"] / 2
        del data["width"]
        return data

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        f = np.hstack
        # create (two horizontal bars) + vertical bar
        bars = pd.DataFrame(
            {
                "x": f([data["xmin"], data["xmin"], data["x"]]),
                "xend": f([data["xmax"], data["xmax"], data["x"]]),
                "y": f([data["ymin"], data["ymax"], data["ymax"]]),
                "yend": f([data["ymin"], data["ymax"], data["ymin"]]),
            }
        )

        copy_missing_columns(bars, data)
        geom_segment.draw_group(bars, panel_params, coord, ax, params)
</file>

<file path="plotnine/geoms/geom_errorbarh.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import copy_missing_columns, resolution
from ..doctools import document
from .geom import geom
from .geom_path import geom_path
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_errorbarh(geom):
    """
    Horizontal interval represented as an errorbar

    {usage}

    Parameters
    ----------
    {common_parameters}
    height : float, default=0.5
        Bar height as a fraction of the resolution of the data.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"y", "xmin", "xmax"}
    DEFAULT_PARAMS = {"height": 0.5}

    draw_legend = staticmethod(geom_path.draw_legend)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "height" not in data:
            if self.params["height"]:
                data["height"] = self.params["height"]
            else:
                data["height"] = resolution(data["y"], False) * 0.9

        data["ymin"] = data["y"] - data["height"] / 2
        data["ymax"] = data["y"] + data["height"] / 2
        del data["height"]
        return data

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        f = np.hstack
        # create (two vertical bars) + horizontal bar
        bars = pd.DataFrame(
            {
                "y": f([data["ymin"], data["ymin"], data["y"]]),
                "yend": f([data["ymax"], data["ymax"], data["y"]]),
                "x": f([data["xmin"], data["xmax"], data["xmin"]]),
                "xend": f([data["xmin"], data["xmax"], data["xmax"]]),
            }
        )

        copy_missing_columns(bars, data)
        geom_segment.draw_group(bars, panel_params, coord, ax, params)
</file>

<file path="plotnine/geoms/geom_freqpoly.py">
from ..doctools import document
from .geom_path import geom_path


@document
class geom_freqpoly(geom_path):
    """
    Frequency polygon

    {usage}

    See [](`~plotnine.geoms.geom_path`) for documentation
    of the parameters.
    """

    DEFAULT_PARAMS = {
        "stat": "bin",
        "lineend": "butt",
        "linejoin": "round",
        "arrow": None,
    }
</file>

<file path="plotnine/geoms/geom_histogram.py">
from ..doctools import document
from .geom_bar import geom_bar


@document
class geom_histogram(geom_bar):
    """
    Histogram

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_bar : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "bin", "position": "stack"}
</file>

<file path="plotnine/geoms/geom_hline.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import order_as_data_mapping
from ..doctools import document
from ..exceptions import PlotnineWarning
from ..mapping import aes
from .geom import geom
from .geom_path import geom_path
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import DataLike


@document
class geom_hline(geom):
    """
    Horizontal line

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
        "alpha": 1,
    }
    REQUIRED_AES = {"yintercept"}
    DEFAULT_PARAMS = {"inherit_aes": False}

    draw_legend = staticmethod(geom_path.draw_legend)
    legend_key_size = staticmethod(geom_path.legend_key_size)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        data, mapping = order_as_data_mapping(data, mapping)
        yintercept = kwargs.pop("yintercept", None)
        if yintercept is not None:
            if mapping:
                warn(
                    "The 'yintercept' parameter has overridden "
                    "the aes() mapping.",
                    PlotnineWarning,
                )
            data = pd.DataFrame({"yintercept": np.repeat(yintercept, 1)})
            mapping = aes(yintercept="yintercept")
            kwargs["show_legend"] = False

        geom.__init__(self, mapping, data, **kwargs)

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        ranges = coord.backtransform_range(panel_params)
        data["y"] = data["yintercept"]
        data["yend"] = data["yintercept"]
        data["x"] = ranges.x[0]
        data["xend"] = ranges.x[1]
        data = data.drop_duplicates()

        for _, gdata in data.groupby("group"):
            gdata.reset_index(inplace=True)
            geom_segment.draw_group(
                gdata, panel_params, coord, ax, self.params
            )
</file>

<file path="plotnine/geoms/geom_jitter.py">
from __future__ import annotations

import typing

from ..doctools import document
from ..exceptions import PlotnineError
from ..positions import position_jitter
from .geom_point import geom_point

if typing.TYPE_CHECKING:
    from typing import Any

    from plotnine import aes
    from plotnine.typing import DataLike


@document
class geom_jitter(geom_point):
    """
    Scatter plot with points jittered to reduce overplotting

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=None
        Proportion to jitter in horizontal direction.
        The default value is that from
        [](`~plotnine.positions.position_jitter`)
    height : float, default=None
        Proportion to jitter in vertical direction.
        The default value is that from
        [](`~plotnine.positions.position_jitter`).
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.

    See Also
    --------
    plotnine.position_jitter
    plotnine.geom_point
    """

    DEFAULT_PARAMS = {
        "position": "jitter",
        "width": None,
        "height": None,
        "random_state": None,
    }

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        if {"width", "height", "random_state"} & set(kwargs):
            if "position" in kwargs:
                raise PlotnineError(
                    "Specify either 'position' or "
                    "'width'/'height'/'random_state'"
                )

            try:
                width = kwargs.pop("width")
            except KeyError:
                width = None

            try:
                height = kwargs.pop("height")
            except KeyError:
                height = None

            try:
                random_state = kwargs.pop("random_state")
            except KeyError:
                random_state = None

            kwargs["position"] = position_jitter(
                width=width, height=height, random_state=random_state
            )
        geom_point.__init__(self, mapping, data, **kwargs)
</file>

<file path="plotnine/geoms/geom_label.py">
from __future__ import annotations

import typing

from .._utils import to_rgba
from ..doctools import document
from .geom_text import geom_text

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.offsetbox import DrawingArea

    from plotnine.layer import layer


@document
class geom_label(geom_text):
    """
    Textual annotations with a background

    {usage}

    Parameters
    ----------
    {common_parameters}
    boxstyle : str, default="round"
        Options are:
        ```python
        'circle'
        'darrow'
        'larrow'
        'rarrow'
        'round '
        'round4'
        'roundtooth'
        'sawtooth'
        'square'
        ````
    boxcolor: str, tuple[float, float, float, float], default=None
        Color of box around the text. If None, the color is
        the same as the text.
    label_padding : float, default=0.25
        Amount of padding
    label_r : float, default=0.25
        Rounding radius of corners.
    label_size : float, default=0.7
        Linewidth of the label boundary.
    tooth_size : float, default=None
        Size of the `roundtooth` or `sawtooth` if they
        are the chosen *boxstyle*. The default depends
        on Matplotlib

    See Also
    --------
    plotnine.geom_text : For documentation of the
        parameters. [](`~matplotlib.patches.BoxStyle`) for the
        parameters that affect the boxstyle.
    """

    DEFAULT_AES = {**geom_text.DEFAULT_AES, "fill": "white"}
    DEFAULT_PARAMS = {
        **geom_text.DEFAULT_PARAMS,
        # boxstyle is one of
        #   circle, larrow, rarrow, round, round4,
        #   roundtooth, sawtooth, square
        #
        # Documentation at matplotlib.patches.BoxStyle
        "boxstyle": "round",
        "boxcolor": None,
        "label_padding": 0.25,
        "label_r": 0.25,
        "label_size": 0.7,
        "tooth_size": None,
    }

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw letter 'a' in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.patches import Rectangle

        fill = to_rgba(data["fill"], data["alpha"])

        if data["fill"]:
            rect = Rectangle(
                (0, 0),
                width=da.width,
                height=da.height,
                linewidth=0,
                facecolor=fill,
                capstyle="projecting",
            )
            da.add_artist(rect)
        return geom_text.draw_legend(data, da, lyr)
</file>

<file path="plotnine/geoms/geom_linerange.py">
from __future__ import annotations

import typing

from ..doctools import document
from .geom import geom
from .geom_path import geom_path
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_linerange(geom):
    """
    Vertical interval represented by lines

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "ymin", "ymax"}

    draw_legend = staticmethod(geom_path.draw_legend)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        data.eval(
            """
            xend = x
            y = ymin
            yend = ymax
            """,
            inplace=True,
        )
        geom_segment.draw_group(data, panel_params, coord, ax, params)
</file>

<file path="plotnine/geoms/geom_point.py">
from __future__ import annotations

import typing

import numpy as np

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from ..scales.scale_shape import FILLED_SHAPES
from .geom import geom

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_point(geom):
    """
    Plot points (Scatter plot)

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "fill": None,
        "shape": "o",
        "size": 1.5,
        "stroke": 0.5,
    }
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"color", "shape", "size"}

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        self.draw_group(data, panel_params, coord, ax, self.params)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        data = coord.transform(data, panel_params)
        units = "shape"
        for _, udata in data.groupby(units, dropna=False):
            udata.reset_index(inplace=True, drop=True)
            geom_point.draw_unit(udata, panel_params, coord, ax, params)

    @staticmethod
    def draw_unit(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        # Our size is in 'points' while scatter wants
        # 'points^2'. The stroke is outside. And pi
        # gives a large enough scaling factor
        # All other sizes for which the MPL units should
        # be in points must scaled using sqrt(pi)
        size = ((data["size"] + data["stroke"]) ** 2) * np.pi
        linewidth = data["stroke"] * SIZE_FACTOR
        color = to_rgba(data["color"], data["alpha"])
        shape = data["shape"].iloc[0]

        # It is common to forget that scatter points are
        # filled and slip-up by manually assigning to the
        # color instead of the fill. We forgive.
        if shape in FILLED_SHAPES:
            if all(c is None for c in data["fill"]):
                fill = color
            else:
                fill = to_rgba(data["fill"], data["alpha"])
        else:
            # Assume unfilled
            fill = color
            color = None

        ax.scatter(
            x=data["x"],
            y=data["y"],
            s=size,
            facecolor=fill,
            edgecolor=color,
            linewidth=linewidth,
            marker=shape,
            zorder=params["zorder"],
            rasterized=params["raster"],
        )

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a point in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.lines import Line2D

        if data["fill"] is None:
            data["fill"] = data["color"]

        size = (data["size"] + data["stroke"]) * SIZE_FACTOR
        edgewidth = data["stroke"] * SIZE_FACTOR
        fill = to_rgba(data["fill"], data["alpha"])
        color = to_rgba(data["color"], data["alpha"])

        key = Line2D(
            [0.5 * da.width],
            [0.5 * da.height],
            marker=data["shape"],
            markersize=size,
            markerfacecolor=fill,
            markeredgecolor=color,
            markeredgewidth=edgewidth,
        )
        da.add_artist(key)
        return da

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        w, h = min_size
        pad_w, pad_h = w * 0.5, h * 0.5
        _size = data["size"] * SIZE_FACTOR
        _edgewidth = 2 * data["stroke"] * SIZE_FACTOR
        _w = _h = _size + _edgewidth
        if data["color"] is not None:
            w = max(w, _w + pad_w)
            h = max(h, _h + pad_h)
        return w, h
</file>

<file path="plotnine/geoms/geom_pointdensity.py">
from ..doctools import document
from .geom_point import geom_point


@document
class geom_pointdensity(geom_point):
    """
    Scatterplot with density estimation at each point

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_pointdensity : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "pointdensity"}
</file>

<file path="plotnine/geoms/geom_pointrange.py">
from __future__ import annotations

import typing
from copy import copy

from ..doctools import document
from .geom import geom
from .geom_linerange import geom_linerange
from .geom_path import geom_path
from .geom_point import geom_point

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_pointrange(geom):
    """
    Vertical interval represented by a line with a point

    {usage}

    Parameters
    ----------
    {common_parameters}
    fatten : float, default=2
        A multiplicative factor used to increase the size of the
        point along the line-range.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "fill": None,
        "linetype": "solid",
        "shape": "o",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y", "ymin", "ymax"}
    DEFAULT_PARAMS = {"fatten": 4}

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        geom_linerange.draw_group(data.copy(), panel_params, coord, ax, params)
        data["size"] = data["size"] * params["fatten"]
        data["stroke"] = geom_point.DEFAULT_AES["stroke"]
        geom_point.draw_group(data, panel_params, coord, ax, params)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a point in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        geom_path.draw_legend(data, da, lyr)
        data["size"] = data["size"] * lyr.geom.params["fatten"]
        data["stroke"] = geom_point.DEFAULT_AES["stroke"]
        geom_point.draw_legend(data, da, lyr)
        return da

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        data = copy(data)
        data["size"] = data["size"] * lyr.geom.params["fatten"]
        data["stroke"] = geom_point.DEFAULT_AES["stroke"]
        return geom_point.legend_key_size(data, min_size, lyr)
</file>

<file path="plotnine/geoms/geom_polygon.py">
from __future__ import annotations

import typing

import numpy as np

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_polygon(geom):
    """
    Polygon, a filled path

    {usage}

    Parameters
    ----------
    {common_parameters}

    Notes
    -----
    All paths in the same `group` aesthetic value make up a polygon.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": None,
        "fill": "#333333",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y"}

    legend_key_size = staticmethod(geom_path.legend_key_size)

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        return data

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        self.draw_group(data, panel_params, coord, ax, self.params)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.collections import PolyCollection

        data = coord.transform(data, panel_params, munch=True)
        data["linewidth"] = data["size"] * SIZE_FACTOR

        # Each group is a polygon with a single facecolor
        # with potentially an edgecolor for every edge.
        verts = []
        facecolor = []
        edgecolor = []
        linestyle = []
        linewidth = []

        # Some stats may order the data in ways that prevent
        # objects from occluding other objects. We do not want
        # to undo that order.
        grouper = data.groupby("group", sort=False)
        for group, df in grouper:
            fill = to_rgba(df["fill"].iloc[0], df["alpha"].iloc[0])
            verts.append(tuple(zip(df["x"], df["y"])))
            facecolor.append("none" if fill is None else fill)
            edgecolor.append(df["color"].iloc[0] or "none")
            linestyle.append(df["linetype"].iloc[0])
            linewidth.append(df["linewidth"].iloc[0])

        col = PolyCollection(
            verts,
            facecolors=facecolor,
            edgecolors=edgecolor,
            linestyles=linestyle,
            linewidths=linewidth,
            zorder=params["zorder"],
            rasterized=params["raster"],
        )

        ax.add_collection(col)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.patches import Rectangle

        # We take into account that the linewidth
        # bestrides the boundary of the rectangle
        linewidth = data["size"] * SIZE_FACTOR
        linewidth = np.min([linewidth, da.width / 4, da.height / 4])

        if data["color"] is None:
            linewidth = 0

        facecolor = to_rgba(data["fill"], data["alpha"])
        if facecolor is None:
            facecolor = "none"

        rect = Rectangle(
            (0 + linewidth / 2, 0 + linewidth / 2),
            width=da.width - linewidth,
            height=da.height - linewidth,
            linewidth=linewidth,
            linestyle=data["linetype"],
            facecolor=facecolor,
            edgecolor=data["color"],
            capstyle="projecting",
        )
        da.add_artist(rect)
        return da
</file>

<file path="plotnine/geoms/geom_qq_line.py">
from ..doctools import document
from .geom_path import geom_path


@document
class geom_qq_line(geom_path):
    """
    Quantile-Quantile Line plot

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_qq_line : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "qq_line"}
</file>

<file path="plotnine/geoms/geom_qq.py">
from ..doctools import document
from .geom_point import geom_point


@document
class geom_qq(geom_point):
    """
    Quantile-Quantile plot

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_qq : The default `stat` for this `geom`.
    """

    DEFAULT_PARAMS = {"stat": "qq"}
</file>

<file path="plotnine/geoms/geom_quantile.py">
from ..doctools import document
from .geom_path import geom_path


@document
class geom_quantile(geom_path):
    """
    Quantile lines from a quantile regression

    {usage}

    Parameters
    ----------
    {common_parameters}
    lineend : Literal["butt", "round", "projecting"], default="butt"
        Line end style. This option is applied for solid linetypes.
    linejoin : Literal["round", "miter", "bevel"], default="round"
        Line join style. This option is applied for solid linetypes.

    See Also
    --------
    plotnine.stat_quantile : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "#3366FF",
        "linetype": "solid",
        "size": 0.5,
    }
    DEFAULT_PARAMS = {
        "stat": "quantile",
        "lineend": "butt",
        "linejoin": "round",
    }
</file>

<file path="plotnine/geoms/geom_raster.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np

from .._utils import resolution
from ..coords import coord_cartesian
from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from .geom import geom
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import DataLike


@document
class geom_raster(geom):
    """
    Rasterized Rectangles specified using center points

    {usage}

    Parameters
    ----------
    {common_parameters}

    hjust : float, default=0.5
        Horizontal justification for the rectangle at point `x`.
        Default is 0.5, which centers the rectangle horizontally.
        Must be in the range `[0, 1]`.
    vjust : float, default=0.5
        Vertical justification for the rectangle at point `y`
        Default is 0.5, which centers the rectangle vertically.
        Must be in the range `[0, 1]`.
    interpolation : str, default=None
        How to calculate values between the center points of
        adjacent rectangles. The default is `None`{.py} not to
        interpolate. Allowed values are:
        ```python
        "antialiased"
        "nearest"
        "bilinear"
        "bicubic"
        "spline16"
        "spline36"
        "hanning"
        "hamming"
        "hermite"
        "kaiser"
        "quadric"
        "catrom"
        "gaussian"
        "bessel"
        "mitchell"
        "sinc"
        "lanczos"
        "blackman"
        ```
    filterrad : float, default=4.0
        The filter radius for filters that have a radius parameter, i.e.
        when interpolation is one of: `sinc`, `lanczos`, `blackman`.
        Must be a number greater than zero.

    See Also
    --------
    plotnine.geom_rect
    plotnine.geom_tile
    """

    DEFAULT_AES = {"alpha": 1, "fill": "#333333"}
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"fill", "xmin", "xmax", "ymin", "ymax"}
    DEFAULT_PARAMS = {
        "vjust": 0.5,
        "hjust": 0.5,
        "interpolation": None,
        "filterrad": 4.0,
        "raster": True,
    }
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        # Silently accept:
        #    1. interpolate
        #    2. bool values for interpolation
        if "interpolate" in kwargs:
            kwargs["interpolation"] = kwargs.pop("interpolate")
        if isinstance(kwargs.get("interpolation"), bool):
            if kwargs["interpolation"] is True:
                kwargs["interpolation"] = "bilinear"
            else:
                kwargs["interpolation"] = None

        super().__init__(mapping, data, **kwargs)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        hjust = self.params["hjust"]
        vjust = self.params["vjust"]
        precision = np.sqrt(np.finfo(float).eps)

        x_diff = np.diff(np.sort(data["x"].unique()))
        if len(x_diff) == 0:
            w = 1
        elif np.any(np.abs(np.diff(x_diff)) > precision):
            warn(
                "Raster pixels are placed at uneven horizontal intervals "
                "and will be shifted. Consider using geom_tile() instead.",
                PlotnineWarning,
            )
            w = x_diff.min()
        else:
            w = x_diff[0]

        y_diff = np.diff(np.sort(data["y"].unique()))
        if len(y_diff) == 0:
            h = 1
        elif np.any(np.abs(np.diff(y_diff)) > precision):
            warn(
                "Raster pixels are placed at uneven vertical intervals "
                "and will be shifted. Consider using geom_tile() instead.",
                PlotnineWarning,
            )
            h = y_diff.min()
        else:
            h = y_diff[0]

        data["xmin"] = data["x"] - w * (1 - hjust)
        data["xmax"] = data["x"] + w * hjust
        data["ymin"] = data["y"] - h * (1 - vjust)
        data["ymax"] = data["y"] + h * vjust
        return data

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        from matplotlib.colors import to_rgba_array
        from matplotlib.image import AxesImage

        if not isinstance(coord, coord_cartesian):
            raise PlotnineError(
                "geom_raster only works with cartesian coordinates"
            )

        data = coord.transform(data, panel_params)
        x = data["x"].to_numpy().astype(float)
        y = data["y"].to_numpy().astype(float)
        facecolor = to_rgba_array(data["fill"].to_numpy())
        facecolor[:, 3] = data["alpha"].to_numpy()

        # Convert vector of data to flat image,
        # figure out dimensions of raster on plot, and the colored
        # indices.
        x_pos = ((x - x.min()) / resolution(x, False)).astype(int)
        y_pos = ((y - y.min()) / resolution(y, False)).astype(int)
        nrow = y_pos.max() + 1
        ncol = x_pos.max() + 1
        yidx, xidx = nrow - y_pos - 1, x_pos

        # Create and "color" the matrix.
        # Any gaps left whites (ones) colors plus zero alpha values
        # allows makes it possible to have a "neutral" interpolation
        # into the gaps when intervals are uneven.
        X = np.ones((nrow, ncol, 4))
        X[:, :, 3] = 0
        X[yidx, xidx] = facecolor

        im = AxesImage(
            ax,
            data=X,
            interpolation=self.params["interpolation"],
            origin="upper",
            extent=(
                data["xmin"].min(),
                data["xmax"].max(),
                data["ymin"].min(),
                data["ymax"].max(),
            ),
            rasterized=self.params["raster"],
            filterrad=self.params["filterrad"],
            zorder=self.params["zorder"],
        )
        ax.add_image(im)
</file>

<file path="plotnine/geoms/geom_rect.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from .geom import geom
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_rect(geom):
    """
    Rectangles

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "color": None,
        "fill": "#595959",
        "linetype": "solid",
        "size": 0.5,
        "alpha": 1,
    }
    REQUIRED_AES = {"xmax", "xmin", "ymax", "ymin"}

    draw_legend = staticmethod(geom_polygon.draw_legend)

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        if not coord.is_linear:
            data = _rectangles_to_polygons(data)
            for _, gdata in data.groupby("group"):
                gdata.reset_index(inplace=True, drop=True)
                geom_polygon.draw_group(
                    gdata, panel_params, coord, ax, self.params
                )
        else:
            self.draw_group(data, panel_params, coord, ax, self.params)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.collections import PolyCollection

        data = coord.transform(data, panel_params, munch=True)
        linewidth = data["size"] * SIZE_FACTOR

        limits = zip(data["xmin"], data["xmax"], data["ymin"], data["ymax"])

        verts = [[(l, b), (l, t), (r, t), (r, b)] for (l, r, b, t) in limits]

        fill = to_rgba(data["fill"], data["alpha"])
        color = data["color"]

        # prevent unnecessary borders
        if all(color.isna()):
            color = "none"

        col = PolyCollection(
            verts,
            facecolors=fill,
            edgecolors=color,
            linestyles=data["linetype"],
            linewidths=linewidth,
            zorder=params["zorder"],
            rasterized=params["raster"],
        )
        ax.add_collection(col)


def _rectangles_to_polygons(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert rect data to polygons

    Parameters
    ----------
    df : dataframe
        Dataframe with *xmin*, *xmax*, *ymin* and *ymax* columns,
        plus others for aesthetics ...

    Returns
    -------
    data : dataframe
        Dataframe with *x* and *y* columns, plus others for
        aesthetics ...
    """
    n = len(df)

    # Helper indexing arrays
    xmin_idx = np.tile([True, True, False, False], n)
    xmax_idx = ~xmin_idx
    ymin_idx = np.tile([True, False, False, True], n)
    ymax_idx = ~ymin_idx

    # There are 2 x and 2 y values for each of xmin, xmax, ymin & ymax
    # The positions are as laid out in the indexing arrays
    # x and y values
    x = np.empty(n * 4)
    y = np.empty(n * 4)
    x[xmin_idx] = df["xmin"].repeat(2)
    x[xmax_idx] = df["xmax"].repeat(2)
    y[ymin_idx] = df["ymin"].repeat(2)
    y[ymax_idx] = df["ymax"].repeat(2)

    # Aesthetic columns and others
    other_cols = df.columns.difference(
        ["x", "y", "xmin", "xmax", "ymin", "ymax"]
    )
    d = {str(col): np.repeat(df[col].to_numpy(), 4) for col in other_cols}
    data = pd.DataFrame({"x": x, "y": y, **d})
    return data
</file>

<file path="plotnine/geoms/geom_ribbon.py">
from __future__ import annotations

import typing

from .._utils import SIZE_FACTOR, to_rgba
from ..coords import coord_flip
from ..doctools import document
from ..exceptions import PlotnineError
from .geom import geom
from .geom_path import geom_path
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import ColorsLike


@document
class geom_ribbon(geom):
    """
    Ribbon plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    outline_type : Literal["upper", "lower", "both", "full"], default="both"
        How to stroke to outline of the region / area.
        If `upper`, draw only upper bounding line.
        If `lower`, draw only lower bounding line.
        If `both`, draw both upper & lower bounding lines.
        If `full`, draw closed polygon around the area.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Aesthetics Descriptions**

    `where`

    :   Define where to exclude horizontal regions from being filled.
        Regions between any two `False` values are skipped.
        For sensible demarcation the value used in the *where* predicate
        expression should match the `ymin` value or expression. i.e.

        ```python
         aes(ymin=0, ymax="col1", where="col1 > 0")  # good
         aes(ymin=0, ymax="col1", where="col1 > 10")  # bad

         aes(ymin=col2, ymax="col1", where="col1 > col2")  # good
         aes(ymin=col2, ymax="col1", where="col1 > col3")  # bad
        ```
    """
    DEFAULT_AES = {
        "alpha": 1,
        "color": "none",
        "fill": "#333333",
        "linetype": "solid",
        "size": 0.5,
        "where": True,
    }
    REQUIRED_AES = {"x", "ymax", "ymin"}
    DEFAULT_PARAMS = {"outline_type": "both"}
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        return data

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        # The outlines need x and y coordinates
        if self.params["outline_type"] in ("upper", "lower", "both"):
            if "xmax" in data and "x" not in data:
                data["x"] = data["xmax"]
            if "ymax" in data and "y" not in data:
                data["y"] = data["ymax"]
        return data

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        _x = "y" if isinstance(coord, coord_flip) else "x"
        data = coord.transform(data, panel_params, munch=True)
        data = data.sort_values(by=["group", _x], kind="mergesort")
        units = ["alpha", "color", "fill", "linetype", "size"]

        if len(data[units].drop_duplicates()) > 1:
            msg = "Aesthetics cannot vary within a ribbon."
            raise PlotnineError(msg)

        for _, udata in data.groupby(units, dropna=False):
            udata.reset_index(inplace=True, drop=True)
            geom_ribbon.draw_unit(udata, panel_params, coord, ax, params)

    @staticmethod
    def draw_unit(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        linewidth = data["size"].iloc[0] * SIZE_FACTOR
        fill = to_rgba(data["fill"], data["alpha"])

        if data["color"].isna().all():
            color: ColorsLike = "none"
        else:
            color = data["color"]

        if fill is None:
            fill = "none"

        if isinstance(coord, coord_flip):
            fill_between = ax.fill_betweenx
            _x, _min, _max = data["y"], data["xmin"], data["xmax"]
        else:
            fill_between = ax.fill_between
            _x, _min, _max = data["x"], data["ymin"], data["ymax"]

        # We only change this defaults for fill_between when necessary
        where = data.get("where", None)
        interpolate = not (where is None or where.all())

        if params["outline_type"] != "full":
            linewidth = 0
            color = "none"

        fill_between(
            _x,
            _min,
            _max,
            where=where,  # type: ignore
            interpolate=interpolate,
            facecolor=fill,
            edgecolor=color,
            linewidth=linewidth,
            linestyle=data["linetype"].iloc[0],
            zorder=params["zorder"],
            rasterized=params["raster"],
        )

        # Alpha does not affect the outlines
        data["alpha"] = 1
        geom_ribbon._draw_outline(data, panel_params, coord, ax, params)

    @staticmethod
    def _draw_outline(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        outline_type = params["outline_type"]

        if outline_type == "full":
            return

        x, y = "x", "y"
        if isinstance(coord, coord_flip):
            x, y = y, x
            data[x], data[y] = data[y], data[x]

        if outline_type in ("lower", "both"):
            geom_path.draw_group(
                data.assign(y=data[f"{y}min"]),
                panel_params,
                coord,
                ax,
                params,
            )

        if outline_type in ("upper", "both"):
            geom_path.draw_group(
                data.assign(y=data[f"{y}max"]),
                panel_params,
                coord,
                ax,
                params,
            )
</file>

<file path="plotnine/geoms/geom_segment.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, interleave, make_line_segments, to_rgba
from ..doctools import document
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_segment(geom):
    """
    Line segments

    {usage}

    Parameters
    ----------
    {common_parameters}
    lineend : Literal["butt", "round", "projecting"], default="butt"
        Line end style. This option is applied for solid linetypes.
    arrow : ~plotnine.geoms.geom_path.arrow, default=None
        Arrow specification. Default is no arrow.

    See Also
    --------
    plotnine.arrow : for adding arrowhead(s) to segments.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }
    REQUIRED_AES = {"x", "y", "xend", "yend"}
    NON_MISSING_AES = {"linetype", "size", "shape"}
    DEFAULT_PARAMS = {"lineend": "butt", "arrow": None}

    draw_legend = staticmethod(geom_path.draw_legend)
    legend_key_size = staticmethod(geom_path.legend_key_size)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.collections import LineCollection

        data = coord.transform(data, panel_params)
        linewidth = data["size"] * SIZE_FACTOR
        color = to_rgba(data["color"], data["alpha"])

        # start point -> end point, sequence of xy points
        # from which line segments are created
        x = interleave(data["x"], data["xend"])
        y = interleave(data["y"], data["yend"])
        segments = make_line_segments(x, y, ispath=False)
        coll = LineCollection(
            list(segments),
            edgecolor=color,
            linewidth=linewidth,
            linestyle=data["linetype"][0],
            capstyle=params.get("lineend"),
            zorder=params["zorder"],
            rasterized=params["raster"],
        )
        ax.add_collection(coll)

        if "arrow" in params and params["arrow"]:
            adata = pd.DataFrame(index=range(len(data) * 2))
            idx = np.arange(1, len(data) + 1)
            adata["group"] = np.hstack([idx, idx])
            adata["x"] = np.hstack([data["x"], data["xend"]])
            adata["y"] = np.hstack([data["y"], data["yend"]])
            adata["linewidth"] = np.hstack([linewidth, linewidth])
            other = ["color", "alpha", "linetype"]
            for param in other:
                adata[param] = np.hstack([data[param], data[param]])

            params["arrow"].draw(
                adata, panel_params, coord, ax, params, constant=False
            )
</file>

<file path="plotnine/geoms/geom_sina.py">
from ..doctools import document
from .geom_point import geom_point


@document
class geom_sina(geom_point):
    """
    Draw a sina plot

    {usage}

    A sina plot is a data visualization chart suitable for plotting
    any single variable in a multiclass dataset. It is an enhanced
    jitter strip chart, where the width of the jitter is controlled
    by the density distribution of the data within each class.

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.stat_sina : The default `stat` for this `geom`.

    References
    ----------
    Sidiropoulos, N., S. H. Sohi, T. L. Pedersen, B. T. Porse, O. Winther,
    N. Rapin, and F. O. Bagger. 2018.
    "SinaPlot: An Enhanced Chart for Simple and Truthful Representation of
    Single Observations over Multiple Classes."
    J. Comp. Graph. Stat 27: 673–76.
    """

    DEFAULT_PARAMS = {"stat": "sina", "position": "dodge"}
</file>

<file path="plotnine/geoms/geom_smooth.py">
from __future__ import annotations

import typing

from .._utils import to_rgba
from ..doctools import document
from .geom import geom
from .geom_line import geom_line, geom_path
from .geom_ribbon import geom_ribbon

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer


@document
class geom_smooth(geom):
    """
    A smoothed conditional mean

    {usage}

    Parameters
    ----------
    {common_parameters}
    legend_fill_ratio : float, default=0.5
        How much (vertically) of the legend box should be filled by
        the color that indicates the confidence intervals. Should be
        in the range [0, 1].

    See Also
    --------
    plotnine.stat_smooth : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {
        "alpha": 0.4,
        "color": "black",
        "fill": "#999999",
        "linetype": "solid",
        "size": 1,
        "ymin": None,
        "ymax": None,
    }
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {"stat": "smooth", "legend_fill_ratio": 0.5}

    legend_key_size = staticmethod(geom_path.legend_key_size)

    def use_defaults(
        self, data: pd.DataFrame, aes_modifiers: dict[str, Any]
    ) -> pd.DataFrame:
        has_ribbon = "ymin" in data and "ymax" in data
        data = super().use_defaults(data, aes_modifiers)

        # When there is no ribbon, the default values for 'ymin'
        # and 'ymax' are None (not numeric). So we remove them
        # prevent any computations that may use them without checking.
        if not has_ribbon:
            del data["ymin"]
            del data["ymax"]
        return data

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.sort_values(["PANEL", "group", "x"])

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        has_ribbon = "ymin" in data and "ymax" in data
        if has_ribbon:
            data2 = data.copy()
            data2["color"] = "none"
            params2 = params.copy()
            params2["outline_type"] = "full"
            geom_ribbon.draw_group(data2, panel_params, coord, ax, params2)

        data["alpha"] = 1
        geom_line.draw_group(data, panel_params, coord, ax, params)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw letter 'a' in the box

        Parameters
        ----------
        data : dataframe
            Legend data
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.patches import Rectangle

        try:
            has_se = lyr.stat.params["se"]
        except KeyError:
            has_se = False

        if has_se:
            fill = to_rgba(data["fill"], data["alpha"])
            r = lyr.geom.params["legend_fill_ratio"]
            bg = Rectangle(
                (0, (1 - r) * da.height / 2),
                width=da.width,
                height=r * da.height,
                facecolor=fill,
                linewidth=0,
            )
            da.add_artist(bg)

        data["alpha"] = 1
        return geom_path.draw_legend(data, da, lyr)
</file>

<file path="plotnine/geoms/geom_spoke.py">
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..doctools import document
from .geom_segment import geom_segment

if TYPE_CHECKING:
    import pandas as pd


@document
class geom_spoke(geom_segment):
    """
    Line segment parameterised by location, direction and distance

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_segment : For documentation of extra
        parameters.
    """

    REQUIRED_AES = {"x", "y", "angle", "radius"}

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            radius = data["radius"]
        except KeyError:
            radius = self.aes_params["radius"]
        try:
            angle = data["angle"]
        except KeyError:
            angle = self.aes_params["angle"]

        data["xend"] = data["x"] + np.cos(angle) * radius
        data["yend"] = data["y"] + np.sin(angle) * radius
        return data
</file>

<file path="plotnine/geoms/geom_step.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import copy_missing_columns
from ..doctools import document
from ..exceptions import PlotnineError
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view


@document
class geom_step(geom_path):
    """
    Stepped connected points

    {usage}

    Parameters
    ----------
    {common_parameters}
    direction : Literal["hv", "vh", "mid"], default="hv"
        horizontal-vertical steps,
        vertical-horizontal steps or steps half-way between adjacent
        x values.

    See Also
    --------
    plotnine.geom_path : For documentation of extra parameters.
    """

    DEFAULT_PARAMS = {"direction": "hv"}

    draw_panel = geom.draw_panel

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        direction = params["direction"]
        n = len(data)
        data = data.sort_values("x", kind="mergesort")
        x = data["x"].to_numpy()
        y = data["y"].to_numpy()

        if direction == "vh":
            # create stepped path -- interleave x with
            # itself and y with itself
            xidx = np.repeat(range(n), 2)[:-1]
            yidx = np.repeat(range(n), 2)[1:]
            new_x, new_y = x[xidx], y[yidx]
        elif direction == "hv":
            xidx = np.repeat(range(n), 2)[1:]
            yidx = np.repeat(range(n), 2)[:-1]
            new_x, new_y = x[xidx], y[yidx]
        elif direction == "mid":
            xidx = np.repeat(range(n - 1), 2)
            yidx = np.repeat(range(n), 2)
            diff = x[1::] - x[:-1:]
            mid_x = x[:-1:] + diff / 2
            new_x = np.hstack([x[0], mid_x[xidx], x[-1]])
            new_y = y[yidx]
        else:
            raise PlotnineError(f"Invalid direction `{direction}`")

        path_data = pd.DataFrame({"x": new_x, "y": new_y})
        copy_missing_columns(path_data, data)
        geom_path.draw_group(path_data, panel_params, coord, ax, params)
</file>

<file path="plotnine/geoms/geom_tile.py">
from __future__ import annotations

import typing

from .._utils import resolution
from ..doctools import document
from .geom_rect import geom_rect

if typing.TYPE_CHECKING:
    import pandas as pd


@document
class geom_tile(geom_rect):
    """
    Rectangles specified using a center points

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_rect
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": None,
        "fill": "#333333",
        "linetype": "solid",
        "size": 0.1,
        "width": None,
        "height": None,
    }
    REQUIRED_AES = {"x", "y"}

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            width = data.pop("width")
        except KeyError:
            width = self.aes_params.get(
                "width",
                resolution(data["x"], False),
            )

        try:
            height = data.pop("height")
        except KeyError:
            height = self.aes_params.get(
                "height",
                resolution(data["y"], False),
            )

        data["xmin"] = data["x"] - width / 2
        data["xmax"] = data["x"] + width / 2
        data["ymin"] = data["y"] - height / 2
        data["ymax"] = data["y"] + height / 2
        return data
</file>

<file path="plotnine/geoms/geom_violin.py">
from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from .._utils import groupby_apply, interleave, resolution
from ..doctools import document
from .geom import geom
from .geom_path import geom_path
from .geom_polygon import geom_polygon

if TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import DataLike, FloatArray


@document
class geom_violin(geom):
    """
    Violin Plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    draw_quantiles : float | list[float], default=None
        draw horizontal lines at the given quantiles (0..1)
        of the density estimate.
    style : str, default="full"
        The type of violin plot to draw. The options are:

        ```python
        'full'        # Regular (2 sided violins)
        'left'        # Left-sided half violins
        'right'       # Right-sided half violins
        'left-right'  # Alternate (left first) half violins by the group
        'right-left'  # Alternate (right first) half violins by the group
        ```

    See Also
    --------
    plotnine.stat_ydensity : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "#333333",
        "fill": "white",
        "linetype": "solid",
        "size": 0.5,
        "weight": 1,
    }
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "stat": "ydensity",
        "position": "dodge",
        "draw_quantiles": None,
        "style": "full",
        "scale": "area",
        "trim": True,
        "width": None,
    }
    draw_legend = staticmethod(geom_polygon.draw_legend)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        if "draw_quantiles" in kwargs:
            kwargs["draw_quantiles"] = np.repeat(kwargs["draw_quantiles"], 1)
            if not all(0 < q < 1 for q in kwargs["draw_quantiles"]):
                raise ValueError(
                    "draw_quantiles must be a float or "
                    "an iterable of floats (>0.0; < 1.0)"
                )

        if "style" in kwargs:
            allowed = ("full", "left", "right", "left-right", "right-left")
            if kwargs["style"] not in allowed:
                raise ValueError(f"style must be either {allowed}")

        super().__init__(mapping, data, **kwargs)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if "width" not in data:
            if self.params["width"]:
                data["width"] = self.params["width"]
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        def func(df: pd.DataFrame) -> pd.DataFrame:
            df["ymin"] = df["y"].min()
            df["ymax"] = df["y"].max()
            df["xmin"] = df["x"] - df["width"] / 2
            df["xmax"] = df["x"] + df["width"] / 2
            return df

        # This is a plyr::ddply
        data = groupby_apply(data, ["group", "PANEL"], func)
        return data

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        params = self.params.copy()
        quantiles = params.pop("draw_quantiles")
        style = params.pop("style")
        zorder = params.pop("zorder")

        for i, (group, df) in enumerate(data.groupby("group")):
            # Place the violins with the smalleer group number on top
            # of those with larger numbers. The group_zorder values should be
            # in the range [zorder, zorder + 1) to stay within the layer.
            group = cast("int", group)
            group_zorder = zorder + 0.9 / group
            params["zorder"] = group_zorder

            # Find the points for the line to go all the way around
            df["xminv"] = df["x"] - df["violinwidth"] * (df["x"] - df["xmin"])
            df["xmaxv"] = df["x"] + df["violinwidth"] * (df["xmax"] - df["x"])
            even = i % 2 == 0
            if (
                style == "left"
                or (style == "left-right" and even)
                or (style == "right-left" and not even)
            ):
                df["xmaxv"] = df["x"]
            elif (
                style == "right"
                or (style == "right-left" and even)
                or (style == "left-right" and not even)
            ):
                df["xminv"] = df["x"]

            # Make sure it's sorted properly to draw the outline
            # i.e violin = kde + mirror kde,
            # bottom to top then top to bottom
            n = len(df)
            polygon_df = pd.concat(
                [df.sort_values("y"), df.sort_values("y", ascending=False)],
                axis=0,
                ignore_index=True,
            )

            _df = polygon_df.iloc
            _loc = polygon_df.columns.get_loc
            _df[:n, _loc("x")] = _df[:n, _loc("xminv")]  # type: ignore
            _df[n:, _loc("x")] = _df[n:, _loc("xmaxv")]  # type: ignore

            # Close the polygon: set first and last point the same
            polygon_df.loc[-1, :] = polygon_df.loc[0, :]

            # plot violin polygon
            geom_polygon.draw_group(
                polygon_df,
                panel_params,
                coord,
                ax,
                params,
            )

            if quantiles is not None:
                # Get dataframe with quantile segments and that
                # with aesthetics then put them together
                # Each quantile segment is defined by 2 points and
                # they all get similar aesthetics
                aes_df = df.drop(["x", "y", "group"], axis=1)
                aes_df.reset_index(inplace=True)
                idx = [0] * 2 * len(quantiles)
                aes_df = aes_df.iloc[idx, :].reset_index(drop=True)
                segment_df = pd.concat(
                    [make_quantile_df(df, quantiles), aes_df], axis=1
                )

                # plot quantile segments
                geom_path.draw_group(
                    segment_df,
                    panel_params,
                    coord,
                    ax,
                    params,
                )


def make_quantile_df(
    data: pd.DataFrame, draw_quantiles: FloatArray
) -> pd.DataFrame:
    """
    Return a dataframe with info needed to draw quantile segments
    """
    from scipy.interpolate import interp1d

    dens = data["density"].cumsum() / data["density"].sum()
    ecdf = interp1d(dens, data["y"], assume_sorted=True)
    ys = ecdf(draw_quantiles)

    # Get the violin bounds for the requested quantiles
    violin_xminvs = interp1d(data["y"], data["xminv"])(ys)
    violin_xmaxvs = interp1d(data["y"], data["xmaxv"])(ys)

    data = pd.DataFrame(
        {
            "x": interleave(violin_xminvs, violin_xmaxvs),
            "y": np.repeat(ys, 2),
            "group": np.repeat(np.arange(1, len(ys) + 1), 2),
        }
    )

    return data
</file>

<file path="plotnine/geoms/geom_vline.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, order_as_data_mapping, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from ..mapping import aes
from .geom import geom
from .geom_segment import geom_segment

if typing.TYPE_CHECKING:
    from typing import Any

    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import DataLike


@document
class geom_vline(geom):
    """
    Vertical line

    {usage}

    Parameters
    ----------
    {common_parameters}
    """

    DEFAULT_AES = {
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
        "alpha": 1,
    }
    REQUIRED_AES = {"xintercept"}
    DEFAULT_PARAMS = {"inherit_aes": False}

    legend_key_size = staticmethod(geom_segment.legend_key_size)

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        data, mapping = order_as_data_mapping(data, mapping)
        xintercept = kwargs.pop("xintercept", None)
        if xintercept is not None:
            if mapping:
                warn(
                    "The 'xintercept' parameter has overridden "
                    "the aes() mapping.",
                    PlotnineWarning,
                )
            data = pd.DataFrame({"xintercept": np.repeat(xintercept, 1)})
            mapping = aes(xintercept="xintercept")
            kwargs["show_legend"] = False

        geom.__init__(self, mapping, data, **kwargs)

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups
        """
        ranges = coord.backtransform_range(panel_params)
        data["x"] = data["xintercept"]
        data["xend"] = data["xintercept"]
        data["y"] = ranges.y[0]
        data["yend"] = ranges.y[1]
        data = data.drop_duplicates()

        for _, gdata in data.groupby("group"):
            gdata.reset_index(inplace=True)
            geom_segment.draw_group(
                gdata, panel_params, coord, ax, self.params
            )

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a vertical line in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.lines import Line2D

        x = [0.5 * da.width] * 2
        y = [0, da.height]
        linewidth = data["size"] * SIZE_FACTOR
        color = to_rgba(data["color"], data["alpha"])
        key = Line2D(
            x,
            y,
            linestyle=data["linetype"],
            linewidth=linewidth,
            color=color,
            solid_capstyle="butt",
            antialiased=False,
        )
        da.add_artist(key)
        return da
</file>

<file path="plotnine/positions/position.py">
from __future__ import annotations

import typing
from abc import ABC
from copy import copy
from warnings import warn

import numpy as np

from .._utils import check_required_aesthetics, groupby_apply
from .._utils.registry import Register
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.aes import X_AESTHETICS, Y_AESTHETICS

if typing.TYPE_CHECKING:
    from typing import Any, Optional

    import pandas as pd

    from plotnine.facets.layout import Layout
    from plotnine.iapi import pos_scales
    from plotnine.typing import TransformCol


class position(ABC, metaclass=Register):
    """Base class for all positions"""

    REQUIRED_AES: set[str] = set()
    """
    Aesthetics required for the positioning
    """
    params: dict[str, Any]

    def __init__(self):
        self.params = {}

    def setup_params(self, data: pd.DataFrame) -> dict[str, Any]:
        """
        Verify, modify & return a copy of the params.
        """
        return copy(self.params)

    def setup_data(
        self, data: pd.DataFrame, params: dict[str, Any]
    ) -> pd.DataFrame:
        """
        Verify & return data
        """
        check_required_aesthetics(
            self.REQUIRED_AES, data.columns, self.__class__.__name__
        )
        return data

    @classmethod
    def compute_layer(
        cls, data: pd.DataFrame, params: dict[str, Any], layout: Layout
    ):
        """
        Compute position for the layer in all panels

        Positions can override this function instead of
        `compute_panel` if the position computations are
        independent of the panel. i.e when not colliding
        """

        def fn(pdata: pd.DataFrame) -> pd.DataFrame:
            """
            Compute function helper
            """
            # Given data belonging to a specific panel, grab
            # the corresponding scales and call the method
            # that does the real computation
            if len(pdata) == 0:
                return pdata
            scales = layout.get_scales(pdata["PANEL"].iloc[0])
            return cls.compute_panel(pdata, scales, params)

        return groupby_apply(data, "PANEL", fn)

    @classmethod
    def compute_panel(
        cls, data: pd.DataFrame, scales: pos_scales, params: dict[str, Any]
    ) -> pd.DataFrame:
        """
        Positions must override this function

        Notes
        -----
        Make necessary adjustments to the columns in the dataframe.

        Create the position transformation functions and
        use self.transform_position() do the rest.

        See Also
        --------
        plotnine.position_jitter.compute_panel
        """
        msg = "{} needs to implement this method"
        raise NotImplementedError(msg.format(cls.__name__))

    @staticmethod
    def transform_position(
        data,
        trans_x: Optional[TransformCol] = None,
        trans_y: Optional[TransformCol] = None,
    ) -> pd.DataFrame:
        """
        Transform all the variables that map onto the x and y scales.

        Parameters
        ----------
        data : dataframe
            Data to transform
        trans_x : callable
            Transforms x scale mappings
            Takes one argument, either a scalar or an array-type
        trans_y : callable
            Transforms y scale mappings
            Takes one argument, either a scalar or an array-type
        """
        if len(data) == 0:
            return data

        if trans_x:
            xs = [name for name in data.columns if name in X_AESTHETICS]
            data[xs] = data[xs].apply(trans_x)

        if trans_y:
            ys = [name for name in data.columns if name in Y_AESTHETICS]
            data[ys] = data[ys].apply(trans_y)

        return data

    @staticmethod
    def strategy(data: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
        """
        Calculate boundaries of geometry object
        """
        return data

    @classmethod
    def _collide_setup(cls, data, params):
        xminmax = ["xmin", "xmax"]
        width = params.get("width", None)

        # Determine width
        if width is not None:
            # Width set manually
            if not all(col in data.columns for col in xminmax):
                data["xmin"] = data["x"] - width / 2
                data["xmax"] = data["x"] + width / 2
        else:
            if not all(col in data.columns for col in xminmax):
                data["xmin"] = data["x"]
                data["xmax"] = data["x"]

            # Width determined from data, must be floating point constant
            widths = (data["xmax"] - data["xmin"]).drop_duplicates()
            widths = widths[~np.isnan(widths)]
            width = widths.iloc[0]

        return data, width

    @classmethod
    def collide(cls, data, params):
        """
        Calculate boundaries of geometry object

        Uses Strategy
        """
        xminmax = ["xmin", "xmax"]
        data, width = cls._collide_setup(data, params)
        if params.get("width", None) is None:
            params["width"] = width

        # Reorder by x position then on group, relying on stable sort to
        # preserve existing ordering. The default stacking order reverses
        # the group in order to match the legend order.
        if params and "reverse" in params and params["reverse"]:
            idx = data.sort_values(["xmin", "group"], kind="mergesort").index
        else:
            data["-group"] = -data["group"]
            idx = data.sort_values(["xmin", "-group"], kind="mergesort").index
            del data["-group"]

        data = data.loc[idx, :]

        # Check for overlap
        intervals = data[xminmax].drop_duplicates().to_numpy().flatten()
        intervals = intervals[~np.isnan(intervals)]

        if len(np.unique(intervals)) > 1 and any(
            np.diff(intervals - intervals.mean()) < -1e-6
        ):
            msg = "{} requires non-overlapping x intervals"
            warn(msg.format(cls.__name__), PlotnineWarning)

        if "ymax" in data:
            data = groupby_apply(data, "xmin", cls.strategy, params)
        elif "y" in data:
            data["ymax"] = data["y"]
            data = groupby_apply(data, "xmin", cls.strategy, params)
            data["y"] = data["ymax"]
        else:
            raise PlotnineError("Neither y nor ymax defined")

        return data

    @classmethod
    def collide2(cls, data, params):
        """
        Calculate boundaries of geometry object

        Uses Strategy
        """
        data, width = cls._collide_setup(data, params)
        if params.get("width", None) is None:
            params["width"] = width

        # Reorder by x position then on group, relying on stable sort to
        # preserve existing ordering. The default stacking order reverses
        # the group in order to match the legend order.
        if params and "reverse" in params and params["reverse"]:
            data["-group"] = -data["group"]
            idx = data.sort_values(["x", "-group"], kind="mergesort").index
            del data["-group"]
        else:
            idx = data.sort_values(["x", "group"], kind="mergesort").index

        data = data.loc[idx, :]
        data.reset_index(inplace=True, drop=True)
        return cls.strategy(data, params)


transform_position = position.transform_position
</file>

<file path="plotnine/scales/__init__.py">
"""
Scales
"""

# limits
from .limits import expand_limits, lims, xlim, ylim

# alpha
from .scale_alpha import (
    scale_alpha,
    scale_alpha_continuous,
    scale_alpha_datetime,
    scale_alpha_discrete,
    scale_alpha_ordinal,
)

# pyright: reportGeneralTypeIssues=true
# fill
# color
from .scale_color import (
    scale_color_brewer,
    scale_color_cmap,
    scale_color_cmap_d,
    scale_color_continuous,
    scale_color_datetime,
    scale_color_desaturate,
    scale_color_discrete,
    scale_color_distiller,
    scale_color_gradient,
    scale_color_gradient2,
    scale_color_gradientn,
    scale_color_gray,
    scale_color_grey,
    scale_color_hue,
    scale_color_ordinal,
    scale_colour_brewer,
    scale_colour_cmap,
    scale_colour_cmap_d,
    scale_colour_continuous,
    scale_colour_datetime,
    scale_colour_desaturate,
    scale_colour_discrete,
    scale_colour_distiller,
    scale_colour_gradient,
    scale_colour_gradient2,
    scale_colour_gradientn,
    scale_colour_gray,
    scale_colour_grey,
    scale_colour_hue,
    scale_colour_ordinal,
    scale_fill_brewer,
    scale_fill_cmap,
    scale_fill_cmap_d,
    scale_fill_continuous,
    scale_fill_datetime,
    scale_fill_desaturate,
    scale_fill_discrete,
    scale_fill_distiller,
    scale_fill_gradient,
    scale_fill_gradient2,
    scale_fill_gradientn,
    scale_fill_gray,
    scale_fill_grey,
    scale_fill_hue,
    scale_fill_ordinal,
)

# identity
from .scale_identity import (
    scale_alpha_identity,
    scale_color_identity,
    scale_colour_identity,
    scale_fill_identity,
    scale_linetype_identity,
    scale_shape_identity,
    scale_size_identity,
    scale_stroke_identity,
)

# linetype
from .scale_linetype import (
    scale_linetype,
    scale_linetype_discrete,
)

# manual
from .scale_manual import (
    scale_alpha_manual,
    scale_color_manual,
    scale_colour_manual,
    scale_fill_manual,
    scale_linetype_manual,
    scale_shape_manual,
    scale_size_manual,
)

# shape
from .scale_shape import (
    scale_shape,
    scale_shape_discrete,
)

# size
from .scale_size import (
    scale_size,
    scale_size_area,
    scale_size_continuous,
    scale_size_datetime,
    scale_size_discrete,
    scale_size_ordinal,
    scale_size_radius,
)

# stroke
from .scale_stroke import (
    scale_stroke,
    scale_stroke_continuous,
)

# xy position and transforms
from .scale_xy import (
    scale_x_continuous,
    scale_x_date,
    scale_x_datetime,
    scale_x_discrete,
    scale_x_log10,
    scale_x_reverse,
    scale_x_sqrt,
    scale_x_symlog,
    scale_x_timedelta,
    scale_y_continuous,
    scale_y_date,
    scale_y_datetime,
    scale_y_discrete,
    scale_y_log10,
    scale_y_reverse,
    scale_y_sqrt,
    scale_y_symlog,
    scale_y_timedelta,
)

__all__ = (
    # color
    "scale_color_brewer",
    "scale_colour_brewer",
    "scale_color_cmap",
    "scale_colour_cmap",
    "scale_color_cmap_d",
    "scale_colour_cmap_d",
    "scale_color_ordinal",
    "scale_colour_ordinal",
    "scale_color_continuous",
    "scale_colour_continuous",
    "scale_color_discrete",
    "scale_colour_discrete",
    "scale_color_distiller",
    "scale_colour_distiller",
    "scale_color_desaturate",
    "scale_colour_desaturate",
    "scale_color_gradient",
    "scale_colour_gradient",
    "scale_color_gradient2",
    "scale_colour_gradient2",
    "scale_color_gradientn",
    "scale_colour_gradientn",
    "scale_color_grey",
    "scale_colour_grey",
    "scale_color_gray",
    "scale_colour_gray",
    "scale_color_hue",
    "scale_colour_hue",
    "scale_color_datetime",
    "scale_colour_datetime",
    # fill
    "scale_fill_brewer",
    "scale_fill_cmap",
    "scale_fill_cmap_d",
    "scale_fill_ordinal",
    "scale_fill_continuous",
    "scale_fill_desaturate",
    "scale_fill_discrete",
    "scale_fill_distiller",
    "scale_fill_gradient",
    "scale_fill_gradient2",
    "scale_fill_gradientn",
    "scale_fill_grey",
    "scale_fill_gray",
    "scale_fill_hue",
    "scale_fill_datetime",
    # alpha
    "scale_alpha",
    "scale_alpha_discrete",
    "scale_alpha_ordinal",
    "scale_alpha_continuous",
    "scale_alpha_datetime",
    # linetype
    "scale_linetype",
    "scale_linetype_discrete",
    # shape
    "scale_shape",
    "scale_shape_discrete",
    # size
    "scale_size",
    "scale_size_area",
    "scale_size_discrete",
    "scale_size_continuous",
    "scale_size_ordinal",
    "scale_size_radius",
    "scale_size_datetime",
    # stroke
    "scale_stroke",
    "scale_stroke_continuous",
    # identity
    "scale_alpha_identity",
    "scale_color_identity",
    "scale_colour_identity",
    "scale_fill_identity",
    "scale_linetype_identity",
    "scale_shape_identity",
    "scale_size_identity",
    "scale_stroke_identity",
    # manual
    "scale_color_manual",
    "scale_colour_manual",
    "scale_fill_manual",
    "scale_shape_manual",
    "scale_linetype_manual",
    "scale_alpha_manual",
    "scale_size_manual",
    # xy position and transforms
    "scale_x_continuous",
    "scale_x_date",
    "scale_x_datetime",
    "scale_x_discrete",
    "scale_x_log10",
    "scale_x_reverse",
    "scale_x_sqrt",
    "scale_x_symlog",
    "scale_x_timedelta",
    "scale_y_continuous",
    "scale_y_date",
    "scale_y_datetime",
    "scale_y_discrete",
    "scale_y_log10",
    "scale_y_reverse",
    "scale_y_sqrt",
    "scale_y_symlog",
    "scale_y_timedelta",
    # limits
    "xlim",
    "ylim",
    "lims",
    "expand_limits",
)
</file>

<file path="plotnine/scales/scale_color.py">
from __future__ import annotations

from dataclasses import KW_ONLY, InitVar, dataclass, field
from typing import Literal, Sequence
from warnings import warn

from .._utils.registry import alias
from ..exceptions import PlotnineWarning
from .scale_continuous import scale_continuous
from .scale_datetime import scale_datetime
from .scale_discrete import scale_discrete


@dataclass
class _scale_color_discrete(scale_discrete):
    """
    Base class for all discrete color scales
    """

    _aesthetics = ["color"]
    _: KW_ONLY
    na_value: str = "#7F7F7F"
    """
    Color of missing values.
    """


@dataclass
class _scale_color_continuous(
    scale_continuous[Literal["legend", "colorbar"] | None],
):
    """
    Base class for all continuous color scales
    """

    _aesthetics = ["color"]
    _: KW_ONLY
    guide: Literal["legend", "colorbar"] | None = "colorbar"
    na_value: str = "#7F7F7F"
    """
    Color of missing values.
    """


# Discrete color scales #
# Note: plotnine operates in the hcl space
@dataclass
class scale_color_hue(_scale_color_discrete):
    """
    Qualitative color scale with evenly spaced hues

    See Also
    --------
    mizani.palettes.hue_pal : The palette class that generates colours
        in HCL space.
    """

    h: InitVar[float | tuple[float, float]] = 15
    """
    Hue. If a float, it is the first hue value, in the range `[0, 360]`.
    The range of the palette will be `[first, first + 360)`.

    If a tuple, it is the range `[first, last)` of the hues.
    """

    c: InitVar[float] = 100
    """
    Chroma. Must be in the range `[0, 100]`
    """

    l: InitVar[float] = 65
    """
    Lightness. Must be in the range [0, 100]
    """

    direction: InitVar[Literal[1, -1]] = 1
    """
    The order of colours in the scale. If -1 the order
    of colours is reversed. The default is 1.
    """

    _: KW_ONLY

    s: None = field(default=None, repr=False)
    """
    Not being used and will be removed in a future version
    """
    color_space: None = field(default=None, repr=False)
    """
    Not being used and will be removed in a future version
    """

    def __post_init__(self, h, c, l, direction):
        from mizani.palettes import hue_pal

        if (s := self.s) is not None:
            warn(
                f"You used {s=} for the saturation which has been ignored. "
                f"{self.__class__.__name__} now works in HCL colorspace. "
                f"Using `s` in future versions will throw an exception.",
                FutureWarning,
            )
            del self.s

        if (color_space := self.color_space) is not None:
            warn(
                f"You used {color_space=} to select a color_space and it "
                f"has been ignored. {self.__class__.__name__} now only works "
                f"in HCL colorspace. Using `color_space` in future versions "
                "will throw an exception.",
                FutureWarning,
            )
            del self.color_space

        super().__post_init__()
        self.palette = hue_pal(h, c, l, direction)


@dataclass
class scale_fill_hue(scale_color_hue):
    """
    Qualitative color scale with evenly spaced hues
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_brewer(_scale_color_discrete):
    """
    Sequential, diverging and qualitative discrete color scales

    See `colorbrewer.org <http://colorbrewer2.org/>`_

    See Also
    --------
    mizani.palette.brewer_pal : The palette class that generates colours
        that generates the brewer colors.
    """

    type: InitVar[
        Literal[
            "diverging",
            "qualitative",
            "sequential",
            "div",
            "qual",
            "seq",
        ]
    ] = "seq"
    """
    Type of data
    """

    palette: InitVar[int | str] = 1
    """
    If a string, will use that named palette. If a number, will index
    into the list of palettes of appropriate type.
    """

    direction: InitVar[Literal[1, -1]] = 1
    """
    Sets the order of colors in the scale. If 1, colors are as output
    [](`~mizani.palettes.brewer_pal`). If -1, the order of colors is
    reversed.
    """

    def __post_init__(self, type, palette, direction):
        from mizani.palettes import brewer_pal

        super().__post_init__()
        self.palette = brewer_pal(  # type: ignore
            type, palette, direction=direction
        )


@dataclass
class scale_fill_brewer(scale_color_brewer):
    """
    Sequential, diverging and qualitative color scales
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_grey(_scale_color_discrete):
    """
    Sequential grey color scale.

    See Also
    --------
    mizani.palettes.grey_pal : The palette class that generates colours
        gray scale color.
    """

    start: InitVar[float] = 0.2
    """
    Grey value at low end of palette.
    """

    end: InitVar[float] = 0.8
    """
    Grey value at high end of palette
    """

    _aesthetics = ["color"]

    def __post_init__(self, start, end):
        from mizani.palettes import grey_pal

        super().__post_init__()
        self.palette = grey_pal(start, end)


@dataclass
class scale_fill_grey(scale_color_grey):
    """
    Sequential grey color scale.
    """

    _aesthetics = ["fill"]


# Continuous color scales #


@dataclass
class scale_color_gradient(_scale_color_continuous):
    """
    Create a 2 point color gradient

    See Also
    --------
    plotnine.scale_color_gradient2
    plotnine.scale_color_gradientn
    mizani.palettes.gradient_n_pal : The palette class that generates
        the colour gradient.
    """

    low: InitVar[str] = "#132B43"
    """
    Low color.
    """

    high: InitVar[str] = "#56B1F7"
    """
    High color.
    """

    def __post_init__(self, low, high):
        from mizani.palettes import gradient_n_pal

        super().__post_init__()
        self.palette = gradient_n_pal([low, high])


@dataclass
class scale_fill_gradient(scale_color_gradient):
    """
    Create a 2 point color gradient
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_desaturate(_scale_color_continuous):
    """
    Create a desaturated color gradient

    See Also
    --------
    mizani.palettes.desaturate_pal : The palette class that generates
        the desaturated colours.
    """

    color: InitVar[str] = "red"
    """
    Color to desaturate
    """

    prop: InitVar[float] = 0
    """
    Saturation channel of color will be multiplied by this value.
    """

    reverse: InitVar[bool] = False
    """
    Whether to go from color to desaturated color or desaturated color
    to color.
    """

    def __post_init__(self, color, prop, reverse):
        from mizani.palettes import desaturate_pal

        super().__post_init__()
        self.palette = desaturate_pal(color, prop, reverse)


@dataclass
class scale_fill_desaturate(scale_color_desaturate):
    """
    Create a desaturated color gradient
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_gradient2(_scale_color_continuous):
    """
    Create a 3 point diverging color gradient

    See Also
    --------
    plotnine.scale_color_gradient
    plotnine.scale_color_gradientn
    mizani.palettes.gradient_n_pal : The palette class that generates
        the colour gradient.
    """

    low: InitVar[str] = "#832424"
    """
    Low color.
    """

    mid: InitVar[str] = "#FFFFFF"
    """
    Mid-point color.

    """
    high: InitVar[str] = "#3A3A98"
    """
    High color.
    """

    midpoint: InitVar[float] = 0
    """
    Mid point of the input data range.
    """

    def __post_init__(self, low, mid, high, midpoint):
        from mizani.bounds import rescale_mid
        from mizani.palettes import gradient_n_pal

        # All rescale functions should have the same signature
        def _rescale_mid(*args, **kwargs):
            return rescale_mid(*args, mid=midpoint, **kwargs)

        self.rescaler = _rescale_mid
        self.palette = gradient_n_pal([low, mid, high])
        super().__post_init__()


@dataclass
class scale_fill_gradient2(scale_color_gradient2):
    """
    Create a 3 point diverging color gradient
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_gradientn(_scale_color_continuous):
    """
    Create a n color gradient

    See Also
    --------
    plotnine.scale_color_gradient
    plotnine.scale_color_gradientn
    mizani.palettes.gradient_n_pal : The palette class that generates
        the colour gradient.
    """

    colors: InitVar[Sequence[str]]
    """
    List of colors
    """

    values: InitVar[Sequence[float] | None] = None
    """
    list of points in the range [0, 1] at which to place each color.
    Must be the same size as `colors`. Default to evenly space the colors
    """

    def __post_init__(self, colors, values):
        from mizani.palettes import gradient_n_pal

        super().__post_init__()
        self.palette = gradient_n_pal(colors, values)


@dataclass
class scale_fill_gradientn(scale_color_gradientn):
    """
    Create a n color gradient
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_distiller(_scale_color_continuous):
    """
    Sequential and diverging continuous color scales

    This is a convenience scale around
    [](`~plotnine.scales.scale_color_gradientn`) with colors from
    [colorbrewer.org](http://colorbrewer2.org). It smoothly
    interpolates 7 colors from a brewer palette to create a
    continuous palette.
    """

    type: InitVar[
        Literal[
            "diverging",
            "qualitative",
            "sequential",
            "div",
            "qual",
            "seq",
        ]
    ] = "seq"
    """
    Type of data
    """

    palette: InitVar[int | str] = 1
    """
    If a string, will use that named palette. If a number, will index
    into the list of palettes of appropriate type.
    """

    values: InitVar[Sequence[float] | None] = None
    """
    List of points in the range [0, 1] at which to place each color.
    Must be the same size as `colors`. Default to evenly space the colors
    """

    direction: InitVar[Literal[1, -1]] = 1
    """
    Sets the order of colors in the scale. If 1, colors are as output
    [](`~mizani.palettes.brewer_pal`). If -1, the order of colors is
    reversed.
    """

    def __post_init__(self, type, palette, values, direction):
        """
        Create colormap that will be used by the palette
        """
        from mizani.palettes import brewer_pal, gradient_n_pal

        if type.lower() in ("qual", "qualitative"):
            warn(
                "Using a discrete color palette in a continuous scale."
                "Consider using type = 'seq' or type = 'div' instead",
                PlotnineWarning,
            )

        # Grab 7 colors from brewer and create a gradient palette
        # An odd number matches the midpoint of the palette to that
        # of the data
        super().__post_init__()
        colors = brewer_pal(type, palette, direction=direction)(7)
        self.palette = gradient_n_pal(colors, values)  # type: ignore


@dataclass
class scale_fill_distiller(scale_color_distiller):
    """
    Sequential, diverging continuous color scales
    """

    _aesthetics = ["fill"]


# matplotlib colormaps
@dataclass
class scale_color_cmap(_scale_color_continuous):
    """
    Create color scales using Matplotlib colormaps

    See Also
    --------
    [](`matplotlib.cm`)
    [](`matplotlib.colors`)
    mizani.palettes.cmap_pal : The palette class that generates
        the colour gradients of this scale.
    """

    cmap_name: InitVar[str] = "viridis"
    """
    A standard Matplotlib colormap name. The default is `viridis`.
    For the list of names checkout the output of
    `matplotlib.cm.cmap_d.keys()` or see
    [colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html).
    """

    def __post_init__(self, cmap_name: str):
        from mizani.palettes import cmap_pal

        super().__post_init__()
        self.palette = cmap_pal(cmap_name)


@dataclass
class scale_fill_cmap(scale_color_cmap):
    """
    Create color scales using Matplotlib colormaps
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_cmap_d(_scale_color_discrete):
    """
    A discrete color scales using Matplotlib colormaps

    See Also
    --------
    [](`matplotlib.cm`)
    [](`matplotlib.colors`)
    mizani.palettes.cmap_pal : The palette class that generates
        the colours of this scale.
    """

    cmap_name: InitVar[str] = "viridis"
    """
    A standard Matplotlib colormap name. The default is `viridis`.
    For the list of names checkout the output of
    `matplotlib.cm.cmap_d.keys()` or see the
    `documentation <http://matplotlib.org/users/colormaps.html>`_.
    """

    def __post_init__(self, cmap_name):
        from mizani.palettes import cmap_d_pal

        super().__post_init__()
        self.palette = cmap_d_pal(cmap_name)


@dataclass
class scale_fill_cmap_d(scale_color_cmap_d):
    """
    Create color scales using Matplotlib colormaps
    """

    _aesthetics = ["fill"]


@dataclass
class scale_color_datetime(scale_datetime, scale_color_cmap):  # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Datetime color scale

    See Also
    --------
    plotnine.scale_color_cmap : The parent class.
    """

    _: KW_ONLY
    guide: Literal["legend", "colorbar"] | None = "colorbar"

    def __post_init__(
        self,
        cmap_name: str,
        date_breaks: str | None,
        date_labels: str | None,
        date_minor_breaks: str | None,
    ):
        from mizani.palettes import cmap_pal

        super().__post_init__(date_breaks, date_labels, date_minor_breaks)
        self.palette = cmap_pal(cmap_name)


@dataclass
class scale_fill_datetime(scale_color_datetime):
    """
    Datetime fill scale
    """

    _aesthetics = ["fill"]


# Default scales
@alias
class scale_color_discrete(scale_color_hue):
    pass


@alias
class scale_color_continuous(scale_color_cmap):
    pass


@alias
class scale_color_ordinal(scale_color_cmap_d):
    pass


@alias
class scale_fill_discrete(scale_fill_hue):
    pass


@alias
class scale_fill_continuous(scale_fill_cmap):
    pass


@alias
class scale_fill_ordinal(scale_fill_cmap_d):
    pass


# American to British spelling
@alias
class scale_colour_hue(scale_color_hue):
    pass


@alias
class scale_color_gray(scale_color_grey):
    pass


@alias
class scale_colour_grey(scale_color_grey):
    pass


@alias
class scale_colour_gray(scale_color_grey):
    pass


@alias
class scale_fill_gray(scale_fill_grey):
    pass


@alias
class scale_colour_brewer(scale_color_brewer):
    pass


@alias
class scale_colour_desaturate(scale_color_desaturate):
    pass


@alias
class scale_colour_gradient(scale_color_gradient):
    pass


@alias
class scale_colour_gradient2(scale_color_gradient2):
    pass


@alias
class scale_colour_gradientn(scale_color_gradientn):
    pass


@alias
class scale_colour_discrete(scale_color_hue):
    pass


@alias
class scale_colour_continuous(scale_color_cmap):
    pass


@alias
class scale_colour_distiller(scale_color_distiller):
    pass


@alias
class scale_colour_cmap(scale_color_cmap):
    pass


@alias
class scale_colour_cmap_d(scale_color_cmap_d):
    pass


@alias
class scale_colour_datetime(scale_color_datetime):
    pass


@alias
class scale_colour_ordinal(scale_color_cmap_d):
    pass
</file>

<file path="plotnine/scales/scale_identity.py">
from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import TYPE_CHECKING, Literal

from .._utils.registry import alias
from .scale_continuous import scale_continuous
from .scale_discrete import scale_discrete

if TYPE_CHECKING:
    from typing import Any, Sequence


class MapTrainMixin:
    """
    Override map and train methods
    """

    def map(self, x, limits=None) -> Sequence[Any]:
        """
        Identity map

        Notes
        -----
        Identity scales bypass the palette completely since the
        map is the identity function.
        """
        return x

    def train(self, x, drop=False):
        # do nothing if no guide,
        # otherwise train so we know what breaks to use
        if self.guide is None:  # pyright: ignore
            return

        return super().train(x)  # pyright: ignore


@dataclass
class scale_color_identity(MapTrainMixin, scale_discrete):
    """
    No color scaling
    """

    _aesthetics = ["color"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


@dataclass
class scale_fill_identity(scale_color_identity):
    """
    No color scaling
    """

    _aesthetics = ["fill"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


@dataclass
class scale_shape_identity(MapTrainMixin, scale_discrete):
    """
    No shape scaling
    """

    _aesthetics = ["shape"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


@dataclass
class scale_linetype_identity(MapTrainMixin, scale_discrete):
    """
    No linetype scaling
    """

    _aesthetics = ["linetype"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


@dataclass
class scale_alpha_identity(
    MapTrainMixin, scale_continuous[Literal["legend"] | None]
):
    """
    No alpha scaling
    """

    _aesthetics = ["alpha"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


@dataclass
class scale_size_identity(
    MapTrainMixin, scale_continuous[Literal["legend"] | None]
):
    """
    No size scaling
    """

    _aesthetics = ["size"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


@dataclass
class scale_stroke_identity(MapTrainMixin, scale_discrete):
    """
    No stroke scaling
    """

    _aesthetics = ["stroke"]
    _: KW_ONLY
    guide: Literal["legend"] | None = None


# American to British spelling
@alias
class scale_colour_identity(scale_color_identity):
    pass
</file>

<file path="plotnine/scales/scale.py">
from __future__ import annotations

from abc import ABC
from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, cast

import numpy as np

from .._utils.registry import Register
from ..exceptions import PlotnineError
from ..mapping.aes import is_position_aes, rename_aesthetics
from ._runtime_typing import (
    BreaksUserT,
    GuideTypeT,
    LimitsUserT,
    RangeT,
    ScaleLabelsUser,
)

if TYPE_CHECKING:
    from typing import Any, Sequence

    import pandas as pd
    from numpy.typing import NDArray

    from plotnine.typing import ScaledAestheticsName

    from ..iapi import range_view, scale_view


@dataclass(kw_only=True)
class scale(
    ABC,
    Generic[RangeT, BreaksUserT, LimitsUserT, GuideTypeT],
    metaclass=Register,
):
    """
    Base class for all scales
    """

    name: str | None = None
    """
    The name of the scale. It is used as the label of the axis or the
    title of the guide. Suitable defaults are chosen depending on
    the type of scale.
    """

    # # major breaks
    breaks: BreaksUserT
    """
    List of major break points. Or a callable that takes a tuple of limits
    and returns a list of breaks. If `True`, automatically calculate the
    breaks.
    """

    limits: LimitsUserT
    """
    Limits of the scale. Most commonly, these are the min & max values
    for the scales. For scales that deal with categoricals, these may be a
    subset or superset of the categories.
    """

    # labels at the breaks
    labels: ScaleLabelsUser = True
    """
    Labels at the `breaks`. Alternatively, a callable that takes an
    array_like of break points as input and returns a list of strings.
    """

    # multiplicative and additive expansion constants
    # fmt: off
    expand: (
        tuple[float, float]
        | tuple[float, float, float, float]
        | None
    ) = None
    # fmt: on

    """
    Multiplicative and additive expansion constants
    that determine how the scale is expanded. If
    specified must be of length 2 or 4. Specifically the
    values are in this order:

    ```
    (mul, add)
    (mul_low, add_low, mul_high, add_high)
    ```

    For example,

    - `(0, 0)` - Do not expand.
    - `(0, 1)` - Expand lower and upper limits by 1 unit.
    - `(1, 0)` - Expand lower and upper limits by 100%.
    - `(0, 0, 0, 0)` - Do not expand, as `(0, 0)`.
    - `(0, 0, 0, 1)` - Expand upper limit by 1 unit.
    - `(0, 1, 0.1, 0)` - Expand lower limit by 1 unit and
      upper limit by 10%.
    - `(0, 0, 0.1, 2)` - Expand upper limit by 10% plus
      2 units.

    If not specified, suitable defaults are chosen.
    """

    # legend or any other guide
    guide: GuideTypeT
    """
    Whether to include a legend
    """

    # What to do with the NA values
    na_value: Any = np.nan
    """
    What value to assign to missing values. Default
    is to assign `np.nan`.
    """

    aesthetics: Sequence[ScaledAestheticsName] = ()
    """
    Aesthetics affected by this scale. These are defined by each scale
    and the user should probably not change them. Have fun.
    """

    _range: RangeT = field(init=False, repr=False)

    # Defined aesthetics for the scale
    _aesthetics: Sequence[ScaledAestheticsName] = field(init=False, repr=False)

    def __post_init__(self):
        breaks = getattr(self, "breaks")

        if (
            np.iterable(breaks)
            and np.iterable(self.labels)
            and len(self.breaks) != len(self.labels)  # type: ignore
        ):
            raise PlotnineError("Breaks and labels have unequal lengths")

        if (
            breaks is None
            and not is_position_aes(self.aesthetics)
            and self.guide is not None
        ):
            self.guide = None  # pyright: ignore

        self.aesthetics = rename_aesthetics(
            self.aesthetics if self.aesthetics else self._aesthetics
        )

    def __radd__(self, other):
        """
        Add this scale to ggplot object
        """
        other.scales.append(copy(self))
        return other

    def map(self, x, limits=None):
        """
        Map every element of x

        The palette should do the real work, this should
        make sure that sensible values are sent and
        return from the palette.
        """
        raise NotImplementedError

    def train(self, x: pd.Series | NDArray):
        """
        Train scale

        Parameters
        ----------
        x :
            A column of data to train over
        """
        raise NotImplementedError

    def dimension(self, expand=None, limits=None):
        """
        Get the phyical size of the scale.
        """
        raise NotImplementedError

    def expand_limits(
        self,
        limits,  # : ScaleLimits
        expand,  # : tuple[float, float] | tuple[float, float, float, float]
        coord_limits,  # : CoordRange | None
        trans,  # : Trans | Type[Trans]
    ) -> range_view:
        """
        Expand the limits of the scale
        """
        raise NotImplementedError

    def transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform dataframe
        """
        raise NotImplementedError

    def transform(self, x):
        """
        Transform array|series x
        """
        raise NotImplementedError

    def inverse_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Inverse transform dataframe
        """
        raise NotImplementedError

    def inverse(self, x):
        """
        Inverse transform array|series x
        """
        raise NotImplementedError

    def view(
        self,
        limits=None,  # : Optional[ScaleLimits]
        range=None,  # : Optional[CoordRange] = None
    ) -> scale_view:
        """
        Information about the trained scale
        """
        raise NotImplementedError

    def default_expansion(
        self,
        mult: float | tuple[float, float] = 0,
        add: Any | tuple[Any, Any] = 0,
        expand=True,
    ) -> tuple[float, float, float, float]:
        """
        Get default expansion for this scale
        """
        if not expand:
            return (0, 0, 0, 0)

        if not (exp := self.expand):
            m1, m2 = mult if isinstance(mult, (tuple, list)) else (mult, mult)
            a1, a2 = cast(
                "tuple[float, float]",
                (add if isinstance(add, (tuple, list)) else (add, add)),
            )
            exp = (m1, a1, m2, a2)
        elif len(exp) == 2:
            exp = (*exp, *exp)

        return exp

    def clone(self):
        return deepcopy(self)

    def reset(self):
        """
        Set the range of the scale to None.

        i.e Forget all the training
        """
        self._range.reset()

    def is_empty(self) -> bool:
        """
        Whether the scale has size information
        """
        if not hasattr(self, "_range"):
            return True
        return self._range.is_empty() and self.limits is None

    @property
    def final_limits(self) -> Any:
        raise NotImplementedError

    def train_df(self, df: pd.DataFrame):
        """
        Train scale from a dataframe
        """
        aesthetics = sorted(set(self.aesthetics) & set(df.columns))
        for ae in aesthetics:
            self.train(df[ae])

    def map_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map df
        """
        if len(df) == 0:
            return df

        aesthetics = set(self.aesthetics) & set(df.columns)
        for ae in aesthetics:
            df[ae] = self.map(df[ae])

        return df

    def get_labels(self, breaks=None) -> Sequence[str]:
        """
        Get labels, calculating them if required
        """
        raise NotImplementedError

    def get_breaks(self, limits=None):
        """
        Get Breaks
        """
        raise NotImplementedError

    def get_bounded_breaks(self, limits=None):
        """
        Return Breaks that are within the limits
        """
        raise NotImplementedError
</file>

<file path="plotnine/stats/stat_bin_2d.py">
import itertools
import types

import numpy as np
import pandas as pd

from .._utils import is_scalar
from ..doctools import document
from ..mapping.evaluation import after_stat
from .binning import fuzzybreaks
from .stat import stat


@document
class stat_bin_2d(stat):
    """
    2 Dimensional bin counts

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=30
        Number of bins. Overridden by binwidth.
    breaks : array_like | tuple[array_like, array_like] , default=None
        Bin boundaries. This supersedes the `binwidth`, `bins`,
        `center` and `boundary`. It can be an array_like or
        a list of two array_likes to provide distinct breaks for
        the `x` and `y` axes.
    binwidth : float, default=None
        The width of the bins. The default is to use bins bins that
        cover the range of the data. You should always override this
        value, exploring multiple widths to find the best to illustrate
        the stories in your data.
    drop : bool, default=False
        If `True`{.py}, removes all cells with zero counts.

    See Also
    --------
    plotnine.geom_rect : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "xmin"    # x lower bound for the bin
    "xmax"    # x upper bound for the bin
    "ymin"    # y lower bound for the bin
    "ymax"    # y upper bound for the bin
    "count"   # number of points in bin
    "density" # density of points in bin, scaled to integrate to 1
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "rect",
        "bins": 30,
        "breaks": None,
        "binwidth": None,
        "drop": True,
    }
    DEFAULT_AES = {"fill": after_stat("count"), "weight": None}
    CREATES = {"xmin", "xmax", "ymin", "ymax", "count", "density"}

    def setup_params(self, data):
        params = self.params
        params["bins"] = dual_param(params["bins"])
        params["breaks"] = dual_param(params["breaks"])
        params["binwidth"] = dual_param(params["binwidth"])

    def compute_group(self, data, scales):
        bins = self.params["bins"]
        breaks = self.params["breaks"]
        binwidth = self.params["binwidth"]
        drop = self.params["drop"]
        weight = data.get("weight")

        if weight is None:
            weight = np.ones(len(data["x"]))

        # The bins will be over the dimension(full size) of the
        # trained x and y scales
        range_x = scales.x.dimension()
        range_y = scales.y.dimension()

        # Trick pd.cut into creating cuts over the range of
        # the scale
        x = np.append(data["x"], range_x)
        y = np.append(data["y"], range_y)

        # create the cutting parameters
        xbreaks = fuzzybreaks(
            scales.x, breaks=breaks.x, binwidth=binwidth.x, bins=bins.x
        )
        ybreaks = fuzzybreaks(
            scales.y, breaks.y, binwidth=binwidth.y, bins=bins.y
        )

        xbins = pd.cut(
            x,
            bins=xbreaks,  # pyright: ignore
            labels=False,
            right=True,
        )
        ybins = pd.cut(
            y,
            bins=ybreaks,  # pyright: ignore
            labels=False,
            right=True,
        )

        # Remove the spurious points
        xbins = xbins[:-2]
        ybins = ybins[:-2]

        # Because we are graphing, we want to see equal breaks
        # The original breaks have an extra room to the left
        ybreaks[0] -= np.diff(np.diff(ybreaks))[0]
        xbreaks[0] -= np.diff(np.diff(xbreaks))[0]

        bins_grid_long = pd.DataFrame(
            {
                "xbins": xbins,
                "ybins": ybins,
                "weight": weight,
            }
        )
        table = bins_grid_long.pivot_table(
            "weight", index=["xbins", "ybins"], aggfunc="sum"
        )["weight"]

        # create rectangles
        rects = []
        keys = itertools.product(
            range(len(ybreaks) - 1), range(len(xbreaks) - 1)
        )
        for j, i in keys:
            try:
                cval = table[(i, j)]
            except KeyError:
                if drop:
                    continue
                cval = 0
            # xmin, xmax, ymin, ymax, count
            row = [
                xbreaks[i],
                xbreaks[i + 1],
                ybreaks[j],
                ybreaks[j + 1],
                cval,
            ]
            rects.append(row)

        new_data = pd.DataFrame(
            rects, columns=["xmin", "xmax", "ymin", "ymax", "count"]
        )
        new_data["density"] = new_data["count"] / new_data["count"].sum()
        return new_data


stat_bin2d = stat_bin_2d


def dual_param(value):
    """
    Return duplicate of parameter value

    Used to apply same value to x & y axes if only one
    value is given.
    """
    if is_scalar(value):
        return types.SimpleNamespace(x=value, y=value)

    if hasattr(value, "x") and hasattr(value, "y"):
        return value

    if len(value) == 2:
        return types.SimpleNamespace(x=value[0], y=value[1])
    else:
        return types.SimpleNamespace(x=value, y=value)
</file>

<file path="plotnine/stats/stat_bin.py">
from warnings import warn

import numpy as np

from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.evaluation import after_stat
from .binning import (
    assign_bins,
    breaks_from_bins,
    breaks_from_binwidth,
    freedman_diaconis_bins,
)
from .stat import stat


@document
class stat_bin(stat):
    """
    Count cases in each interval

    {usage}

    Parameters
    ----------
    {common_parameters}
    binwidth : float, default=None
        The width of the bins. The default is to use bins bins that
        cover the range of the data. You should always override this
        value, exploring multiple widths to find the best to illustrate
        the stories in your data.
    bins : int, default=None
        Number of bins. Overridden by binwidth. If `None`{.py},
        a number is computed using the freedman-diaconis method.
    breaks : array_like, default=None
        Bin boundaries. This supersedes the `binwidth`, `bins`,
        `center` and `boundary`.
    center : float, default=None
        The center of one of the bins. Note that if center is above
        or below the range of the data, things will be shifted by
        an appropriate number of widths. To center on integers, for
        example, use `width=1`{.py} and `center=0`{.py}, even if 0 i
        s outside the range of the data. At most one of center and
        boundary may be specified.
    boundary : float, default=None
        A boundary between two bins. As with center, things are
        shifted when boundary is outside the range of the data.
        For example, to center on integers, use `width=1`{.py} and
        `boundary=0.5`{.py}, even if 1 is outside the range of the
        data. At most one of center and boundary may be specified.
    closed : Literal["left", "right"], default="right"
        Which edge of the bins is included.
    pad : bool, default=False
        If `True`{.py}, adds empty bins at either side of x.
        This ensures that frequency polygons touch 0.

    See Also
    --------
    plotnine.histogram : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "count"    # number of points in bin
    "density"  # density of points in bin, scaled to integrate to 1
    "ncount"   # count, scaled to maximum of 1
    "ndensity" # density, scaled to maximum of 1
    "ngroup"   # number of points in group
    ```

    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "histogram",
        "position": "stack",
        "binwidth": None,
        "bins": None,
        "breaks": None,
        "center": None,
        "boundary": None,
        "closed": "right",
        "pad": False,
    }
    DEFAULT_AES = {"y": after_stat("count"), "weight": None}
    CREATES = {"width", "count", "density", "ncount", "ndensity", "ngroup"}

    def setup_params(self, data):
        params = self.params

        if "y" in data or "y" in params:
            msg = "stat_bin() must not be used with a y aesthetic."
            raise PlotnineError(msg)

        if params["closed"] not in ("right", "left"):
            raise PlotnineError("`closed` should either 'right' or 'left'")

        if (
            params["breaks"] is None
            and params["binwidth"] is None
            and params["bins"] is None
        ):
            params["bins"] = freedman_diaconis_bins(data["x"])
            msg = (
                "'stat_bin()' using 'bins = {}'. "
                "Pick better value with 'binwidth'."
            )
            warn(msg.format(params["bins"]), PlotnineWarning)

    def compute_group(self, data, scales):
        params = self.params
        if params["breaks"] is not None:
            breaks = np.asarray(params["breaks"])
            if hasattr(scales.x, "transform"):
                breaks = scales.x.transform(breaks)
        elif params["binwidth"] is not None:
            breaks = breaks_from_binwidth(
                scales.x.dimension(),
                params["binwidth"],
                params["center"],
                params["boundary"],
            )
        else:
            breaks = breaks_from_bins(
                scales.x.dimension(),
                params["bins"],
                params["center"],
                params["boundary"],
            )

        new_data = assign_bins(
            data["x"],
            breaks,
            data.get("weight"),
            params["pad"],
            params["closed"],
        )
        return new_data
</file>

<file path="plotnine/stats/stat_boxplot.py">
import numpy as np
import pandas as pd

from .._utils import resolution
from ..doctools import document
from .stat import stat


@document
class stat_boxplot(stat):
    """
    Compute boxplot statistics

    {usage}

    Parameters
    ----------
    {common_parameters}
    coef : float, default=1.5
        Length of the whiskers as a multiple of the Interquartile
        Range.

    See Also
    --------
    plotnine.geom_boxplot: The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "width"  # width of boxplot
    "lower"  # lower hinge, 25% quantile
    "middle" # median, 50% quantile
    "upper"  # upper hinge, 75% quantile

    # lower edge of notch, computed as;
    # median - 1.58 * IQR / sqrt(n)
    "notchlower"

    # upper edge of notch, computed as;
    # median + 1.58 * IQR / sqrt(n)
    "notchupper"

    # lower whisker, computed as; smallest observation
    # greater than or equal to lower hinge - 1.5 * IQR
    "ymin"

    # upper whisker, computed as; largest observation
    # less than or equal to upper hinge + 1.5 * IQR
    "ymax"
    ```

        'n'     # Number of observations at a position

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('width')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"weight"}
    DEFAULT_PARAMS = {
        "geom": "boxplot",
        "position": "dodge",
        "coef": 1.5,
        "width": None,
    }
    CREATES = {
        "lower",
        "upper",
        "middle",
        "ymin",
        "ymax",
        "outliers",
        "notchupper",
        "notchlower",
        "width",
        "relvarwidth",
        "n",
    }

    def setup_data(self, data):
        if "x" not in data:
            data["x"] = 0
        return data

    def setup_params(self, data):
        if self.params["width"] is None:
            x = data.get("x", 0)
            self.params["width"] = resolution(x, False) * 0.75

    def compute_group(self, data, scales):
        n = len(data)
        y = data["y"].to_numpy()
        if "weight" in data:
            weights = data["weight"]
            total_weight = np.sum(weights)
        else:
            weights = None
            total_weight = len(y)
        res = weighted_boxplot_stats(
            y, weights=weights, whis=self.params["coef"]
        )

        if len(np.unique(data["x"])) > 1:
            width = np.ptp(data["x"]) * 0.9
        else:
            width = self.params["width"]

        if isinstance(data["x"].dtype, pd.CategoricalDtype):
            x = data["x"].iloc[0]
        else:
            x = np.mean([data["x"].min(), data["x"].max()])

        d = {
            "ymin": res["whislo"],
            "lower": res["q1"],
            "middle": [res["med"]],
            "upper": res["q3"],
            "ymax": res["whishi"],
            "outliers": [res["fliers"]],
            "notchupper": res["cihi"],
            "notchlower": res["cilo"],
            "x": x,
            "width": width,
            "relvarwidth": np.sqrt(total_weight),
            "n": n,
        }
        return pd.DataFrame(d)


def weighted_percentile(a, q, weights=None):
    """
    Compute the weighted q-th percentile of data

    Parameters
    ----------
    a : array_like
        Input that can be converted into an array.
    q : array_like[float]
        Percentile or sequence of percentiles to compute. Must be int
        the range [0, 100]
    weights : array_like
        Weights associated with the input values.
    """
    # Calculate and interpolate weighted percentiles
    # method derived from https://en.wikipedia.org/wiki/Percentile
    # using numpy's standard C = 1
    if weights is None:
        weights = np.ones(len(a))

    weights = np.asarray(weights)
    q = np.asarray(q)

    C = 1
    idx_s = np.argsort(a)
    a_s = a[idx_s]
    w_n = weights[idx_s]
    S_N = np.sum(weights)
    S_n = np.cumsum(w_n)
    p_n = (S_n - C * w_n) / (S_N + (1 - 2 * C) * w_n)
    pcts = np.interp(q / 100.0, p_n, a_s)
    return pcts


def weighted_boxplot_stats(x, weights=None, whis=1.5):
    """
    Calculate weighted boxplot plot statistics

    Parameters
    ----------
    x : array_like
        Data
    weights : array_like
        Weights associated with the data.
    whis : float
        Position of the whiskers beyond the interquartile range.
        The data beyond the whisker are considered outliers.

        If a float, the lower whisker is at the lowest datum above
        `Q1 - whis*(Q3-Q1)`, and the upper whisker at the highest
        datum below `Q3 + whis*(Q3-Q1)`, where Q1 and Q3 are the
        first and third quartiles.  The default value of
        `whis = 1.5` corresponds to Tukey's original definition of
        boxplots.

    Notes
    -----
    This method adapted from Matplotlibs boxplot_stats. The key difference
    is the use of a weighted percentile calculation and then using linear
    interpolation to map weight percentiles back to data.
    """
    if weights is None:
        q1, med, q3 = np.percentile(x, (25, 50, 75))
        n = len(x)
    else:
        q1, med, q3 = weighted_percentile(x, (25, 50, 75), weights)
        n = np.sum(weights)

    iqr = q3 - q1
    mean = np.average(x, weights=weights)
    cilo = med - 1.58 * iqr / np.sqrt(n)
    cihi = med + 1.58 * iqr / np.sqrt(n)

    # low extreme
    loval = q1 - whis * iqr
    lox = x[x >= loval]
    whislo = q1 if (len(lox) == 0 or np.min(lox) > q1) else np.min(lox)

    # high extreme
    hival = q3 + whis * iqr
    hix = x[x <= hival]
    whishi = q3 if (len(hix) == 0 or np.max(hix) < q3) else np.max(hix)

    bpstats = {
        "fliers": x[(x < whislo) | (x > whishi)],
        "mean": mean,
        "med": med,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "whislo": whislo,
        "whishi": whishi,
        "cilo": cilo,
        "cihi": cihi,
    }
    return bpstats
</file>

<file path="plotnine/stats/stat_count.py">
import numpy as np
import pandas as pd

from .._utils import resolution
from ..doctools import document
from ..exceptions import PlotnineError
from ..mapping.evaluation import after_stat
from .stat import stat


@document
class stat_count(stat):
    """
    Counts the number of cases at each x position

    {usage}

    Parameters
    ----------
    {common_parameters}
    width : float, default=None
        Bar width. If None, set to 90% of the resolution of the data.

    See Also
    --------
    plotnine.geom_histogram : The default `geom` for this `stat`.
    plotnine.stat_bin
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "count"  # Number of observations at a position
    "prop"   # Ratio of points in the panel at a position
    ```

    """

    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "histogram",
        "position": "stack",
        "width": None,
    }
    DEFAULT_AES = {"y": after_stat("count")}
    CREATES = {"count", "prop"}

    def setup_params(self, data):
        if self.params["width"] is None:
            self.params["width"] = resolution(data["x"], False) * 0.9

    def compute_group(self, data, scales):
        x = data["x"]
        if ("y" in data) or ("y" in self.params):
            msg = "stat_count() must not be used with a y aesthetic"
            raise PlotnineError(msg)

        weight = data.get("weight", [1] * len(x))
        width = self.params["width"]
        xdata_long = pd.DataFrame({"x": x, "weight": weight})
        # weighted frequency count
        count = xdata_long.pivot_table("weight", index=["x"], aggfunc="sum")[
            "weight"
        ]
        x = count.index
        count = count.to_numpy()
        return pd.DataFrame(
            {
                "count": count,
                "prop": count / np.abs(count).sum(),
                "x": x,
                "width": width,
            }
        )
</file>

<file path="plotnine/stats/stat_density.py">
from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, cast
from warnings import warn

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.evaluation import after_stat
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArray, FloatArrayLike


# NOTE: Parameter descriptions are in
# statsmodels/nonparametric/kde.py
@document
class stat_density(stat):
    """
    Compute density estimate

    {usage}

    Parameters
    ----------
    {common_parameters}
    kernel : str, default="gaussian"
        Kernel used for density estimation. One of:
        ```python
        "biweight"
        "cosine"
        "cosine2"
        "epanechnikov"
        "gaussian"
        "triangular"
        "triweight"
        "uniform"
        ```
    adjust : float, default=1
        An adjustment factor for the `bw`. Bandwidth becomes
        `bw * adjust`{.py}.
        Adjustment of the bandwidth.
    trim : bool, default=False
        This parameter only matters if you are displaying multiple
        densities in one plot. If `False`{.py}, the default, each
        density is computed on the full range of the data. If
        `True`{.py}, each density is computed over the range of that
        group; this typically means the estimated x values will not
        line-up, and hence you won't be able to stack density values.
    n : int, default=1024
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    gridsize : int, default=None
        If gridsize is `None`{.py}, `max(len(x), 50)`{.py} is used.
    bw : str | float, default="nrd0"
        The bandwidth to use, If a float is given, it is the bandwidth.
        The options are:

        ```python
        "nrd0"
        "normal_reference"
        "scott"
        "silverman"
        ```

        `nrd0` is a port of `stats::bw.nrd0` in R; it is eqiuvalent
        to `silverman` when there is more than 1 value in a group.
    cut : float, default=3
        Defines the length of the grid past the lowest and highest
        values of `x` so that the kernel goes to zero. The end points
        are `-/+ cut*bw*{min(x) or max(x)}`.
    clip : tuple[float, float], default=(-inf, inf)
        Values in `x` that are outside of the range given by clip are
        dropped. The number of values in `x` is then shortened.
    bounds: tuple[float, float], default=(-inf, inf)
        The domain boundaries of the data. When the domain is finite the
        estimated density will be corrected to remove asymptotic boundary
        effects that are usually biased away from the probability density
        function being estimated.

    See Also
    --------
    plotnine.geom_density : The default `geom` for this `stat`.
    statsmodels.nonparametric.kde.KDEUnivariate
    statsmodels.nonparametric.kde.KDEUnivariate.fit
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    'density'   # density estimate

    'count'     # density * number of points,
                # useful for stacked density plots

    'scaled'    # density estimate, scaled to maximum of 1
    'n'         # Number of observations at a position
    ```


    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "density",
        "position": "stack",
        "kernel": "gaussian",
        "adjust": 1,
        "trim": False,
        "n": 1024,
        "gridsize": None,
        "bw": "nrd0",
        "cut": 3,
        "clip": (-np.inf, np.inf),
        "bounds": (-np.inf, np.inf),
    }
    DEFAULT_AES = {"y": after_stat("density")}
    CREATES = {"density", "count", "scaled", "n"}

    def setup_params(self, data):
        params = self.params
        lookup = {
            "biweight": "biw",
            "cosine": "cos",
            "cosine2": "cos2",
            "epanechnikov": "epa",
            "gaussian": "gau",
            "triangular": "tri",
            "triweight": "triw",
            "uniform": "uni",
        }

        with suppress(KeyError):
            params["kernel"] = lookup[params["kernel"].lower()]

        if params["kernel"] not in lookup.values():
            msg = (
                f"kernel should be one of {lookup.keys()}. "
                f"You may use the abbreviations {lookup.values()}"
            )
            raise PlotnineError(msg)

    def compute_group(self, data, scales):
        weight = data.get("weight")

        if self.params["trim"]:
            range_x = data["x"].min(), data["x"].max()
        else:
            range_x = scales.x.dimension()

        return compute_density(data["x"], weight, range_x, self.params)


def compute_density(x, weight, range, params):
    """
    Compute density
    """
    import statsmodels.api as sm

    x = np.asarray(x, dtype=float)
    not_nan = ~np.isnan(x)
    x = x[not_nan]
    bw = cast("str | float", params["bw"])
    kernel = params["kernel"]
    bounds = params["bounds"]
    has_bounds = not (np.isneginf(bounds[0]) and np.isposinf(bounds[1]))
    n = len(x)

    if n == 0 or (n == 1 and isinstance(bw, str)):
        if n == 1:
            warn(
                "To compute the density of a group with only one "
                "value set the bandwidth manually. e.g `bw=0.1`",
                PlotnineWarning,
            )
        warn(
            "Groups with fewer than 2 data points have been removed.",
            PlotnineWarning,
        )
        return pd.DataFrame()

    # kde is computed efficiently using fft. But the fft does
    # not support weights and is only available with the
    # gaussian kernel. When weights are relevant we
    # turn off the fft.
    if weight is None:
        if kernel != "gau":
            weight = np.ones(n) / n
    else:
        weight = np.asarray(weight, dtype=float)

    fft = kernel == "gau" and weight is None

    if bw == "nrd0":
        bw = nrd0(x)

    kde = sm.nonparametric.KDEUnivariate(x)
    kde.fit(
        kernel=kernel,
        bw=bw,  # type: ignore
        fft=fft,
        weights=weight,
        adjust=params["adjust"],
        cut=params["cut"],
        gridsize=params["gridsize"],
        clip=params["clip"],
    )

    if has_bounds:
        # kde.support is the grid over which the kernel function is
        # defined and the first and last values of this grid are:
        #
        #     [min(x)-cut*bw, max(x)+cut*bw]
        #
        # i.e. the grid is wider than the ptp range of x.
        # Evaluating values beyond the ptp range helps us calculate a
        # boundary corrections. So we widen the range over which we will
        # evaluate, so that it contains all points supported by the grid.
        x2 = np.linspace(
            kde.support[0],  # pyright: ignore
            kde.support[-1],  # pyright: ignore
            params["n"],
        )
    else:
        x2 = np.linspace(range[0], range[1], params["n"])

    try:
        y = kde.evaluate(x2)
        if np.isscalar(y) and np.isnan(y):
            raise ValueError("kde.evaluate returned nan")
    except ValueError:
        y = []
        for _x in x2:
            result = kde.evaluate(_x)
            if isinstance(result, (float, int)):
                y.append(result)
            else:
                y.append(result[0])

    y = np.asarray(y)

    # Evaluations outside the kernel domain return np.nan,
    # these values and corresponding x2s are dropped.
    # The kernel domain is defined by the values in x, but
    # the evaluated values in x2 could have a much wider range.
    not_nan = ~np.isnan(y)
    x2 = x2[not_nan]
    y = y[not_nan]

    if has_bounds:
        x2, y = fit_density_to_bounds(x2, y, range, bounds)

    return pd.DataFrame(
        {
            "x": x2,
            "density": y,
            "scaled": y / np.max(y) if len(y) else [],
            "count": y * n,
            "n": n,
        }
    )


def nrd0(x: FloatArrayLike) -> float:
    """
    Port of R stats::bw.nrd0

    This is equivalent to statsmodels silverman when x has more than
    1 unique value. It can never give a zero bandwidth.

    Parameters
    ----------
    x : array_like
        Values whose density is to be estimated

    Returns
    -------
    out : float
        Bandwidth of x
    """
    from scipy.stats import iqr

    n = len(x)
    if n < 1:
        raise ValueError(
            "Need at least 2 data points to compute the nrd0 bandwidth."
        )

    std: float = np.std(x, ddof=1)  # pyright: ignore
    std_estimate: float = iqr(x) / 1.349
    low_std = min(std, std_estimate)
    if low_std == 0:
        low_std = std_estimate or np.abs(np.asarray(x)[0]) or 1
    return 0.9 * low_std * (n**-0.2)


def fit_density_to_bounds(
    x: FloatArray,
    y: FloatArray,
    range: tuple[float, float],
    bounds: tuple[float, float],
) -> tuple[FloatArray, FloatArray]:
    """
    Fit calculated density to the given bounds

    Parameters
    ----------
    x :
        Points at which the density is estimated. `x` is expected to
        to include all values of the density grid.
    y :
        Estimated density.
    range :
    bounds :
        Valid boundary (domain) of the x values.

    Returns
    -------
    x_bound :
        Points that fall within the bounds at which the density is
        estimated.
    y_bound :
        Estimated densities at points within the bounds.
    """

    def interpolate(x2: FloatArray) -> FloatArray:
        # Interpolate (linearly) along the density function
        # The values at points beyond (left or right) the original
        # grid (x) are zero.
        return np.interp(x2, x, y, left=0, right=0)

    # The boundary corrections work by:
    # 1. reflecting values outside the bounds so that they fall within
    #    the bounds to give a correction values
    # 2. adding the correction values to the original density
    new_range = max(range[0], bounds[0]), min(range[1], bounds[1])
    x_bound = np.linspace(new_range[0], new_range[1], len(x))
    y_bound = (
        interpolate(x_bound)
        + interpolate(2 * bounds[0] - x_bound)
        + interpolate(2 * bounds[1] - x_bound)
    )
    return x_bound, y_bound
</file>

<file path="plotnine/stats/stat_ecdf.py">
import numpy as np
import pandas as pd

from ..doctools import document
from ..mapping.evaluation import after_stat
from .stat import stat


@document
class stat_ecdf(stat):
    """
    Empirical Cumulative Density Function

    {usage}

    Parameters
    ----------
    {common_parameters}
    n  : int, default=None
        This is the number of points to interpolate with.
        If `None`{.py}, do not interpolate.
    pad : bool, default=True
        If True, pad the domain with `-inf` and `+inf` so that
        ECDF does not have discontinuities at the extremes.

    See Also
    --------
    plotnine.geom_step : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "x"     # x in the data
    "ecdf"  # cumulative density corresponding to x
    ```
    """

    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {"geom": "step", "n": None, "pad": True}
    DEFAULT_AES = {"y": after_stat("ecdf")}
    CREATES = {"ecdf"}

    def compute_group(self, data, scales):
        from statsmodels.distributions.empirical_distribution import ECDF

        n, pad = self.params["n"], self.params["pad"]

        # If n is None, use raw values; otherwise interpolate
        if n is None:
            x = np.unique(data["x"])
        else:
            x = np.linspace(data["x"].min(), data["x"].max(), n)

        if pad:
            x = np.hstack([-np.inf, x, np.inf])

        ecdf = ECDF(data["x"].to_numpy())(x)
        res = pd.DataFrame({"x": x, "ecdf": ecdf})
        return res
</file>

<file path="plotnine/stats/stat_ellipse.py">
from __future__ import annotations

from typing import TYPE_CHECKING
from warnings import warn

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineWarning
from .stat import stat

if TYPE_CHECKING:
    from typing import Any, Optional

    from plotnine.typing import FloatArray, FloatArrayLike


@document
class stat_ellipse(stat):
    """
    Calculate normal confidence interval ellipse

    {usage}

    Parameters
    ----------
    {common_parameters}
    type : Literal["t", "norm", "euclid"], default="t"
        The type of ellipse.
        `t` assumes a multivariate t-distribution.
        `norm` assumes a multivariate normal distribution.
        `euclid` draws a circle with the radius equal to
        `level`, representing the euclidean distance from the center.

    level : float, default=0.95
        The confidence level at which to draw the ellipse.
    segments : int, default=51
        Number of segments to be used in drawing the ellipse.

    See Also
    --------
    plotnine.geom_path : The default `geom` for this `stat`.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "path",
        "type": "t",
        "level": 0.95,
        "segments": 51,
    }

    def compute_group(self, data, scales):
        import scipy.stats as stats
        from scipy import linalg

        level = self.params["level"]
        segments = self.params["segments"]
        type_ = self.params["type"]

        dfn = 2
        dfd = len(data) - 1

        if dfd < 3:
            warn("Too few points to calculate an ellipse", PlotnineWarning)
            return pd.DataFrame({"x": [], "y": []})

        m: FloatArray = np.asarray(data[["x", "y"]])

        # The stats used to create the ellipse
        if type_ == "t":
            res = cov_trob(m)
            cov = res["cov"]
            center = res["center"]
        elif type_ == "norm":
            cov = np.cov(m, rowvar=False)
            center = np.mean(m, axis=0)
        elif type_ == "euclid":
            cov = np.cov(m, rowvar=False)
            cov = np.diag(np.repeat(np.diag(cov).min(), 2))
            center = np.mean(m, axis=0)
        else:
            raise ValueError(f"Unknown value for type={type_}")

        # numpy's cholesky function does not guarantee upper/lower
        # triangular factorization.
        chol_decomp = linalg.cholesky(cov, lower=False)

        # Parameters of the ellipse
        if type_ == "euclid":
            radius = level / chol_decomp.max()
        else:
            radius = np.sqrt(dfn * stats.f.ppf(level, dfn, dfd))

        space = np.linspace(0, 2 * np.pi, segments)

        # Catesian coordinates
        unit_circle = np.column_stack([np.cos(space), np.sin(space)])
        res = center + radius * np.dot(unit_circle, chol_decomp)

        return pd.DataFrame({"x": res[:, 0], "y": res[:, 1]})


def cov_trob(
    x,
    wt: Optional[FloatArrayLike] = None,
    cor=False,
    center: FloatArrayLike | bool = True,
    nu=5,
    maxit=25,
    tol=0.01,
):
    """
    Covariance Estimation for Multivariate t Distribution

    Estimates a covariance or correlation matrix assuming the
    data came from a multivariate t distribution: this provides
    some degree of robustness to outlier without giving a high
    breakdown point.

    **credit**: This function a port of the R function
    `MASS::cov.trob`.

    Parameters
    ----------
    x : array
        data matrix. Missing values (NaNs) are not allowed.
    wt : array
        A vector of weights for each case: these are treated as
        if the case i actually occurred `wt[i]` times.
    cor : bool
        Flag to choose between returning the correlation
        (`cor=True`) or covariance (`cor=False`) matrix.
    center : array | bool
        A logical value or a numeric vector providing the location
        about which the covariance is to be taken.
        If `center=False`, no centering is done; if
        `center=True` the MLE of the location vector is used.
    nu : int
        'degrees of freedom' for the multivariate t distribution.
        Must exceed 2 (so that the covariance matrix is finite).
    maxit : int
        Maximum number of iterations in fitting.
    tol : float
        Convergence tolerance for fitting.

    Returns
    -------
    out : dict
        A dictionary with with the following key-value

        - `cov` : the fitted covarince matrix.
        - `center` : the estimated or specified location vector.
        - `wt` : the specified weights: only returned if the
           wt argument was given.
        - `n_obs` : the number of cases used in the fitting.
        - `cor` : the fitted correlation matrix: only returned
          if `cor=True`.
        - `call` : The matched call.
        - `iter` : The number of iterations used.

    References
    ----------
    - J. T. Kent, D. E. Tyler and Y. Vardi (1994) A curious likelihood
      identity for the multivariate t-distribution. *Communications in
      Statistics-Simulation and Computation* **23**, 441-453.

    - Venables, W. N. and Ripley, B. D. (1999) *Modern Applied
      Statistics with S-PLUS*. Third Edition. Springer.

    """
    from scipy import linalg

    def test_values(x):
        if pd.isna(x).any() or np.isinf(x).any():
            raise ValueError("Missing or infinite values in 'x'")

    def scale_simp(x: FloatArray, center: FloatArray, n: int, p: int):
        return x - np.repeat([center], n, axis=0)

    x = np.asarray(x)
    n, p = x.shape
    test_values(x)
    ans: dict[str, Any] = {}

    # wt
    if wt is None:
        wt = np.ones(n)
    else:
        wt = np.asarray(wt)
        ans["wt0"] = wt

        if len(wt) != n:
            raise ValueError(
                "length of 'wt' must equal number of observations."
            )
        if any(wt < 0):
            raise ValueError("Negative weights not allowed.")
        if not np.sum(wt):
            raise ValueError("No positive weights.")

        x = x[wt > 0, :]
        wt = wt[wt > 0]
        n, _ = x.shape

    wt = wt[:, np.newaxis]  # pyright: ignore[reportCallIssue,reportArgumentType,reportOptionalSubscript]

    # loc
    use_loc = False
    if isinstance(center, bool):
        if center:
            loc = np.sum(wt * x, axis=0) / wt.sum()
            use_loc = True
        else:
            loc = np.zeros(p)
    else:
        if len(center) != p:
            raise ValueError("'center' is not the right length")
        loc = np.asarray(center)

    # Default values for the typechecker
    iteration = 0
    X = np.array([], ndmin=x.ndim)

    w = wt * (1 + p / nu)
    for iteration in range(maxit):
        w0 = w
        X = scale_simp(x, loc, n, p)
        _, s, v = linalg.svd(np.sqrt(w / np.sum(w)) * X)
        wX = X @ v.T @ np.diag(np.full(p, 1 / s))
        Q = np.squeeze((wX**2) @ np.ones(p))
        w = (wt * (nu + p)) / (nu + Q)[:, np.newaxis]
        if use_loc:
            loc = np.sum(w * x, axis=0) / w.sum()
        if all(np.abs(w - w0) < tol):
            break
    else:  # nobreak
        _c1 = np.mean(w) - np.mean(wt) > tol
        _c2 = np.abs(np.mean(w * Q) / p - 1) > tol  # pyright: ignore
        if _c1 and _c2:
            warn("Convergence probably failed.", PlotnineWarning)

    _a = np.sqrt(w) * X
    cov = (_a.T @ _a) / np.sum(wt)

    if cor:
        sd = np.sqrt(np.diag(cov))
        ans["cor"] = (cov / sd) / np.repeat([sd], p, axis=0).T

    ans.update(
        cov=cov,
        center=loc,
        n_obs=n,
        iter=iteration,
    )
    return ans
</file>

<file path="plotnine/stats/stat_function.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from ..mapping.evaluation import after_stat
from ..scales.scale_continuous import scale_continuous
from .stat import stat

if typing.TYPE_CHECKING:
    from typing import Callable

    from plotnine.typing import FloatArrayLike


@document
class stat_function(stat):
    """
    Superimpose a function onto a plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    fun : callable
        Function to evaluate.
    n : int, default=101
        Number of points at which to evaluate the function.
    xlim : tuple, default=None
        `x` limits for the range. The default depends on
        the `x` aesthetic. There is not an `x` aesthetic
        then the `xlim` must be provided.
    args : Optional[tuple[Any] | dict[str, Any]], default=None
        Arguments to pass to `fun`.

    See Also
    --------
    plotnine.geom_path : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "x"   # x points at which the function is evaluated
    "fx"  # points evaluated at each x
    ```

    """

    DEFAULT_PARAMS = {
        "geom": "path",
        "fun": None,
        "n": 101,
        "args": None,
        "xlim": None,
    }

    DEFAULT_AES = {"y": after_stat("fx")}
    CREATES = {"fx"}

    def __init__(self, mapping=None, data=None, **kwargs):
        if data is None:

            def _data_func(data: pd.DataFrame) -> pd.DataFrame:
                if data.empty:
                    data = pd.DataFrame({"group": [1]})
                return data

            data = _data_func

        super().__init__(mapping, data, **kwargs)

    def setup_params(self, data):
        if not callable(self.params["fun"]):
            raise PlotnineError(
                "stat_function requires parameter 'fun' to be "
                "a function or any other callable object"
            )

    def compute_group(self, data, scales):
        old_fun: Callable[..., FloatArrayLike] = self.params["fun"]
        n = self.params["n"]
        args = self.params["args"]
        xlim = self.params["xlim"]
        range_x = xlim or scales.x.dimension((0, 0))

        if isinstance(args, (list, tuple)):

            def fun(x):
                return old_fun(x, *args)

        elif isinstance(args, dict):

            def fun(x):
                return old_fun(x, **args)

        elif args is not None:

            def fun(x):
                return old_fun(x, args)

        else:

            def fun(x):
                return old_fun(x)

        x = np.linspace(range_x[0], range_x[1], n)

        # continuous scale
        if isinstance(scales.x, scale_continuous):
            x = scales.x.inverse(x)

        # We know these can handle array_likes
        if isinstance(old_fun, (np.ufunc, np.vectorize)):
            fx = fun(x)
        else:
            fx = [fun(val) for val in x]

        new_data = pd.DataFrame({"x": x, "fx": fx})
        return new_data
</file>

<file path="plotnine/stats/stat_hull.py">
import numpy as np
import pandas as pd

from ..doctools import document
from .stat import stat


@document
class stat_hull(stat):
    """
    2 Dimensional Convex Hull

    {usage}

    Parameters
    ----------
    {common_parameters}
    qhull_options: str, default=None
        Additional options to pass to Qhull.
        See `Qhull <http://www.qhull.org/>`__ documentation
        for details.

    Raises
    ------
    scipy.spatial.QhullError
        Raised when Qhull encounters an error condition,
        such as geometrical degeneracy when options to resolve are
        not enabled.

    See Also
    --------
    plotnine.geom_path : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "area"  # Area of the convex hull
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {"geom": "path", "qhull_options": None}
    CREATES = {"area"}

    def compute_group(self, data, scales):
        from scipy.spatial import ConvexHull

        hull = ConvexHull(
            data[["x", "y"]], qhull_options=self.params["qhull_options"]
        )
        idx = np.hstack([hull.vertices, hull.vertices[0]])

        new_data = pd.DataFrame(
            {
                "x": data["x"].iloc[idx].to_numpy(),
                "y": data["y"].iloc[idx].to_numpy(),
                "area": hull.area,
            }
        )
        return new_data
</file>

<file path="plotnine/stats/stat_identity.py">
from ..doctools import document
from .stat import stat


@document
class stat_identity(stat):
    """
    Identity (do nothing) statistic

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_point : The default `geom` for this `stat`.
    """

    DEFAULT_PARAMS = {"geom": "point"}

    def compute_panel(self, data, scales):
        return data
</file>

<file path="plotnine/stats/stat_quantile.py">
from warnings import warn

import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineWarning
from .stat import stat


# method_args are any of the keyword args (other than q) for
# statsmodels.regression.quantile_regression.QuantReg.fit
@document
class stat_quantile(stat):
    """
    Compute quantile regression lines

    {usage}

    Parameters
    ----------
    {common_parameters}
    quantiles : tuple, default=(0.25, 0.5, 0.75)
        Quantiles of y to compute
    formula : str, default="y ~ x"
        Formula relating y variables to x variables
    method_args : dict, default=None
        Extra arguments passed on to the model fitting method,
        [](`~statsmodels.regression.quantile_regression.QuantReg.fit`).

    See Also
    --------
    plotnine.geom_quantile : The default `geom` for this `stat`.
    statsmodels.regression.quantile_regression.QuantReg
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "quantile"  # quantile
    "group"     # group identifier
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('quantile')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "quantile",
        "quantiles": (0.25, 0.5, 0.75),
        "formula": "y ~ x",
        "method_args": {},
    }
    CREATES = {"quantile", "group"}

    def setup_params(self, data):
        params = self.params
        if params["formula"] is None:
            params["formula"] = "y ~ x"
            warn("Formula not specified, using '{}'", PlotnineWarning)
        else:
            params["eval_env"] = self.environment.to_patsy_env()

        try:
            iter(params["quantiles"])
        except TypeError:
            params["quantiles"] = (params["quantiles"],)

    def compute_group(self, data, scales):
        res = [
            quant_pred(q, data, self.params) for q in self.params["quantiles"]
        ]
        return pd.concat(res, axis=0, ignore_index=True)


def quant_pred(q, data, params):
    """
    Quantile precitions
    """
    import statsmodels.formula.api as smf

    mod = smf.quantreg(
        params["formula"],
        data,
        eval_env=params.get("eval_env"),
    )
    reg_res = mod.fit(q=q, **params["method_args"])
    out = pd.DataFrame(
        {
            "x": [data["x"].min(), data["x"].max()],
            "quantile": q,
            "group": f"{data['group'].iloc[0]}-{q}",
        }
    )
    out["y"] = reg_res.predict(out)
    return out
</file>

<file path="plotnine/stats/stat_smooth.py">
import warnings

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineWarning
from .smoothers import predictdf
from .stat import stat


@document
class stat_smooth(stat):
    """
    Calculate a smoothed conditional mean

    {usage}

    Parameters
    ----------
    {common_parameters}
    method : str | callable, default="auto"
        The available methods are:
        ```python
        "auto"       # Use loess if (n<1000), glm otherwise
        "lm", "ols"  # Linear Model
        "wls"        # Weighted Linear Model
        "rlm"        # Robust Linear Model
        "glm"        # Generalized linear Model
        "gls"        # Generalized Least Squares
        "lowess"     # Locally Weighted Regression (simple)
        "loess"      # Locally Weighted Regression
        "mavg"       # Moving Average
        "gpr"        # Gaussian Process Regressor
        ```

        If a `callable` is passed, it must have the signature:

        ```python
        def my_smoother(data, xseq, params):
            # * data - has the x and y values for the model
            # * xseq - x values to be predicted
            # * params - stat parameters
            #
            # It must return a new dataframe. Below is the
            # template used internally by Plotnine

            # Input data into the model
            x, y = data["x"], data["y"]

            # Create and fit a model
            model = Model(x, y)
            results = Model.fit()

            # Create output data by getting predictions on
            # the xseq values
            data = pd.DataFrame({
                "x": xseq,
                "y": results.predict(xseq)})

            # Compute confidence intervals, this depends on
            # the model. However, given standard errors and the
            # degrees of freedom we can compute the confidence
            # intervals using the t-distribution.
            #
            # For an alternative, implement confidence intervals by
            # the bootstrap method
            if params["se"]:
                from plotnine.utils.smoothers import tdist_ci
                y = data["y"]            # The predicted value
                df = 123                 # Degrees of freedom
                stderr = results.stderr  # Standard error
                level = params["level"]  # The parameter value
                low, high = tdist_ci(y, df, stderr, level)
                data["se"] = stderr
                data["ymin"] = low
                data["ymax"] = high

            return data
        ```

        For *loess* smoothing you must install the `scikit-misc` package.
        You can install it using with `pip install scikit-misc` or
        `pip install plotnine[all]`.
    formula : formula_like, default=None
        An object that can be used to construct a patsy design matrix.
        This is usually a string. You can only use a formula if `method`
        is one of *lm*, *ols*, *wls*, *glm*, *rlm* or *gls*, and in the
        [formula](https://patsy.readthedocs.io/en/stable/formulas.html)
        you may refer to the `x` and `y` aesthetic variables.
    se : bool, default=True
        If `True`{.py} draw confidence interval around the smooth line.
    n : int, default=80
        Number of points to evaluate the smoother at. Some smoothers
        like *mavg* do not support this.
    fullrange : bool, default: False
        If `True`{.py} the fit will span the full range of the plot.
    level : float, default=0.95
        Level of confidence to use if `se=True`{.py}.
    span : float, default=2/3.
        Controls the amount of smoothing for the *loess* smoother.
        Larger number means more smoothing. It should be in the
        `(0, 1)` range.
    method_args : dict, default={}
        Additional arguments passed on to the modelling method.

    See Also
    --------
    plotnine.geom_smooth : The default `geom` for this `stat`.
    statsmodels.regression.linear_model.OLS
    statsmodels.regression.linear_model.WLS
    statsmodels.robust.robust_linear_model.RLM
    statsmodels.genmod.generalized_linear_model.GLM
    statsmodels.regression.linear_model.GLS
    statsmodels.nonparametric.smoothers_lowess.lowess
    skmisc.loess.loess
    pandas.DataFrame.rolling
    sklearn.gaussian_process.GaussianProcessRegressor

    Notes
    -----
    [](`~plotnine.geoms.geom_smooth`) and [](`~plotnine.stats.stat_smooth`) are
    effectively aliases, they both use the same arguments.
    Use [](`~plotnine.geoms.geom_smooth`) unless
    you want to display the results with a non-standard geom.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "se"    # Standard error of points in bin
    "ymin"  # Lower confidence limit
    "ymax"  # Upper confidence limit
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('se')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "smooth",
        "method": "auto",
        "se": True,
        "n": 80,
        "formula": None,
        "fullrange": False,
        "level": 0.95,
        "span": 0.75,
        "method_args": {},
    }
    CREATES = {"se", "ymin", "ymax"}

    def setup_data(self, data):
        """
        Override to modify data before compute_layer is called
        """
        data = data[np.isfinite(data["x"]) & np.isfinite(data["y"])]
        return data

    def setup_params(self, data):
        params = self.params
        # Use loess/lowess for small datasets
        # and glm for large
        if params["method"] == "auto":
            max_group = data["group"].value_counts().max()
            if max_group < 1000:
                try:
                    from skmisc.loess import loess  # noqa: F401

                    params["method"] = "loess"
                except ImportError:
                    params["method"] = "lowess"
            else:
                params["method"] = "glm"

        if (
            params["method"] == "mavg"
            and "window" not in params["method_args"]
        ):
            window = len(data) // 10
            warnings.warn(
                "No 'window' specified in the method_args. "
                f"Using window = {window}. "
                "The same window is used for all groups or "
                "facets",
                PlotnineWarning,
                stacklevel=2,
            )
            params["method_args"]["window"] = window

        if params["formula"]:
            allowed = {"lm", "ols", "wls", "glm", "rlm", "gls"}
            if params["method"] not in allowed:
                raise ValueError(
                    "You can only use a formula with `method` is "
                    f"one of {allowed}"
                )
            params["environment"] = self.environment

    def compute_group(self, data, scales):
        data = data.sort_values("x")
        n = self.params["n"]

        x_unique = data["x"].unique()

        if len(x_unique) < 2:
            warnings.warn(
                "Smoothing requires 2 or more points. Got "
                f"{len(x_unique)}. Not enough points for smoothing. "
                "If this message a surprise, make sure the column "
                "mapped to the x aesthetic has the right dtype.",
                PlotnineWarning,
            )
            # Not enough data to fit
            return pd.DataFrame()

        if data["x"].dtype.kind == "i":
            if self.params["fullrange"]:
                xseq = scales.x.dimension()
            else:
                xseq = np.sort(x_unique)
        else:
            if self.params["fullrange"]:
                rangee = scales.x.dimension()
            else:
                rangee = [data["x"].min(), data["x"].max()]
            xseq = np.linspace(rangee[0], rangee[1], n)

        return predictdf(data, xseq, self.params)
</file>

<file path="plotnine/stats/stat_sum.py">
from .._utils import groupby_apply
from ..doctools import document
from ..mapping.aes import ALL_AESTHETICS
from ..mapping.evaluation import after_stat
from .stat import stat


@document
class stat_sum(stat):
    """
    Sum unique values

    Useful for overplotting on scatterplots.

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_point : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "n"     # Number of observations at a position
    "prop"  # Ratio of points in that panel at a position
    ```
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {"geom": "point"}
    DEFAULT_AES = {"size": after_stat("n"), "weight": 1}
    CREATES = {"n", "prop"}

    def compute_panel(self, data, scales):
        if "weight" not in data:
            data["weight"] = 1

        def count(df):
            """
            Do a weighted count
            """
            df["n"] = df["weight"].sum()
            return df.iloc[0:1]

        def ave(df):
            """
            Calculate proportion values
            """
            df["prop"] = df["n"] / df["n"].sum()
            return df

        # group by all present aesthetics other than the weight,
        # then sum them (i.e no. of uniques) to get the raw count
        # 'n', and the proportions 'prop' per group
        s: set[str] = set(data.columns) & ALL_AESTHETICS
        by = list(s.difference(["weight"]))
        counts = groupby_apply(data, by, count)
        counts = groupby_apply(counts, "group", ave)
        return counts
</file>

<file path="plotnine/stats/stat_unique.py">
from ..doctools import document
from .stat import stat


@document
class stat_unique(stat):
    """
    Remove duplicates

    {usage}

    Parameters
    ----------
    {common_parameters}

    See Also
    --------
    plotnine.geom_point : The default `geom` for this `stat`.
    """

    DEFAULT_PARAMS = {"geom": "point"}

    def compute_panel(self, data, scales):
        return data.drop_duplicates()
</file>

<file path="plotnine/stats/stat_ydensity.py">
from contextlib import suppress

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat
from .stat_density import compute_density, stat_density


@document
class stat_ydensity(stat):
    """
    Density estimate

    {usage}

    Parameters
    ----------
    {common_parameters}
    kernel : str, default="gaussian"
        Kernel used for density estimation. One of:

        ```python
        "biweight"
        "cosine"
        "cosine2"
        "epanechnikov"
        "gaussian"
        "triangular"
        "triweight"
        "uniform"
        ```
    adjust : float, default=1
        An adjustment factor for the `bw`. Bandwidth becomes
        `bw * adjust`{.py}.
        Adjustment of the bandwidth.
    trim : bool, default=False
        This parameter only matters if you are displaying multiple
        densities in one plot. If `False`{.py}, the default, each
        density is computed on the full range of the data. If
        `True`{.py}, each density is computed over the range of that
        group; this typically means the estimated x values will not
        line-up, and hence you won't be able to stack density values.
    n : int, default=1024
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    bw : str | float, default="nrd0"
        The bandwidth to use, If a float is given, it is the bandwidth.
        The `str` choices are:

        ```python
        "nrd0"
        "normal_reference"
        "scott"
        "silverman"
        ```

        `nrd0` is a port of `stats::bw.nrd0` in R; it is eqiuvalent
        to `silverman` when there is more than 1 value in a group.
    scale : Literal["area", "count", "width"], default="area"
        How to scale the violins. The options are:
        If `area` all violins have the same area, before trimming the tails.
        If `count` the areas are scaled proportionally to the number of
        observations.
        If `width` all violins have the same maximum width.

    See Also
    --------
    plotnine.geom_violin : The default `geom` for this `stat`.
    statsmodels.nonparametric.kde.KDEUnivariate
    statsmodels.nonparametric.kde.KDEUnivariate.fit
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "width"        # Maximum width of density, [0, 1] range.
    "violinwidth"  # Shape of the violin
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('width')`{.py}.
    """
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"weight"}
    DEFAULT_PARAMS = {
        "geom": "violin",
        "position": "dodge",
        "adjust": 1,
        "kernel": "gaussian",
        "n": 1024,
        "trim": True,
        "bw": "nrd0",
        "scale": "area",
    }
    DEFAULT_AES = {"weight": None}
    CREATES = {"width", "violinwidth"}

    def setup_data(self, data):
        if "x" not in data:
            data["x"] = 0
        return data

    def setup_params(self, data):
        params = self.params

        valid_scale = ("area", "count", "width")
        if params["scale"] not in valid_scale:
            msg = "Parameter scale should be one of {}"
            raise PlotnineError(msg.format(valid_scale))

        lookup = {
            "biweight": "biw",
            "cosine": "cos",
            "cosine2": "cos2",
            "epanechnikov": "epa",
            "gaussian": "gau",
            "triangular": "tri",
            "triweight": "triw",
            "uniform": "uni",
        }

        with suppress(KeyError):
            params["kernel"] = lookup[params["kernel"].lower()]

        if params["kernel"] not in lookup.values():
            msg = (
                f"kernel should be one of {lookup.keys()}. "
                f"You may use the abbreviations {lookup.values()}"
            )
            raise PlotnineError(msg)

        missing_params = stat_density.DEFAULT_PARAMS.keys() - params.keys()
        for key in missing_params:
            params[key] = stat_density.DEFAULT_PARAMS[key]

    def compute_panel(self, data, scales):
        params = self.params
        data = super().compute_panel(data, scales)

        if not len(data):
            return data

        if params["scale"] == "area":
            data["violinwidth"] = data["density"] / data["density"].max()
        elif params["scale"] == "count":
            data["violinwidth"] = (
                data["density"]
                / data["density"].max()
                * data["n"]
                / data["n"].max()
            )
        elif params["scale"] == "width":
            data["violinwidth"] = data["scaled"]
        else:
            msg = "Unknown scale value '{}'"
            raise PlotnineError(msg.format(params["scale"]))

        return data

    def compute_group(self, data, scales):
        n = len(data)
        if n == 0:
            return pd.DataFrame()

        weight = data.get("weight")

        if self.params["trim"]:
            range_y = data["y"].min(), data["y"].max()
        else:
            range_y = scales.y.dimension()

        dens = compute_density(data["y"], weight, range_y, self.params)

        if not len(dens):
            return dens

        dens["y"] = dens["x"]
        dens["x"] = np.mean([data["x"].min(), data["x"].max()])

        # Compute width if x has multiple values
        if len(np.unique(data["x"])) > 1:
            dens["width"] = np.ptp(data["x"]) * 0.9

        return dens
</file>

<file path="plotnine/facets/facet_grid.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import add_margins, cross_join, join_keys, match, ninteraction
from ..exceptions import PlotnineError
from .facet import (
    add_missing_facets,
    combine_vars,
    eval_facet_vars,
    facet,
    layout_null,
)
from .strips import Strips, strip

if typing.TYPE_CHECKING:
    from typing import Literal, Optional, Sequence

    from matplotlib.axes import Axes

    from plotnine.iapi import layout_details
    from plotnine.typing import FacetSpaceRatios


class facet_grid(facet):
    """
    Wrap 1D Panels onto 2D surface

    Parameters
    ----------
    rows :
        Variable expressions along the rows of the facets/panels.
        Each expression is evaluated within the context of the dataframe.
    cols :
        Variable expressions along the columns of the facets/panels.
        Each expression is evaluated within the context of the dataframe.
    margins :
        variable names to compute margins for.
        True will compute all possible margins.
    space :
        Control the size of the  `x` or `y` sides of the panels.
        The size also depends to the `scales` parameter.

        If a string, it should be one of
        `['fixed', 'free', 'free_x', 'free_y']`{.py}.

        If a `dict`, it indicates the relative facet size ratios such as:

        ```python
        {"x": [1, 2], "y": [3, 1, 1]}
        ```

        This means that in the horizontal direction, the second panel
        will be twice the length of the first. In the vertical direction
        the top facet will be the 3 times longer then the second and
        third facets.

        Note that the number of dimensions in the list must equal the
        number of facets that will be produced.
    shrink :
        Whether to shrink the scales to the output of the
        statistics instead of the raw data.
    labeller :
        How to label the facets. A string value if it should be
        one of `["label_value", "label_both", "label_context"]`{.py}.
    as_table :
        If `True`, the facets are laid out like a table with
        the highest values at the bottom-right. If `False`
        the facets are laid out like a plot with the highest
        value a the top-right
    drop :
        If `True`, all factor levels not used in the data
        will automatically be dropped. If `False`, all
        factor levels will be shown, regardless of whether
        or not they appear in the data.
    """

    def __init__(
        self,
        rows: Optional[str | Sequence[str]] = None,
        cols: Optional[str | Sequence[str]] = None,
        *,
        margins: bool | Sequence[str] = False,
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
        space: (
            Literal["fixed", "free", "free_x", "free_y"] | FacetSpaceRatios
        ) = "fixed",
        shrink: bool = True,
        labeller: Literal[
            "label_value", "label_both", "label_context"
        ] = "label_value",
        as_table: bool = True,
        drop: bool = True,
    ):
        facet.__init__(
            self,
            scales=scales,
            shrink=shrink,
            labeller=labeller,
            as_table=as_table,
            drop=drop,
        )
        self.rows, self.cols = parse_grid_rows_cols(rows, cols)
        self.space = space
        self.margins = margins

    def _make_gridspec(self):
        """
        Create gridspec for the panels
        """
        from plotnine._mpl.gridspec import p9GridSpec

        layout = self.layout
        space = self.space
        ratios = {}

        # Calculate the width (x) & height (y) ratios for space=free[xy]
        if isinstance(space, str):
            if space in {"free", "free_x"}:
                pidx: list[int] = (
                    layout.layout.sort_values("COL")
                    .drop_duplicates("COL")
                    .index.tolist()
                )
                panel_views = [layout.panel_params[i] for i in pidx]
                ratios["width_ratios"] = [
                    np.ptp(pv.x.range) for pv in panel_views
                ]

            if space in {"free", "free_y"}:
                pidx = (
                    layout.layout.sort_values("ROW")
                    .drop_duplicates("ROW")
                    .index.tolist()
                )
                panel_views = [layout.panel_params[i] for i in pidx]
                ratios["height_ratios"] = [
                    np.ptp(pv.y.range) for pv in panel_views
                ]

        if isinstance(self.space, dict):
            if len(self.space["x"]) != self.ncol:
                raise ValueError(
                    "The number of x-ratios for the facet space sizes "
                    "should match the number of columns."
                )

            if len(self.space["y"]) != self.nrow:
                raise ValueError(
                    "The number of y-ratios for the facet space sizes "
                    "should match the number of rows."
                )

            ratios["width_ratios"] = self.space.get("x")
            ratios["height_ratios"] = self.space.get("y")

        return p9GridSpec(
            self.nrow,
            self.ncol,
            self.figure,
            nest_into=self.plot._gridspec[0],
            **ratios,
        )

    def compute_layout(self, data: list[pd.DataFrame]) -> pd.DataFrame:
        if not self.rows and not self.cols:
            self.nrow, self.ncol = 1, 1
            return layout_null()

        base_rows = combine_vars(
            data, self.environment, self.rows, drop=self.drop
        )

        if not self.as_table:
            # Reverse the order of the rows
            base_rows = base_rows[::-1]
        base_cols = combine_vars(
            data, self.environment, self.cols, drop=self.drop
        )

        base = cross_join(base_rows, base_cols)

        if self.margins:
            base = add_margins(base, (self.rows, self.cols), self.margins)
            base = base.drop_duplicates().reset_index(drop=True)

        n = len(base)
        panel = ninteraction(base, drop=True)
        panel = pd.Categorical(panel, categories=range(1, n + 1))  # pyright: ignore[reportArgumentType]

        if self.rows:
            rows = ninteraction(base[self.rows], drop=True)
        else:
            rows = [1] * len(panel)

        if self.cols:
            cols = ninteraction(base[self.cols], drop=True)
        else:
            cols = [1] * len(panel)

        layout = pd.DataFrame(
            {
                "PANEL": panel,
                "ROW": rows,
                "COL": cols,
            }
        )
        layout = pd.concat([layout, base], axis=1)
        layout = layout.sort_values("PANEL")
        layout.reset_index(drop=True, inplace=True)

        # Relax constraints, if necessary
        layout["SCALE_X"] = layout["COL"] if self.free["x"] else 1
        layout["SCALE_Y"] = layout["ROW"] if self.free["y"] else 1
        layout["AXIS_X"] = layout["ROW"] == layout["ROW"].max()
        layout["AXIS_Y"] = layout["COL"] == layout["COL"].min()

        self.nrow = layout["ROW"].max()
        self.ncol = layout["COL"].max()
        return layout

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        if not len(data):
            data["PANEL"] = pd.Categorical(
                [], categories=layout["PANEL"].cat.categories, ordered=True
            )
            return data

        vars = (*self.rows, *self.cols)
        margin_vars: tuple[list[str], list[str]] = (
            list(data.columns.intersection(self.rows)),
            list(data.columns.intersection(self.cols)),
        )
        data = add_margins(data, margin_vars, self.margins)

        facet_vals = eval_facet_vars(data, vars, self.environment)
        data, facet_vals = add_missing_facets(data, layout, vars, facet_vals)

        # assign each point to a panel
        if len(facet_vals) and len(facet_vals.columns):
            keys = join_keys(facet_vals, layout, vars)
            data["PANEL"] = match(keys["x"], keys["y"], start=1)
        else:
            # Special case of no facetting
            data["PANEL"] = 1

        # matching dtype and
        # the categories(panel numbers) for the data should be in the
        # same order as the panels. i.e the panels are the reference,
        # they "know" the right order
        data["PANEL"] = pd.Categorical(
            data["PANEL"],
            categories=layout["PANEL"].cat.categories,
            ordered=True,
        )

        data.reset_index(drop=True, inplace=True)
        return data

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        lst = []
        if layout_info.is_top and self.cols:
            s = strip(self.cols, layout_info, self, ax, "top")
            lst.append(s)
        if layout_info.is_right and self.rows:
            s = strip(self.rows, layout_info, self, ax, "right")
            lst.append(s)
        return Strips(lst)


def parse_grid_rows_cols(
    rows: Optional[str | Sequence[str]] = None,
    cols: Optional[str | Sequence[str]] = None,
) -> tuple[list[str], list[str]]:
    """
    Return the rows & cols that make up the grid
    """
    if cols is None and isinstance(rows, str):  # formula
        return parse_grid_facets_old(rows)

    if cols is None:
        cols = []
    elif isinstance(cols, str):
        cols = [cols]

    if rows is None:
        rows = []
    elif isinstance(rows, str):
        rows = [rows]

    return list(rows), list(cols)


def parse_grid_facets_old(
    facets: str | tuple[str | Sequence[str], str | Sequence[str]],
) -> tuple[list[str], list[str]]:
    """
    Return two lists of facetting variables, for the rows & columns

    This parse the old & silently deprecated style.
    """
    valid_seqs = [
        "(var1,)",
        "('var1', '.')",
        "('var1', 'var2')",
        "('.', 'var1')",
        "((var1, var2), (var3, var4))",
    ]
    error_msg_s = (
        f"Valid sequences for specifying 'facets' look like {valid_seqs}"
    )

    valid_forms = [
        "var1",
        "var1 ~ .",
        "var1 ~ var2",
        ". ~ var1",
        "var1 + var2 ~ var3 + var4",
        ". ~ func(var1) + func(var2)",
        ". ~ func(var1+var3) + func(var2)",
    ] + valid_seqs
    error_msg_f = f"Valid formula for 'facet_grid' look like {valid_forms}"

    if not isinstance(facets, str):
        if len(facets) == 1:
            rows = ensure_list_spec(facets[0])
            cols = []
        elif len(facets) == 2:
            rows = ensure_list_spec(facets[0])
            cols = ensure_list_spec(facets[1])
        else:
            raise PlotnineError(error_msg_s)
        return list(rows), list(cols)

    if "~" not in facets:
        rows = ensure_list_spec(facets)
        return list(rows), []

    # Example of allowed formulae
    # "c ~ a + b'
    # '. ~ func(a) + func(b)'
    # 'func(c) ~ func(a+1) + func(b+2)'
    try:
        lhs, rhs = facets.split("~")
    except ValueError as e:
        raise PlotnineError(error_msg_f) from e
    else:
        lhs = lhs.strip()
        rhs = rhs.strip()

    rows = ensure_list_spec(lhs)
    cols = ensure_list_spec(rhs)
    return list(rows), list(cols)


def ensure_list_spec(term: Sequence[str] | str) -> Sequence[str]:
    """
    Convert a str specification to a list spec

    e.g.
    'a' -> ['a']
    'a + b' -> ['a', 'b']
    '.' -> []
    '' -> []
    """
    if isinstance(term, str):
        splitter = " + " if " + " in term else "+"
        if term in [".", ""]:
            return []
        return [var.strip() for var in term.split(splitter)]
    else:
        return term
</file>

<file path="plotnine/facets/facet.py">
from __future__ import annotations

import itertools
import types
import typing
from copy import copy, deepcopy

import numpy as np
import pandas as pd
import pandas.api.types as pdtypes

from .._utils import cross_join, match
from ..exceptions import PlotnineError
from ..scales.scales import Scales
from .strips import Strips

if typing.TYPE_CHECKING:
    from typing import Any, Literal, Optional, Sequence

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from plotnine import ggplot, theme
    from plotnine._mpl.gridspec import p9GridSpec
    from plotnine.coords.coord import coord
    from plotnine.facets.labelling import CanBeStripLabellingFunc
    from plotnine.facets.layout import Layout
    from plotnine.iapi import layout_details, panel_view
    from plotnine.layer import Layers
    from plotnine.mapping import Environment
    from plotnine.scales.scale import scale


class facet:
    """
    Base class for all facets

    Parameters
    ----------
    scales :
        Whether `x` or `y` scales should be allowed (free)
        to vary according to the data on each of the panel.
    shrink :
        Whether to shrink the scales to the output of the
        statistics instead of the raw data. Default is `True`.
    labeller :
        How to label the facets. A string value if it should be
        one of `["label_value", "label_both", "label_context"]`{.py}.
    as_table :
        If `True`, the facets are laid out like a table with
        the highest values at the bottom-right. If `False`
        the facets are laid out like a plot with the highest
        value a the top-right
    drop :
        If `True`, all factor levels not used in the data
        will automatically be dropped. If `False`, all
        factor levels will be shown, regardless of whether
        or not they appear in the data.
    dir :
        Direction in which to layout the panels. `h` for
        horizontal and `v` for vertical.
    """

    # number of columns
    ncol: int

    # number of rows
    nrow: int

    as_table = True
    drop = True
    shrink = True

    # Which axis scales are free
    free: dict[Literal["x", "y"], bool]

    # A dict of parameters created depending on the data
    # (Intended for extensions)
    params: dict[str, Any]

    # Theme object, automatically updated before drawing the plot
    theme: theme

    # Figure object on which the facet panels are created
    figure: Figure

    # coord object, automatically updated before drawing the plot
    coordinates: coord

    # layout object, automatically updated before drawing the plot
    layout: Layout

    # Axes
    axs: list[Axes]

    # ggplot object that the facet belongs to
    plot: ggplot

    # Facet strips
    strips: Strips

    # The plot environment
    environment: Environment

    def __init__(
        self,
        scales: Literal["fixed", "free", "free_x", "free_y"] = "fixed",
        shrink: bool = True,
        labeller: CanBeStripLabellingFunc = "label_value",
        as_table: bool = True,
        drop: bool = True,
        dir: Literal["h", "v"] = "h",
    ):
        from .labelling import as_labeller

        self.shrink = shrink
        self.labeller = as_labeller(labeller)
        self.as_table = as_table
        self.drop = drop
        self.dir = dir
        allowed_scales = ["fixed", "free", "free_x", "free_y"]
        if scales not in allowed_scales:
            raise ValueError(
                "Argument `scales` must be one of {allowed_scales}."
            )
        self.free = {
            "x": scales in ("free_x", "free"),
            "y": scales in ("free_y", "free"),
        }

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add facet to ggplot object
        """
        other.facet = copy(self)
        other.facet.environment = other.environment
        return other

    def setup(self, plot: ggplot):
        self.plot = plot
        self.layout = plot.layout
        self.figure = plot.figure

        if hasattr(plot, "axs"):
            gs, self.axs = plot._sub_gridspec, plot.axs
        else:
            gs, self.axs = self._make_axes()

        self.coordinates = plot.coordinates
        self.theme = plot.theme
        self.layout.axs = self.axs
        self.strips = Strips.from_facet(self)
        return gs, self.axs

    def setup_data(self, data: list[pd.DataFrame]) -> list[pd.DataFrame]:
        """
        Allow the facet to manipulate the data

        Parameters
        ----------
        data :
            Data for each of the layers

        Returns
        -------
        :
            Data for each of the layers

        Notes
        -----
        This method will be called after [](`~plotnine.facet.setup_params`),
        therefore the `params` property will be set.
        """
        return data

    def setup_params(self, data: list[pd.DataFrame]):
        """
        Create facet parameters

        Parameters
        ----------
        data :
            Plot data and data for the layers
        """
        self.params = {}

    def init_scales(
        self,
        layout: pd.DataFrame,
        x_scale: Optional[scale] = None,
        y_scale: Optional[scale] = None,
    ) -> types.SimpleNamespace:
        scales = types.SimpleNamespace()

        if x_scale is not None:
            n = layout["SCALE_X"].max()
            scales.x = Scales([x_scale.clone() for i in range(n)])

        if y_scale is not None:
            n = layout["SCALE_Y"].max()
            scales.y = Scales([y_scale.clone() for i in range(n)])

        return scales

    def map(self, data: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
        """
        Assign a data points to panels

        Parameters
        ----------
        data :
            Data for a layer
        layout :
            As returned by self.compute_layout

        Returns
        -------
        :
            Data with all points mapped to the panels
            on which they will be plotted.
        """
        msg = "{} should implement this method."
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def compute_layout(
        self,
        data: list[pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Compute layout

        Parameters
        ----------
        data :
            Dataframe for a each layer
        """
        msg = "{} should implement this method."
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def finish_data(self, data: pd.DataFrame, layout: Layout) -> pd.DataFrame:
        """
        Modify data before it is drawn out by the geom

        The default is to return the data without modification.
        Subclasses should override this method as the require.

        Parameters
        ----------
        data :
            A single layer's data.
        layout :
            Layout

        Returns
        -------
        :
            Modified layer data
        """
        return data

    def train_position_scales(self, layout: Layout, layers: Layers) -> facet:
        """
        Compute ranges for the x and y scales
        """
        _layout = layout.layout
        panel_scales_x = layout.panel_scales_x
        panel_scales_y = layout.panel_scales_y

        # loop over each layer, training x and y scales in turn
        for layer in layers:
            data = layer.data
            match_id = match(data["PANEL"], _layout["PANEL"])
            if panel_scales_x:
                x_vars = list(
                    set(panel_scales_x[0].aesthetics) & set(data.columns)
                )
                # the scale index for each data point
                SCALE_X = _layout["SCALE_X"].iloc[match_id].tolist()
                panel_scales_x.train(data, x_vars, SCALE_X)

            if panel_scales_y:
                y_vars = list(
                    set(panel_scales_y[0].aesthetics) & set(data.columns)
                )
                # the scale index for each data point
                SCALE_Y = _layout["SCALE_Y"].iloc[match_id].tolist()
                panel_scales_y.train(data, y_vars, SCALE_Y)

        return self

    def make_strips(self, layout_info: layout_details, ax: Axes) -> Strips:
        """
        Create strips for the facet

        Parameters
        ----------
        layout_info :
            Layout information. Row from the layout table

        ax :
            Axes to label
        """
        return Strips()

    def set_limits_breaks_and_labels(self, panel_params: panel_view, ax: Axes):
        """
        Add limits, breaks and labels to the axes

        Parameters
        ----------
        panel_params :
            range information for the axes
        ax :
            Axes
        """
        from .._mpl.ticker import MyFixedFormatter

        def _inf_to_none(
            t: tuple[float, float],
        ) -> tuple[float | None, float | None]:
            """
            Replace infinities with None
            """
            a = t[0] if np.isfinite(t[0]) else None
            b = t[1] if np.isfinite(t[1]) else None
            return (a, b)

        theme = self.theme

        # limits
        ax.set_xlim(*_inf_to_none(panel_params.x.range))
        ax.set_ylim(*_inf_to_none(panel_params.y.range))

        if typing.TYPE_CHECKING:
            assert callable(ax.set_xticks)
            assert callable(ax.set_yticks)

        # breaks, labels
        ax.set_xticks(panel_params.x.breaks, panel_params.x.labels)
        ax.set_yticks(panel_params.y.breaks, panel_params.y.labels)

        # minor breaks
        ax.set_xticks(panel_params.x.minor_breaks, minor=True)
        ax.set_yticks(panel_params.y.minor_breaks, minor=True)

        # When you manually set the tick labels MPL changes the locator
        # so that it no longer reports the x & y positions
        # Fixes https://github.com/has2k1/plotnine/issues/187
        ax.xaxis.set_major_formatter(MyFixedFormatter(panel_params.x.labels))
        ax.yaxis.set_major_formatter(MyFixedFormatter(panel_params.y.labels))

        pad_x = theme.get_margin("axis_text_x").pt.t
        pad_y = theme.get_margin("axis_text_y").pt.r

        ax.tick_params(axis="x", which="major", pad=pad_x)
        ax.tick_params(axis="y", which="major", pad=pad_y)

    def __deepcopy__(self, memo: dict[Any, Any]) -> facet:
        """
        Deep copy without copying the dataframe and environment
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a deepcopy of the figure & the axes
        shallow = {"axs", "first_ax", "last_ax"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)

        return result

    def _make_gridspec(self):
        """
        Create gridspec for the panels
        """
        from plotnine._mpl.gridspec import p9GridSpec

        return p9GridSpec(
            self.nrow, self.ncol, self.figure, nest_into=self.plot._gridspec[0]
        )

    def _make_axes(self) -> tuple[p9GridSpec, list[Axes]]:
        """
        Create and return subplot axes
        """

        num_panels = len(self.layout.layout)
        axsarr = np.empty((self.nrow, self.ncol), dtype=object)
        gs = self._make_gridspec()

        # Create axes
        it = itertools.product(range(self.nrow), range(self.ncol))
        for i, (row, col) in enumerate(it):
            axsarr[row, col] = self.figure.add_subplot(gs[i])

        # Rearrange axes
        # They are ordered to match the positions in the layout table
        if self.dir == "h":
            order: Literal["C", "F"] = "C"
            if not self.as_table:
                axsarr = axsarr[::-1]
        elif self.dir == "v":
            order = "F"
            if not self.as_table:
                axsarr = np.array([row[::-1] for row in axsarr])
        else:
            raise ValueError(f'Bad value `dir="{self.dir}"` for direction')

        axs = axsarr.ravel(order)

        # Delete unused axes
        for ax in axs[num_panels:]:
            self.figure.delaxes(ax)
        axs = axs[:num_panels]
        return gs, list(axs)

    def _aspect_ratio(self) -> Optional[float]:
        """
        Return the aspect_ratio
        """
        aspect_ratio = self.theme.getp("aspect_ratio")
        if aspect_ratio == "auto":
            # If the panels have different limits the coordinates
            # cannot compute a common aspect ratio
            if not self.free["x"] and not self.free["y"]:
                aspect_ratio = self.coordinates.aspect(
                    self.layout.panel_params[0]
                )
            else:
                aspect_ratio = None

        return aspect_ratio


def combine_vars(
    data: list[pd.DataFrame],
    environment: Environment,
    vars: Sequence[str],
    drop: bool = True,
) -> pd.DataFrame:
    """
    Generate all combinations of data needed for facetting

    The first data frame in the list should be the default data
    for the plot. Other data frames in the list are ones that are
    added to the layers.
    """
    if len(vars) == 0:
        return pd.DataFrame()

    # For each layer, compute the facet values
    values = [
        eval_facet_vars(df, vars, environment) for df in data if df is not None
    ]

    # Form the base data frame which contains all combinations
    # of facetting variables that appear in the data
    has_all = [x.shape[1] == len(vars) for x in values]
    if not any(has_all):
        raise PlotnineError(
            "At least one layer must contain all variables used for facetting"
        )
    base = pd.concat([x for i, x in enumerate(values) if has_all[i]], axis=0)
    base = base.drop_duplicates()

    if not drop:
        base = unique_combs(base)

    # sorts according to order of factor levels
    base = base.sort_values(base.columns.tolist())

    # Systematically add on missing combinations
    for i, value in enumerate(values):
        if has_all[i] or len(value.columns) == 0:
            continue
        old = base.loc[:, list(base.columns.difference(value.columns))]
        new = value.loc[
            :, list(base.columns.intersection(value.columns))
        ].drop_duplicates()

        if not drop:
            new = unique_combs(new)

        base = pd.concat([base, cross_join(old, new)], ignore_index=True)

    if len(base) == 0:
        raise PlotnineError("Faceting variables must have at least one value")

    base = base.reset_index(drop=True)
    return base


def unique_combs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate all possible combinations of the values in the columns
    """

    def _unique(s: pd.Series[Any]) -> npt.NDArray[Any] | pd.Index:
        if isinstance(s.dtype, pdtypes.CategoricalDtype):
            return s.cat.categories
        return s.unique()

    # List of unique values from every column
    lst = (_unique(x) for _, x in df.items())
    rows = list(itertools.product(*lst))
    _df = pd.DataFrame(rows, columns=df.columns)

    # preserve the column dtypes
    for col in df:
        t = df[col].dtype
        _df[col] = _df[col].astype(t)
    return _df


def layout_null() -> pd.DataFrame:
    """
    Layout Null
    """
    layout = pd.DataFrame(
        {
            "PANEL": pd.Categorical([1]),
            "ROW": 1,
            "COL": 1,
            "SCALE_X": 1,
            "SCALE_Y": 1,
            "AXIS_X": True,
            "AXIS_Y": True,
        }
    )
    return layout


def add_missing_facets(
    data: pd.DataFrame,
    layout: pd.DataFrame,
    vars: Sequence[str],
    facet_vals: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Add missing facets
    """
    # When in a dataframe some layer does not have all
    # the facet variables, add the missing facet variables
    # and create new data where the points(duplicates) are
    # present in all the facets
    missing_facets = list(set(vars) - set(facet_vals.columns.tolist()))
    if missing_facets:
        to_add = layout.loc[:, missing_facets].drop_duplicates()
        to_add.reset_index(drop=True, inplace=True)

        # a point for each facet, [0, 1, ..., n-1, 0, 1, ..., n-1, ...]
        data_rep = np.tile(np.arange(len(data)), len(to_add))
        # a facet for each point, [0, 0, 0, 1, 1, 1, ... n-1, n-1, n-1]
        facet_rep = np.repeat(np.arange(len(to_add)), len(data))

        data = data.iloc[data_rep, :].reset_index(drop=True)
        facet_vals = facet_vals.iloc[data_rep, :].reset_index(drop=True)
        to_add = to_add.iloc[facet_rep, :].reset_index(drop=True)
        facet_vals = pd.concat(
            [facet_vals, to_add], axis=1, ignore_index=False
        )

    return data, facet_vals


def eval_facet_vars(
    data: pd.DataFrame, vars: Sequence[str], env: Environment
) -> pd.DataFrame:
    """
    Evaluate facet variables

    Parameters
    ----------
    data :
        Factet dataframe
    vars :
        Facet variables
    env :
        Plot environment

    Returns
    -------
    :
        Facet values that correspond to the specified
        variables.
    """

    # To allow expressions in facet formula
    def I(value: Any) -> Any:
        return value

    env = env.with_outer_namespace({"I": I})
    facet_vals = pd.DataFrame(index=data.index)

    for name in vars:
        if name in data:
            # This is a limited solution. If a keyword is
            # part of an expression it will fail in the
            # else statement below
            res = data[name]
        elif str.isidentifier(name):
            # All other non-statements
            continue
        else:
            # Statements
            try:
                res = env.eval(name, inner_namespace=data)
            except NameError:
                continue
        facet_vals[name] = res

    return facet_vals
</file>

<file path="plotnine/geoms/geom_dotplot.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np

from .._utils import groupby_apply, resolution, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from .geom import geom
from .geom_path import geom_path

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import FloatSeries


@document
class geom_dotplot(geom):
    """
    Dot plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    stackdir : Literal["up", "down", "center", "centerwhole"], default="up"
        Direction in which to stack the dots. Options are
    stackratio : float, default=1
        How close to stack the dots. If value is less than 1,
        the dots overlap, if greater than 1 they are spaced.
    dotsize : float, default=1
        Diameter of dots relative to `binwidth`.
    stackgroups : bool, default=False
        If `True`{.py}, the dots are stacked across groups.

    See Also
    --------
    plotnine.stat_bindot : The default `stat` for this `geom`.
    """

    DEFAULT_AES = {"alpha": 1, "color": "black", "fill": "black"}
    REQUIRED_AES = {"x", "y"}
    NON_MISSING_AES = {"size", "shape"}
    DEFAULT_PARAMS = {
        "stat": "bindot",
        "stackdir": "up",
        "stackratio": 1,
        "dotsize": 1,
        "stackgroups": False,
    }

    legend_key_size = staticmethod(geom_path.legend_key_size)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        gp = self.params
        sp = self.params["stat_params"]

        # Issue warnings when parameters don't make sense
        if gp["position"] == "stack":
            warn(
                'position="stack" doesn"t work properly with '
                "geom_dotplot. Use stackgroups=True instead.",
                PlotnineWarning,
            )
        if (
            gp["stackgroups"]
            and sp["method"] == "dotdensity"
            and sp["binpositions"] == "bygroup"
        ):
            warn(
                "geom_dotplot called with stackgroups=TRUE and "
                'method="dotdensity". You probably want to set '
                'binpositions="all"',
                PlotnineWarning,
            )

        if "width" not in data:
            if sp["width"]:
                data["width"] = sp["width"]
            else:
                data["width"] = resolution(data["x"], False) * 0.9

        # Set up the stacking function and range
        if gp["stackdir"] in (None, "up"):

            def stackdots(a: FloatSeries) -> FloatSeries:
                return a - 0.5

            stackaxismin: float = 0
            stackaxismax: float = 1
        elif gp["stackdir"] == "down":

            def stackdots(a: FloatSeries) -> FloatSeries:
                return -a + 0.5

            stackaxismin = -1
            stackaxismax = 0
        elif gp["stackdir"] == "center":

            def stackdots(a: FloatSeries) -> FloatSeries:
                return a - 1 - np.max(a - 1) / 2

            stackaxismin = -0.5
            stackaxismax = 0.5
        elif gp["stackdir"] == "centerwhole":

            def stackdots(a: FloatSeries) -> FloatSeries:
                return a - 1 - np.floor(np.max(a - 1) / 2)

            stackaxismin = -0.5
            stackaxismax = 0.5
        else:
            raise ValueError(f"Invalid value stackdir={gp['stackdir']}")

        # Fill the bins: at a given x (or y),
        # if count=3, make 3 entries at that x
        idx = [i for i, c in enumerate(data["count"]) for j in range(int(c))]
        data = data.iloc[idx]
        data.reset_index(inplace=True, drop=True)
        # Next part will set the position of each dot within each stack
        # If stackgroups=TRUE, split only on x (or y) and panel;
        # if not stacking, also split by group
        groupvars = [sp["binaxis"], "PANEL"]
        if not gp["stackgroups"]:
            groupvars.append("group")

        # Within each x, or x+group, set countidx=1,2,3,
        # and set stackpos according to stack function
        def func(df: pd.DataFrame) -> pd.DataFrame:
            df["countidx"] = range(1, len(df) + 1)
            df["stackpos"] = stackdots(df["countidx"])
            return df

        # Within each x, or x+group, set countidx=1,2,3, and set
        # stackpos according to stack function
        data = groupby_apply(data, groupvars, func)

        # Set the bounding boxes for the dots
        if sp["binaxis"] == "x":
            # ymin, ymax, xmin, and xmax define the bounding
            # rectangle for each stack. Can't do bounding box per dot,
            # because y position isn't real.
            # After position code is rewritten, each dot should have
            # its own bounding box.
            data["xmin"] = data["x"] - data["binwidth"] / 2
            data["xmax"] = data["x"] + data["binwidth"] / 2
            data["ymin"] = stackaxismin
            data["ymax"] = stackaxismax
            data["y"] = 0
        elif sp["binaxis"] == "y":
            # ymin, ymax, xmin, and xmax define the bounding
            # rectangle for each stack. Can't do bounding box per dot,
            # because x position isn't real.
            # xmin and xmax aren't really the x bounds. They're just
            # set to the standard x +- width/2 so that dot clusters
            # can be dodged like other geoms.
            # After position code is rewritten, each dot should have
            # its own bounding box.
            def func(df: pd.DataFrame) -> pd.DataFrame:
                df["ymin"] = df["y"].min() - data["binwidth"][0] / 2
                df["ymax"] = df["y"].max() + data["binwidth"][0] / 2
                return df

            data = groupby_apply(data, "group", func)
            data["xmin"] = data["x"] + data["width"] * stackaxismin
            data["xmax"] = data["x"] + data["width"] * stackaxismax

        return data

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.collections import PatchCollection
        from matplotlib.patches import Ellipse

        data = coord.transform(data, panel_params)
        fill = to_rgba(data["fill"], data["alpha"])
        color = to_rgba(data["color"], data["alpha"])
        ranges = coord.range(panel_params)

        # For perfect circles the width/height of the circle(ellipse)
        # should factor in the dimensions of axes
        bbox = ax.get_window_extent().transformed(
            ax.figure.dpi_scale_trans.inverted()
        )
        ax_width, ax_height = bbox.width, bbox.height

        factor = (ax_width / ax_height) * np.ptp(ranges.y) / np.ptp(ranges.x)
        size = data["binwidth"].iloc[0] * params["dotsize"]
        offsets = data["stackpos"] * params["stackratio"]

        binaxis = params["stat_params"]["binaxis"]
        if binaxis == "x":
            width, height = size, size * factor
            xpos, ypos = data["x"], data["y"] + height * offsets
        elif binaxis == "y":
            width, height = size / factor, size
            xpos, ypos = data["x"] + width * offsets, data["y"]
        else:
            raise ValueError(f"Invalid valid value binaxis={binaxis}")

        circles = []
        for xy in zip(xpos, ypos):
            patch = Ellipse(xy, width=width, height=height)
            circles.append(patch)

        coll = PatchCollection(
            circles,
            edgecolors=color,
            facecolors=fill,
            rasterized=params["raster"],
        )
        ax.add_collection(coll)

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a point in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.lines import Line2D

        fill = to_rgba(data["fill"], data["alpha"])
        key = Line2D(
            [0.5 * da.width],
            [0.5 * da.height],
            marker="o",
            markersize=da.width / 2,
            markerfacecolor=fill,
            markeredgecolor=data["color"],
        )
        da.add_artist(key)
        return da
</file>

<file path="plotnine/geoms/geom_map.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from .._utils import SIZE_FACTOR, to_rgba
from ..doctools import document
from ..exceptions import PlotnineError
from .geom import geom
from .geom_point import geom_point
from .geom_polygon import geom_polygon

if typing.TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from matplotlib.patches import PathPatch
    from shapely.geometry.polygon import LinearRing, Polygon

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import DataLike


@document
class geom_map(geom):
    """
    Draw map feature

    {usage}

    The map feature are drawn without any special projections.

    Parameters
    ----------
    {common_parameters}

    Notes
    -----
    This geom is best suited for plotting a shapefile read into
    geopandas dataframe. The dataframe should have a `geometry`
    column.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "#111111",
        "fill": "#333333",
        "linetype": "solid",
        "shape": "o",
        "size": 0.5,
        "stroke": 0.5,
    }
    REQUIRED_AES = {"geometry"}

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        geom.__init__(self, mapping, data, **kwargs)
        # Almost all geodataframes loaded from shapefiles
        # have a geometry column.
        if "geometry" not in self.mapping:
            self.mapping["geometry"] = "geometry"

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if not len(data):
            return data

        # Remove any NULL geometries, and remember
        # All the non-Null shapes in a shapefile are required to be
        # of the same shape type.
        bool_idx = np.array([g is not None for g in data["geometry"]])
        if not np.all(bool_idx):
            data = data.loc[bool_idx]

        # Add polygon limits. Scale training uses them
        try:
            bounds = data["geometry"].bounds
        except AttributeError:
            # The geometry is not a GeoSeries
            # Bounds calculation is extracted from
            # geopandas.base.GeoPandasBase.bounds
            bounds = pd.DataFrame(
                np.array([x.bounds for x in data["geometry"]]),
                columns=["xmin", "ymin", "xmax", "ymax"],
                index=data.index,
            )
        else:
            bounds.rename(
                columns={
                    "minx": "xmin",
                    "maxx": "xmax",
                    "miny": "ymin",
                    "maxy": "ymax",
                },
                inplace=True,
            )

        data = pd.concat([data, bounds], axis=1)
        return data

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        if not len(data):
            return

        params = self.params
        data.loc[data["color"].isna(), "color"] = "none"
        data.loc[data["fill"].isna(), "fill"] = "none"

        geom_type = data.geometry.iloc[0].geom_type
        if geom_type in ("Polygon", "MultiPolygon"):
            from matplotlib.collections import PatchCollection

            linewidth = data["size"] * SIZE_FACTOR
            fill = to_rgba(data["fill"], data["alpha"])
            patches = [PolygonPatch(g) for g in data["geometry"]]
            coll = PatchCollection(
                patches,
                edgecolor=data["color"],
                facecolor=fill,
                linestyle=data["linetype"],
                linewidth=linewidth,
                zorder=params["zorder"],
                rasterized=params["raster"],
            )
            ax.add_collection(coll)
        elif geom_type == "Point":
            # Extract point coordinates from shapely geom
            # and plot with geom_point
            arr = np.array([list(g.coords)[0] for g in data["geometry"]])
            data["x"] = arr[:, 0]
            data["y"] = arr[:, 1]
            for _, gdata in data.groupby("group"):
                gdata.reset_index(inplace=True, drop=True)
                geom_point.draw_group(gdata, panel_params, coord, ax, params)
        elif geom_type == "MultiPoint":
            # Where n is the length of the dataframe (no. of multipoints),
            #       m is the number of all points in all multipoints
            #
            # - MultiPoint -> List of Points (tuples) (n -> m)
            # - Explode the list, to create a dataframe were each point
            #      is associated with the right aesthetics (n -> m)
            # - Create x & y columns from the points (m -> m)
            data["points"] = [
                [p.coords[0] for p in mp.geoms] for mp in data["geometry"]
            ]
            data = data.explode("points", ignore_index=True)
            data["x"] = [p[0] for p in data["points"]]
            data["y"] = [p[1] for p in data["points"]]
            geom_point.draw_group(data, panel_params, coord, ax, params)
        elif geom_type in ("LineString", "MultiLineString"):
            from matplotlib.collections import LineCollection

            linewidth = data["size"] * SIZE_FACTOR
            color = to_rgba(data["color"], data["alpha"])
            segments = []
            for g in data["geometry"]:
                if g.geom_type == "LineString":
                    segments.append(g.coords)
                else:
                    segments.extend(_g.coords for _g in g.geoms)

            coll = LineCollection(
                segments,
                edgecolor=color,
                linewidth=linewidth,
                linestyle=data["linetype"],
                zorder=params["zorder"],
                rasterized=params["raster"],
            )
            ax.add_collection(coll)
        else:
            raise TypeError(f"Could not plot geometry of type '{geom_type}'")

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        data["size"] = data["stroke"]
        del data["stroke"]
        return geom_polygon.draw_legend(data, da, lyr)


def PolygonPatch(
    obj: Polygon,
) -> PathPatch:
    """
    Return a Matplotlib patch from a Polygon/MultiPolygon Geometry

    Parameters
    ----------
    obj : shapley.geometry.Polygon | shapley.geometry.MultiPolygon
        A Polygon or MultiPolygon to create a patch for description

    Returns
    -------
    result : matplotlib.patches.PathPatch
        A patch representing the shapely geometry

    Notes
    -----
    This functionality was originally provided by the descartes package
    by Sean Gillies (BSD license, https://pypi.org/project/descartes)
    which is nolonger being maintained.
    """
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path

    def cw_coords(ring: LinearRing) -> npt.NDArray[Any]:
        """
        Return Clockwise array coordinates

        Parameters
        ----------
        ring: shapely.geometry.polygon.LinearRing
            LinearRing

        Returns
        -------
        out: ndarray
            (n x 2) array of coordinate points.
        """
        if ring.is_ccw:
            return np.asarray(ring.coords)[:, :2][::-1]
        return np.asarray(ring.coords)[:, :2]

    def ccw_coords(ring: LinearRing) -> npt.NDArray[Any]:
        """
        Return Counter Clockwise array coordinates

        Parameters
        ----------
        ring: shapely.geometry.polygon.LinearRing
            LinearRing

        Returns
        -------
        out: ndarray
            (n x 2) array of coordinate points.
        """
        if ring.is_ccw:
            return np.asarray(ring.coords)[:, :2]
        return np.asarray(ring.coords)[:, :2][::-1]

    # The interiors are holes in the Polygon
    # MPL draws a hole if the vertex points are specified
    # in an opposite direction. So we use Clockwise for
    # the exterior/shell and Counter-Clockwise for any
    # interiors/holes
    if obj.geom_type == "Polygon":
        _exterior = [Path(cw_coords(obj.exterior))]
        _interior = [Path(ccw_coords(ring)) for ring in obj.interiors]
    else:
        # A MultiPolygon has one or more Polygon geoms.
        # Concatenate the exterior of all the Polygons
        # and the interiors
        _exterior = []
        _interior = []
        for p in obj.geoms:  # type: ignore
            _exterior.append(Path(cw_coords(p.exterior)))
            _interior.extend([Path(ccw_coords(ring)) for ring in p.interiors])

    path = Path.make_compound_path(*_exterior, *_interior)
    return PathPatch(path)


def check_geopandas():
    try:
        import geopandas  # noqa: F401
    except ImportError as e:
        msg = "geom_map requires geopandas. Please install geopandas."
        raise PlotnineError(msg) from e
</file>

<file path="plotnine/geoms/geom_rug.py">
from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np

from .._utils import SIZE_FACTOR, make_line_segments, to_rgba
from ..coords import coord_flip
from ..doctools import document
from .geom import geom
from .geom_path import geom_path

if TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.typing import FloatArray


@document
class geom_rug(geom):
    """
    Marginal rug plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    sides : str, default="bl"
        Sides onto which to draw the marks. Any combination
        chosen from the characters `"btlr"`, for *bottom*, *top*,
        *left* or *right* side marks.
    length: float, default=0.03
        length of marks in fractions of horizontal/vertical panel size.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "size": 0.5,
        "linetype": "solid",
    }
    DEFAULT_PARAMS = {"sides": "bl", "length": 0.03}

    draw_legend = staticmethod(geom_path.draw_legend)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        from matplotlib.collections import LineCollection

        data = coord.transform(data, panel_params)
        sides = params["sides"]

        # coord_flip does not flip the side(s) on which the rugs
        # are plotted. We do the flipping here
        if isinstance(coord, coord_flip):
            t = str.maketrans("tblr", "rlbt")
            sides = sides.translate(t)

        linewidth = data["size"] * SIZE_FACTOR

        has_x = "x" in data.columns
        has_y = "y" in data.columns

        if has_x or has_y:
            n = len(data)
        else:
            return

        rugs = []
        xmin, xmax = panel_params.x.range
        ymin, ymax = panel_params.y.range
        xheight = (xmax - xmin) * params["length"]
        yheight = (ymax - ymin) * params["length"]

        if has_x:
            x = cast("FloatArray", np.repeat(data["x"].to_numpy(), 2))

            if "b" in sides:
                y = np.tile([ymin, ymin + yheight], n)
                rugs.extend(make_line_segments(x, y, ispath=False))

            if "t" in sides:
                y = np.tile([ymax - yheight, ymax], n)
                rugs.extend(make_line_segments(x, y, ispath=False))

        if has_y:
            y = cast("FloatArray", np.repeat(data["y"].to_numpy(), 2))

            if "l" in sides:
                x = np.tile([xmin, xmin + xheight], n)
                rugs.extend(make_line_segments(x, y, ispath=False))

            if "r" in sides:
                x = np.tile([xmax - xheight, xmax], n)
                rugs.extend(make_line_segments(x, y, ispath=False))

        color = to_rgba(data["color"], data["alpha"])
        coll = LineCollection(
            rugs,
            edgecolor=color,
            linewidth=linewidth,
            linestyle=data["linetype"],
            zorder=params["zorder"],
            rasterized=params["raster"],
        )
        ax.add_collection(coll)
</file>

<file path="plotnine/geoms/geom_text.py">
from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, cast
from warnings import warn

import numpy as np

from .._utils import order_as_data_mapping, to_rgba
from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..positions import position_nudge
from .geom import geom

if TYPE_CHECKING:
    from typing import Any, Sequence

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from matplotlib.text import Text

    from plotnine import aes
    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import DataLike


# Note: hjust & vjust are parameters instead of aesthetics
# due to a limitation imposed by MPL
# see: https://github.com/matplotlib/matplotlib/pull/1181
@document
class geom_text(geom):
    """
    Textual annotations

    {usage}

    Parameters
    ----------
    {common_parameters}
    parse : bool, default=False
        If `True`{.py}, the labels will be rendered with
        [latex](http://matplotlib.org/users/usetex.html).
    nudge_x : float, default=0
        Horizontal adjustment to apply to the text
    nudge_y : float, default=0
        Vertical adjustment to apply to the text
    adjust_text: dict, default=None
        Parameters to [](`~adjustText.adjust_text`) will repel
        overlapping texts. This parameter takes priority of over
        `nudge_x` and `nudge_y`.
        `adjust_text` does not work well when it is used in the
        first layer of the plot, or if it is the only layer.
        For more see the documentation at
        https://github.com/Phlya/adjustText/wiki .
    format_string : str, default=None
        If not `None`{.py}, then the text is formatted with this
        string using [](`str.format`) e.g:

        ```python
        # 2.348 -> "2.35%"
        geom_text(format_string="{:.2f}%")
        ```
    path_effects : list, default=None
        If not `None`{.py}, then the text will use these effects.
        See
        [](https://matplotlib.org/tutorials/advanced/patheffects_guide.html)
        documentation for more details.

    See Also
    --------
    plotnine.geom_label
    matplotlib.text.Text
    matplotlib.patheffects

    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Aesthetics Descriptions**

    `size`

    :   Float or one of:

        ```python
        {
            "xx-small", "x-small", "small", "medium", "large",
            "x-large", "xx-large"
        }
        ```

    `ha`

    :   Horizontal alignment. One of `{"left", "center", "right"}`{.py}.

    `va`

    :   Vertical alignment. One of
        `{"top", "center", "bottom", "baseline", "center_baseline"}`{.py}.

    `family`

    :   Font family. Can be a font name
        e.g. "Arial", "Helvetica", "Times", ... or a family that is one of
        `{"serif", "sans-serif", "cursive", "fantasy", "monospace"}}`{.py}

    `fontweight`

    :   Font weight. A numeric value in range 0-1000 or a string that is
        one of:

        ```python
        {
            "ultralight", "light", "normal", "regular", "book", "medium",
            "roman", "semibold", "demibold", "demi", "bold", "heavy",
            "extra bold", "black"
        }
        ```

    `fontstyle`

    :   Font style. One of `{"normal", "italic", "oblique"}`{.py}.

    `fontvariant`

    :   Font variant. One of `{"normal", "small-caps"}`{.py}.
    """
    DEFAULT_AES = {
        "alpha": 1,
        "angle": 0,
        "color": "black",
        "size": 11,
        "lineheight": 1.2,
        "ha": "center",
        "va": "center",
        "family": None,
        "fontweight": "normal",
        "fontstyle": "normal",
        "fontvariant": None,
    }
    REQUIRED_AES = {"label", "x", "y"}
    DEFAULT_PARAMS = {
        "parse": False,
        "nudge_x": 0,
        "nudge_y": 0,
        "adjust_text": None,
        "format_string": None,
        "path_effects": None,
    }

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        data, mapping = order_as_data_mapping(data, mapping)
        nudge_kwargs = {}
        adjust_text = kwargs.get("adjust_text")
        if adjust_text is None:
            with suppress(KeyError):
                nudge_kwargs["x"] = kwargs["nudge_x"]
            with suppress(KeyError):
                nudge_kwargs["y"] = kwargs["nudge_y"]
            if nudge_kwargs:
                kwargs["position"] = position_nudge(**nudge_kwargs)
        else:
            check_adjust_text()

        # Accommodate the old names
        if mapping and "hjust" in mapping:
            mapping["ha"] = mapping.pop("hjust")

        if mapping and "vjust" in mapping:
            mapping["va"] = mapping.pop("vjust")

        geom.__init__(self, mapping, data, **kwargs)

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        parse = self.params["parse"]
        fmt = self.params["format_string"]

        def _format(series: pd.Series, tpl: str) -> list[str | None]:
            """
            Format items in series

            Missing values are preserved as None
            """
            if series.dtype == "float":
                return [None if np.isnan(l) else tpl.format(l) for l in series]
            else:
                return [None if l is None else tpl.format(l) for l in series]

        # format
        if fmt:
            data["label"] = _format(data["label"], fmt)

        # Parse latex
        if parse:
            data["label"] = _format(data["label"], "${}$")

        return data

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        super().draw_panel(data, panel_params, coord, ax)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        data = coord.transform(data, panel_params)
        zorder = params["zorder"]

        # Bind color and alpha
        color = to_rgba(data["color"], data["alpha"])

        # Create a dataframe for the plotting data required
        # by ax.text
        ae_names = list(set(geom_text.DEFAULT_AES) | geom_text.REQUIRED_AES)
        plot_data = data[ae_names]
        plot_data.rename(
            {
                "label": "s",
                "angle": "rotation",
                "lineheight": "linespacing",
            },
            axis=1,
            inplace=True,
        )
        plot_data["color"] = color  # pyright: ignore[reportCallIssue,reportArgumentType]
        plot_data["zorder"] = zorder
        plot_data["rasterized"] = params["raster"]
        plot_data["clip_on"] = True

        # 'boxstyle' indicates geom_label so we need an MPL bbox
        draw_label = "boxstyle" in params
        if draw_label:
            fill = to_rgba(data.pop("fill"), data["alpha"])
            if isinstance(fill, tuple):
                fill = [list(fill)] * len(data["x"])
            plot_data["facecolor"] = fill  # pyright: ignore[reportCallIssue,reportArgumentType]

            tokens = [params["boxstyle"], f"pad={params['label_padding']}"]
            if params["boxstyle"] in {"round", "round4"}:
                tokens.append(f"rounding_size={params['label_r']}")
            elif params["boxstyle"] in ("roundtooth", "sawtooth"):
                tokens.append(f"tooth_size={params['tooth_size']}")

            boxstyle = ",".join(tokens)
            bbox = {"linewidth": params["label_size"], "boxstyle": boxstyle}
        else:
            bbox = {}

        texts: Sequence[Text] = []

        # For labels add a bbox
        for i in range(len(data)):
            kw = cast("dict[str, Any]", plot_data.iloc[i].to_dict())
            if draw_label:
                kw["bbox"] = bbox
                kw["bbox"]["edgecolor"] = params["boxcolor"] or kw["color"]
                kw["bbox"]["facecolor"] = kw.pop("facecolor")
            text_elem = ax.text(**kw)
            texts.append(text_elem)
            if params["path_effects"]:
                text_elem.set_path_effects(params["path_effects"])

        # TODO: Do adjust text per panel
        if params["adjust_text"] is not None:
            if zorder == 1:
                warn(
                    "For better results with adjust_text, it should "
                    "not be the first layer or the only layer.",
                    PlotnineWarning,
                )
            do_adjust_text(
                texts,
                ax,
                params["adjust_text"],
                color[0],
                float(data["size"].mean()),
                zorder,
            )

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw letter 'a' in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.text import Text

        color = to_rgba(data["color"], data["alpha"])

        key = Text(
            x=0.5 * da.width,
            y=0.5 * da.height,
            text="a",
            size=data["size"],
            family=data["family"],
            color=color,
            rotation=data["angle"],
            horizontalalignment="center",
            verticalalignment="center",
        )
        da.add_artist(key)
        return da

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        w, h = min_size
        _w = _h = data["size"]
        if data["color"] is not None:
            w = max(w, _w)
            h = max(h, _h)
        return w, h


def check_adjust_text():
    try:
        pass
    except ImportError as err:
        msg = "To use adjust_text you must install the adjustText package."
        raise PlotnineError(msg) from err


def do_adjust_text(
    texts: Sequence[Text],
    ax: Axes,
    params: dict[str, Any],
    color: Any,
    size: float,
    zorder: float,
):
    from adjustText import adjust_text

    # Mark all axis as stale
    # When anything is drawn onto the axes, its limits become stable and
    # have to be recalculated. When we use ax.add_collection directly, it is
    # on us mark the axis limits as stale. For now the staleness only affects
    # adjust_text, so we do a single "reset" here instead of all the places
    # we use ax.add_collection.
    ax._request_autoscale_view()  # pyright: ignore[reportAttributeAccessIssue]

    _default_params = {
        "expand": (1.5, 1.5),
    }
    # The default arrowprops that are passed to
    # matplotlib.patches.FancyArrowPatch
    _default_arrowprops = {
        "arrowstyle": "->",
        "linewidth": 0.5,
        "color": color,
        # The head_length, tail_length and tail_width of the arrow are
        # specified on the same scale as the fontsize, but their
        # default values are in the [0, 1] range. The true values are
        # obtained by multiplying by the mutation_scale. The default
        # value of mutation_scale is 1, so the arrow is effectively
        # invisible. A good default for this usecase is the size of
        # text.
        "mutation_scale": size,
        # The zorder is of the text / label box, we want the arrow to
        # be between the layer before the text and the text.
        "zorder": zorder - 0.5,
    }
    params = _default_params | params
    params["arrowprops"] = _default_arrowprops | params.get("arrowprops", {})
    adjust_text(texts, ax=ax, **params)
</file>

<file path="plotnine/stats/binning.py">
from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from ..exceptions import PlotnineError
from ..scales.scale_discrete import scale_discrete

if typing.TYPE_CHECKING:
    from typing import Literal, Optional

    from plotnine.typing import FloatArray, FloatArrayLike


__all__ = (
    "freedman_diaconis_bins",
    "breaks_from_bins",
    "breaks_from_binwidth",
    "assign_bins",
    "fuzzybreaks",
)


def freedman_diaconis_bins(a):
    """
    Calculate number of hist bins using Freedman-Diaconis rule.
    """
    from scipy.stats import iqr

    # From http://stats.stackexchange.com/questions/798/
    a = np.asarray(a)
    h = 2 * iqr(a, nan_policy="omit") / (len(a) ** (1 / 3))

    # fall back to sqrt(a) bins if iqr is 0
    if h == 0:
        bins = np.ceil(np.sqrt(a.size))
    else:
        bins = np.ceil((np.nanmax(a) - np.nanmin(a)) / h)

    return int(bins)


def breaks_from_binwidth(
    x_range: tuple[float, float],
    binwidth: float,
    center: Optional[float] = None,
    boundary: Optional[float] = None,
) -> FloatArray:
    """
    Calculate breaks given binwidth

    Parameters
    ----------
    x_range :
        Range over with to calculate the breaks. Must be
        of size 2.
    binwidth :
        Separation between the breaks
    center :
        The center of one of the bins
    boundary :
        A boundary between two bins

    Returns
    -------
    out : array_like
        Sequence of break points.
    """
    if binwidth <= 0:
        raise PlotnineError("The 'binwidth' must be positive.")

    if boundary is not None and center is not None:
        raise PlotnineError(
            "Only one of 'boundary' and 'center' may be specified."
        )
    elif boundary is None:
        # When center is None, put the min and max of data in outer
        # half of their bins
        boundary = binwidth / 2
        if center is not None:
            boundary = center - boundary

    shift = np.floor((x_range[0] - boundary) / binwidth)
    origin = boundary + shift * binwidth
    # The nextafter reduction prevents numerical roundoff in the
    # binwidth from creating an extra break beyond the one that
    # includes x_range[1].
    max_x = np.nextafter(x_range[1] + binwidth, -np.inf)
    breaks = np.arange(origin, max_x, binwidth)
    return breaks


def breaks_from_bins(
    x_range: tuple[float, float],
    bins: int = 30,
    center: Optional[float] = None,
    boundary: Optional[float] = None,
) -> FloatArray:
    """
    Calculate breaks given binwidth

    Parameters
    ----------
    x_range :
        Range over with to calculate the breaks. Must be
        of size 2.
    bins :
        Number of bins
    center :
        The center of one of the bins
    boundary :
        A boundary between two bins

    Returns
    -------
    out : array_like
        Sequence of break points.
    """
    if bins < 1:
        raise PlotnineError("Need at least one bin.")
    elif bins == 1:
        binwidth = x_range[1] - x_range[0]
        boundary = x_range[1]
    else:
        binwidth = (x_range[1] - x_range[0]) / (bins - 1)

    return breaks_from_binwidth(x_range, binwidth, center, boundary)


def assign_bins(
    x,
    breaks: FloatArrayLike,
    weight: Optional[FloatArrayLike] = None,
    pad: bool = False,
    closed: Literal["right", "left"] = "right",
):
    """
    Assign value in x to bins demacated by the break points

    Parameters
    ----------
    x :
        Values to be binned.
    breaks :
        Sequence of break points.
    weight :
        Weight of each value in `x`. Used in creating the frequency
        table. If `None`, then each value in `x` has a weight of 1.
    pad :
        If `True`, add empty bins at either end of `x`.
    closed :
        Whether the right or left edges of the bins are part of the
        bin.

    Returns
    -------
    out : dataframe
        Bin count and density information.
    """
    right = closed == "right"
    # If weight not supplied to, use one (no weight)
    if weight is None:
        weight = np.ones(len(x))
    else:
        # If weight is a dtype that isn't writeable
        # and does not own it's memory. Using a list
        # as an intermediate easily solves this.
        weight = np.array(list(weight))
        weight[np.isnan(weight)] = 0

    bin_idx = pd.cut(
        x,
        bins=breaks,  # type: ignore
        labels=False,
        right=right,
        include_lowest=True,
    )
    bin_widths = np.diff(breaks)
    bin_x = (breaks[:-1] + breaks[1:]) * 0.5  # type: ignore

    # Create a dataframe with two columns:
    #   - the bins to which each x is assigned
    #   - the weight of each x value
    # Then create a weighted frequency table
    bins_long = pd.DataFrame({"bin_idx": bin_idx, "weight": weight})
    wftable = bins_long.pivot_table(
        "weight", index=["bin_idx"], aggfunc="sum"
    )["weight"]

    # Empty bins get no value in the computed frequency table.
    # We need to add the zeros and since frequency table is a
    # Series object, we need to keep it ordered
    if len(wftable) < len(bin_x):
        empty_bins = set(range(len(bin_x))) - set(bin_idx)
        for b in empty_bins:
            wftable.loc[b] = 0  # pyright: ignore
        wftable = wftable.sort_index()
    bin_count = wftable.tolist()

    if pad:
        bw0 = bin_widths[0]
        bwn = bin_widths[-1]
        bin_count = np.hstack([0, bin_count, 0])
        bin_widths = np.hstack([bw0, bin_widths, bwn])
        bin_x = np.hstack([bin_x[0] - bw0, bin_x, bin_x[-1] + bwn])

    return result_dataframe(bin_count, bin_x, bin_widths)


def result_dataframe(count, x, width, xmin=None, xmax=None):
    """
    Create a dataframe to hold bin information
    """
    if xmin is None:
        xmin = x - width / 2

    if xmax is None:
        xmax = x + width / 2

    # Eliminate any numerical roundoff discrepancies
    # between the edges
    xmin[1:] = xmax[:-1]
    density = (count / width) / np.sum(np.abs(count))

    out = pd.DataFrame(
        {
            "count": count,
            "x": x,
            "xmin": xmin,
            "xmax": xmax,
            "width": width,
            "density": density,
            "ncount": count / np.max(np.abs(count)),
            "ndensity": density / np.max(np.abs(density)),
            "ngroup:": np.sum(np.abs(count)),
        }
    )
    return out


def fuzzybreaks(
    scale, breaks=None, boundary=None, binwidth=None, bins=30, right=True
) -> FloatArray:
    """
    Compute fuzzy breaks

    For a continuous scale, fuzzybreaks "preserve" the range of
    the scale. The fuzzing is close to numerical roundoff and
    is visually imperceptible.

    Parameters
    ----------
    scale : scale
        Scale
    breaks : array_like
        Sequence of break points. If provided and the scale is not
        discrete, they are returned.
    boundary : float
        First break. If `None` a suitable on is computed using
        the range of the scale and the binwidth.
    binwidth : float
        Separation between the breaks
    bins : int
        Number of bins
    right : bool
        If `True` the right edges of the bins are part of the
        bin. If `False` then the left edges of the bins are part
        of the bin.

    Returns
    -------
    out : array_like
    """
    from mizani.utils import round_any

    # Bins for categorical data should take the width
    # of one level, and should show up centered over
    # their tick marks. All other parameters are ignored.
    if isinstance(scale, scale_discrete):
        breaks = scale.get_breaks()
        return -0.5 + np.arange(1, len(breaks) + 2)
    else:
        if breaks is not None:
            breaks = scale.transform(breaks)

    if breaks is not None:
        return breaks

    recompute_bins = binwidth is not None
    srange = scale.final_limits

    if binwidth is None or np.isnan(binwidth):
        binwidth = (srange[1] - srange[0]) / bins

    if boundary is None or np.isnan(boundary):
        boundary = round_any(srange[0], binwidth, np.floor)

    if recompute_bins:
        bins = int(np.ceil((srange[1] - boundary) / binwidth))

    # To minimise precision errors, we do not pass the boundary and
    # binwidth into np.arange as params. The resulting breaks
    # can then be adjusted to the next floating point number.
    breaks = np.arange(boundary, srange[1] + binwidth, binwidth)
    return _adjust_breaks(breaks, right)


def _adjust_breaks(breaks: FloatArray, right: bool) -> FloatArray:
    """
    Adjust breaks to include/exclude every right break

    If right=True, the breaks create intervals closed on right
    i.e. [_] (_] (_] (_]
    If right=False, the breaks create intervals closed on the left
    i.e. [_) [_) [_) [_]
    """
    limit, idx = (np.inf, 0) if right else (-np.inf, -1)
    fuzzy = np.nextafter(breaks, limit)
    fuzzy[idx] = np.nextafter(breaks[idx], -limit)
    return fuzzy
</file>

<file path="plotnine/stats/smoothers.py">
from __future__ import annotations

import warnings
from contextlib import suppress
from typing import TYPE_CHECKING, Callable, cast

import numpy as np
import pandas as pd

from .._utils import get_valid_kwargs
from ..exceptions import PlotnineError, PlotnineWarning

if TYPE_CHECKING:
    import statsmodels.api as sm

    from plotnine.typing import FloatArray


def predictdf(data, xseq, params) -> pd.DataFrame:
    """
    Make prediction on the data

    This is a general function responsible for dispatching
    to functions that do predictions for the specific models.
    """
    methods: dict[str, Callable[..., pd.DataFrame]] = {
        "lm": lm,
        "ols": lm,
        "wls": lm,
        "rlm": rlm,
        "glm": glm,
        "gls": gls,
        "lowess": lowess,
        "loess": loess,
        "mavg": mavg,
        "gpr": gpr,
    }

    method = cast("str | Callable[..., pd.DataFrame]", params["method"])

    if isinstance(method, str):
        try:
            method = methods[method]
        except KeyError as e:
            msg = f"Method should be one of {list(methods.keys())}"
            raise PlotnineError(msg) from e

    if not callable(method):
        msg = (
            "'method' should either be a string or a function"
            "with the signature `func(data, xseq, params)`"
        )
        raise PlotnineError(msg)

    return method(data, xseq, params)


def lm(data, xseq, params) -> pd.DataFrame:
    """
    Fit OLS / WLS if data has weight
    """
    import statsmodels.api as sm

    if params["formula"]:
        return lm_formula(data, xseq, params)

    X = sm.add_constant(data["x"])
    Xseq = sm.add_constant(xseq)
    weights = data.get("weight", None)

    if weights is None:
        init_kwargs, fit_kwargs = separate_method_kwargs(
            params["method_args"], sm.OLS, sm.OLS.fit
        )
        model = sm.OLS(data["y"], X, **init_kwargs)
    else:
        if np.any(weights < 0):
            raise ValueError("All weights must be greater than zero.")
        init_kwargs, fit_kwargs = separate_method_kwargs(
            params["method_args"], sm.WLS, sm.WLS.fit
        )
        model = sm.WLS(data["y"], X, weights=data["weight"], **init_kwargs)

    results = model.fit(**fit_kwargs)
    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(Xseq)

    if params["se"]:
        alpha = 1 - params["level"]
        prstd, iv_l, iv_u = wls_prediction_std(results, Xseq, alpha=alpha)
        data["se"] = prstd
        data["ymin"] = iv_l
        data["ymax"] = iv_u

    return data


def lm_formula(data, xseq, params) -> pd.DataFrame:
    """
    Fit OLS / WLS using a formula
    """
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    eval_env = params["environment"].to_patsy_env()
    formula = params["formula"]
    weights = data.get("weight", None)

    if weights is None:
        init_kwargs, fit_kwargs = separate_method_kwargs(
            params["method_args"], sm.OLS, sm.OLS.fit
        )
        model = smf.ols(formula, data, eval_env=eval_env, **init_kwargs)
    else:
        if np.any(weights < 0):
            raise ValueError("All weights must be greater than zero.")
        init_kwargs, fit_kwargs = separate_method_kwargs(
            params["method_args"], sm.OLS, sm.OLS.fit
        )
        model = smf.wls(
            formula, data, weights=weights, eval_env=eval_env, **init_kwargs
        )

    results = model.fit(**fit_kwargs)
    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(data)

    if params["se"]:
        from patsy import dmatrices  # pyright: ignore

        _, predictors = dmatrices(formula, data, eval_env=eval_env)
        alpha = 1 - params["level"]
        prstd, iv_l, iv_u = wls_prediction_std(
            results, predictors, alpha=alpha
        )
        data["se"] = prstd
        data["ymin"] = iv_l
        data["ymax"] = iv_u
    return data


def rlm(data, xseq, params) -> pd.DataFrame:
    """
    Fit RLM
    """
    import statsmodels.api as sm

    if params["formula"]:
        return rlm_formula(data, xseq, params)

    X = sm.add_constant(data["x"])
    Xseq = sm.add_constant(xseq)

    init_kwargs, fit_kwargs = separate_method_kwargs(
        params["method_args"], sm.RLM, sm.RLM.fit
    )
    model = sm.RLM(data["y"], X, **init_kwargs)
    results = model.fit(**fit_kwargs)

    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(Xseq)

    if params["se"]:
        warnings.warn(
            "Confidence intervals are not yet implemented for RLM smoothing.",
            PlotnineWarning,
        )

    return data


def rlm_formula(data, xseq, params) -> pd.DataFrame:
    """
    Fit RLM using a formula
    """
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    eval_env = params["environment"].to_patsy_env()
    formula = params["formula"]
    init_kwargs, fit_kwargs = separate_method_kwargs(
        params["method_args"], sm.RLM, sm.RLM.fit
    )
    model = smf.rlm(formula, data, eval_env=eval_env, **init_kwargs)
    results = model.fit(**fit_kwargs)
    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(data)

    if params["se"]:
        warnings.warn(
            "Confidence intervals are not yet implemented for RLM smoothing.",
            PlotnineWarning,
        )

    return data


def gls(data, xseq, params) -> pd.DataFrame:
    """
    Fit GLS
    """
    import statsmodels.api as sm

    if params["formula"]:
        return gls_formula(data, xseq, params)

    X = sm.add_constant(data["x"])
    Xseq = sm.add_constant(xseq)

    init_kwargs, fit_kwargs = separate_method_kwargs(
        params["method_args"], sm.OLS, sm.OLS.fit
    )
    model = sm.GLS(data["y"], X, **init_kwargs)
    results = model.fit(**fit_kwargs)

    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(Xseq)

    if params["se"]:
        alpha = 1 - params["level"]
        prstd, iv_l, iv_u = wls_prediction_std(results, Xseq, alpha=alpha)
        data["se"] = prstd
        data["ymin"] = iv_l
        data["ymax"] = iv_u

    return data


def gls_formula(data, xseq, params):
    """
    Fit GLL using a formula
    """
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    eval_env = params["environment"].to_patsy_env()
    formula = params["formula"]
    init_kwargs, fit_kwargs = separate_method_kwargs(
        params["method_args"], sm.GLS, sm.GLS.fit
    )
    model = smf.gls(formula, data, eval_env=eval_env, **init_kwargs)
    results = model.fit(**fit_kwargs)
    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(data)

    if params["se"]:
        from patsy import dmatrices  # pyright: ignore

        _, predictors = dmatrices(formula, data, eval_env=eval_env)
        alpha = 1 - params["level"]
        prstd, iv_l, iv_u = wls_prediction_std(
            results, predictors, alpha=alpha
        )
        data["se"] = prstd
        data["ymin"] = iv_l
        data["ymax"] = iv_u
    return data


def glm(data, xseq, params) -> pd.DataFrame:
    """
    Fit GLM
    """
    import statsmodels.api as sm

    if params["formula"]:
        return glm_formula(data, xseq, params)

    X = sm.add_constant(data["x"])
    Xseq = sm.add_constant(xseq)

    init_kwargs, fit_kwargs = separate_method_kwargs(
        params["method_args"], sm.GLM, sm.GLM.fit
    )

    if isinstance(family := init_kwargs.get("family"), str):
        init_kwargs["family"] = _glm_family(family)

    model = sm.GLM(data["y"], X, **init_kwargs)
    results = model.fit(**fit_kwargs)

    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(Xseq)

    if params["se"]:
        prediction = results.get_prediction(Xseq)
        ci = prediction.conf_int(alpha=1 - params["level"])
        data["ymin"] = ci[:, 0]
        data["ymax"] = ci[:, 1]

    return data


def glm_formula(data, xseq, params):
    """
    Fit with GLM formula
    """
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    eval_env = params["environment"].to_patsy_env()
    init_kwargs, fit_kwargs = separate_method_kwargs(
        params["method_args"], sm.GLM, sm.GLM.fit
    )

    if isinstance(family := init_kwargs.get("family"), str):
        init_kwargs["family"] = _glm_family(family)

    model = smf.glm(params["formula"], data, eval_env=eval_env, **init_kwargs)
    results = model.fit(**fit_kwargs)
    data = pd.DataFrame({"x": xseq})
    data["y"] = results.predict(data)

    if params["se"]:
        xdata = pd.DataFrame({"x": xseq})
        prediction = results.get_prediction(xdata)
        ci = prediction.conf_int(alpha=1 - params["level"])
        data["ymin"] = ci[:, 0]
        data["ymax"] = ci[:, 1]
    return data


def lowess(data, xseq, params) -> pd.DataFrame:
    """
    Lowess fitting
    """
    import statsmodels.api as sm

    for k in ("is_sorted", "return_sorted"):
        with suppress(KeyError):
            del params["method_args"][k]
            warnings.warn(f"Smoothing method argument: {k}, has been ignored.")

    result = sm.nonparametric.lowess(
        data["y"],
        data["x"],
        frac=params["span"],
        is_sorted=True,
        **params["method_args"],
    )
    data = pd.DataFrame({"x": result[:, 0], "y": result[:, 1]})

    if params["se"]:
        warnings.warn(
            "Confidence intervals are not yet implemented"
            " for lowess smoothings.",
            PlotnineWarning,
        )

    return data


def loess(data, xseq, params) -> pd.DataFrame:
    """
    Loess smoothing
    """
    try:
        from skmisc.loess import loess as loess_klass
    except ImportError as e:
        msg = "For loess smoothing, install 'scikit-misc'"
        raise PlotnineError(msg) from e

    try:
        weights = data["weight"]
    except KeyError:
        weights = None

    kwargs = params["method_args"]

    extrapolate = min(xseq) < min(data["x"]) or max(xseq) > max(data["x"])
    if "surface" not in kwargs and extrapolate:
        # Creates a loess model that allows extrapolation
        # when making predictions
        kwargs["surface"] = "direct"
        warnings.warn(
            "Making prediction outside the data range, "
            'setting loess control parameter `surface="direct"`.',
            PlotnineWarning,
        )

    if "span" not in kwargs:
        kwargs["span"] = params["span"]

    lo = loess_klass(data["x"], data["y"], weights, **kwargs)
    lo.fit()

    data = pd.DataFrame({"x": xseq})

    if params["se"]:
        alpha = 1 - params["level"]
        prediction = lo.predict(xseq, stderror=True)
        ci = prediction.confidence(alpha=alpha)
        data["se"] = prediction.stderr
        data["ymin"] = ci.lower
        data["ymax"] = ci.upper
    else:
        prediction = lo.predict(xseq, stderror=False)

    data["y"] = prediction.values  # noqa: PD011

    return data


def mavg(data, xseq, params) -> pd.DataFrame:
    """
    Fit moving average
    """
    window = params["method_args"]["window"]

    # The first average comes after the full window size
    # has been swept over
    rolling = data["y"].rolling(**params["method_args"])
    y = rolling.mean()[window:]
    n = len(data)
    stderr = rolling.std()[window:]
    x = data["x"][window:]
    data = pd.DataFrame({"x": x, "y": y})
    data.reset_index(inplace=True, drop=True)

    if params["se"]:
        dof = n - window  # Original - Used
        data["ymin"], data["ymax"] = tdist_ci(y, dof, stderr, params["level"])
        data["se"] = stderr

    return data


def gpr(data, xseq, params):
    """
    Fit gaussian process
    """
    try:
        from sklearn import gaussian_process
    except ImportError as e:
        msg = (
            "To use gaussian process smoothing, "
            "You need to install scikit-learn."
        )
        raise PlotnineError(msg) from e

    kwargs = params["method_args"]
    if not kwargs:
        warnings.warn(
            "See sklearn.gaussian_process.GaussianProcessRegressor "
            "for parameters to pass in as 'method_args'",
            PlotnineWarning,
        )

    regressor = gaussian_process.GaussianProcessRegressor(**kwargs)
    X = np.atleast_2d(data["x"]).T
    n = len(data)
    Xseq = np.atleast_2d(xseq).T
    regressor.fit(X, data["y"])

    data = pd.DataFrame({"x": xseq})
    if params["se"]:
        y, stderr = regressor.predict(Xseq, return_std=True)
        data["y"] = y
        data["se"] = cast("FloatArray", stderr)
        data["ymin"], data["ymax"] = tdist_ci(
            y, n - 1, stderr, params["level"]
        )
    else:
        data["y"] = cast(
            "FloatArray", regressor.predict(Xseq, return_std=False)
        )

    return data


def tdist_ci(x, dof, stderr, level):
    """
    Confidence Intervals using the t-distribution
    """
    import scipy.stats as stats

    q = (1 + level) / 2
    if dof is None:
        delta = stats.norm.ppf(q) * stderr
    else:
        delta = stats.t.ppf(q, dof) * stderr
    return x - delta, x + delta


# Override wls_prediction_std from statsmodels to calculate the confidence
# interval instead of only the prediction interval
def wls_prediction_std(
    res, exog=None, weights=None, alpha=0.05, interval="confidence"
):
    """
    Calculate standard deviation and confidence interval

    Applies to WLS and OLS, not to general GLS,
    that is independently but not identically distributed observations

    Parameters
    ----------
    res : regression-result
        results of WLS or OLS regression required attributes see notes
    exog : array_like
        exogenous variables for points to predict
    weights : scalar | array_like
        weights as defined for WLS (inverse of variance of observation)
    alpha : float
        confidence level for two-sided hypothesis
    interval : str
        Type of interval to compute. One of "confidence" or "prediction"

    Returns
    -------
    predstd : array_like
        Standard error of prediction. It must be the same length as rows
        of exog.
    interval_l, interval_u : array_like
        Lower und upper confidence bounds

    Notes
    -----
    The result instance needs to have at least the following
    res.model.predict() : predicted values or
    res.fittedvalues : values used in estimation
    res.cov_params() : covariance matrix of parameter estimates

    If exog is 1d, then it is interpreted as one observation,
    i.e. a row vector.

    testing status: not compared with other packages

    References
    ----------
    Greene p.111 for OLS, extended to WLS by analogy
    """
    import scipy.stats as stats

    # work around current bug:
    #    fit doesn't attach results to model, predict broken
    # res.model.results

    covb = res.cov_params()
    if exog is None:
        exog = res.model.exog
        predicted = res.fittedvalues
        if weights is None:
            weights = res.model.weights
    else:
        exog = np.atleast_2d(exog)
        if covb.shape[1] != exog.shape[1]:
            raise ValueError("wrong shape of exog")
        predicted = res.model.predict(res.params, exog)
        if weights is None:
            weights = 1.0
        else:
            weights = np.asarray(weights)
            if weights.size > 1 and len(weights) != exog.shape[0]:
                raise ValueError("weights and exog do not have matching shape")

    # full covariance:
    # predvar = res3.mse_resid + np.diag(np.dot(X2,np.dot(covb,X2.T)))
    # predication variance only
    predvar = res.mse_resid / weights
    ip = (exog * np.dot(covb, exog.T).T).sum(1)
    if interval == "confidence":
        predstd = np.sqrt(ip)
    elif interval == "prediction":
        predstd = np.sqrt(ip + predvar)
    else:
        raise ValueError(f"Unknown value for {interval=}")

    tppf = stats.t.isf(alpha / 2.0, res.df_resid)
    interval_u = predicted + tppf * predstd
    interval_l = predicted - tppf * predstd
    return predstd, interval_l, interval_u


def separate_method_kwargs(method_args, init_method, fit_method):
    """
    Categorise kwargs passed to the stat

    Some args are of the init method others for the fit method
    The separation is done by introspecting the init & fit methods
    """
    # inspect the methods
    init_kwargs = get_valid_kwargs(init_method, method_args)
    fit_kwargs = get_valid_kwargs(fit_method, method_args)

    # Warn about unknown kwargs
    known_kwargs = set(init_kwargs) | set(fit_kwargs)
    unknown_kwargs = set(method_args) - known_kwargs
    if unknown_kwargs:
        raise PlotnineError(
            "The following method arguments could not be recognised: "
            f"{list(unknown_kwargs)}"
        )
    return init_kwargs, fit_kwargs


def _glm_family(family: str) -> sm.families.Family:
    """
    Get glm-family instance

    Ref: https://www.statsmodels.org/stable/glm.html#families
    """
    import statsmodels.api as sm

    lookup: dict[str, type[sm.families.Family]] = {
        "binomial": sm.families.Binomial,
        "gamma": sm.families.Gamma,
        "gaussian": sm.families.Gaussian,
        "inverseGaussian": sm.families.InverseGaussian,
        "negativeBinomial": sm.families.NegativeBinomial,
        "poisson": sm.families.Poisson,
        "tweedie": sm.families.Tweedie,
    }
    try:
        return lookup[family.lower()](link=None)  # pyright: ignore
    except KeyError as err:
        msg = f"GLM family should be one of {tuple(lookup)}"
        raise ValueError(msg) from err
</file>

<file path="plotnine/stats/stat_bindot.py">
from __future__ import annotations

import typing
from warnings import warn

import numpy as np
import pandas as pd

from .._utils import groupby_apply
from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..mapping.evaluation import after_stat
from .binning import (
    assign_bins,
    breaks_from_bins,
    breaks_from_binwidth,
    freedman_diaconis_bins,
)
from .stat import stat

if typing.TYPE_CHECKING:
    from typing import Optional

    from plotnine.typing import FloatArrayLike


@document
class stat_bindot(stat):
    """
    Binning for a dot plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    bins : int, default=None
        Number of bins. Overridden by binwidth. If `None`{.py},
        a number is computed using the freedman-diaconis method.
    binwidth : float, default=None
        When `method="dotdensity"`{.py}, this specifies the maximum
        binwidth. When `method="histodot"`{.py}, this specifies the
        binwidth. This supersedes the `bins`.
    origin : float, default=None
        When `method="histodot"`{.py}, origin of the first bin.
    width : float, default=0.9
        When `binaxis="y"`{.py}, the spacing of the dotstacks for
        dodging.
    binaxis : Literal["x", "y"], default="x"
        Axis to bin along.
    method : Literal["dotdensity", "histodot"], default="dotdensity"
        Whether to do dot-density binning or fixed widths binning.
    binpositions : Literal["all", "bygroup"], default="bygroup"
        Position of the bins when `method="dotdensity"`{.py}. The value
        - `bygroup` -  positions of the bins for each group are
        determined separately.
        - `all` - positions of the bins are determined with all
        data taken together. This aligns the dots
        stacks across multiple groups.
    drop : bool, default=False
        If `True`{.py}, remove all bins with zero counts.
    right : bool, default=True
        When `method="histodot"`{.py}, `True`{.py} means include right
        edge of the bins and if `False`{.py} the left edge is included.
    breaks : FloatArray, default=None
        Bin boundaries for `method="histodot"`{.py}. This supersedes the
        `binwidth` and `bins`.

    See Also
    --------
    plotnine.geom_dotplot : The default `geom` for this `stat`.
    plotnine.stat_bin
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "count"    # number of points in bin
    "density"  # density of points in bin, scaled to integrate to 1
    "ncount"   # count, scaled to maximum of 1
    "ndensity" # density, scaled to maximum of 1
    ```

    """

    REQUIRED_AES = {"x"}
    NON_MISSING_AES = {"weight"}
    DEFAULT_PARAMS = {
        "geom": "dotplot",
        "bins": None,
        "binwidth": None,
        "origin": None,
        "width": 0.9,
        "binaxis": "x",
        "method": "dotdensity",
        "binpositions": "bygroup",
        "drop": False,
        "right": True,
        "breaks": None,
    }
    DEFAULT_AES = {"y": after_stat("count")}
    CREATES = {"width", "count", "density", "ncount", "ndensity"}

    def setup_params(self, data):
        params = self.params

        if (
            params["breaks"] is None
            and params["binwidth"] is None
            and params["bins"] is None
        ):
            bins = freedman_diaconis_bins(data["x"])
            params["bins"] = bins
            warn(
                f"'stat_bindot' is using '{bins=}'. "
                "Pick better value with 'binwidth'",
                PlotnineWarning,
            )

    def compute_panel(self, data, scales):
        params = self.params
        if (
            params["method"] == "dotdensity"
            and params["binpositions"] == "all"
        ):
            binaxis = params["binaxis"]
            weight = data.get("weight")
            if binaxis == "x":
                newdata = densitybin(
                    x=data["x"],
                    weight=weight,
                    binwidth=params["binwidth"],
                    bins=params["bins"],
                )
                data = data.sort_values("x")
                data.reset_index(inplace=True, drop=True)
                newdata = newdata.sort_values("x")
                newdata.reset_index(inplace=True, drop=True)
            elif binaxis == "y":
                newdata = densitybin(
                    x=data["y"],
                    weight=weight,
                    binwidth=params["binwidth"],
                    bins=params["bins"],
                )
                data = data.sort_values("y")
                data.reset_index(inplace=True, drop=True)
                newdata = newdata.sort_values("x")
                newdata.reset_index(inplace=True, drop=True)
            else:
                raise ValueError(f"Unknown value {binaxis=}")

            data["bin"] = newdata["bin"]
            data["binwidth"] = newdata["binwidth"]
            data["weight"] = newdata["weight"]
            data["bincenter"] = newdata["bincenter"]
        return super().compute_panel(data, scales)

    def compute_group(self, data, scales):
        params = self.params
        # Check that weights are whole numbers
        # (for dots, weights must be whole)
        weight = data.get("weight")
        if weight is not None:
            int_status = [(w * 1.0).is_integer() for w in weight]
            if not all(int_status):
                raise PlotnineError(
                    "Weights for stat_bindot must be nonnegative integers."
                )

        if params["binaxis"] == "x":
            rangee = scales.x.dimension((0, 0))
            values = data["x"].to_numpy()
            midline = 0  # Make pyright happy
        else:
            rangee = scales.y.dimension((0, 0))
            values = data["y"].to_numpy()
            # The middle of each group, on the stack axis
            midline = np.mean([data["x"].min(), data["x"].max()])

        if params["method"] == "histodot":
            if params["binwidth"] is not None:
                breaks = breaks_from_binwidth(
                    rangee, params["binwidth"], boundary=params["origin"]
                )
            else:
                breaks = breaks_from_bins(
                    rangee, params["bins"], boundary=params["origin"]
                )

            closed = "right" if params["right"] else "left"
            data = assign_bins(
                values, breaks, weight, pad=False, closed=closed
            )
            # for consistency
            data.rename(
                columns={"width": "binwidth", "x": "bincenter"}, inplace=True
            )
        elif params["method"] == "dotdensity":
            # If bin centers are found by group instead of by all,
            # find the bin centers (If binpositions=="all", then
            # we'll already have bin centers.)
            if params["binpositions"] == "bygroup":
                data = densitybin(
                    x=values,
                    weight=weight,
                    binwidth=params["binwidth"],
                    bins=params["bins"],
                    rangee=rangee,
                )

            # Collapse each bin and get a count
            def func(df):
                return pd.DataFrame(
                    {
                        "binwidth": [df["binwidth"].iloc[0]],
                        "bincenter": [df["bincenter"].iloc[0]],
                        "count": [int(df["weight"].sum())],
                    }
                )

            # plyr::ddply + plyr::summarize
            data = groupby_apply(data, "bincenter", func)

            if data["count"].sum() != 0:
                data.loc[np.isnan(data["count"]), "count"] = 0
                data["ncount"] = data["count"] / data["count"].abs().max()
                if params["drop"]:
                    data = data[data["count"] > 0]
                    data.reset_index(inplace=True, drop=True)

        if params["binaxis"] == "x":
            data["x"] = data.pop("bincenter")
            # For x binning, the width of the geoms
            # is same as the width of the bin
            data["width"] = data["binwidth"]
        else:
            data["y"] = data.pop("bincenter")
            # For y binning, set the x midline.
            # This is needed for continuous x axis
            data["x"] = midline

        return data


def densitybin(
    x,
    weight: FloatArrayLike | None,
    binwidth: float | None,
    bins: int = 30,
    rangee: Optional[tuple[float, float]] = None,
):
    """
    Do density binning

    It does not collapse each bin with a count.

    Parameters
    ----------
    x : array_like
        Numbers to bin
    weight : array_like
        Weights
    binwidth : numeric
        Size of the bins
    bins : int
        Number of bins
    rangee : tuple
        Range of x

    Returns
    -------
    data : DataFrame
    """
    if all(pd.isna(x)):
        return pd.DataFrame()

    weight = np.ones(len(x)) if weight is None else np.array(list(weight))
    weight[np.isnan(weight)] = 0

    if rangee is None:
        rangee = np.min(x), np.max(x)
    if bins is None:
        bins = 30
    if binwidth is None:
        binwidth = np.ptp(rangee) / bins

    # Sort weight and x, by x
    order = np.argsort(x)
    weight = weight[order]
    x = x[order]

    cbin = 0  # Current bin ID
    bin_ids = []  # The bin ID for each observation
    # End position of current bin (scan left to right)
    binend = -np.inf

    # Scan list and put dots in bins
    for value in x:
        # If past end of bin, start a new bin at this point
        if value >= binend:
            binend = value + binwidth
            cbin = cbin + 1
        bin_ids.append(cbin)

    def func(series):
        return (series.min() + series.max()) / 2

    results = pd.DataFrame(
        {
            "x": x,
            "bin": bin_ids,
            "binwidth": binwidth,
            "weight": weight,
        }
    )
    # This is a plyr::ddply
    results["bincenter"] = results.groupby("bin")["x"].transform(func)
    return results
</file>

<file path="plotnine/stats/stat_pointdensity.py">
from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from ..mapping.evaluation import after_stat
from .density import get_var_type, kde
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArray


@document
class stat_pointdensity(stat):
    """
    Compute density estimation for each point

    {usage}

    Parameters
    ----------
    {common_parameters}
    package : Literal["statsmodels", "scipy", "sklearn"], default="statsmodels"
        Package whose kernel density estimation to use.
    kde_params : dict, default=None
        Keyword arguments to pass on to the kde class.

    See Also
    --------
    plotnine.geom_density_2d : The default `geom` for this `stat`.
    statsmodels.nonparametric.kde.KDEMultivariate
    scipy.stats.gaussian_kde
    sklearn.neighbors.KernelDensity
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "density"   # Computed density at a point
    ```

    """
    REQUIRED_AES = {"x", "y"}
    DEFAULT_AES = {"color": after_stat("density")}
    DEFAULT_PARAMS = {
        "geom": "density_2d",
        "package": "statsmodels",
        "kde_params": None,
    }
    CREATES = {"density"}

    def setup_params(self, data):
        params = self.params
        if params["kde_params"] is None:
            params["kde_params"] = {}

        kde_params = params["kde_params"]
        if params["package"] == "statsmodels":
            params["package"] = "statsmodels-m"
            if "var_type" not in kde_params:
                x_type = get_var_type(data["x"])
                y_type = get_var_type(data["y"])
                kde_params["var_type"] = f"{x_type}{y_type}"

    def compute_group(self, data, scales):
        package = self.params["package"]
        kde_params = self.params["kde_params"]
        x = cast("FloatArray", data["x"].to_numpy())
        y = cast("FloatArray", data["y"].to_numpy())

        var_data = np.array([x, y]).T
        density = kde(var_data, var_data, package, **kde_params)

        data = pd.DataFrame(
            {
                "x": data["x"],
                "y": data["y"],
                "density": density.flatten(),
            }
        )

        return data
</file>

<file path="plotnine/stats/stat_qq_line.py">
from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat
from .stat_qq import theoretical_qq

if TYPE_CHECKING:
    from plotnine.typing import FloatArray


@document
class stat_qq_line(stat):
    """
    Calculate line through quantile-quantile plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    distribution : str, default="norm"
        Distribution or distribution function name. The default is
        *norm* for a normal probability plot. Objects that look enough
        like a stats.distributions instance (i.e. they have a ppf
        method) are also accepted. See [scipy stats ](`scipy.stats`)
        for available distributions.
    dparams : dict, default=None
        Distribution-specific shape parameters (shape parameters plus
        location and scale).
    quantiles : array_like, default=None
        Probability points at which to calculate the theoretical
        quantile values. If provided, must be the same number as
        as the sample data points. The default is to use calculated
        theoretical points, use to `alpha_beta` control how
        these points are generated.
    alpha_beta : tuple, default=(3/8, 3/8)
        Parameter values to use when calculating the quantiles.
    line_p : tuple, default=(0.25, 0.75)
        Quantiles to use when fitting a Q-Q line. Must be 2 values.
    fullrange : bool, default=False
        If `True`{.py} the fit will span the full range of the plot.

    See Also
    --------
    plotnine.geom_qq_line : The default `geom` for this `stat`.
    scipy.stats.mstats.plotting_positions : Uses `alpha_beta`
        to calculate the quantiles.
    """

    REQUIRED_AES = {"sample"}
    DEFAULT_PARAMS = {
        "geom": "qq_line",
        "distribution": "norm",
        "dparams": {},
        "quantiles": None,
        "alpha_beta": (3 / 8, 3 / 8),
        "line_p": (0.25, 0.75),
        "fullrange": False,
    }
    CREATES = {"x", "y"}

    def setup_params(self, data):
        if len(self.params["line_p"]) != 2:
            raise PlotnineError(
                "Cannot fit line quantiles. 'line_p' must be of length 2"
            )

    def compute_group(self, data, scales):
        from scipy.stats.mstats import mquantiles

        from .distributions import get_continuous_distribution

        line_p = self.params["line_p"]
        dparams = self.params["dparams"]

        # Compute theoretical values
        sample = cast("FloatArray", data["sample"].sort_values().to_numpy())
        theoretical = theoretical_qq(
            sample,
            self.params["distribution"],
            alpha=self.params["alpha_beta"][0],
            beta=self.params["alpha_beta"][1],
            quantiles=self.params["quantiles"],
            distribution_params=dparams,
        )

        # Compute slope & intercept of the line through the quantiles
        cdist = get_continuous_distribution(self.params["distribution"])
        x_coords = cdist.ppf(line_p, **dparams)
        y_coords = mquantiles(sample, line_p)
        slope = (np.diff(y_coords) / np.diff(x_coords))[0]
        intercept = y_coords[0] - slope * x_coords[0]

        # Get x,y points that describe the line
        if self.params["fullrange"] and scales.x:
            x = scales.x.dimension()
        else:
            x = theoretical.min(), theoretical.max()

        x = np.asarray(x)
        y = slope * x + intercept
        data = pd.DataFrame({"x": x, "y": y})
        return data
</file>

<file path="plotnine/stats/stat_summary_bin.py">
from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from .._utils import groupby_apply
from ..doctools import document
from ..exceptions import PlotnineWarning
from ..scales.scale_discrete import scale_discrete
from .binning import fuzzybreaks
from .stat import stat
from .stat_summary import make_summary_fun

if TYPE_CHECKING:
    from plotnine.typing import IntArray


@document
class stat_summary_bin(stat):
    """
    Summarise y values at x intervals

    {usage}

    Parameters
    ----------
    {common_parameters}
    binwidth : float | tuple, default=None
        The width of the bins. The default is to use bins bins that
        cover the range of the data. You should always override this
        value, exploring multiple widths to find the best to illustrate
        the stories in your data.
    bins : int | tuple, default=30
        Number of bins. Overridden by binwidth.
    breaks : array_like | tuple[array_like, array_like], default=None
        Bin boundaries. This supersedes the `binwidth`, `bins`
        and `boundary` arguments.
    boundary : float | tuple, default=None
        A boundary between two bins. As with center, things are
        shifted when boundary is outside the range of the data.
        For example, to center on integers, use `width=1`{.py} and
        `boundary=0.5`{.py}, even if 1 is outside the range of the
        data. At most one of center and boundary may be specified.
    fun_data : str | callable, default="mean_se"
        If a string, should be one of `mean_cl_boot`, `mean_cl_normal`,
        `mean_sdl`, `median_hilow`, `mean_se`.
        If a function, it should that takes an array and return a
        dataframe with three rows indexed as `y`, `ymin` and `ymax`.
    fun_y : callable, default=None
        A function that takes an array_like and returns a single value
    fun_ymax : callable, default=None
        A function that takes an array_like and returns a single value
    fun_args : dict, default=None
        Arguments to any of the functions. Provided the names of the
        arguments of the different functions are in not conflict, the
        arguments will be assigned to the right functions. If there is
        a conflict, create a wrapper function that resolves the
        ambiguity in the argument names.
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.

    Notes
    -----
    The *binwidth*, *bins*, *breaks* and *boundary* arguments can be a
    tuples with two values `(xaxis-value, yaxis-value)` of the
    required type.

    See Also
    --------
    plotnine.geom_pointrange : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "bin"    # bin identifier
    "width"  # bin width
    "ymin"   # ymin computed by the summary function
    "ymax"   # ymax computed by the summary function
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('ymin')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "pointrange",
        "bins": 30,
        "breaks": None,
        "binwidth": None,
        "boundary": None,
        "fun_data": None,
        "fun_y": None,
        "fun_ymin": None,
        "fun_ymax": None,
        "fun_args": None,
        "random_state": None,
    }
    CREATES = {"bin", "width", "ymin", "ymax"}

    def setup_params(self, data):
        keys = ("fun_data", "fun_y", "fun_ymin", "fun_ymax")
        if not any(self.params[k] for k in keys):
            PlotnineWarning(
                "No summary function, supplied, defaulting to mean_se()"
            )
            self.params["fun_data"] = "mean_se"

        if self.params["fun_args"] is None:
            self.params["fun_args"] = {}

        if (
            "random_state" not in self.params["fun_args"]
            and self.params["random_state"]
        ):
            random_state = self.params["random_state"]
            if random_state is None:
                random_state = np.random
            elif isinstance(random_state, int):
                random_state = np.random.RandomState(random_state)

            self.params["fun_args"]["random_state"] = random_state

    def compute_group(self, data, scales):
        bins = self.params["bins"]
        breaks = self.params["breaks"]
        binwidth = self.params["binwidth"]
        boundary = self.params["boundary"]

        func = make_summary_fun(
            self.params["fun_data"],
            self.params["fun_y"],
            self.params["fun_ymin"],
            self.params["fun_ymax"],
            self.params["fun_args"],
        )

        breaks = fuzzybreaks(scales.x, breaks, boundary, binwidth, bins)
        bins = len(breaks) - 1
        data["bin"] = pd.cut(
            data["x"],
            bins=breaks,  # pyright: ignore
            labels=False,
            include_lowest=True,
        )

        def func_wrapper(data: pd.DataFrame) -> pd.DataFrame:
            """
            Add `bin` column to each summary result.
            """
            result = func(data)
            result["bin"] = data["bin"].iloc[0]
            return result

        # This is a plyr::ddply
        out = groupby_apply(data, "bin", func_wrapper)
        centers = (breaks[:-1] + breaks[1:]) * 0.5
        bin = cast("IntArray", out["bin"].to_numpy())
        bin_centers = centers[bin]
        out["x"] = bin_centers
        out["bin"] += 1
        if isinstance(scales.x, scale_discrete):
            out["width"] = 0.9
        else:
            out["width"] = np.diff(breaks)[bins - 1]

        return out
</file>

<file path="plotnine/stats/stat_summary.py">
from typing import cast

import numpy as np
import pandas as pd

from .._utils import get_valid_kwargs, uniquecols
from ..doctools import document
from ..exceptions import PlotnineError
from .stat import stat


def bootstrap_statistics(
    series,
    statistic,
    n_samples=1000,
    confidence_interval=0.95,
    random_state=None,
):
    """
    Default parameters taken from
    R's Hmisc smean.cl.boot
    """
    if random_state is None:
        random_state = np.random

    alpha = 1 - confidence_interval
    size = (n_samples, len(series))
    inds = random_state.randint(0, len(series), size=size)
    samples = series.to_numpy()[inds]
    means = np.sort(statistic(samples, axis=1))
    return pd.DataFrame(
        {
            "ymin": means[int((alpha / 2) * n_samples)],
            "ymax": means[int((1 - alpha / 2) * n_samples)],
            "y": [statistic(series)],
        }
    )


def mean_cl_boot(
    series, n_samples=1000, confidence_interval=0.95, random_state=None
):
    """
    Bootstrapped mean with confidence interval

    Parameters
    ----------
    series : pandas.Series
        Values
    n_samples : int, default=1000
        Number of sample to draw.
    confidence_interval : float
        Confidence interval in the range (0, 1).
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    """
    return bootstrap_statistics(
        series,
        np.mean,
        n_samples=n_samples,
        confidence_interval=confidence_interval,
        random_state=random_state,
    )


def mean_cl_normal(series, confidence_interval=0.95):
    """
    Mean with confidence interval assuming normal distribution

    Credit: from http://stackoverflow.com/a/15034143

    Parameters
    ----------
    series : pandas.Series
        Values
    confidence_interval : float
        Confidence interval in the range (0, 1).
    """
    import scipy.stats as stats

    a = np.asarray(series)
    m = np.mean(a)
    se = stats.sem(a)
    h = se * stats.t._ppf((1 + confidence_interval) / 2, len(a) - 1)
    return pd.DataFrame({"y": [m], "ymin": m - h, "ymax": m + h})


def mean_sdl(series, mult=2):
    """
    Mean +/- a constant times the standard deviation

    Parameters
    ----------
    series : pandas.Series
        Values
    mult : float
        Multiplication factor.
    """
    m = series.mean()
    s = series.std()
    return pd.DataFrame({"y": [m], "ymin": m - mult * s, "ymax": m + mult * s})


def median_hilow(series, confidence_interval=0.95):
    """
    Median and a selected pair of outer quantiles having equal tail areas

    Parameters
    ----------
    series : pandas.Series
        Values
    confidence_interval : float
        Confidence interval in the range (0, 1).
    """
    tail = (1 - confidence_interval) / 2
    return pd.DataFrame(
        {
            "y": [np.median(series)],
            "ymin": np.percentile(series, 100 * tail),
            "ymax": np.percentile(series, 100 * (1 - tail)),
        }
    )


def mean_se(series, mult=1):
    """
    Calculate mean and standard errors on either side

    Parameters
    ----------
    series : pandas.Series
        Values
    mult : float
        Multiplication factor.
    """
    m = np.mean(series)
    se = mult * np.sqrt(np.var(series) / len(series))
    return pd.DataFrame({"y": [m], "ymin": m - se, "ymax": m + se})


function_dict = {
    "mean_cl_boot": mean_cl_boot,
    "mean_cl_normal": mean_cl_normal,
    "mean_sdl": mean_sdl,
    "median_hilow": median_hilow,
    "mean_se": mean_se,
}


def make_summary_fun(fun_data, fun_y, fun_ymin, fun_ymax, fun_args):
    """
    Make summary function
    """
    if isinstance(fun_data, str):
        fun_data = function_dict[fun_data]

    if any([fun_y, fun_ymin, fun_ymax]):

        def func(df) -> pd.DataFrame:
            d = {}
            if fun_y:
                kwargs = get_valid_kwargs(fun_y, fun_args)
                d["y"] = [fun_y(df["y"], **kwargs)]
            if fun_ymin:
                kwargs = get_valid_kwargs(fun_ymin, fun_args)
                d["ymin"] = [fun_ymin(df["y"], **kwargs)]
            if fun_ymax:
                kwargs = get_valid_kwargs(fun_ymax, fun_args)
                d["ymax"] = [fun_ymax(df["y"], **kwargs)]
            return pd.DataFrame(d)

    elif fun_data:
        kwargs = get_valid_kwargs(fun_data, fun_args)

        def func(df) -> pd.DataFrame:
            return fun_data(df["y"], **kwargs)

    else:
        raise ValueError(f"Bad value for function fun_data={fun_data}")

    return func


@document
class stat_summary(stat):
    """
    Calculate summary statistics depending on x

    {usage}

    Parameters
    ----------
    {common_parameters}
    fun_data : str | callable, default="mean_cl_boot"
        If string, it should be one of:

        ```python
        # Bootstrapped mean, confidence interval
        # Arguments:
        #     n_samples - No. of samples to draw
        #     confidence_interval
        #     random_state
        "mean_cl_boot"

        # Mean, C.I. assuming normal distribution
        # Arguments:
        #     confidence_interval
        "mean_cl_normal"

        # Mean, standard deviation * constant
        # Arguments:
        #     mult - multiplication factor
        "mean_sdl"

        # Median, outlier quantiles with equal tail areas
        # Arguments:
        #     confidence_interval
        "median_hilow"

        # Mean, Standard Errors * constant
        # Arguments:
        #     mult - multiplication factor
        "mean_se"
        ```

        or any function that takes a array and returns a dataframe
        with three columns named `y`, `ymin` and `ymax`.
    fun_y : callable, default=None
        Any function that takes a array_like and returns a value
    fun_ymin : callable, default=None
        Any function that takes an array_like and returns a value
    fun_ymax : callable, default=None
        Any function that takes an array_like and returns a value
    fun_args : dict, default=None
        Arguments to any of the functions. Provided the names of the
        arguments of the different functions are in not conflict, the
        arguments will be assigned to the right functions. If there is
        a conflict, create a wrapper function that resolves the
        ambiguity in the argument names.
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.

    Notes
    -----
    If any of `fun_y`, `fun_ymin` or `fun_ymax` are provided, the
    value of `fun_data` will be ignored.

    See Also
    --------
    plotnine.geom_pointrange : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "ymin"  # ymin computed by the summary function
    "ymax"  # ymax computed by the summary function
    "n"     # Number of observations at a position
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('ymin')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "pointrange",
        "fun_data": "mean_cl_boot",
        "fun_y": None,
        "fun_ymin": None,
        "fun_ymax": None,
        "fun_args": None,
        "random_state": None,
    }
    CREATES = {"ymin", "ymax", "n"}

    def setup_params(self, data):
        keys = ("fun_data", "fun_y", "fun_ymin", "fun_ymax")
        if not any(self.params[k] for k in keys):
            raise PlotnineError("No summary function")

        if self.params["fun_args"] is None:
            self.params["fun_args"] = {}

        if (
            "random_state" not in self.params["fun_args"]
            and self.params["random_state"]
        ):
            random_state = self.params["random_state"]
            if random_state is None:
                random_state = np.random
            elif isinstance(random_state, int):
                random_state = np.random.RandomState(random_state)

            self.params["fun_args"]["random_state"] = random_state

    def compute_panel(self, data, scales):
        func = make_summary_fun(
            self.params["fun_data"],
            self.params["fun_y"],
            self.params["fun_ymin"],
            self.params["fun_ymax"],
            self.params["fun_args"],
        )

        # break a dataframe into pieces, summarise each piece,
        # and join the pieces back together, retaining original
        # columns unaffected by the summary.
        summaries = []
        for (group, x), df in data.groupby(["group", "x"]):
            summary = func(df)
            summary["x"] = x  # pyright: ignore[reportCallIssue,reportArgumentType]
            summary["group"] = cast("int", group)
            summary["n"] = len(df)
            unique = uniquecols(df)
            if "y" in unique:
                unique = unique.drop("y", axis=1)
            merged = summary.merge(unique, on=["group", "x"])
            summaries.append(merged)

        new_data = pd.concat(summaries, axis=0, ignore_index=True)
        return new_data
</file>

<file path="plotnine/themes/theme_void.py">
from ..options import get_option
from .elements import (
    element_blank,
    element_line,
    element_text,
    margin,
    margin_auto,
)
from .theme import theme


class theme_void(theme):
    """
    A classic-looking theme, with x & y axis lines and
    no gridlines.

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family.
    """

    def __init__(self, base_size=11, base_family=None):
        base_family = base_family or get_option("base_family")
        m = get_option("base_margin")
        # Use only inherited elements and make everything blank
        theme.__init__(
            self,
            line=element_blank(),
            rect=element_blank(),
            text=element_text(
                family=base_family,
                style="normal",
                color="black",
                size=base_size,
                linespacing=1.2,
                rotation=0,
                margin=margin(),
            ),
            axis_text_x=element_blank(),
            axis_text_y=element_blank(),
            axis_title_x=element_blank(),
            axis_title_y=element_blank(),
            axis_ticks_length=0,
            aspect_ratio=get_option("aspect_ratio"),
            dpi=get_option("dpi"),
            figure_size=get_option("figure_size"),
            legend_box_margin=0,
            legend_box_spacing=m * 3,
            legend_key_spacing_x=6,
            legend_key_spacing_y=2,
            legend_frame=element_blank(),
            legend_key_size=base_size * 0.8 * 1.8,
            legend_ticks_length=0.2,
            legend_margin=0,
            legend_position="right",
            legend_spacing=10,
            legend_text=element_text(
                size=base_size * 0.8,
                margin=margin_auto(m / 1.5, unit="fig"),
            ),
            legend_ticks=element_line(color="#CCCCCC", size=1),
            legend_title=element_text(
                margin=margin(t=m, l=m * 2, b=m / 2, r=m * 2, unit="fig")
            ),
            panel_spacing=m,
            plot_caption=element_text(
                size=base_size * 0.8,
                ha="right",
                va="bottom",
                ma="left",
                margin=margin(t=m, unit="fig"),
            ),
            plot_footer=element_text(
                size=base_size * 0.8,
                ha="left",
                va="bottom",
                ma="left",
                margin=margin(t=1 / 3, b=1 / 3, unit="lines"),
            ),
            plot_margin=0,
            plot_subtitle=element_text(
                size=base_size * 1,
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_title=element_text(
                size=base_size * 1.2,
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_tag=element_text(
                size=base_size * 1.2,
                va="center",
                ha="center",
            ),
            plot_title_position="panel",
            plot_caption_position="panel",
            plot_footer_position="plot",
            plot_tag_location="margin",
            plot_tag_position="topleft",
            strip_align=0,
            strip_text=element_text(size=base_size * 0.8),
            complete=True,
        )
</file>

<file path="plotnine/stats/stat_density_2d.py">
from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from .density import get_var_type, kde
from .stat import stat

if TYPE_CHECKING:
    from plotnine.typing import FloatArrayLike


@document
class stat_density_2d(stat):
    """
    Compute 2D kernel density estimation

    {usage}

    Parameters
    ----------
    {common_parameters}
    contour : bool, default=True
        Whether to create contours of the 2d density estimate.
    n : int, default=64
        Number of equally spaced points at which the density is to
        be estimated. For efficient computation, it should be a power
        of two.
    levels : int | array_like, default=5
        Contour levels. If an integer, it specifies the maximum number
        of levels, if array_like it is the levels themselves.
    package : Literal["statsmodels", "scipy", "sklearn"], default="statsmodels"
        Package whose kernel density estimation to use.
    kde_params : dict
        Keyword arguments to pass on to the kde class.

    See Also
    --------
    plotnine.geom_density_2d : The default `geom` for this `stat`.
    statsmodels.nonparametric.kernel_density.KDEMultivariate
    scipy.stats.gaussian_kde
    sklearn.neighbors.KernelDensity
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "level"     # density level of a contour
    "density"   # Computed density at a point
    "piece"     # Numeric id of a contour in a given group
    ```

    `level` is only relevant when contours are computed. `density`
    is available only when no contours are computed. `piece` is
    largely irrelevant.
    """
    REQUIRED_AES = {"x"}
    DEFAULT_PARAMS = {
        "geom": "density_2d",
        "contour": True,
        "package": "statsmodels",
        "kde_params": None,
        "n": 64,
        "levels": 5,
    }
    CREATES = {"y"}

    def setup_params(self, data):
        params = self.params
        if params["kde_params"] is None:
            params["kde_params"] = {}

        kde_params = params["kde_params"]
        if params["package"] == "statsmodels":
            params["package"] = "statsmodels-m"
            if "var_type" not in kde_params:
                x_type = get_var_type(data["x"])
                y_type = get_var_type(data["y"])
                kde_params["var_type"] = f"{x_type}{y_type}"

    def compute_group(self, data, scales):
        params = self.params
        package = params["package"]
        kde_params = params["kde_params"]

        group = data["group"].iloc[0]
        range_x = scales.x.dimension()
        range_y = scales.y.dimension()
        _x = np.linspace(range_x[0], range_x[1], params["n"])
        _y = np.linspace(range_y[0], range_y[1], params["n"])

        # The grid must have a "similar" shape (n, p) to the var_data
        X, Y = np.meshgrid(_x, _y)
        x = cast("FloatArrayLike", data["x"].to_numpy())
        y = cast("FloatArrayLike", data["y"].to_numpy())
        var_data = np.array([x, y]).T
        grid = np.array([X.flatten(), Y.flatten()]).T
        density = kde(var_data, grid, package, **kde_params)

        if params["contour"]:
            Z = density.reshape(len(_x), len(_y))
            data = contour_lines(X, Y, Z, params["levels"])
            # Each piece should have a distinct group
            groups = str(group) + "-00" + data["piece"].astype(str)
            data["group"] = groups
        else:
            data = pd.DataFrame(
                {
                    "x": X.flatten(),
                    "y": Y.flatten(),
                    "density": density.flatten(),
                    "group": group,
                    "level": 1,
                    "piece": 1,
                }
            )

        return data


def contour_lines(X, Y, Z, levels: int | FloatArrayLike):
    """
    Calculate contour lines
    """
    from contourpy import contour_generator

    # Preparation of values and the creating of contours is
    # adapted from MPL with some adjustments.
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Z = np.asarray(Z, dtype=np.float64)
    zmin, zmax = Z.min(), Z.max()
    cgen = contour_generator(
        X, Y, Z, name="mpl2014", corner_mask=False, chunk_size=0
    )

    if isinstance(levels, int):
        from mizani.breaks import breaks_extended

        levels = breaks_extended(n=levels)((zmin, zmax))

    # The counter_generator gives us a list of vertices that
    # represent all the contour lines at that level. There
    # may be 0, 1 or more vertices at a level. Each one of
    # these we call a piece, and it represented as an nx2 array.
    #
    # We want x-y values that describe *all* the contour lines
    # in tidy format. Therefore each x-y vertex has a
    # corresponding level and piece id.
    segments = []
    piece_ids = []
    level_values = []
    start_pid = 1
    for level in levels:
        vertices, *_ = cgen.create_contour(level)
        for pid, piece in enumerate(vertices, start=start_pid):
            n = len(piece)  # pyright: ignore
            segments.append(piece)
            piece_ids.append(np.repeat(pid, n))
            level_values.append(np.repeat(level, n))
            start_pid = pid + 1

    # Collapse the info and make it fit for dataframe columns
    if segments:
        x, y = np.vstack(segments).T
        piece = np.hstack(piece_ids)
        level = np.hstack(level_values)
    else:
        x, y = [], []
        piece = []
        level = []

    data = pd.DataFrame(
        {
            "x": x,
            "y": y,
            "level": level,
            "piece": piece,
        }
    )
    return data
</file>

<file path="plotnine/stats/stat_qq.py">
from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from ..doctools import document
from ..exceptions import PlotnineError
from ..mapping.evaluation import after_stat
from .stat import stat

if TYPE_CHECKING:
    from typing import Any

    from plotnine.typing import FloatArray, FloatArrayLike


# Note: distribution should be a name from scipy.stat.distribution
@document
class stat_qq(stat):
    """
    Calculation for quantile-quantile plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    distribution : str, default="norm"
        Distribution or distribution function name. The default is
        *norm* for a normal probability plot. Objects that look enough
        like a stats.distributions instance (i.e. they have a ppf
        method) are also accepted. See [scipy stats](`scipy.stats`)
        for available distributions.
    dparams : dict, default=None
        Distribution-specific shape parameters (shape parameters plus
        location and scale).
    quantiles : array_like, default=None
        Probability points at which to calculate the theoretical
        quantile values. If provided, must be the same number as
        as the sample data points. The default is to use calculated
        theoretical points, use to `alpha_beta` control how
        these points are generated.
    alpha_beta : tuple, default=(3/8, 3/8)
        Parameter values to use when calculating the quantiles.

    See Also
    --------
    plotnine.geom_qq : The default `geom` for this `stat`.
    scipy.stats.mstats.plotting_positions : Uses `alpha_beta`
        to calculate the quantiles.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    'theoretical'  # theoretical quantiles
    'sample'       # sample quantiles
    ```

    """
    REQUIRED_AES = {"sample"}
    DEFAULT_AES = {"x": after_stat("theoretical"), "y": after_stat("sample")}
    DEFAULT_PARAMS = {
        "geom": "qq",
        "distribution": "norm",
        "dparams": {},
        "quantiles": None,
        "alpha_beta": (3 / 8, 3 / 8),
    }

    def compute_group(self, data, scales):
        sample = cast("FloatArray", data["sample"].sort_values().to_numpy())
        theoretical = theoretical_qq(
            sample,
            self.params["distribution"],
            alpha=self.params["alpha_beta"][0],
            beta=self.params["alpha_beta"][1],
            quantiles=self.params["quantiles"],
            distribution_params=self.params["dparams"],
        )
        return pd.DataFrame({"sample": sample, "theoretical": theoretical})


def theoretical_qq(
    x: FloatArray,
    distribution: str,
    alpha: float,
    beta: float,
    quantiles: FloatArrayLike | None,
    distribution_params: dict[str, Any],
) -> FloatArray:
    """
    Caculate theoretical qq distribution
    """
    from scipy.stats.mstats import plotting_positions

    from .distributions import get_continuous_distribution

    if quantiles is None:
        quantiles = plotting_positions(x, alpha, beta)
    elif len(quantiles) != len(x):
        raise PlotnineError(
            "The number of quantile values is not the same as "
            "the number of sample values."
        )

    cdist = get_continuous_distribution(distribution)
    return cdist.ppf(np.asarray(quantiles), **distribution_params)
</file>

<file path="plotnine/themes/targets.py">
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from matplotlib.collections import LineCollection
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    from matplotlib.text import Text

    from plotnine._mpl.offsetbox import ColoredDrawingArea
    from plotnine._mpl.patches import StripTextPatch
    from plotnine._mpl.text import StripText
    from plotnine.iapi import legend_artists


@dataclass
class ThemeTargets:
    """
    Artists that will be themed

    This includes only artist that cannot be easily accessed from
    the figure or the axes.
    """

    axis_title_x: Optional[Text] = None
    axis_title_y: Optional[Text] = None
    legend_frame: Optional[Rectangle] = None
    legend_key: list[ColoredDrawingArea] = field(default_factory=list)
    legends: Optional[legend_artists] = None
    legend_text_colorbar: list[Text] = field(default_factory=list)
    legend_text_legend: list[Text] = field(default_factory=list)
    legend_ticks: Optional[LineCollection] = None
    legend_title: Optional[Text] = None
    panel_border: list[Rectangle] = field(default_factory=list)
    plot_caption: Optional[Text] = None
    plot_subtitle: Optional[Text] = None
    plot_footer: Optional[Text] = None
    plot_tag: Optional[Text] = None
    plot_title: Optional[Text] = None
    plot_background: Optional[Rectangle] = None
    plot_footer_background: Optional[Rectangle] = None
    plot_footer_line: Optional[Line2D] = None
    strip_background_x: list[StripTextPatch] = field(default_factory=list)
    strip_background_y: list[StripTextPatch] = field(default_factory=list)
    strip_text_x: list[StripText] = field(default_factory=list)
    strip_text_y: list[StripText] = field(default_factory=list)
</file>

<file path="plotnine/themes/theme_matplotlib.py">
from ..options import get_option
from .elements import (
    element_blank,
    element_line,
    element_rect,
    element_text,
    margin,
    margin_auto,
)
from .theme import theme


class theme_matplotlib(theme):
    """
    The default matplotlib look and feel.

    The theme can be used (and has the same parameter
    to customize) like a [](`matplotlib.rc_context`) manager.

    Parameters
    ----------
    rc : dict
        rcParams which should be applied on top of mathplotlib default.
    fname : str
        Filename to a matplotlibrc file
    use_defaults : bool
        If `True` (the default) resets the plot setting
        to the (current) `matplotlib.rcParams` values
    """

    def __init__(self, rc=None, fname=None, use_defaults=True):
        import matplotlib as mpl

        m = get_option("base_margin")
        base_size = mpl.rcParams.get("font.size", 11)
        linewidth = mpl.rcParams.get("grid.linewidth", 0.8)
        half_line = base_size / 2

        super().__init__(
            line=element_line(size=linewidth),
            rect=element_rect(size=linewidth),
            text=element_text(
                size=base_size,
                linespacing=1,
                rotation=0,
                margin={},
            ),
            aspect_ratio=get_option("aspect_ratio"),
            axis_text=element_text(margin=margin(t=2.4, r=2.4, unit="pt")),
            axis_title_x=element_text(
                va="bottom", ha="center", margin=margin(t=m, unit="fig")
            ),
            axis_line=element_blank(),
            axis_title_y=element_text(
                angle=90,
                va="center",
                ha="left",
                margin=margin(r=m, unit="fig"),
            ),
            dpi=get_option("dpi"),
            figure_size=get_option("figure_size"),
            legend_background=element_rect(color="none"),
            legend_box_margin=0,
            legend_box_spacing=m * 3,
            legend_key_spacing_x=6,
            legend_key_spacing_y=2,
            legend_frame=element_rect(color="black"),
            legend_key_size=16,
            legend_ticks_length=0.2,
            legend_margin=0,
            legend_position="right",
            legend_spacing=10,
            legend_text=element_text(margin=margin_auto(m / 2, unit="fig")),
            legend_ticks=element_line(color="black"),
            legend_title=element_text(
                ha="left",
                margin=margin(t=m, l=m * 2, b=m / 2, r=m * 2, unit="fig"),
            ),
            panel_border=element_rect(color="black"),
            panel_grid=element_blank(),
            panel_spacing=m,
            plot_caption=element_text(
                ha="right",
                va="bottom",
                ma="left",
                margin=margin(t=m, unit="fig"),
            ),
            plot_footer=element_text(
                ha="left",
                va="bottom",
                ma="left",
                margin=margin(t=1 / 3, b=1 / 3, unit="lines"),
            ),
            plot_margin=m,
            plot_subtitle=element_text(
                size=base_size * 0.9,
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_footer_background=element_blank(),
            plot_footer_line=element_blank(),
            plot_title=element_text(
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_tag=element_text(
                size=base_size * 1.2,
                va="center",
                ha="center",
            ),
            plot_title_position="panel",
            plot_caption_position="panel",
            plot_footer_position="plot",
            plot_tag_location="margin",
            plot_tag_position="topleft",
            strip_align=0,
            strip_background=element_rect(
                fill="#D9D9D9", color="black", size=linewidth
            ),
            strip_text=element_text(
                linespacing=1.5,
                margin=margin_auto(half_line * 0.8),
            ),
            strip_text_y=element_text(rotation=-90),
            complete=True,
        )

        if use_defaults:
            _copy = mpl.rcParams.copy()
            if "tk.pythoninspect" in _copy:
                del _copy["tk.pythoninspect"]
            self._rcParams.update(_copy)

        if fname:
            self._rcParams.update(mpl.rc_params_from_file(fname))
        if rc:
            self._rcParams.update(rc)
</file>

<file path="plotnine/themes/theme_seaborn.py">
from ..options import get_option
from .elements import (
    element_blank,
    element_line,
    element_rect,
    element_text,
    margin,
    margin_auto,
)
from .theme import theme


class theme_seaborn(theme):
    """
    Theme for seaborn.

    Credit to Michael Waskom's seaborn:

        - http://stanford.edu/~mwaskom/software/seaborn
        - https://github.com/mwaskom/seaborn

    Parameters
    ----------
    style: "white", "dark", "whitegrid", "darkgrid",  "ticks"
        Style of axis background.
    context: "notebook", "talk", "paper", "poster"]``
        Intended context for resulting figures.
    font : str
        Font family, see matplotlib font manager.
    font_scale : float
        Separate scaling factor to independently scale the
        size of the font elements.
    """

    def __init__(
        self,
        style="darkgrid",
        context="notebook",
        font="sans-serif",
        font_scale=1,
    ):
        from .seaborn_rcmod import set_theme

        rcparams = set_theme(
            context=context, style=style, font=font, font_scale=font_scale
        )
        base_size = rcparams["font.size"]
        half_line = base_size / 2
        line_margin = half_line * 0.8 / 2
        m = get_option("base_margin")

        super().__init__(
            aspect_ratio=get_option("aspect_ratio"),
            dpi=get_option("dpi"),
            figure_size=get_option("figure_size"),
            text=element_text(size=base_size, rotation=0, margin={}),
            axis_text=element_text(
                size=base_size * 0.8,
                margin=margin(
                    t=line_margin,
                    b=line_margin,
                    l=line_margin,
                    r=line_margin,
                    unit="pt",
                ),
            ),
            axis_title_x=element_text(
                va="bottom", ha="center", margin=margin(t=m, unit="fig")
            ),
            axis_title_y=element_text(
                angle=90,
                va="center",
                ha="left",
                margin=margin(r=m, unit="fig"),
            ),
            legend_box_margin=0,
            legend_box_spacing=m * 3,  # figure units
            legend_key_spacing_x=6,
            legend_key_spacing_y=2,
            legend_key_size=base_size * 0.8 * 1.8,
            legend_frame=element_blank(),
            legend_ticks_length=0.2,
            legend_margin=0,
            legend_position="right",
            legend_spacing=10,  # points
            legend_text=element_text(
                size=base_size * 0.8,
                margin=margin_auto(m / 1.5, unit="fig"),
            ),
            legend_ticks=element_line(color="#CCCCCC", size=1),
            legend_title=element_text(
                margin=margin(t=m, l=m * 2, b=m / 2, r=m * 2, unit="fig")
            ),
            panel_spacing=m,
            panel_background=element_rect(fill=rcparams["axes.facecolor"]),
            plot_caption=element_text(
                size=base_size * 0.8,
                ha="right",
                va="bottom",
                ma="left",
                margin=margin(t=m, unit="fig"),
            ),
            plot_footer=element_text(
                size=base_size * 0.8,
                ha="left",
                va="bottom",
                ma="left",
                margin=margin(t=1 / 3, b=1 / 3, unit="lines"),
            ),
            plot_footer_background=element_blank(),
            plot_footer_line=element_blank(),
            plot_margin=m,
            plot_subtitle=element_text(
                size=base_size * 1,
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_title=element_text(
                size=base_size * 1.2,
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_tag=element_text(
                size=base_size * 1.2,
                va="center",
                ha="center",
            ),
            plot_title_position="panel",
            plot_caption_position="panel",
            plot_footer_position="plot",
            plot_tag_location="margin",
            plot_tag_position="topleft",
            strip_align=0,
            strip_background=element_rect(color="none", fill="#D1CDDF"),
            strip_text=element_text(
                size=base_size * 0.8,
                linespacing=1.5,
                margin=margin_auto(half_line * 0.8),
            ),
            strip_text_y=element_text(rotation=-90),
            complete=True,
        )

        self._rcParams.update(rcparams)
</file>

<file path="plotnine/geoms/geom_path.py">
from __future__ import annotations

from collections import Counter
from contextlib import suppress
from typing import TYPE_CHECKING
from warnings import warn

import numpy as np

from .._utils import SIZE_FACTOR, make_line_segments, match, to_rgba
from ..doctools import document
from ..exceptions import PlotnineWarning
from .geom import geom

if TYPE_CHECKING:
    from typing import Any, Literal, Sequence

    import numpy.typing as npt
    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea
    from matplotlib.path import Path

    from plotnine.coords.coord import coord
    from plotnine.iapi import panel_view
    from plotnine.layer import layer
    from plotnine.typing import BoolArray


@document
class geom_path(geom):
    """
    Connected points

    {usage}

    Parameters
    ----------
    {common_parameters}
    lineend : Literal["butt", "round", "projecting"], default="butt"
        Line end style. This option is applied for solid linetypes.
    linejoin : Literal["round", "miter", "bevel"], default="round"
        Line join style. This option is applied for solid linetypes.
    arrow : ~plotnine.geoms.geom_path.arrow, default=None
        Arrow specification. Default is no arrow.

    See Also
    --------
    plotnine.arrow : for adding arrowhead(s) to paths.
    """

    DEFAULT_AES = {
        "alpha": 1,
        "color": "black",
        "linetype": "solid",
        "size": 0.5,
    }

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "lineend": "butt",
        "linejoin": "round",
        "arrow": None,
    }

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        def keep(x: Sequence[float]) -> BoolArray:
            # first non-missing to last non-missing
            first = match([False], x, nomatch=1, start=0)[0]
            last = len(x) - match([False], x[::-1], nomatch=1, start=0)[0]
            bool_idx = np.hstack(
                [
                    np.repeat(False, first),
                    np.repeat(True, last - first),
                    np.repeat(False, len(x) - last),
                ]
            )
            return bool_idx

        # Get indices where any row for the select aesthetics has
        # NaNs at the beginning or the end. Those we drop
        bool_idx = (
            data[["x", "y", "size", "color", "linetype"]]
            .isna()  # Missing
            .apply(keep, axis=0)
        )  # Beginning or the End
        bool_idx = np.all(bool_idx, axis=1)  # Across the aesthetics

        # return data
        n1 = len(data)
        data = data.loc[bool_idx]
        data.reset_index(drop=True, inplace=True)
        n2 = len(data)

        if n2 != n1 and not self.params["na_rm"]:
            geom = self.__class__.__name__
            msg = f"{geom}: Removed {n1 - n2} rows containing missing values."
            warn(msg, PlotnineWarning)

        return data

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        if not any(data["group"].duplicated()):
            geom = self.__class__.__name__
            warn(
                f"{geom}: Each group consist of only one "
                "observation. Do you need to adjust the "
                "group aesthetic?",
                PlotnineWarning,
            )

        # drop lines with less than two points
        c = Counter(data["group"])
        counts = np.array([c[v] for v in data["group"]])
        data = data[counts >= 2]

        if len(data) < 2:
            return

        # dataframe mergesort is stable, we rely on that here
        data = data.sort_values("group", kind="mergesort")
        data.reset_index(drop=True, inplace=True)

        # When the parameters of the path are not constant
        # with in the group, then the lines that make the paths
        # can be drawn as separate segments
        cols = {"color", "size", "linetype", "alpha", "group"}
        cols = cols & set(data.columns)
        num_unique_rows = len(data.drop_duplicates(cols))
        ngroup = len(np.unique(data["group"].to_numpy()))

        constant = num_unique_rows == ngroup
        self.params["constant"] = constant

        if not constant:
            self.draw_group(data, panel_params, coord, ax, self.params)
        else:
            for _, gdata in data.groupby("group"):
                gdata.reset_index(inplace=True, drop=True)
                self.draw_group(gdata, panel_params, coord, ax, self.params)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        data = coord.transform(data, panel_params, munch=True)
        data["linewidth"] = data["size"] * SIZE_FACTOR

        if "constant" in params:
            constant: bool = params.pop("constant")
        else:
            constant = len(np.unique(data["group"].to_numpy())) == 1

        if not constant:
            _draw_segments(data, ax, params)
        else:
            _draw_lines(data, ax, params)

        if "arrow" in params and params["arrow"]:
            params["arrow"].draw(
                data, panel_params, coord, ax, params, constant=constant
            )

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a horizontal line in the box

        Parameters
        ----------
        data : Series
            Data Row
        da : DrawingArea
            Canvas
        lyr : layer
            Layer

        Returns
        -------
        out : DrawingArea
        """
        from matplotlib.lines import Line2D

        linewidth = data["size"] * SIZE_FACTOR
        x = [0, da.width]
        y = [0.5 * da.height] * 2
        color = to_rgba(data["color"], data["alpha"])

        key = Line2D(
            x,
            y,
            linestyle=data["linetype"],
            linewidth=linewidth,
            color=color,
            solid_capstyle="butt",
            antialiased=False,
        )
        da.add_artist(key)
        return da

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        w, h = min_size
        pad_w, pad_h = w * 0.5, h * 0.5
        _w = _h = data.get("size", 0) * SIZE_FACTOR
        if data["color"] is not None:
            w = max(w, _w + pad_w)
            h = max(h, _h + pad_h)
        return w, h


class arrow:
    """
    Define arrow (actually an arrowhead)

    This is used to define arrow heads for
    [](`~plotnine.geoms.geom_path`).

    Parameters
    ----------
    angle :
        angle in degrees between the tail a
        single edge.
    length :
        of the edge in "inches"
    ends :
        At which end of the line to draw the
        arrowhead
    type :
        When it is closed, it is also filled
    """

    def __init__(
        self,
        angle: float = 30,
        length: float = 0.2,
        ends: Literal["first", "last", "both"] = "last",
        type: Literal["open", "closed"] = "open",
    ):
        self.angle = angle
        self.length = length
        self.ends = ends
        self.type = type

    def draw(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
        constant: bool = True,
    ):
        """
        Draw arrows at the end(s) of the lines

        Parameters
        ----------
        data : dataframe
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params : panel_view
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Attributes are of interest
            to the geom are:

            ```python
            "panel_params.x.range"  # tuple
            "panel_params.y.range"  # tuple
            ```
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the
            geom.
        ax : axes
            Axes on which to plot.
        constant: bool
            If the path attributes vary along the way. If false,
            the arrows are per segment of the path
        params : dict
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        first = self.ends in ("first", "both")
        last = self.ends in ("last", "both")

        data = data.sort_values("group", kind="mergesort")
        data["color"] = to_rgba(data["color"], data["alpha"])  # pyright: ignore[reportCallIssue,reportArgumentType]

        if self.type == "open":
            data["facecolor"] = "none"
        else:
            data["facecolor"] = data["color"]

        if not constant:
            from matplotlib.collections import PathCollection

            # Get segments/points (x1, y1) -> (x2, y2)
            # for which to calculate the arrow heads
            idx1: list[int] = []
            idx2: list[int] = []
            for _, df in data.groupby("group"):
                idx1.extend(df.index[:-1].to_list())
                idx2.extend(df.index[1:].to_list())

            d = {
                "zorder": params["zorder"],
                "rasterized": params["raster"],
                "edgecolor": data.loc[idx1, "color"],
                "facecolor": data.loc[idx1, "facecolor"],
                "linewidth": data.loc[idx1, "linewidth"],
                "linestyle": data.loc[idx1, "linetype"],
            }

            x1 = data.loc[idx1, "x"].to_numpy()
            y1 = data.loc[idx1, "y"].to_numpy()
            x2 = data.loc[idx2, "x"].to_numpy()
            y2 = data.loc[idx2, "y"].to_numpy()

            if first:
                paths = self.get_paths(x1, y1, x2, y2, panel_params, coord, ax)
                coll = PathCollection(paths, **d)
                ax.add_collection(coll)
            if last:
                x1, y1, x2, y2 = x2, y2, x1, y1
                paths = self.get_paths(x1, y1, x2, y2, panel_params, coord, ax)
                coll = PathCollection(paths, **d)
                ax.add_collection(coll)
        else:
            from matplotlib.patches import PathPatch

            d = {
                "zorder": params["zorder"],
                "rasterized": params["raster"],
                "edgecolor": data["color"].iloc[0],
                "facecolor": data["facecolor"].iloc[0],
                "linewidth": data["linewidth"].iloc[0],
                "linestyle": data["linetype"].iloc[0],
                "joinstyle": "round",
                "capstyle": "butt",
            }

            if first:
                x1, x2 = data["x"].iloc[0:2]
                y1, y2 = data["y"].iloc[0:2]
                x1, y1, x2, y2 = (np.array([i]) for i in (x1, y1, x2, y2))
                paths = self.get_paths(x1, y1, x2, y2, panel_params, coord, ax)
                patch = PathPatch(paths[0], **d)
                ax.add_artist(patch)

            if last:
                x1, x2 = data["x"].iloc[-2:]
                y1, y2 = data["y"].iloc[-2:]
                x1, y1, x2, y2 = x2, y2, x1, y1
                x1, y1, x2, y2 = (np.array([i]) for i in (x1, y1, x2, y2))
                paths = self.get_paths(x1, y1, x2, y2, panel_params, coord, ax)
                patch = PathPatch(paths[0], **d)
                ax.add_artist(patch)

    def get_paths(
        self,
        x1: npt.ArrayLike,
        y1: npt.ArrayLike,
        x2: npt.ArrayLike,
        y2: npt.ArrayLike,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ) -> list[Path]:
        """
        Compute paths that create the arrow heads

        Parameters
        ----------
        x1, y1, x2, y2 : array_like
            List of points that define the tails of the arrows.
            The arrow heads will be at x1, y1. If you need them
            at x2, y2 reverse the input.
        panel_params : panel_view
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Attributes are of interest
            to the geom are:

            ```python
            "panel_params.x.range"  # tuple
            "panel_params.y.range"  # tuple
            ```
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the geom.
        ax : axes
            Axes on which to plot.

        Returns
        -------
        out : list of Path
            Paths that create arrow heads
        """
        from matplotlib.path import Path

        # The arrowhead path has 3 vertices,
        # plus a dummy vertex for the STOP code
        dummy = (0, 0)

        # codes list remains the same after initialization
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.STOP]

        # We need the axes dimensions so that we can
        # compute scaling factors
        width, height = _axes_get_size_inches(ax)
        width_ = np.ptp(panel_params.x.range)
        height_ = np.ptp(panel_params.y.range)

        # scaling factors to prevent skewed arrowheads
        lx = self.length * width_ / width
        ly = self.length * height_ / height

        # angle in radians
        a = self.angle * np.pi / 180

        # direction of arrow head
        xdiff, ydiff = x2 - x1, y2 - y1  # type: ignore
        rotations = np.arctan2(ydiff / ly, xdiff / lx)

        # Arrow head vertices
        v1x = x1 + lx * np.cos(rotations + a)
        v1y = y1 + ly * np.sin(rotations + a)
        v2x = x1 + lx * np.cos(rotations - a)
        v2y = y1 + ly * np.sin(rotations - a)

        # create a path for each arrow head
        paths = []
        for t in zip(v1x, v1y, x1, y1, v2x, v2y):  # type: ignore
            verts = [t[:2], t[2:4], t[4:], dummy]
            paths.append(Path(verts, codes))

        return paths


def _draw_segments(data: pd.DataFrame, ax: Axes, params: dict[str, Any]):
    """
    Draw independent line segments between all the
    points
    """
    from matplotlib.collections import LineCollection

    color = to_rgba(data["color"], data["alpha"])
    # All we do is line-up all the points in a group
    # into segments, all in a single list.
    # Along the way the other parameters are put in
    # sequences accordingly
    indices: list[int] = []  # for attributes of starting point of each segment
    _segments = []
    for _, df in data.groupby("group"):
        idx = df.index
        indices.extend(idx[:-1].to_list())  # One line from two points
        x = data["x"].iloc[idx]
        y = data["y"].iloc[idx]
        _segments.append(make_line_segments(x, y, ispath=True))

    segments = np.vstack(_segments).tolist()

    edgecolor = color if color is None else [color[i] for i in indices]
    linewidth = data.loc[indices, "linewidth"]
    linestyle = data.loc[indices, "linetype"]

    coll = LineCollection(
        segments,
        edgecolor=edgecolor,
        linewidth=linewidth,
        linestyle=linestyle,
        capstyle=params.get("lineend"),
        zorder=params["zorder"],
        rasterized=params["raster"],
    )
    ax.add_collection(coll)


def _draw_lines(data: pd.DataFrame, ax: Axes, params: dict[str, Any]):
    """
    Draw a path with the same characteristics from the
    first point to the last point
    """
    from matplotlib.lines import Line2D

    color = to_rgba(data["color"].iloc[0], data["alpha"].iloc[0])
    join_style = _get_joinstyle(data, params)
    lines = Line2D(
        data["x"],
        data["y"],
        color=color,
        linewidth=data["linewidth"].iloc[0],
        linestyle=data["linetype"].iloc[0],
        zorder=params["zorder"],
        rasterized=params["raster"],
        **join_style,
    )
    ax.add_artist(lines)


def _get_joinstyle(
    data: pd.DataFrame, params: dict[str, Any]
) -> dict[str, Any]:
    with suppress(KeyError):
        if params["linejoin"] == "mitre":
            params["linejoin"] = "miter"

    with suppress(KeyError):
        if params["lineend"] == "square":
            params["lineend"] = "projecting"

    joinstyle = params.get("linejoin", "miter")
    capstyle = params.get("lineend", "butt")
    d = {}
    if data["linetype"].iloc[0] == "solid":
        d["solid_joinstyle"] = joinstyle
        d["solid_capstyle"] = capstyle
    elif data["linetype"].iloc[0] == "dashed":
        d["dash_joinstyle"] = joinstyle
        d["dash_capstyle"] = capstyle
    return d


def _axes_get_size_inches(ax: Axes) -> tuple[float, float]:
    """
    Size of axes in inches

    Parameters
    ----------
    ax : axes
        Axes

    Returns
    -------
    out : tuple[float, float]
        (width, height) of ax in inches
    """
    fig = ax.get_figure()
    bbox = ax.get_window_extent().transformed(
        fig.dpi_scale_trans.inverted()  # pyright: ignore
    )
    return bbox.width, bbox.height
</file>

<file path="plotnine/stats/stat_sina.py">
from typing import TYPE_CHECKING, cast

import numpy as np
import pandas as pd

from .._utils import array_kind, jitter, nextafter_range, resolution
from ..doctools import document
from ..exceptions import PlotnineError
from ..mapping.aes import has_groups
from .binning import breaks_from_bins, breaks_from_binwidth
from .stat import stat
from .stat_density import compute_density

if TYPE_CHECKING:
    from plotnine.typing import FloatArray, IntArray


@document
class stat_sina(stat):
    """
    Compute Sina plot values

    {usage}

    Parameters
    ----------
    {common_parameters}
    binwidth : float, default=None
        The width of the bins. The default is to use bins that
        cover the range of the data. You should always override this
        value, exploring multiple widths to find the best to
        illustrate the stories in your data.
    bins : int, default=50
        Number of bins. Overridden by binwidth.
    method : Literal["density", "counts"], default="density"
        Choose the method to spread the samples within the same bin
        along the x-axis. Available methods: "density", "counts"
        (can be abbreviated, e.g. "d"). See Details.
    maxwidth : float, default=None
        Control the maximum width the points can spread into.
        Values should be in the range (0, 1).
    adjust : float, default=1
        Adjusts the bandwidth of the density kernel when
        `method="density"`. see [](`~plotnine.stats.stat_density`).
    bw : str | float, default="nrd0"
        The bandwidth to use, If a float is given, it is the bandwidth.
        The `str`{.py} choices are:
        `"nrd0", "normal_reference", "scott", "silverman"`{.py}

        `nrd0` is a port of `stats::bw.nrd0` in R; it is eqiuvalent
        to `silverman` when there is more than 1 value in a group.
    bin_limit : int, default=1
        If the samples within the same y-axis bin are more
        than `bin_limit`, the samples's X coordinates will be adjusted.
        This parameter is effective only when `method="counts"`{.py}
    random_state : int | ~numpy.random.RandomState, default=None
        Seed or Random number generator to use. If `None`, then
        numpy global generator [](`numpy.random`) is used.
    scale : Literal["area", "count", "width"], default="area"
        How to scale the sina groups.

        - `area` - Scale by the largest density/bin among the different sinas
        - `count` - areas are scaled proportionally to the number of points
        - `width` - Only scale according to the maxwidth parameter.
    style :
        Type of sina plot to draw. The options are
        ```python
        'full'        # Regular (2 sided)
        'left'        # Left-sided half
        'right'       # Right-sided half
        'left-right'  # Alternate (left first) half by the group
        'right-left'  # Alternate (right first) half by the group
        ```

    See Also
    --------
    plotnine.geom_sina : The default `geom` for this `stat`.
    """

    _aesthetics_doc = """
    {aesthetics_table}

    **Options for computed aesthetics**

    ```python
    "quantile"  # quantile
    "group"     # group identifier
    ```

    Calculated aesthetics are accessed using the `after_stat` function.
    e.g. `after_stat('quantile')`{.py}.
    """

    REQUIRED_AES = {"x", "y"}
    DEFAULT_PARAMS = {
        "geom": "sina",
        "position": "dodge",
        "binwidth": None,
        "bins": None,
        "method": "density",
        "bw": "nrd0",
        "maxwidth": None,
        "adjust": 1,
        "bin_limit": 1,
        "random_state": None,
        "scale": "area",
        "style": "full",
    }
    CREATES = {"scaled"}

    def setup_data(self, data):
        if (
            array_kind.continuous(data["x"])
            and not has_groups(data)
            and (data["x"] != data["x"].iloc[0]).any()
        ):
            raise TypeError(
                "Continuous x aesthetic -- did you forget aes(group=...)?"
            )
        return data

    def setup_params(self, data):
        params = self.params
        random_state = params["random_state"]

        if params["maxwidth"] is None:
            params["maxwidth"] = resolution(data["x"], False) * 0.9

        if params["binwidth"] is None and self.params["bins"] is None:
            params["bins"] = 50

        if random_state is None:
            params["random_state"] = np.random
        elif isinstance(random_state, int):
            params["random_state"] = np.random.RandomState(random_state)

        # Required by compute_density
        params["kernel"] = "gau"  # It has to be a gaussian kernel
        params["cut"] = 0
        params["gridsize"] = None
        params["clip"] = (-np.inf, np.inf)
        params["bounds"] = (-np.inf, np.inf)
        params["n"] = 512

    def compute_panel(self, data, scales):
        params = self.params
        maxwidth = params["maxwidth"]
        random_state = params["random_state"]
        data = super().compute_panel(data, scales)

        if not len(data):
            return data

        if params["scale"] == "area":
            data["sinawidth"] = data["density"] / data["density"].max()
        elif params["scale"] == "count":
            data["sinawidth"] = (
                data["density"]
                / data["density"].max()
                * data["n"]
                / data["n"].max()
            )
        elif params["scale"] == "width":
            data["sinawidth"] = data["scaled"]
        else:
            msg = "Unknown scale value '{}'"
            raise PlotnineError(msg.format(params["scale"]))

        is_infinite = ~np.isfinite(data["sinawidth"])
        if is_infinite.any():
            data.loc[is_infinite, "sinawidth"] = 0

        data["xmin"] = data["x"] - maxwidth / 2
        data["xmax"] = data["x"] + maxwidth / 2
        data["x_diff"] = (
            random_state.uniform(-1, 1, len(data))
            * maxwidth
            * data["sinawidth"]
            / 2
        )
        data["width"] = maxwidth

        # jitter y values if the input is integer,
        # but not if it is the same value
        y = data["y"].to_numpy()
        all_integers = (y == np.floor(y)).all()
        some_are_unique = len(np.unique(y)) > 1
        if all_integers and some_are_unique:
            data["y"] = jitter(y, random_state=random_state)

        return data

    def compute_group(self, data, scales):
        binwidth = self.params["binwidth"]
        maxwidth = self.params["maxwidth"]
        bin_limit = self.params["bin_limit"]
        weight = None
        y = data["y"]

        if len(data) == 0:
            return pd.DataFrame()

        elif len(data) < 3:
            data["density"] = 0
            data["scaled"] = 1
        elif len(np.unique(y)) < 2:
            data["density"] = 1
            data["scaled"] = 1
        elif self.params["method"] == "density":
            from scipy.interpolate import interp1d

            # density kernel estimation
            range_y = y.min(), y.max()
            dens = compute_density(y, weight, range_y, self.params)
            densf = interp1d(
                dens["x"],
                dens["density"],
                bounds_error=False,
                fill_value="extrapolate",  # pyright: ignore
            )
            data["density"] = densf(y)
            data["scaled"] = data["density"] / dens["density"].max()
        else:
            expanded_y_range = nextafter_range(scales.y.dimension())
            if binwidth is not None:
                bins = breaks_from_binwidth(expanded_y_range, binwidth)
            else:
                bins = breaks_from_bins(expanded_y_range, self.params["bins"])

            # bin based estimation
            bin_index = pd.cut(y, bins, include_lowest=True, labels=False)  # pyright: ignore[reportCallIssue,reportArgumentType]
            data["density"] = (
                pd.Series(bin_index)
                .groupby(bin_index)
                .apply(len)[bin_index]
                .to_numpy()
            )
            data.loc[data["density"] <= bin_limit, "density"] = 0
            data["scaled"] = data["density"] / data["density"].max()

        # Compute width if x has multiple values
        if len(data["x"].unique()) > 1:
            width = np.ptp(data["x"]) * maxwidth
        else:
            width = maxwidth

        data["width"] = width
        data["n"] = len(data)
        data["x"] = np.mean([data["x"].max(), data["x"].min()])

        return data

    def finish_layer(self, data):
        # Rescale x in case positions have been adjusted
        style = self.params["style"]
        x_mean = cast("FloatArray", data["x"].to_numpy())
        x_mod = (data["xmax"] - data["xmin"]) / data["width"]
        data["x"] = data["x"] + data["x_diff"] * x_mod
        group = cast("IntArray", data["group"].to_numpy())
        x = cast("FloatArray", data["x"].to_numpy())
        even = group % 2 == 0

        def mirror_x(bool_idx):
            """
            Mirror x locations along the mean value
            """
            data.loc[bool_idx, "x"] = 2 * x_mean[bool_idx] - x[bool_idx]

        match style:
            case "left":
                mirror_x(x_mean < x)
            case "right":
                mirror_x(x < x_mean)
            case "left-right":
                mirror_x(even & (x < x_mean) | ~even & (x_mean < x))
            case "right-left":
                mirror_x(even & (x_mean < x) | ~even & (x < x_mean))

        return data
</file>

<file path="plotnine/themes/theme_gray.py">
from .._utils.registry import alias
from ..options import get_option
from .elements import (
    element_blank,
    element_line,
    element_rect,
    element_text,
    margin,
    margin_auto,
)
from .theme import theme


class theme_gray(theme):
    """
    A gray background with white gridlines.

    This is the default theme

    Parameters
    ----------
    base_size : int
        Base font size. All text sizes are a scaled versions of
        the base font size.
    base_family : str
        Base font family. If `None`, use [](`plotnine.options.base_family`).
    """

    def __init__(self, base_size=11, base_family=None):
        base_family = base_family or get_option("base_family")
        half_line = base_size / 2
        quarter_line = base_size / 4
        fifth_line = base_size / 5
        eighth_line = base_size / 8
        m = get_option("base_margin")

        super().__init__(
            line=element_line(
                color="black", size=1, linetype="solid", lineend="butt"
            ),
            rect=element_rect(
                fill="white", color="black", size=1, linetype="solid"
            ),
            text=element_text(
                family=base_family,
                style="normal",
                color="black",
                ma="center",
                size=base_size,
                linespacing=1.2,
                rotation=0,
                margin=margin(),
            ),
            aspect_ratio=get_option("aspect_ratio"),
            axis_line=element_line(),
            axis_line_x=element_blank(),
            axis_line_y=element_blank(),
            axis_text=element_text(size=base_size * 0.8, color="#4D4D4D"),
            axis_text_x=element_text(va="top", margin=margin(t=fifth_line)),
            axis_text_y=element_text(ha="right", margin=margin(r=fifth_line)),
            axis_ticks=element_line(color="#333333"),
            axis_ticks_length=0,
            axis_ticks_length_major=quarter_line,
            axis_ticks_length_minor=eighth_line,
            axis_ticks_minor=element_blank(),
            axis_title_x=element_text(
                va="bottom", ha="center", margin=margin(t=m, unit="fig")
            ),
            axis_title_y=element_text(
                angle=90,
                va="center",
                ha="left",
                margin=margin(r=m, unit="fig"),
            ),
            dpi=get_option("dpi"),
            figure_size=get_option("figure_size"),
            # legend, None values are for parameters where the
            # drawing routines can make better decisions than
            # can be pre-determined in the theme.
            legend_background=element_rect(color="none"),
            legend_box_margin=0,  # points
            legend_box_spacing=m * 3,  # figure units
            legend_frame=element_blank(),
            legend_key_spacing_x=6,
            legend_key_spacing_y=2,
            legend_key_size=base_size * 0.8 * 1.8,
            legend_ticks_length=0.2,
            legend_margin=0,  # points
            legend_position="right",
            legend_spacing=10,  # points
            legend_text=element_text(
                size=base_size * 0.8,
                margin=margin_auto(m / 1.5, unit="fig"),
            ),
            legend_ticks=element_line(color="#CCCCCC", size=1),
            legend_title=element_text(
                margin=margin(t=m, l=m * 2, b=m / 2, r=m * 2, unit="fig")
            ),
            panel_background=element_rect(fill="#EBEBEB", color="none"),
            panel_border=element_blank(),
            panel_grid_major=element_line(color="white", size=1),
            panel_grid_minor=element_line(color="white", size=0.5),
            panel_spacing=m,
            plot_background=element_rect(color="white"),
            plot_caption=element_text(
                size=base_size * 0.8,
                ha="right",
                va="bottom",
                ma="left",
                margin=margin(t=m, unit="fig"),
            ),
            plot_footer=element_text(
                size=base_size * 0.8,
                ha="left",
                va="bottom",
                ma="left",
                margin=margin(t=1 / 3, b=1 / 3, unit="lines"),
            ),
            plot_footer_background=element_blank(),
            plot_footer_line=element_blank(),
            plot_margin=m,
            plot_subtitle=element_text(
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_title=element_text(
                size=base_size * 1.2,
                va="top",
                ma="left",
                margin=margin(b=m, unit="fig"),
            ),
            plot_tag=element_text(
                size=base_size * 1.2,
                va="center",
                ha="center",
            ),
            plot_title_position="panel",
            plot_caption_position="panel",
            plot_footer_position="plot",
            plot_tag_location="margin",
            plot_tag_position="topleft",
            strip_align=0,
            strip_background=element_rect(color="none", fill="#D9D9D9"),
            strip_background_x=element_rect(width=1),
            strip_background_y=element_rect(height=1),
            strip_text=element_text(
                color="#1A1A1A",
                size=base_size * 0.8,
                linespacing=1.5,
                margin=margin_auto(half_line * 0.8),
            ),
            strip_text_y=element_text(rotation=-90),
            complete=True,
        )


@alias
class theme_grey(theme_gray):
    pass
</file>

<file path="plotnine/themes/themeable.py">
"""
Provide theamables, the elements of plot can be style with theme()

From the ggplot2 documentation the axis.title inherits from text.
What this means is that axis.title and text have the same elements
that may be themed, but the scope of what they apply to is different.
The scope of text covers all text in the plot, axis.title applies
only to the axis.title. In matplotlib terms this means that a theme
that covers text also has to cover axis.title.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING
from warnings import warn

import numpy as np

from .._utils import has_alpha_channel, to_rgba
from .._utils.registry import RegistryHierarchyMeta
from ..exceptions import PlotnineError, deprecated_themeable_name
from .elements import element_blank
from .elements.element_base import element_base

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any, Optional, Sequence, Type

    from matplotlib.artist import Artist
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from plotnine import theme
    from plotnine.themes.targets import ThemeTargets


class themeable(metaclass=RegistryHierarchyMeta):
    """
    Abstract class of things that can be themed.

    Every subclass of themeable is stored in a dict at
    [](`~plotnine.theme.themeables.themeable.register`) with the name
    of the subclass as the key.

    It is the base of a class hierarchy that uses inheritance in a
    non-traditional manner. In the textbook use of class inheritance,
    superclasses are general and subclasses are specializations. In some
    since the hierarchy used here is the opposite in that superclasses
    are more specific than subclasses.

    It is probably better to think if this hierarchy of leveraging
    Python's multiple inheritance to implement composition. For example
    the `axis_title` themeable is *composed of* the `x_axis_title` and the
    `y_axis_title`. We are just using multiple inheritance to specify
    this composition.

    When implementing a new themeable based on the ggplot2 documentation,
    it is important to keep this in mind and reverse the order of the
    "inherits from" in the documentation.

    For example, to implement,

    - `axis_title_x` - `x` axis label (element_text;
      inherits from `axis_title`)
    - `axis_title_y` - `y` axis label (element_text;
      inherits from `axis_title`)


    You would have this implementation:


    ```python
    class axis_title_x(themeable):
        ...

    class axis_title_y(themeable):
        ...

    class axis_title(axis_title_x, axis_title_y):
        ...
    ```

    If the superclasses fully implement the subclass, the body of the
    subclass should be "pass". Python(__mro__) will do the right thing.

    When a method does require implementation, call `super()`{.py}
    then add the themeable's implementation to the axes.

    Notes
    -----
    A user should never create instances of class
    [](`~plotnine.themes.themeable.Themeable`) or subclasses of it.
    """

    _omit: Sequence[str] = ()
    """
    Properties to ignore during the apply stage.

    These properties may have been used when creating the artists and
    applying them would create a conflict or an error.
    """

    def __init__(self, theme_element: element_base | str | float):
        self.theme_element = theme_element
        if isinstance(theme_element, element_base):
            self._properties: dict[str, Any] = theme_element.properties
        else:
            # The specific themeable takes this value and
            # does stuff with rcParams or sets something
            # on some object attached to the axes/figure
            self._properties = {"value": theme_element}

    @staticmethod
    def from_class_name(name: str, theme_element: Any) -> themeable:
        """
        Create a themeable by name

        Parameters
        ----------
        name : str
            Class name
        theme_element : element object
            An element of the type required by the theme.
            For lines, text and rects it should be one of:
            [](`~plotnine.themes.element_line`),
            [](`~plotnine.themes.element_rect`),
            [](`~plotnine.themes.element_text`) or
            [](`~plotnine.themes.element_blank`)

        Returns
        -------
        out : plotnine.themes.themeable.themeable
        """
        msg = f"There no themeable element called: {name}"
        try:
            klass: Type[themeable] = themeable._registry[name]
        except KeyError as e:
            raise PlotnineError(msg) from e

        if not issubclass(klass, themeable):
            raise PlotnineError(msg)

        return klass(theme_element)

    @classmethod
    def registry(cls) -> Mapping[str, Any]:
        return themeable._registry

    def is_blank(self) -> bool:
        """
        Return True if theme_element is made of element_blank
        """
        return isinstance(self.theme_element, element_blank)

    def merge(self, other: themeable):
        """
        Merge properties of other into self

        Raises
        ------
        ValueError
            If any of the properties are blank
        """
        if self.is_blank() or other.is_blank():
            raise ValueError("Cannot merge if there is a blank.")
        else:
            self._properties.update(other._properties)

    def __eq__(self, other: object) -> bool:
        "Mostly for unittesting."
        return other is self or (
            isinstance(other, type(self))
            and self._properties == other._properties
        )

    @property
    def rcParams(self) -> dict[str, Any]:
        """
        Return themeables rcparams to an rcparam dict before plotting.

        Returns
        -------
        dict
            Dictionary of legal matplotlib parameters.

        This method should always call super(...).rcParams and
        update the dictionary that it returns with its own value, and
        return that dictionary.

        This method is called before plotting. It tends to be more
        useful for general themeables. Very specific themeables
        often cannot be be themed until they are created as a
        result of the plotting process.
        """
        return {}

    @property
    def properties(self):
        """
        Return only the properties that can be applied
        """
        d = self._properties.copy()
        for key in self._omit:
            with suppress(KeyError):
                del d[key]
        return d

    def apply(self, theme: theme):
        """
        Called by the theme to apply the themeable

        Subclasses should not have to override this method
        """
        blanks = (self.blank_figure, self.blank_ax)
        applys = (self.apply_figure, self.apply_ax)
        do_figure, do_ax = blanks if self.is_blank() else applys

        do_figure(theme.figure, theme.targets)
        for ax in theme.axs:
            do_ax(ax)

    def apply_ax(self, ax: Axes):
        """
        Called after a chart has been plotted.

        Subclasses can override this method to customize the plot
        according to the theme.

        This method should be implemented as `super().apply_ax()`{.py}
        followed by extracting the portion of the axes specific to this
        themeable then applying the properties.


        Parameters
        ----------
        ax : matplotlib.axes.Axes
        """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        """
        Apply theme to the figure
        """

    def blank_ax(self, ax: Axes):
        """
        Blank out theme elements
        """

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        """
        Blank out elements on the figure
        """


class Themeables(dict[str, themeable]):
    """
    Collection of themeables

    The key is the name of the class.
    """

    def update(self, other: Themeables, **kwargs):  # type: ignore
        """
        Update themeables with those from `other`

        This method takes care of inserting the `themeable`
        into the underlying dictionary. Before doing the
        insertion, any existing themeables that will be
        affected by a new from `other` will either be merged
        or removed. This makes sure that a general themeable
        of type [](`~plotnine.theme.themeables.text`) can be
        added to override an existing specific one of type
        [](`~plotnine.theme.themeables.axis_text_x`).
        """
        for new in other.values():
            new_key = new.__class__.__name__

            # 1st in the mro is self, the
            # last 2 are (themeable, object)
            for child in new.__class__.mro()[1:-2]:
                child_key = child.__name__
                try:
                    self[child_key].merge(new)
                except KeyError:
                    pass
                except ValueError:
                    # Blank child is will be overridden
                    del self[child_key]
            try:
                self[new_key].merge(new)
            except (KeyError, ValueError):
                # Themeable type is new or
                # could not merge blank element.
                self[new_key] = new

    @property
    def _dict(self):
        """
        Themeables in reverse based on the inheritance hierarchy.

        Themeables should be applied or merged in order from general
        to specific. i.e.
            - apply [](`~plotnine.theme.themeables.axis_line`)
              before [](`~plotnine.theme.themeables.axis_line_x`)
            - merge [](`~plotnine.theme.themeables.axis_line_x`)
              into [](`~plotnine.theme.themeables.axis_line`)
        """
        hierarchy = themeable._hierarchy
        result: dict[str, themeable] = {}
        for lst in hierarchy.values():
            for name in reversed(lst):
                if name in self and name not in result:
                    result[name] = self[name]
        return result

    def setup(self, theme: theme):
        """
        Setup themeables for theming
        """
        # Setup theme elements
        for name, th in self.items():
            if isinstance(th.theme_element, element_base):
                th.theme_element.setup(theme, name)

    def items(self):
        """
        List of (name, themeable) in reverse based on the inheritance.
        """
        return self._dict.items()

    def values(self):
        """
        List of themeables in reverse based on the inheritance hierarchy.
        """
        return self._dict.values()

    def getp(self, key: str | tuple[str, str], default: Any = None) -> Any:
        """
        Get the value a specific themeable(s) property

        Themeables store theming attribute values in the
        [](`~plotnine.themes.themeables.Themeable.properties`)
        [](`dict`). The goal of this method is to look a value from
        that dictionary, and fallback along the inheritance hierarchy
        of themeables.

        Parameters
        ----------
        key :
            Themeable and property name to lookup. If a `str`,
            the name is assumed to be "value".

        default :
            Value to return if lookup fails
        Returns
        -------
        out : object
            Value

        Raises
        ------
        KeyError
            If key is in not in any of themeables
        """
        if isinstance(key, str):
            key = (key, "value")

        name, prop = key
        hlist = themeable._hierarchy[name]
        scalar = key == "value"
        for th in hlist:
            with suppress(KeyError):
                value = self[th]._properties[prop]
                if not scalar or value is not None:
                    return value

        return default

    def get_ha(self, name: str) -> float:
        """
        Get the horizontal alignement of themeable as a float

        The themeable should be and element_text
        """
        lookup = {"left": 0.0, "center": 0.5, "right": 1.0}
        ha: str | float = self.getp((name, "ha"), "center")
        if isinstance(ha, str):
            ha = lookup[ha]
        return ha

    def get_va(self, name) -> float:
        """
        Get the vertical alignement of themeable as a float

        The themeable should be and element_text
        """
        lookup = {
            "bottom": 0.0,
            "center": 0.5,
            "baseline": 0.5,
            "center_baseline": 0.5,
            "top": 1.0,
        }
        va: str | float = self.getp((name, "va"), "center")
        if isinstance(va, str):
            va = lookup[va]
        return va

    def property(self, name: str, key: str = "value") -> Any:
        """
        Get the value a specific themeable(s) property

        Themeables store theming attribute values in the
        [](`~plotnine.theme.themeables.Themeable.properties`)
        [](`dict`). The goal of this method is to look a value from
        that dictionary, and fallback along the inheritance hierarchy
        of themeables.

        Parameters
        ----------
        name : str
            Themeable name
        key : str
            Property name to lookup

        Returns
        -------
        out : object
            Value

        Raises
        ------
        KeyError
            If key is in not in any of themeables
        """
        default = object()
        res = self.getp((name, key), default)
        if res is default:
            hlist = themeable._hierarchy[name]
            msg = f"'{key}' is not in the properties of {hlist}"
            raise KeyError(msg)
        return res

    def is_blank(self, name: str) -> bool:
        """
        Return True if the themeable *name* is blank

        If the *name* is not in the list of themeables then
        the lookup falls back to inheritance hierarchy.
        If none of the themeables are in the hierarchy are
        present, `False` is returned.

        Parameters
        ----------
        names : str
            Themeable, in order of most specific to most
            general.
        """
        for th in themeable._hierarchy[name]:
            if element := self.get(th):
                return element.is_blank()

        return False


class MixinSequenceOfValues(themeable):
    """
    Make themeable also accept a sequence to values

    This makes it possible to apply a different style value similar artists.

    e.g.

        theme(axis_text_x=element_text(color=("red", "green", "blue")))

    The number of values in the list must match the number of objects
    targeted by the themeable..
    """

    def set(
        self, artists: Sequence[Artist], props: Optional[dict[str, Any]] = None
    ):
        if props is None:
            props = self.properties

        n = len(artists)
        sequence_props = {}
        for name, value in props.items():
            if (
                isinstance(value, (list, tuple, np.ndarray))
                and len(value) == n
            ):
                sequence_props[name] = value

        for key in sequence_props:
            del props[key]

        for a in artists:
            a.set(**props)

        for name, values in sequence_props.items():
            for a, value in zip(artists, values):
                a.set(**{name: value})


def blend_alpha(
    properties: dict[str, Any], key: str = "color"
) -> dict[str, Any]:
    """
    Blend color with alpha

    When setting color property values of matplotlib objects,
    for a color with an alpha channel, we don't want the alpha
    property if any to have any effect on that color.
    """
    if (color := properties.get(key)) is not None:
        if "alpha" in properties:
            properties[key] = to_rgba(color, properties["alpha"])
            properties["alpha"] = None
        elif has_alpha_channel(color):
            properties["alpha"] = None
    return properties


# element_text themeables


class axis_title_x(themeable):
    """
    x axis label

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.axis_title_x:
            props = self.properties
            # ha can be a float and is handled by the layout manager
            with suppress(KeyError):
                del props["ha"]
            text.set(**props)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.axis_title_x:
            text.set_visible(False)


class axis_title_y(themeable):
    """
    y axis label

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.axis_title_y:
            props = self.properties
            # va can be a float and is handled by the layout manager
            with suppress(KeyError):
                del props["va"]
            text.set(**props)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.axis_title_y:
            text.set_visible(False)


class axis_title(axis_title_x, axis_title_y):
    """
    Axis labels

    Parameters
    ----------
    theme_element : element_text
    """


class legend_title(themeable):
    """
    Legend title

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.legend_title:
            text.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.legend_title:
            text.set_visible(False)


class legend_text_legend(MixinSequenceOfValues):
    """
    Legend text for the common legend

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Horizontal alignment `ha` has no effect when the text is to the
    left or to the right. Likewise vertical alignment `va` has no
    effect when the text at the top or the bottom.
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if texts := targets.legend_text_legend:
            self.set(texts)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if texts := targets.legend_text_legend:
            for text in texts:
                text.set_visible(False)


class legend_text_colorbar(MixinSequenceOfValues):
    """
    Colorbar text

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Horizontal alignment `ha` has no effect when the text is to the
    left or to the right. Likewise vertical alignment `va` has no
    effect when the text at the top or the bottom.
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if texts := targets.legend_text_colorbar:
            self.set(texts)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if texts := targets.legend_text_colorbar:
            for text in texts:
                text.set_visible(False)


legend_text_colourbar = legend_text_colorbar


class legend_text(legend_text_legend, legend_text_colorbar):
    """
    Legend text

    Parameters
    ----------
    theme_element : element_text
    """


class plot_title(themeable):
    """
    Plot title

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    The default horizontal alignment for the title is center. However the
    title will be left aligned if and only if there is a subtitle and its
    horizontal alignment has not been set (so it defaults to the left).

    The defaults ensure that, short titles are not awkwardly left-aligned,
    and that a title and a subtitle will not be awkwardly mis-aligned in
    the center or with different alignments.
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.plot_title:
            props = self.properties
            # ha can be a float and is handled by the layout manager
            with suppress(KeyError):
                del props["ha"]
            text.set(**props)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.plot_title:
            text.set_visible(False)


class plot_subtitle(themeable):
    """
    Plot subtitle

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    The default horizontal alignment for the subtitle is left. And when
    it is present, by default it drags the title to the left. The subtitle
    drags the title to the left only if none of the two has their horizontal
    alignment are set.
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.plot_subtitle:
            text.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.plot_subtitle:
            text.set_visible(False)


class plot_caption(themeable):
    """
    Plot caption

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.plot_caption:
            text.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.plot_caption:
            text.set_visible(False)


class plot_footer(themeable):
    """
    Plot footer

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if text := targets.plot_footer:
            text.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.plot_footer:
            text.set_visible(False)


class plot_tag(themeable):
    """
    Plot tag

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    The `ha` & `va` of element_text have no effect in some cases. e.g.
    if [](:class:`~plotnine.themes.themeable.plot_tag_position`) is "margin"
    and the tag is at the top it cannot be vertically aligned.

    Also `ha` & `va` can be floats if it makes sense to justify the tag
    over a span. e.g. along the panel or plot, or when aligning with
    other tags in a composition.
    """

    _omit = ["margin"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        props = self.properties

        if "va" in props and not isinstance(props["va"], str):
            del props["va"]

        if "ha" in props and not isinstance(props["ha"], str):
            del props["ha"]

        if text := targets.plot_tag:
            text.set(**props)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if text := targets.plot_tag:
            text.set_visible(False)


class plot_title_position(themeable):
    """
    How to align the plot title and plot subtitle

    Parameters
    ----------
    theme_element : Literal["panel", "plot"], default = "panel"
        If "panel", the title / subtitle are aligned with respect
        to the panels. If "plot", they are aligned with the plot,
        excluding the margin space
    """


class plot_caption_position(themeable):
    """
    How to align the plot caption

    Parameters
    ----------
    theme_element : Literal["panel", "plot"], default = "panel"
        If "panel", the caption is aligned with respect to the
        panels. If "plot", it is aligned with the plot, excluding
        the margin space.
    """


class plot_footer_position(themeable):
    """
    How to align the plot footer

    Parameters
    ----------
    theme_element : Literal["panel", "plot"], default = "plot"
        If "panel", the footer is aligned with respect to the
        panels. If "plot", it is aligned with the plot, excluding
        the margin space.
    """


class plot_tag_location(themeable):
    """
    The area where the tag will be positioned

    Parameters
    ----------
    theme_element : Literal["margin", "plot", "panel"], default = "margin"
        If "margin", it is placed within the plot_margin.
        If "plot", it is placed in the figure, ignoring any margins.
        If "panel", it is placed within the panel area.
    """


class plot_tag_position(themeable):
    """
    Position of the tag

    Parameters
    ----------
    theme_element : Literal["topleft", "top", "topright", "left" \
                    "right", "bottomleft", "bottom", "bottomleft"] \
                    | tuple[float, float], default = "topleft"
        If the value is a string, the tag will be managed by the layout
        manager. If it is a tuple of (x, y) coordinates, they should be
        in figure space and the tag will be ignored by the layout manager.
    """


class strip_text_x(MixinSequenceOfValues):
    """
    Facet labels along the horizontal axis

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if texts := targets.strip_text_x:
            self.set(texts)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if texts := targets.strip_text_x:
            for text in texts:
                text.set_visible(False)


class strip_text_y(MixinSequenceOfValues):
    """
    Facet labels along the vertical axis

    Parameters
    ----------
    theme_element : element_text
    """

    _omit = ["margin", "ha", "va"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if texts := targets.strip_text_y:
            self.set(texts)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if texts := targets.strip_text_y:
            for text in texts:
                text.set_visible(False)


class strip_text(strip_text_x, strip_text_y):
    """
    Facet labels along both axes

    Parameters
    ----------
    theme_element : element_text
    """


class title(
    axis_title,
    legend_title,
    plot_title,
    plot_subtitle,
    plot_caption,
    plot_footer,
    plot_tag,
):
    """
    All titles on the plot

    Parameters
    ----------
    theme_element : element_text
    """


class axis_text_x(MixinSequenceOfValues):
    """
    x-axis tick labels

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Use the `margin` to control the gap between the ticks and the
    text. e.g.

    ```python
    theme(axis_text_x=element_text(margin={"t": 5, "units": "pt"}))
    ```

    creates a margin of 5 points.
    """

    _omit = ["margin", "va"]

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)

        # TODO: Remove this code when the minimum matplotlib >= 3.10.0,
        # and use the commented one below it
        import matplotlib as mpl
        from packaging import version

        vinstalled = version.parse(mpl.__version__)
        v310 = version.parse("3.10.0")
        name = "labelbottom" if vinstalled >= v310 else "labelleft"
        if not ax.xaxis.get_tick_params()[name]:
            return

        # if not ax.xaxis.get_tick_params()["labelbottom"]:
        #     return

        labels = [t.label1 for t in ax.xaxis.get_major_ticks()]
        self.set(labels)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        for t in ax.xaxis.get_major_ticks():
            t.label1.set_visible(False)


class axis_text_y(MixinSequenceOfValues):
    """
    y-axis tick labels

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Use the `margin` to control the gap between the ticks and the
    text. e.g.

    ```python
    theme(axis_text_y=element_text(margin={"r": 5, "units": "pt"}))
    ```

    creates a margin of 5 points.
    """

    _omit = ["margin", "ha"]

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)

        if not ax.yaxis.get_tick_params()["labelleft"]:
            return

        labels = [t.label1 for t in ax.yaxis.get_major_ticks()]
        self.set(labels)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        for t in ax.yaxis.get_major_ticks():
            t.label1.set_visible(False)


class axis_text(axis_text_x, axis_text_y):
    """
    Axis tick labels

    Parameters
    ----------
    theme_element : element_text

    Notes
    -----
    Use the `margin` to control the gap between the ticks and the
    text. e.g.

    ```python
    theme(axis_text=element_text(margin={"t": 5, "r": 5, "units": "pt"}))
    ```

    creates a margin of 5 points.
    """


class text(axis_text, legend_text, strip_text, title):
    """
    All text elements in the plot

    Parameters
    ----------
    theme_element : element_text
    """

    @property
    def rcParams(self) -> dict[str, Any]:
        rcParams = super().rcParams

        family = self.properties.get("family")

        style = self.properties.get("style")
        weight = self.properties.get("weight")
        size = self.properties.get("size")
        color = self.properties.get("color")

        if family:
            rcParams["font.family"] = family
        if style:
            rcParams["font.style"] = style
        if weight:
            rcParams["font.weight"] = weight
        if size:
            rcParams["font.size"] = size
            rcParams["xtick.labelsize"] = size
            rcParams["ytick.labelsize"] = size
            rcParams["legend.fontsize"] = size
        if color:
            rcParams["text.color"] = color

        return rcParams


# element_line themeables


class axis_line_x(themeable):
    """
    x-axis line

    Parameters
    ----------
    theme_element : element_line
    """

    position = "bottom"
    _omit = ["solid_capstyle"]

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        properties = self.properties
        # MPL has a default zorder of 2.5 for spines
        # so layers 3+ would be drawn on top of the spines
        if "zorder" not in properties:
            properties["zorder"] = 10000
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set(**properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)


class axis_line_y(themeable):
    """
    y-axis line

    Parameters
    ----------
    theme_element : element_line
    """

    position = "left"
    _omit = ["solid_capstyle"]

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        properties = self.properties
        # MPL has a default zorder of 2.5 for spines
        # so layers 3+ would be drawn on top of the spines
        if "zorder" not in properties:
            properties["zorder"] = 10000
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set(**properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)


class axis_line(axis_line_x, axis_line_y):
    """
    x & y axis lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_minor_x(MixinSequenceOfValues):
    """
    x-axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        # The ggplot._draw_breaks_and_labels uses set_tick_params to
        # turn off the ticks that will not show. That sets the location
        # key (e.g. params["bottom"]) to False. It also sets the artist
        # to invisible. Theming should not change those artists to visible,
        # so we return early.
        params = ax.xaxis.get_tick_params(which="minor")
        if not params.get("bottom", False):
            return

        # We have to use both
        #    1. Axis.set_tick_params()
        #    2. Tick.tick1line.set()
        # We split the properties so that set_tick_params keeps
        # record of the properties it cares about so that it does
        # not undo them. GH703
        # https://github.com/matplotlib/matplotlib/issues/26008
        tick_params = {}
        properties = self.properties
        with suppress(KeyError):
            tick_params["width"] = properties.pop("linewidth")
        with suppress(KeyError):
            tick_params["color"] = properties.pop("color")

        if tick_params:
            ax.xaxis.set_tick_params(which="minor", **tick_params)

        lines = [t.tick1line for t in ax.xaxis.get_minor_ticks()]
        self.set(lines, properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_visible(False)


class axis_ticks_minor_y(MixinSequenceOfValues):
    """
    y-axis minor tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        params = ax.yaxis.get_tick_params(which="minor")
        if not params.get("left", False):
            return

        tick_params = {}
        properties = self.properties
        with suppress(KeyError):
            tick_params["width"] = properties.pop("linewidth")
        with suppress(KeyError):
            tick_params["color"] = properties.pop("color")

        if tick_params:
            ax.yaxis.set_tick_params(which="minor", **tick_params)

        lines = [t.tick1line for t in ax.yaxis.get_minor_ticks()]
        self.set(lines, properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        for tick in ax.yaxis.get_minor_ticks():
            tick.tick1line.set_visible(False)


class axis_ticks_major_x(MixinSequenceOfValues):
    """
    x-axis major tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        params = ax.xaxis.get_tick_params(which="major")

        # TODO: Remove this code when the minimum matplotlib >= 3.10.0,
        # and use the commented one below it
        import matplotlib as mpl
        from packaging import version

        vinstalled = version.parse(mpl.__version__)
        v310 = version.parse("3.10.0")
        name = "bottom" if vinstalled >= v310 else "left"
        if not params.get(name, False):
            return

        # if not params.get("bottom", False):
        #     return

        tick_params = {}
        properties = self.properties
        with suppress(KeyError):
            tick_params["width"] = properties.pop("linewidth")
        with suppress(KeyError):
            tick_params["color"] = properties.pop("color")

        if tick_params:
            ax.xaxis.set_tick_params(which="major", **tick_params)

        lines = [t.tick1line for t in ax.xaxis.get_major_ticks()]
        self.set(lines, properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)


class axis_ticks_major_y(MixinSequenceOfValues):
    """
    y-axis major tick lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        params = ax.yaxis.get_tick_params(which="major")
        if not params.get("left", False):
            return

        tick_params = {}
        properties = self.properties
        with suppress(KeyError):
            tick_params["width"] = properties.pop("linewidth")
        with suppress(KeyError):
            tick_params["color"] = properties.pop("color")

        if tick_params:
            ax.yaxis.set_tick_params(which="major", **tick_params)

        lines = [t.tick1line for t in ax.yaxis.get_major_ticks()]
        self.set(lines, properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_visible(False)


class axis_ticks_major(axis_ticks_major_x, axis_ticks_major_y):
    """
    x & y axis major tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_minor(axis_ticks_minor_x, axis_ticks_minor_y):
    """
    x & y axis minor tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_x(axis_ticks_major_x, axis_ticks_minor_x):
    """
    x major and minor axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks_y(axis_ticks_major_y, axis_ticks_minor_y):
    """
    y major and minor axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class axis_ticks(axis_ticks_major, axis_ticks_minor):
    """
    x & y major and minor axis tick lines

    Parameters
    ----------
    theme_element : element_line
    """


class legend_ticks(themeable):
    """
    The ticks on a legend

    Parameters
    ----------
    theme_element : element_line
    """

    _omit = ["solid_capstyle"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if coll := targets.legend_ticks:
            coll.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if coll := targets.legend_ticks:
            coll.set_visible(False)


class panel_grid_major_x(themeable):
    """
    Vertical major grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.xaxis.grid(which="major", **blend_alpha(self.properties))

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.grid(False, which="major", axis="x")


class panel_grid_major_y(themeable):
    """
    Horizontal major grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.yaxis.grid(which="major", **blend_alpha(self.properties))

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.grid(False, which="major", axis="y")


class panel_grid_minor_x(themeable):
    """
    Vertical minor grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.xaxis.grid(which="minor", **self.properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.grid(False, which="minor", axis="x")


class panel_grid_minor_y(themeable):
    """
    Horizontal minor grid lines

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.yaxis.grid(which="minor", **self.properties)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.grid(False, which="minor", axis="y")


class panel_grid_major(panel_grid_major_x, panel_grid_major_y):
    """
    Major grid lines

    Parameters
    ----------
    theme_element : element_line
    """


class panel_grid_minor(panel_grid_minor_x, panel_grid_minor_y):
    """
    Minor grid lines

    Parameters
    ----------
    theme_element : element_line
    """


class panel_grid(panel_grid_major, panel_grid_minor):
    """
    Grid lines

    Parameters
    ----------
    theme_element : element_line
    """


class plot_footer_line(themeable):
    """
    Line above the footer

    Parameters
    ----------
    theme_element : element_line
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if targets.plot_footer_line:
            targets.plot_footer_line.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if targets.plot_footer_line:
            targets.plot_footer_line.set_visible(False)


class line(axis_line, axis_ticks, panel_grid, legend_ticks, plot_footer_line):
    """
    All line elements

    Parameters
    ----------
    theme_element : element_line
    """

    @property
    def rcParams(self) -> dict[str, Any]:
        rcParams = super().rcParams
        color = self.properties.get("color")
        linewidth = self.properties.get("linewidth")
        linestyle = self.properties.get("linestyle")
        d = {}

        if color:
            d["axes.edgecolor"] = color
            d["xtick.color"] = color
            d["ytick.color"] = color
            d["grid.color"] = color
        if linewidth:
            d["axes.linewidth"] = linewidth
            d["xtick.major.width"] = linewidth
            d["xtick.minor.width"] = linewidth
            d["ytick.major.width"] = linewidth
            d["ytick.minor.width"] = linewidth
            d["grid.linewidth"] = linewidth
        if linestyle:
            d["grid.linestyle"] = linestyle

        rcParams.update(d)
        return rcParams


# element_rect themeables


class legend_key(MixinSequenceOfValues):
    """
    Legend key background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        properties = self.properties
        edgecolor = properties.get("edgecolor", None)

        if isinstance(self, rect) and edgecolor:
            del properties["edgecolor"]

        # Prevent invisible strokes from having any effect
        if edgecolor in ("none", "None"):
            properties["linewidth"] = 0

        rects = [da.patch for da in targets.legend_key]
        self.set(rects, properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        for da in targets.legend_key:
            da.patch.set_visible(False)


class legend_frame(themeable):
    """
    Frame around colorbar

    Parameters
    ----------
    theme_element : element_rect
    """

    _omit = ["facecolor"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if rect := targets.legend_frame:
            rect.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if rect := targets.legend_frame:
            rect.set_visible(False)


class legend_background(themeable):
    """
    Legend background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        # anchored offset box
        if legends := targets.legends:
            properties = self.properties

            # Prevent invisible strokes from having any effect
            if properties.get("edgecolor") in ("none", "None"):
                properties["linewidth"] = 0

            for aob in legends.boxes:
                aob.patch.set(**properties)
                if properties:
                    aob._drawFrame = True  # type: ignore
                    # some small sensible padding
                    if not aob.pad:
                        aob.pad = 0.2

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if legends := targets.legends:
            for aob in legends.boxes:
                aob.patch.set_visible(False)


class legend_box_background(themeable):
    """
    Legend box background

    Parameters
    ----------
    theme_element : element_rect

    Notes
    -----
    Not Implemented. We would have to place the outermost
    VPacker/HPacker boxes that hold the individual legends
    onto an object that has a patch.
    """


class panel_background(legend_key):
    """
    Panel background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        d = blend_alpha(self.properties, "facecolor")
        d["edgecolor"] = "none"
        d["linewidth"] = 0
        ax.patch.set(**d)

    def blank_ax(self, ax: Axes):
        super().blank_ax(ax)
        ax.patch.set_visible(False)


class panel_border(MixinSequenceOfValues):
    """
    Panel border

    Parameters
    ----------
    theme_element : element_rect
    """

    _omit = ["facecolor"]

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if not (rects := targets.panel_border):
            return

        d = blend_alpha(self.properties, "edgecolor")

        with suppress(KeyError):
            if d["edgecolor"] == "none" or d["size"] == 0:
                return

        self.set(rects, d)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        for rect in targets.panel_border:
            rect.set_visible(False)


class plot_background(themeable):
    """
    Plot background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if targets.plot_background:
            targets.plot_background.set(**self.properties)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if targets.plot_background:
            targets.plot_background.set_visible(False)


class plot_footer_background(themeable):
    """
    Footer background

    The background is placed across the entire with of the plot,
    or the composition. And the height is determined by the height
    of the footer including the top and bottom margin.

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if targets.plot_footer_background:
            props = self.properties
            props["linewidth"] = 0
            props["edgecolor"] = "none"
            targets.plot_footer_background.set(**props)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        if targets.plot_footer_background:
            targets.plot_footer_background.set_visible(False)


class strip_background_x(MixinSequenceOfValues):
    """
    Horizontal facet label background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if bboxes := targets.strip_background_x:
            self.set(bboxes)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        for rect in targets.strip_background_x:
            rect.set_visible(False)


class strip_background_y(MixinSequenceOfValues):
    """
    Vertical facet label background

    Parameters
    ----------
    theme_element : element_rect
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        super().apply_figure(figure, targets)
        if bboxes := targets.strip_background_y:
            self.set(bboxes)

    def blank_figure(self, figure: Figure, targets: ThemeTargets):
        super().blank_figure(figure, targets)
        for rect in targets.strip_background_y:
            rect.set_visible(False)


class strip_background(strip_background_x, strip_background_y):
    """
    Facet label background

    Parameters
    ----------
    theme_element : element_rect
    """


class rect(
    legend_frame,
    legend_background,
    panel_background,
    panel_border,
    plot_background,
    plot_footer_background,
    strip_background,
):
    """
    All rectangle elements

    Parameters
    ----------
    theme_element : element_rect
    """


# themeables with scalar values


class axis_ticks_length_major_x(themeable):
    """
    x-axis major-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        value: float | complex = self.properties["value"]

        try:
            visible = ax.xaxis.get_major_ticks()[0].tick1line.get_visible()
        except IndexError:
            value = 0
        else:
            if not visible:
                value = 0

        if isinstance(value, (float, int)):
            tickdir = "in" if value < 0 else "out"
        else:
            tickdir = "inout"

        ax.xaxis.set_tick_params(
            which="major", length=abs(value), tickdir=tickdir
        )


class axis_ticks_length_major_y(themeable):
    """
    y-axis major-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        value: float | complex = self.properties["value"]

        try:
            visible = ax.yaxis.get_major_ticks()[0].tick1line.get_visible()
        except IndexError:
            value = 0
        else:
            if not visible:
                value = 0

        if isinstance(value, (float, int)):
            tickdir = "in" if value < 0 else "out"
        else:
            tickdir = "inout"

        ax.yaxis.set_tick_params(
            which="major", length=abs(value), tickdir=tickdir
        )


class axis_ticks_length_major(
    axis_ticks_length_major_x, axis_ticks_length_major_y
):
    """
    Axis major-tick length

    Parameters
    ----------
    theme_element : float
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """


class axis_ticks_length_minor_x(themeable):
    """
    x-axis minor-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        value: float | complex = self.properties["value"]

        if isinstance(value, (float, int)):
            tickdir = "in" if value < 0 else "out"
        else:
            tickdir = "inout"

        ax.xaxis.set_tick_params(
            which="minor", length=abs(value), tickdir=tickdir
        )


class axis_ticks_length_minor_y(themeable):
    """
    x-axis minor-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        value: float | complex = self.properties["value"]

        if isinstance(value, (float, int)):
            tickdir = "in" if value < 0 else "out"
        else:
            tickdir = "inout"

        ax.yaxis.set_tick_params(
            which="minor", length=abs(value), tickdir=tickdir
        )


class axis_ticks_length_minor(
    axis_ticks_length_minor_x, axis_ticks_length_minor_y
):
    """
    Axis minor-tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """


class axis_ticks_length(axis_ticks_length_major, axis_ticks_length_minor):
    """
    Axis tick length

    Parameters
    ----------
    theme_element : float | complex
        Value in points. A negative value creates the ticks
        inside the plot panel. A complex value (e.g. `3j`)
        creates ticks that span both in and out of the panel.
    """


class panel_spacing_x(themeable):
    """
    Horizontal spacing between the facet panels

    Parameters
    ----------
    theme_element : float
        Size as a fraction of the figure width.
    """


class panel_spacing_y(themeable):
    """
    Vertical spacing between the facet panels

    Parameters
    ----------
    theme_element : float
        Size as a fraction of the figure width.

    Notes
    -----
    It is deliberate to have the vertical spacing be a fraction of
    the width. That means that when
    [](`~plotnine.theme.themeables.panel_spacing_x`) is the
    equal [](`~plotnine.theme.themeables.panel_spacing_x`),
    the spaces in both directions will be equal.
    """


class panel_spacing(panel_spacing_x, panel_spacing_y):
    """
    Spacing between the facet panels

    Parameters
    ----------
    theme_element : float
        Size as a fraction of the figure's dimension.
    """


# TODO: Distinct margins in all four directions
class plot_margin_left(themeable):
    """
    Plot Margin on the left

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin_right(themeable):
    """
    Plot Margin on the right

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin_top(themeable):
    """
    Plot Margin at the top

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin_bottom(themeable):
    """
    Plot Margin at the bottom

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class plot_margin(
    plot_margin_left, plot_margin_right, plot_margin_top, plot_margin_bottom
):
    """
    Plot Margin

    Parameters
    ----------
    theme_element : float
        Must be in the [0, 1] range. It is specified
        as a fraction of the figure width and figure
        height.
    """


class panel_ontop(themeable):
    """
    Place panel background & gridlines over/under the data layers

    Parameters
    ----------
    theme_element : bool
        Default is False.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.set_axisbelow(not self.properties["value"])


class aspect_ratio(themeable):
    """
    Aspect ratio of the panel(s)

    Parameters
    ----------
    theme_element : float
        `panel_height / panel_width`

    Notes
    -----
    For a fixed relationship between the `x` and `y` scales,
    use [](`~plotnine.coords.coord_fixed`).
    """


class dpi(themeable):
    """
    DPI with which to draw/save the figure

    Parameters
    ----------
    theme_element : int
    """

    # fig.set_dpi does not work
    # https://github.com/matplotlib/matplotlib/issues/24644

    @property
    def rcParams(self) -> dict[str, Any]:
        rcParams = super().rcParams
        rcParams["figure.dpi"] = self.properties["value"]
        return rcParams


class figure_size(themeable):
    """
    Figure size in inches

    Parameters
    ----------
    theme_element : tuple
        (width, height) in inches
    """

    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        figure.set_size_inches(self.properties["value"])


class legend_box(themeable):
    """
    How to box up multiple legends

    Parameters
    ----------
    theme_element : Literal["vertical", "horizontal"]
        Whether to stack up the legends vertically or
        horizontally.
    """


class legend_box_margin(themeable):
    """
    Padding between the legends and the box

    Parameters
    ----------
    theme_element : int
        Value in points.
    """


class legend_box_just(themeable):
    """
    Justification of guide boxes

    Parameters
    ----------
    theme_element : Literal["left", "right", "center", "top", "bottom", \
                    "baseline"], default=None
        If `None`, the value that will apply depends on
        [](`~plotnine.theme.themeables.legend_box`).
    """


class legend_justification_right(themeable):
    """
    Justification of legends placed on the right

    Parameters
    ----------
    theme_element : Literal["bottom", "center", "top"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the right column.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"bottom"` and `1` is `"top"`.
    """


class legend_justification_left(themeable):
    """
    Justification of legends placed on the left

    Parameters
    ----------
    theme_element : Literal["bottom", "center", "top"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the left column.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"bottom"` and `1` is `"top"`.
    """


class legend_justification_top(themeable):
    """
    Justification of legends placed at the top

    Parameters
    ----------
    theme_element : Literal["left", "center", "right"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the top row.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"left"` and `1` is `"right"`.
    """


class legend_justification_bottom(themeable):
    """
    Justification of legends placed at the bottom

    Parameters
    ----------
    theme_element : Literal["left", "center", "right"] | float
        How to justify the entire group with 1 or more guides. i.e. How
        to slide the legend along the bottom row.
        If a float, it should be in the range `[0, 1]`, where
        `0` is `"left"` and `1` is `"right"`.
    """


class legend_justification_inside(themeable):
    """
    Justification of legends placed inside the axes

    Parameters
    ----------
    theme_element : Literal["left", "right", "center", "top", "bottom"] | \
                    float | tuple[float, float]
        How to justify the entire group with 1 or more guides. i.e. What
        point of the legend box to place at the destination point in the
        panels area.

        If a float, it should be in the range `[0, 1]`, and it implies the
        horizontal part and with the vertical part fixed at `0.5`.

        Therefore a float value of `0.8` equivalent to a tuple value of
        `(0.8, 0.5)`.
    """


class legend_justification(
    legend_justification_right,
    legend_justification_left,
    legend_justification_top,
    legend_justification_bottom,
    legend_justification_inside,
):
    """
    Justification of any legend

    Parameters
    ----------
    theme_element : Literal["left", "right", "center", "top", "bottom"] | \
                    float | tuple[float, float]
        How to justify the entire group with 1 or more guides.
    """


class legend_direction(themeable):
    """
    Layout items in the legend

    Parameters
    ----------
    theme_element : Literal["vertical", "horizontal"]
        Vertically or horizontally
    """


class legend_key_width(themeable):
    """
    Legend key background width

    Parameters
    ----------
    theme_element : float
        Value in points
    """


class legend_key_height(themeable):
    """
    Legend key background height

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_key_size(legend_key_width, legend_key_height):
    """
    Legend key background width and height

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_ticks_length(themeable):
    """
    Length of ticks in the legend

    Parameters
    ----------
    theme_element : float
        A good value should be in the range `[0, 0.5]`.
    """


class legend_margin(themeable):
    """
    Padding between the legend and the inner box

    Parameters
    ----------
    theme_element : float
        Value in points
    """


class legend_box_spacing(themeable):
    """
    Spacing between the legend and the plotting area

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_spacing(themeable):
    """
    Spacing between two adjacent legends

    Parameters
    ----------
    theme_element : float
        Value in points.
    """


class legend_position_inside(themeable):
    """
    Location of legend

    Parameters
    ----------
    theme_element : tuple[float, float]
        Where to place legends that are inside the panels / facets area.
        The values should be in the range `[0, 1]`. The default is to
        put it in the center (`(.5, .5)`) of the panels area.
    """


class legend_position(legend_position_inside):
    """
    Location of legend

    Parameters
    ----------
    theme_element : Literal["right", "left", "top", "bottom", "inside"] | \
                    tuple[float, float] | Literal["none"]
        Where to put the legend. Along the edge or inside the panels.

        If "inside", the default location is
        [](:class:`~plotnine.themes.themeable.legend_position_inside`).

        A tuple of values implies "inside" the panels at those exact values,
        which should be in the range `[0, 1]` within the panels area.

        A value of `"none"` turns off the legend.
    """


class legend_title_position(themeable):
    """
    Position of legend title

    Parameters
    ----------
    theme_element : Literal["top", "bottom", "left", "right"] | None
        Position of the legend title. The default depends on the position
        of the legend.
    """


class legend_text_position(themeable):
    """
    Position of the legend text

    Alignment of legend title

    Parameters
    ----------
    theme_element : Literal["top", "bottom", "left", "right"] | \
                    Sequence[Literal["top", "bottom"]] | \
                    Sequence[Literal["left", "right"]] | \
                    Literal["top-bottom", "bottom-top"] | \
                    Literal["left-right", "right-left"] | \
                    None
        Position of the legend key text.
        It must be compatible with the position of the legend e.g.
        when the legend is at the top or bottom, text can only be top
        or bottom as well.
        The default depends on the position of the legend.
        Use a sequence to specify the position of each text, or
        hyphenated values like `"left-right"` to alternate the position.

    Notes
    -----
    Sequences and alternation only works well for colorbars.
    """


class legend_key_spacing_x(themeable):
    """
    Horizontal spacing between two entries in a legend

    Parameters
    ----------
    theme_element : int
        Size in points
    """


class legend_key_spacing_y(themeable):
    """
    Vertical spacing between two entries in a legend

    Parameters
    ----------
    theme_element : int
        Size in points
    """


class legend_key_spacing(legend_key_spacing_x, legend_key_spacing_y):
    """
    Spacing between two entries in a legend

    Parameters
    ----------
    theme_element : int
        Size in points
    """


class strip_align_x(themeable):
    """
    Vertical alignment of the strip & its background w.r.t the panel border

    Parameters
    ----------
    theme_element : float
        Value as a proportion of the strip size. A good value
        should be the range `[-1, 0.5]`. A negative value
        puts the strip inside the axes. A positive value creates
        a margin between the strip and the axes. `0` puts the
        strip on top of the panels.
    """


class strip_align_y(themeable):
    """
    Horizontal alignment of the strip & its background w.r.t the panel border

    Parameters
    ----------
    theme_element : float
        Value as a proportion of the strip size. A good value
        should be the range `[-1, 0.5]`. A negative value
        puts the strip inside the axes. A positive value creates
        a margin between the strip and the axes. `0` puts the
        strip exactly beside the panels.
    """


class strip_align(strip_align_x, strip_align_y):
    """
    Alignment of the strip & its background w.r.t the panel border

    Parameters
    ----------
    theme_element : float
        Value as a proportion of the strip text size. A good value
        should be the range `[-1, 0.5]`. A negative value
        puts the strip inside the axes and a positive value
        creates a space between the strip and the axes.
    """


class svg_usefonts(themeable):
    """
    How to renderer fonts for svg images

    Parameters
    ----------
    theme_element : bool
        If `True`, assume fonts are installed on the machine where
        the SVG will be viewed.

        If `False`, embed characters as paths; this is supported by
        most SVG renderers.

        You should probably set this to `True` if you intend to edit
        the svg file.
    """

    @property
    def rcParams(self) -> dict[str, Any]:
        rcParams = super().rcParams

        rcParams["svg.fonttype"] = (
            "none" if self.properties.get("value") else "path"
        )
        return rcParams


# Deprecated


class subplots_adjust(themeable):
    def apply_figure(self, figure: Figure, targets: ThemeTargets):
        warn(
            "You no longer need to use subplots_adjust to make space for "
            "the legend or text around the panels. This parameter will be "
            "removed in a future version. You can still use 'plot_margin' "
            "'panel_spacing' for your other spacing needs.",
            FutureWarning,
        )


@deprecated_themeable_name
class legend_entry_spacing(legend_key_spacing):
    pass


@deprecated_themeable_name
class legend_entry_spacing_x(legend_key_spacing_x):
    pass


@deprecated_themeable_name
class legend_entry_spacing_y(legend_key_spacing_y):
    pass


class legend_title_align(themeable):
    def __init__(self):
        msg = (
            "Themeable 'legend_title_align' is deprecated. Use the "
            "horizontal and vertical alignment parameters ha & va "
            "of 'element_text' with 'lenged_title'."
        )
        warn(msg, FutureWarning, stacklevel=1)


class axis_ticks_direction_x(themeable):
    """
    x-axis tick direction

    Parameters
    ----------
    theme_element : Literal["in", "out"]
        `in` for ticks inside the panel.
        `out` for ticks outside the panel.
    """

    def __init__(self, theme_element):
        msg = (
            f"Themeable '{self.__class__.__name__}' is deprecated and"
            "will be removed in a future version. "
            "Use +ve or -ve values of the axis_ticks_length"
            "to affect the direction of the ticks."
        )
        warn(msg, FutureWarning, stacklevel=1)
        super().__init__(theme_element)

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.xaxis.set_tick_params(
            which="major", tickdir=self.properties["value"]
        )


class axis_ticks_direction_y(themeable):
    """
    y-axis tick direction

    Parameters
    ----------
    theme_element : Literal["in", "out"]
        `in` for ticks inside the panel.
        `out` for ticks outside the panel.
    """

    def __init__(self, theme_element):
        msg = (
            f"Themeable '{self.__class__.__name__}' is deprecated and"
            "will be removed in a future version. "
            "Use +ve/-ve/complex values of the axis_ticks_length"
            "to affect the direction of the ticks."
        )
        warn(msg, FutureWarning, stacklevel=1)
        super().__init__(theme_element)

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        ax.yaxis.set_tick_params(
            which="major", tickdir=self.properties["value"]
        )


class axis_ticks_direction(axis_ticks_direction_x, axis_ticks_direction_y):
    """
    axis tick direction

    Parameters
    ----------
    theme_element : Literal["in", "out"]
        `in` for ticks inside the panel.
        `out` for ticks outside the panel.
    """


class axis_ticks_pad_major_x(themeable):
    """
    x-axis major-tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        val = self.properties["value"]

        for t in ax.xaxis.get_major_ticks():
            _val = val if t.tick1line.get_visible() else 0
            t.set_pad(_val)


class axis_ticks_pad_major_y(themeable):
    """
    y-axis major-tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_major_y`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_major_y`)
    is zero.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        val = self.properties["value"]

        for t in ax.yaxis.get_major_ticks():
            _val = val if t.tick1line.get_visible() else 0
            t.set_pad(_val)


class axis_ticks_pad_major(axis_ticks_pad_major_x, axis_ticks_pad_major_y):
    """
    Axis major-tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_major`) are blank,
    but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_major`) is zero.
    """


class axis_ticks_pad_minor_x(themeable):
    """
    x-axis minor-tick padding

    Parameters
    ----------
    theme_element : float

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_minor_x`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_minor_x`) is zero.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        val = self.properties["value"]

        for t in ax.xaxis.get_minor_ticks():
            _val = val if t.tick1line.get_visible() else 0
            t.set_pad(_val)


class axis_ticks_pad_minor_y(themeable):
    """
    y-axis minor-tick padding

    Parameters
    ----------
    theme_element : float

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_minor_y`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_minor_y`)
    is zero.
    """

    def apply_ax(self, ax: Axes):
        super().apply_ax(ax)
        val = self.properties["value"]

        for t in ax.yaxis.get_minor_ticks():
            _val = val if t.tick1line.get_visible() else 0
            t.set_pad(_val)


class axis_ticks_pad_minor(axis_ticks_pad_minor_x, axis_ticks_pad_minor_y):
    """
    Axis minor-tick padding

    Parameters
    ----------
    theme_element : float

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks_minor`) are
    blank, but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length_minor`) is zero.
    """


class axis_ticks_pad(axis_ticks_pad_major, axis_ticks_pad_minor):
    """
    Axis tick padding

    Parameters
    ----------
    theme_element : float
        Value in points.

    Note
    ----
    Padding is not applied when the
    [](`~plotnine.theme.themeables.axis_ticks`) are blank,
    but it does apply when the
    [](`~plotnine.theme.themeables.axis_ticks_length`) is zero.
    """

    def __init__(self, theme_element):
        x = theme_element
        msg = (
            f"Themeable '{self.__class__.__name__}' is deprecated and"
            "will be removed in a future version. "
            "Use the margin parameter of axis_text. e.g.\n"
            f"axis_text_x(margin={{'t': {x}}})\n"
            f"axis_text_y(margin={{'r': {x}}})\n"
            f"axis_text(margin={{'t': {x}, 'r': {x}}})"
        )
        warn(msg, FutureWarning, stacklevel=1)
        super().__init__(theme_element)
</file>

<file path="plotnine/themes/theme.py">
from __future__ import annotations

import typing
from copy import copy, deepcopy
from functools import cached_property
from typing import overload

from ..exceptions import PlotnineError
from ..options import get_option, set_option
from .targets import ThemeTargets
from .themeable import Themeables, themeable

if typing.TYPE_CHECKING:
    from typing import Type

    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from typing_extensions import Self

    from plotnine import ggplot

    from .elements import margin


# All complete themes are initiated with these rcparams. They
# can be overridden.
DEFAULT_RCPARAMS = {
    "axes.axisbelow": "True",
    "font.sans-serif": [
        "Helvetica",
        "DejaVu Sans",  # MPL ships with this one
        "Avant Garde",
        "Computer Modern Sans serif",
        "Arial",
    ],
    "font.serif": [
        "Times",
        "Palatino",
        "New Century Schoolbook",
        "Bookman",
        "Computer Modern Roman",
        "Times New Roman",
    ],
    "lines.antialiased": "True",
    "patch.antialiased": "True",
    "timezone": "UTC",
}


class theme:
    """
    Base class for themes

    In general, only complete themes should subclass this class.

    Parameters
    ----------
    complete : bool
        Themes that are complete will override any existing themes.
        themes that are not complete (ie. partial) will add to or
        override specific elements of the current theme. e.g:

        ```python
        theme_gray() + theme_xkcd()
        ```

        will be completely determined by [](`~plotnine.themes.theme_xkcd`),
        but:

        ```python
        theme_gray() + theme(axis_text_x=element_text(angle=45))
        ```

        will only modify the x-axis text.
    kwargs: Any
        kwargs are `themeables`. The themeables are elements that are
        subclasses of `themeable`. Many themeables are defined using
        theme elements i.e

        - [](`~plotnine.themes.element_line`)
        - [](`~plotnine.themes.element_rect`)
        - [](`~plotnine.themes.element_text`)

        These simply bind together all the aspects of a themeable
        that can be themed. See [](`~plotnine.themes.themeable.themeable`).

    Notes
    -----
    When subclassing, make sure to call `theme.__init__`{.py}.
    After which you can customise `self._rcParams`{.py} within
    the `__init__` method of the new theme. The `rcParams`
    should not be modified after that.
    """

    complete: bool

    # This is set when the figure is created,
    # it is useful at legend drawing time and
    # when applying the theme.
    plot: ggplot
    figure: Figure
    axs: list[Axes]

    # Dictionary to collect matplotlib objects that will
    # be targeted for theming by the themeables
    # It is initialised in the setup method.
    targets: ThemeTargets
    _is_retina = False

    def __init__(
        self,
        complete=False,
        # Generate themeables keyword parameters with
        #
        #     from plotnine.themes.themeable import themeable
        #     for name in themeable.registry():
        #         print(f'{name}=None,')
        axis_title_x=None,
        axis_title_y=None,
        axis_title=None,
        legend_title=None,
        legend_text_legend=None,
        legend_text_colorbar=None,
        legend_text=None,
        plot_title=None,
        plot_subtitle=None,
        plot_caption=None,
        plot_footer=None,
        plot_tag=None,
        plot_title_position=None,
        plot_caption_position=None,
        plot_footer_position=None,
        plot_tag_location=None,
        plot_tag_position=None,
        strip_text_x=None,
        strip_text_y=None,
        strip_text=None,
        title=None,
        axis_text_x=None,
        axis_text_y=None,
        axis_text=None,
        text=None,
        axis_line_x=None,
        axis_line_y=None,
        axis_line=None,
        axis_ticks_minor_x=None,
        axis_ticks_minor_y=None,
        axis_ticks_major_x=None,
        axis_ticks_major_y=None,
        axis_ticks_major=None,
        axis_ticks_minor=None,
        axis_ticks_x=None,
        axis_ticks_y=None,
        axis_ticks=None,
        legend_ticks=None,
        panel_grid_major_x=None,
        panel_grid_major_y=None,
        panel_grid_minor_x=None,
        panel_grid_minor_y=None,
        panel_grid_major=None,
        panel_grid_minor=None,
        panel_grid=None,
        plot_footer_line=None,
        line=None,
        legend_key=None,
        legend_frame=None,
        legend_background=None,
        legend_box_background=None,
        panel_background=None,
        panel_border=None,
        plot_background=None,
        plot_footer_background=None,
        strip_background_x=None,
        strip_background_y=None,
        strip_background=None,
        rect=None,
        axis_ticks_length_major_x=None,
        axis_ticks_length_major_y=None,
        axis_ticks_length_major=None,
        axis_ticks_length_minor_x=None,
        axis_ticks_length_minor_y=None,
        axis_ticks_length_minor=None,
        axis_ticks_length=None,
        panel_spacing_x=None,
        panel_spacing_y=None,
        panel_spacing=None,
        plot_margin_left=None,
        plot_margin_right=None,
        plot_margin_top=None,
        plot_margin_bottom=None,
        plot_margin=None,
        panel_ontop=None,
        aspect_ratio=None,
        dpi=None,
        figure_size=None,
        legend_box=None,
        legend_box_margin=None,
        legend_box_just=None,
        legend_justification_right=None,
        legend_justification_left=None,
        legend_justification_top=None,
        legend_justification_bottom=None,
        legend_justification_inside=None,
        legend_justification=None,
        legend_direction=None,
        legend_key_width=None,
        legend_key_height=None,
        legend_key_size=None,
        legend_ticks_length=None,
        legend_margin=None,
        legend_box_spacing=None,
        legend_spacing=None,
        legend_position_inside=None,
        legend_position=None,
        legend_title_position=None,
        legend_text_position=None,
        legend_key_spacing_x=None,
        legend_key_spacing_y=None,
        legend_key_spacing=None,
        strip_align_x=None,
        strip_align_y=None,
        strip_align=None,
        svg_usefonts=None,
        **kwargs,
    ):
        self.themeables = Themeables()
        self.complete = complete

        if complete:
            self._rcParams = deepcopy(DEFAULT_RCPARAMS)
        else:
            self._rcParams = {}

        # Themeables
        official_themeables = themeable.registry()
        locals_args = dict(locals())
        it = (
            (name, element)
            for name, element in locals_args.items()
            if element is not None and name in official_themeables
        )
        new = themeable.from_class_name

        for name, element in it:
            self.themeables[name] = new(name, element)

        # Unofficial themeables for extensions
        # or those that have been deprecated
        for name, element in kwargs.items():
            self.themeables[name] = new(name, element)

    def __eq__(self, other: object) -> bool:
        """
        Test if themes are equal

        Mostly for testing purposes
        """
        return other is self or (
            isinstance(other, type(self))
            and other.themeables == self.themeables
            and other.rcParams == self.rcParams
        )

    @cached_property
    def T(self):
        """
        Convenient access to the themeables
        """
        return self.themeables

    @cached_property
    def getp(self):
        """
        Convenient access into the properties of the themeables
        """
        return self.themeables.getp

    def get_margin(self, name: str) -> margin:
        """
        Return the margin propery of a element_text themeables
        """
        return self.themeables.getp((name, "margin"))

    @cached_property
    def get_ha(self):
        return self.themeables.get_ha

    @cached_property
    def get_va(self):
        return self.themeables.get_va

    def apply(self):
        """
        Apply this theme, then apply additional modifications in order.

        This method will be called once after plot has completed.
        Subclasses that override this method should make sure that the
        base class method is called.
        """
        for th in self.T.values():
            th.apply(self)

    def _setup(
        self,
        figure: Figure,
        axs: list[Axes] | None = None,
        title: str | None = None,
        subtitle: str | None = None,
    ):
        """
        Setup theme for applying

        This method will be called when the figure and axes have been created
        but before any plotting or other artists have been added to the
        figure. This method gives the theme and the elements references to
        the figure and/or axes.

        It also initialises where the artists to be themed will be stored.
        """
        self.figure = figure
        self.axs = axs if axs is not None else []

        if title or subtitle:
            self._smart_title_and_subtitle_ha(title, subtitle)

        self.targets = ThemeTargets()
        self.T.setup(self)

    @property
    def rcParams(self):
        """
        Return rcParams dict for this theme.

        Notes
        -----
        Subclasses should not need to override this method method as long as
        self._rcParams is constructed properly.

        rcParams are used during plotting. Sometimes the same theme can be
        achieved by setting rcParams before plotting or a apply
        after plotting. The choice of how to implement it is is a matter of
        convenience in that case.

        There are certain things can only be themed after plotting. There
        may not be an rcParam to control the theme or the act of plotting
        may cause an entity to come into existence before it can be themed.

        """
        try:
            rcParams = deepcopy(self._rcParams)
        except NotImplementedError:
            # deepcopy raises an error for objects that are derived from or
            # composed of matplotlib.transform.TransformNode.
            # Not desirable, but probably requires upstream fix.
            # In particular, XKCD uses matplotlib.patheffects.withStrok
            rcParams = copy(self._rcParams)

        for th in self.T.values():
            rcParams.update(th.rcParams)
        return rcParams

    def add_theme(self, other: theme) -> theme:
        """
        Add themes together

        Subclasses should not override this method.

        This will be called when adding two instances of class 'theme'
        together.
        A complete theme will annihilate any previous themes. Partial themes
        can be added together and can be added to a complete theme.
        """
        if other.complete:
            return other

        self.themeables.update(deepcopy(other.themeables))
        return self

    def __add__(self, other: theme) -> theme:
        """
        Add other theme to this theme
        """
        if not isinstance(other, theme):
            msg = f"Adding theme failed. {other} is not a theme"
            raise PlotnineError(msg)
        self = deepcopy(self)
        return self.add_theme(other)

    @overload
    def __radd__(self, other: theme) -> theme: ...

    @overload
    def __radd__(self, other: ggplot) -> ggplot: ...

    def __radd__(self, other: theme | ggplot) -> theme | ggplot:
        """
        Add theme to ggplot object or to another theme

        This will be called in one of two ways:

        ```python
        ggplot() + theme()
        theme1() + theme2()
        ```

        In both cases, `self` is the [](`~plotnine.themes.theme`)
        on the right hand side.

        Subclasses should not override this method.
        """
        # ggplot() + theme, get theme
        # if hasattr(other, 'theme'):
        if not isinstance(other, theme):
            if self.complete:
                other.theme = self
            else:
                # If no theme has been added yet,
                # we modify the default theme
                other.theme = other.theme or theme_get()
                other.theme = other.theme.add_theme(self)
            return other
        # theme1 + theme2
        else:
            if self.complete:
                # e.g. other + theme_gray()
                return self
            else:
                # e.g. other + theme(...)
                return other.add_theme(self)

    def __iadd__(self, other: theme) -> Self:
        """
        Add theme to theme
        """
        self.add_theme(other)
        return self

    def __deepcopy__(self, memo: dict) -> theme:
        """
        Deep copy without copying the figure
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        shallow = {"plot", "figure", "axs"}
        skip = {"targets"}
        for key, item in old.items():
            if key in skip:
                continue
            elif key in shallow:
                new[key] = item
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)

        return result

    def to_retina(self) -> theme:
        """
        Return a retina-sized version of this theme

        The result is a theme that has double the dpi.
        """
        if self._is_retina:
            return deepcopy(self)

        dpi = self.getp("dpi")
        self = self + theme(dpi=dpi * 2)
        self._is_retina = True
        return self

    def _smart_title_and_subtitle_ha(
        self, title: str | None, subtitle: str | None
    ):
        """
        Smartly add the horizontal alignment for the title and subtitle
        """
        from .elements import element_text

        has_title = bool(title) and not self.T.is_blank("plot_title")
        has_subtitle = bool(subtitle) and not self.T.is_blank("plot_subtitle")

        title_ha = self.getp(("plot_title", "ha"))
        subtitle_ha = self.getp(("plot_subtitle", "ha"))

        default_title_ha, default_subtitle_ha = "center", "left"
        kwargs = {}

        if has_title and title_ha is None:
            if has_subtitle and not subtitle_ha:
                title_ha = default_subtitle_ha
            else:
                title_ha = default_title_ha
            kwargs["plot_title"] = element_text(ha=title_ha)

        if has_subtitle and subtitle_ha is None:
            subtitle_ha = default_subtitle_ha
            kwargs["plot_subtitle"] = element_text(ha=subtitle_ha)

        if kwargs:
            self += theme(**kwargs)

    @property
    def _figure_size_px(self) -> tuple[int, int]:
        """
        Return the size of the output in pixels
        """
        dpi = self.getp("dpi")
        width, height = self.getp("figure_size")
        return (int(width * dpi), int(height * dpi))


def theme_get() -> theme:
    """
    Return the default theme

    The default theme is the one set (using [](`~plotnine.themes.theme_set`))
    by the user. If none has been set, then [](`~plotnine.themes.theme_gray`)
    is the default.
    """
    from .theme_gray import theme_gray

    _theme = get_option("current_theme")
    if isinstance(_theme, type):
        _theme = _theme()
    return _theme or theme_gray()


def theme_set(new: theme | Type[theme]) -> theme:
    """
    Change the current(default) theme

    Parameters
    ----------
    new : theme
        New default theme

    Returns
    -------
    out : theme
        Previous theme
    """
    if not isinstance(new, theme) and not issubclass(new, theme):
        raise PlotnineError("Expecting object to be a theme")

    out: theme = get_option("current_theme")
    set_option("current_theme", new)
    return out


def theme_update(**kwargs: themeable):
    """
    Modify elements of the current theme

    Parameters
    ----------
    kwargs : dict
        Theme elements
    """
    assert "complete" not in kwargs
    theme_set(theme_get() + theme(**kwargs))  # pyright: ignore
</file>

<file path="plotnine/geoms/geom.py">
from __future__ import annotations

import typing
from abc import ABC
from contextlib import suppress
from copy import deepcopy
from itertools import chain, repeat

import numpy as np

from .._utils import (
    data_mapping_as_kwargs,
    remove_missing,
)
from .._utils.registry import Register
from ..exceptions import PlotnineError
from ..layer import layer
from ..mapping.aes import rename_aesthetics
from ..mapping.evaluation import evaluate

if typing.TYPE_CHECKING:
    from typing import Any

    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.offsetbox import DrawingArea

    from plotnine import aes, ggplot
    from plotnine.coords.coord import coord
    from plotnine.facets.layout import Layout
    from plotnine.iapi import panel_view
    from plotnine.mapping import Environment
    from plotnine.typing import DataLike


_BASE_PARAMS: dict[str, Any] = {
    "stat": "identity",
    "position": "identity",
    "na_rm": False,
}


class geom(ABC, metaclass=Register):
    """Base class of all Geoms"""

    DEFAULT_AES: dict[str, Any] = {}
    """Default aesthetics for the geom"""

    REQUIRED_AES: set[str] = set()
    """Required aesthetics for the geom"""

    NON_MISSING_AES: set[str] = set()
    """Required aesthetics for the geom"""

    DEFAULT_PARAMS: dict[str, Any] = {}
    """Required parameters for the geom"""

    data: DataLike
    """Geom/layer specific dataframe"""

    mapping: aes
    """Mappings i.e. `aes(x="col1", fill="col2")`{.py}"""

    aes_params: dict[str, Any] = {}  # setting of aesthetic
    params: dict[str, Any]  # parameter settings

    # Plot namespace, it gets its value when the plot is being
    # built.
    environment: Environment

    # The geom responsible for the legend if draw_legend is
    # not implemented
    legend_geom: str = "point"

    # Documentation for the aesthetics. It is added under the
    # documentation for mapping parameter. Use {aesthetics}
    # placeholder to insert a table for all the aesthetics and
    # their default values.
    _aesthetics_doc: str = "{aesthetics_table}"

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        kwargs = rename_aesthetics(kwargs)
        kwargs = data_mapping_as_kwargs((data, mapping), kwargs)
        self._raw_kwargs = kwargs  # Will be used to create stat & layer

        # separate aesthetics and parameters
        possible_params = _BASE_PARAMS | self.DEFAULT_PARAMS
        self.aes_params = {
            ae: kwargs[ae] for ae in self.aesthetics() & set(kwargs)
        }
        self.params = possible_params | {
            k: v for k, v in kwargs.items() if k in possible_params
        }
        self.mapping = kwargs["mapping"]
        self.data = kwargs["data"]

    @classmethod
    def aesthetics(cls: type[geom]) -> set[str]:
        """
        Return all the aesthetics for this geom

        geoms should not override this method.
        """
        main = cls.DEFAULT_AES.keys() | cls.REQUIRED_AES
        other = {"group"}
        # Need to recognize both spellings
        if "color" in main:
            other.add("colour")
        if "outlier_color" in main:
            other.add("outlier_colour")
        return main | other

    def __deepcopy__(self, memo: dict[Any, Any]) -> geom:
        """
        Deep copy without copying the self.data dataframe

        geoms should not override this method.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a deepcopy of data, or environment
        shallow = {"data", "_raw_kwargs", "environment"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item  # pyright: ignore[reportIndexIssue]
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)  # pyright: ignore[reportIndexIssue]

        return result

    def setup_params(self, data: pd.DataFrame):
        """
        Override this method to verify and/or adjust parameters

        Parameters
        ----------
        data :
            Data
        """

    def setup_aes_params(self, data: pd.DataFrame):
        """
        Override this method to verify and/or adjust aesthetic parameters

        Parameters
        ----------
        data :
            Data
        """

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the data before drawing takes place

        This function is called *before* position adjustments are done.
        It is used by geoms to create the final aesthetics used for
        drawing. The base class method does nothing, geoms can override
        this method for two reasons:

        1. The `stat` does not create all the aesthetics (usually
           position aesthetics) required for drawing the `geom`,
           but those aesthetics can be computed from the available
           data. For example [](`~plotnine.geoms.geom_boxplot`)
           and [](`~plotnine.geoms.geom_violin`).

        2. The `geom` inherits from another `geom` (superclass) which
           does the drawing and the superclass requires certain aesthetics
           to be present in the data. For example
           [](`~plotnine.geoms.geom_tile`) and
           [](`~plotnine.geoms.geom_area`).

        Parameters
        ----------
        data :
            Data used for drawing the geom.

        Returns
        -------
        :
            Data used for drawing the geom.
        """
        return data

    def use_defaults(
        self, data: pd.DataFrame, aes_modifiers: dict[str, Any]
    ) -> pd.DataFrame:
        """
        Combine data with defaults and set aesthetics from parameters

        geoms should not override this method.

        Parameters
        ----------
        data :
            Data used for drawing the geom.
        aes_modifiers :
            Aesthetics to evaluate

        Returns
        -------
        :
            Data used for drawing the geom.
        """
        from plotnine.mapping import _atomic as atomic
        from plotnine.mapping._atomic import ae_value

        missing_aes = (
            self.DEFAULT_AES.keys()
            - self.aes_params.keys()
            - set(data.columns.to_list())
        )

        # Not in data and not set, use default
        for ae in missing_aes:
            data[ae] = self.DEFAULT_AES[ae]

        # Evaluate/Modify the mapped aesthetics
        evaled = evaluate(aes_modifiers, data, self.environment)
        for ae in evaled.columns.intersection(data.columns):
            data[ae] = evaled[ae]

        num_panels = len(data["PANEL"].unique()) if "PANEL" in data else 1
        across_panels = num_panels > 1 and not self.params["inherit_aes"]

        # Aesthetics set as parameters in the geom/stat
        for ae, value in self.aes_params.items():
            if isinstance(value, (str, int, float, np.integer, np.floating)):
                data[ae] = value
            elif isinstance(value, ae_value):
                data[ae] = value * len(data)
            elif across_panels:
                value = list(chain(*repeat(value, num_panels)))
                data[ae] = value
            else:
                # Try to make sense of aesthetics whose values can be tuples
                # or sequences of sorts.
                ae_value_cls: type[ae_value] | None = getattr(atomic, ae, None)
                if ae_value_cls:
                    with suppress(ValueError):
                        data[ae] = ae_value_cls(value) * len(data)
                        continue

                # This should catch the aesthetic assignments to
                # non-numeric or non-string values or sequence of values.
                # e.g. x=datetime, x=Sequence[datetime],
                #      x=Sequence[float], shape=Sequence[str]
                try:
                    data[ae] = value
                except ValueError as e:
                    msg = f"'{ae}={value}' does not look like a valid value"
                    raise PlotnineError(msg) from e

        return data

    def draw_layer(self, data: pd.DataFrame, layout: Layout, coord: coord):
        """
        Draw layer across all panels

        geoms should not override this method.

        Parameters
        ----------
        data :
            DataFrame specific for this layer
        layout :
            Layout object created when the plot is getting
            built
        coord :
            Type of coordinate axes
        params :
            Combined *geom* and *stat* parameters. Also
            includes the stacking order of the layer in
            the plot (*zorder*)
        """
        for pid, pdata in data.groupby("PANEL", observed=True):
            if len(pdata) == 0:
                continue
            ploc = pdata["PANEL"].iloc[0] - 1
            panel_params = layout.panel_params[ploc]
            ax = layout.axs[ploc]
            self.draw_panel(pdata, panel_params, coord, ax)

    def draw_panel(
        self,
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
    ):
        """
        Plot all groups

        For efficiency, geoms that do not need to partition
        different groups before plotting should override this
        method and avoid the groupby.

        Parameters
        ----------
        data :
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params :
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Attributes are of interest
            to the geom are:

            ```python
            "panel_params.x.range"  # tuple
            "panel_params.y.range"  # tuple
            ```
        coord :
            Coordinate (e.g. coord_cartesian) system of the geom.
        ax :
            Axes on which to plot.
        params :
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        for _, gdata in data.groupby("group"):
            gdata.reset_index(inplace=True, drop=True)
            self.draw_group(gdata, panel_params, coord, ax, self.params)

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        """
        Plot data belonging to a group.

        Parameters
        ----------
        data :
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params :
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Keys of interest to
            the geom are:

            ```python
            "x_range"  # tuple
            "y_range"  # tuple
            ```
        coord : coord
            Coordinate (e.g. coord_cartesian) system of the geom.
        ax : axes
            Axes on which to plot.
        params : dict
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        msg = "The geom should implement this method."
        raise NotImplementedError(msg)

    @staticmethod
    def draw_unit(
        data: pd.DataFrame,
        panel_params: panel_view,
        coord: coord,
        ax: Axes,
        params: dict[str, Any],
    ):
        """
        Plot data belonging to a unit.

        A matplotlib plot function may require that an aethestic
        have a single unique value. e.g. `linestyle="dashed"`{.py}
        and not `linestyle=["dashed", "dotted", ...]`{.py}.
        A single call to such a function can only plot lines with
        the same linestyle. However, if the plot we want has more
        than one line with different linestyles, we need to group
        the lines with the same linestyle and plot them as one
        unit. In this case, draw_group calls this function to do
        the plotting. For an example see
        [](`~plotnine.geoms.geom_point`).

        Parameters
        ----------
        data :
            Data to be plotted by this geom. This is the
            dataframe created in the plot_build pipeline.
        panel_params :
            The scale information as may be required by the
            axes. At this point, that information is about
            ranges, ticks and labels. Keys of interest to
            the geom are:

            ```python
            "x_range"  # tuple
            "y_range"  # tuple
            ```

            In rare cases a geom may need access to the x or y scales.
            Those are available at:

            ```python
            "scales"   # SimpleNamespace
            ```
        coord :
            Coordinate (e.g. coord_cartesian) system of the
            geom.
        ax :
            Axes on which to plot.
        params :
            Combined parameters for the geom and stat. Also
            includes the `zorder`.
        """
        msg = "The geom should implement this method."
        raise NotImplementedError(msg)

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add layer representing geom object on the right

        Parameters
        ----------
        plot :
            ggplot object

        Returns
        -------
        :
            ggplot object with added layer.
        """
        other += layer(geom=self)
        return other

    def handle_na(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows with NaN values

        geoms that infer extra information from missing values
        should override this method. For example
        [](`~plotnine.geoms.geom_path`).

        Parameters
        ----------
        data :
            Data

        Returns
        -------
        :
            Data without the NaNs.

        Notes
        -----
        Shows a warning if the any rows are removed and the
        `na_rm` parameter is False. It only takes into account
        the columns of the required aesthetics.
        """
        return remove_missing(
            data,
            self.params.get("na_rm", False),
            list(self.REQUIRED_AES | self.NON_MISSING_AES),
            self.__class__.__name__,
        )

    @staticmethod
    def draw_legend(
        data: pd.Series[Any], da: DrawingArea, lyr: layer
    ) -> DrawingArea:
        """
        Draw a rectangle in the box

        Parameters
        ----------
        data :
            A row of the data plotted to this layer
        da :
            Canvas on which to draw
        lyr :
            Layer that the geom belongs to.

        Returns
        -------
        :
            The DrawingArea after a layer has been drawn onto it.
        """
        msg = "The geom should implement this method."
        raise NotImplementedError(msg)

    @staticmethod
    def legend_key_size(
        data: pd.Series[Any], min_size: tuple[int, int], lyr: layer
    ) -> tuple[int, int]:
        """
        Calculate the size of key that would fit the layer contents

        Parameters
        ----------
        data :
            A row of the data plotted to this layer
        min_size :
            Initial size which should be expanded to fit the contents.
        lyr :
            Layer
        """
        return min_size
</file>

<file path="plotnine/stats/stat.py">
from __future__ import annotations

import typing
from copy import deepcopy
from warnings import warn

import pandas as pd

from .._utils import (
    check_required_aesthetics,
    data_mapping_as_kwargs,
    groupby_apply,
    remove_missing,
    uniquecols,
)
from .._utils.registry import Register
from ..layer import layer
from ..mapping import aes

if typing.TYPE_CHECKING:
    from typing import Any

    from plotnine import ggplot
    from plotnine.facets.layout import Layout
    from plotnine.iapi import pos_scales
    from plotnine.mapping import Environment
    from plotnine.typing import DataLike

from abc import ABC

_BASE_PARAMS = {
    "geom": "blank",
    "position": "identity",
    "na_rm": False,
}

DROPPED_TPL = """
The following aesthetics were dropped during processing: {dropped}.
plotnine could not infer the correct grouping.
Did you forget to specify a `group` aesthetic or to convert a numerical \
variable into a categorial?
"""


class stat(ABC, metaclass=Register):
    """Base class of all stats"""

    DEFAULT_AES: dict[str, Any] = {}
    """Default aesthetics for the stat"""

    REQUIRED_AES: set[str] = set()
    """Required aesthetics for the stat"""

    NON_MISSING_AES: set[str] = set()
    """Required aesthetics for the stat"""

    DEFAULT_PARAMS: dict[str, Any] = {}
    """Required parameters for the stat"""

    CREATES: set[str] = set()
    """
    Stats may modify existing columns or create extra
    columns.

    Any extra columns that may be created by the stat
    should be specified in this set
    see: stat_bin

    Documentation for the aesthetics. It ie added under the
    documentation for mapping parameter. Use {aesthetics_table}
    placeholder to insert a table for all the aesthetics and
    their default values.
    """

    _aesthetics_doc = "{aesthetics_table}"

    # Plot namespace, it gets its value when the plot is being
    # built.
    environment: Environment

    def __init__(
        self,
        mapping: aes | None = None,
        data: DataLike | None = None,
        **kwargs: Any,
    ):
        possible_params = _BASE_PARAMS | self.DEFAULT_PARAMS
        possible_params_set = set(possible_params)
        kwargs = data_mapping_as_kwargs((data, mapping), kwargs)
        self._raw_kwargs = kwargs  # Will be used to create the geom
        self.params = possible_params | {
            k: v for k, v in kwargs.items() if k in possible_params_set
        }
        self.DEFAULT_AES = aes(**self.DEFAULT_AES)
        self.aes_params = {
            ae: kwargs[ae] for ae in self.aesthetics() & set(kwargs)
        }

    def __deepcopy__(self, memo: dict[Any, Any]) -> stat:
        """
        Deep copy without copying the self.data dataframe

        stats should not override this method.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        # don't make a _raw_kwargs
        shallow = {"_raw_kwargs"}
        for key, item in old.items():
            if key in shallow:
                new[key] = item  # pyright: ignore[reportIndexIssue]
                memo[id(new[key])] = new[key]
            else:
                new[key] = deepcopy(item, memo)  # pyright: ignore[reportIndexIssue]

        return result

    @classmethod
    def aesthetics(cls) -> set[str]:
        """
        Return a set of all non-computed aesthetics for this stat.

        stats should not override this method.
        """
        aesthetics = cls.REQUIRED_AES.copy()
        calculated = aes(**cls.DEFAULT_AES)._calculated
        for ae in set(cls.DEFAULT_AES) - set(calculated):
            aesthetics.add(ae)
        return aesthetics

    def use_defaults(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Combine data with defaults and set aesthetics from parameters

        stats should not override this method.

        Parameters
        ----------
        data :
            Data used for drawing the geom.

        Returns
        -------
        out :
            Data used for drawing the geom.
        """
        missing = (
            self.aesthetics() - set(self.aes_params.keys()) - set(data.columns)
        )

        for ae in missing - self.REQUIRED_AES:
            if self.DEFAULT_AES[ae] is not None:
                data[ae] = self.DEFAULT_AES[ae]

        missing = self.aes_params.keys() - set(data.columns)

        for ae in self.aes_params:
            data[ae] = self.aes_params[ae]

        return data

    def setup_params(self, data: pd.DataFrame):
        """
        Override this to verify and/or adjust parameters

        Parameters
        ----------
        data :
            Data

        Returns
        -------
        out :
            Parameters used by the stats.
        """

    def setup_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Override to modify data before compute_layer is called

        Parameters
        ----------
        data :
            Data

        Returns
        -------
        out :
            Data
        """
        return data

    def finish_layer(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Modify data after the aesthetics have been mapped

        This can be used by stats that require access to the mapped
        values of the computed aesthetics, part 3 as shown below.

            1. stat computes and creates variables
            2. variables mapped to aesthetics
            3. stat sees and modifies data according to the
               aesthetic values

        The default to is to do nothing.

        Parameters
        ----------
        data :
            Data for the layer
        params :
            Parameters

        Returns
        -------
        data :
            Modified data
        """
        return data

    def compute_layer(
        self, data: pd.DataFrame, layout: Layout
    ) -> pd.DataFrame:
        """
        Calculate statistics for this layers

        This is the top-most computation method for the
        stat. It does not do any computations, but it
        knows how to verify the data, partition it call the
        next computation method and merge results.

        stats should not override this method.

        Parameters
        ----------
        data :
            Data points for all objects in a layer.
        layout :
            Panel layout information
        """
        check_required_aesthetics(
            self.REQUIRED_AES,
            list(data.columns) + list(self.params.keys()),
            self.__class__.__name__,
        )

        data = remove_missing(
            data,
            na_rm=self.params.get("na_rm", False),
            vars=list(self.REQUIRED_AES | self.NON_MISSING_AES),
            name=self.__class__.__name__,
            finite=True,
        )

        def fn(pdata):
            """
            Compute function helper
            """
            # Given data belonging to a specific panel, grab
            # the corresponding scales and call the method
            # that does the real computation
            if len(pdata) == 0:
                return pdata
            pscales = layout.get_scales(pdata["PANEL"].iloc[0])
            return self.compute_panel(pdata, pscales)

        return groupby_apply(data, "PANEL", fn)

    def compute_panel(self, data: pd.DataFrame, scales: pos_scales):
        """
        Calculate the statistics for all the groups

        Return the results in a single dataframe.

        This is a default function that can be overridden
        by individual stats

        Parameters
        ----------
        data :
            data for the computing
        scales :
            x (``scales.x``) and y (``scales.y``) scale objects.
            The most likely reason to use scale information is
            to find out the physical size of a scale. e.g.

            ```python
            range_x = scales.x.dimension()
            ```
        params :
            The parameters for the stat. It includes default
            values if user did not set a particular parameter.
        """
        if not len(data):
            return type(data)()

        stats = []
        for _, old in data.groupby("group"):
            new = self.compute_group(old, scales)
            new.reset_index(drop=True, inplace=True)
            unique = uniquecols(old)
            missing = unique.columns.difference(new.columns)
            idx = [0] * len(new)
            u = unique.loc[idx, missing].reset_index(drop=True)
            # concat can have problems with empty dataframes that
            # have an index
            if u.empty and len(u):
                u = type(data)()

            group_result = pd.concat([new, u], axis=1)
            stats.append(group_result)

        stats = pd.concat(stats, axis=0, ignore_index=True)
        dropped = data.columns.difference(stats.columns).to_list()
        if dropped:
            warn(DROPPED_TPL.format(dropped=dropped))
        # Note: If the data coming in has columns with non-unique
        # values with-in group(s), this implementation loses the
        # columns. Individual stats may want to do some preparation
        # before then fall back on this implementation or override
        # it completely.
        return stats

    def compute_group(
        self, data: pd.DataFrame, scales: pos_scales
    ) -> pd.DataFrame:
        """
        Calculate statistics for the group

        All stats should implement this method

        Parameters
        ----------
        data :
            Data for a group
        scales :
            x (``scales.x``) and y (``scales.y``) scale objects.
            The most likely reason to use scale information is
            to find out the physical size of a scale. e.g.

            ```python
            range_x = scales.x.dimension()
            ```
        params :
            Parameters
        """
        msg = "{} should implement this method."
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def __radd__(self, other: ggplot) -> ggplot:
        """
        Add layer representing stat object on the right

        Parameters
        ----------
        gg :
            ggplot object

        Returns
        -------
        out :
            ggplot object with added layer
        """
        other += layer(stat=self)
        return other
</file>

</files>
