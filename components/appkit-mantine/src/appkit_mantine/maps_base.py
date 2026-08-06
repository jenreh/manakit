"""Shared base plumbing for the MapCN (https://mapcn.dev) component wrappers.

These components wrap a locally-bundled JSX port of mapcn.dev's MapLibre GL
React components. Unlike most of ``appkit_mantine``, the underlying elements
are plain DOM nodes rendered by MapLibre GL rather than ``@mantine/core``
components, so they intentionally do **not** inherit Mantine layout style
props (``w``, ``h``, ``m``, ``p``, ...) — passing those through would leak
into the MapLibre GL constructor options.

Size the map by wrapping it in a container with an explicit height, matching
mapcn's own usage pattern::

    rx.box(mn.map(center=[-74.006, 40.7128], zoom=11), height="400px", width="100%")
"""

from __future__ import annotations

from typing import Literal

import reflex as rx

from appkit_mantine.base import MantineComponentBase

_MAPS_JSX = rx.asset("maps.jsx", shared=True)

# importable_path omits the ?v= content hash, which Vite would treat as an
# optimized-dep URL and cache immutably, pinning a stale React instance.
MAPS_LIBRARY = _MAPS_JSX.importable_path
"""Local asset path for the ported MapCN React components."""

MAPLIBRE_GL_DEPENDENCY = "maplibre-gl@^5.8.0"

MapControlPosition = Literal["top-left", "top-right", "bottom-left", "bottom-right"]
"""Shared corner-position type for map overlays (controls, directions panel)."""


class MapComponentBase(MantineComponentBase):
    """Base class for all MapCN map component wrappers."""

    library = MAPS_LIBRARY

    lib_dependencies: list[str] = [
        MAPLIBRE_GL_DEPENDENCY,
    ]

    def _get_custom_code(self) -> str:
        """MapCN components bundle their own CSS import; skip Mantine's."""
        return ""


class MapConfigNode(MapComponentBase):
    """Base class for non-visual "config node" components consumed by ``Map``.

    Config nodes (e.g. :class:`~appkit_mantine.maps_navigation.MapNavigation`)
    don't render their own visible content directly. Instead they configure
    behavior on the parent :class:`~appkit_mantine.maps.Map` — fetching
    data, adding MapLibre GL layers/markers, publishing state via React
    context — similar to ``MapRoute``/``MapArc``/``MapGeoJSON``.
    """
