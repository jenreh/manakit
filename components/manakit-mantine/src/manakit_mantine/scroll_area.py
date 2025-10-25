"""Mantine ScrollArea components wrapper for Reflex.

Provides ScrollArea and ScrollArea.Autosize components with custom scrollbars,
scroll position tracking, and overflow detection capabilities.
See `scroll_area()` and `scroll_area_autosize()` functions for detailed usage
and examples.

Documentation: https://mantine.dev/core/scroll-area/
"""

from __future__ import annotations

import secrets
from typing import Any, Literal

import reflex as rx
from reflex.event import EventHandler, EventSpec
from reflex.vars.base import Var

from manakit_mantine.base import MANTINE_LIBARY, MANTINE_VERSION


class ScrollArea(rx.Component):
    """Mantine ScrollArea component wrapper for Reflex.

    Based on: https://mantine.dev/core/scroll-area/

    Provides custom scrollbars with various behavior modes and scroll position
    tracking capabilities. Supports different scrollbar visibility modes and
    programmatic scroll control.

    Example:
        ```python
        import reflex as rx
        import manakit_mantine as mn


        def my_component():
            return mn.scroll_area(
                rx.text("Long content that will scroll..."),
                # More content...
                height="200px",
                type="hover",
                scrollbars="y",
                on_scroll_position_change=lambda pos: print(f"Scrolled to: {pos}"),
            )
        ```
    """

    library = f"{MANTINE_LIBARY}@{MANTINE_VERSION}"

    tag = "ScrollArea"

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';"""

    # Scrollbar behavior control
    type: Var[Literal["auto", "scroll", "always", "hover", "never"]] = "auto"
    """Defines scrollbars behavior: hover (visible on hover), scroll (visible on
    scroll), always (always visible), never (always hidden), auto (overflow auto)."""

    offset_scrollbars: Var[bool | Literal["x", "y", "present"]] = True
    """Adds padding to offset scrollbars: x (horizontal only), y (vertical only),
    xy (both), present (only when scrollbars are visible)."""

    scrollbars: Var[Literal[False, "x", "y", "xy"]] = "xy"
    """Axis at which scrollbars are rendered: x (horizontal), y (vertical),
    xy (both), false (none)."""

    # Styling and sizing
    scrollbar_size: Var[str | int] = "0.75rem"
    """Scrollbar size, any valid CSS value for width/height, numbers converted
    to rem."""

    scroll_hide_delay: Var[int] = 300
    """Delay in ms to hide scrollbars, applicable only when type is hover or scroll."""

    # Behavior
    overscroll_behavior: Var[Literal["contain", "auto", "none"]] = None
    """Controls overscroll-behavior of the viewport (contain, none, auto)."""

    # Viewport control
    viewport_ref: Var[Any] = None
    """Assigns viewport element ref for programmatic scrolling."""

    viewport_props: Var[dict] = None
    """Props passed down to the viewport element."""

    # Event handlers
    on_scroll_position_change: EventHandler[lambda position: [position]] = None
    """Called with current position (x and y coordinates) when viewport is scrolled."""

    on_top_reached: EventHandler[rx.event.no_args_event_spec] = None
    """Called when scrollarea is scrolled all the way to the top."""

    on_bottom_reached: EventHandler[rx.event.no_args_event_spec] = None
    """Called when scrollarea is scrolled all the way to the bottom."""


class ScrollAreaAutosize(ScrollArea):
    """Mantine ScrollArea.Autosize component wrapper for Reflex.

    Based on: https://mantine.dev/core/scroll-area/#scrollareaautosize

    Creates scrollable containers that only show scrollbars when content exceeds
    the specified max-height. Supports overflow change detection for dynamic layouts.

    Example:
        ```python
        import reflex as rx
        import manakit_mantine as mn


        def my_component():
            return mn.scroll_area_autosize(
                rx.text("Content that may exceed max height..."),
                # Dynamic content...
                max_height="300px",
                max_width="400px",
                on_overflow_change=lambda overflow: print(
                    f"Overflow changed: {overflow}"
                ),
            )
        ```
    """

    tag = "ScrollArea.Autosize"

    # Size constraints
    mah: Var[str | int] = None
    """Maximum height - container becomes scrollable when content exceeds this
    height."""

    maw: Var[str | int] = None
    """Maximum width - container becomes scrollable when content exceeds this width."""

    # Overflow detection
    on_overflow_change: EventHandler[lambda overflow: [overflow]] = None


class ScrollAreaWithState(rx.ComponentState):
    """ScrollArea + Controls mit State-basiertem Scroll-Resume und IO-basierten Buttons."""

    # letzter bekannter Scroll-Y (px)
    scroll_y: int = 0

    # DOM-IDs (bei Mount gesetzt)
    viewport_id: str = ""
    wrapper_id: str = ""

    # ---------- Events (müssen öffentlich sein!) ----------

    @rx.event
    def on_position(self, position: dict) -> None:
        """Mantine onScrollPositionChange -> {x, y}"""
        try:
            self.scroll_y = int(position.get("y", 0))
        except Exception:
            self.scroll_y = 0

    @rx.event
    def save_scroll(self, y: int) -> None:
        """Scrollwert aus dem Browser übernehmen."""
        self.scroll_y = int(y)

    @rx.event
    def capture_scroll_from_dom(self) -> EventSpec:
        """ScrollTop einmalig aus dem DOM lesen (z. B. vor Unmount)."""
        if not self.viewport_id:
            return None
        js = (
            "(function(){"
            f"const w=document.getElementById('{self.wrapper_id}');"
            "const vp=w?.querySelector('[data-radix-scroll-area-viewport]')||"
            "document.getElementById('"
            f"{self.viewport_id}"
            "');"
            "if(!vp)return 0;"
            "const y=vp.scrollTop;"
            "const key=w?.dataset?.mnkScrollPersistKey;"
            "if(key){try{localStorage.setItem(key,String(y));}catch(e){};}"
            "return y;"
            "})()"
        )
        return rx.call_script(js, callback=self.save_scroll)

    @rx.event
    def track_scroll(self) -> EventSpec:
        """Bei Scroll-Ereignissen den aktuellen ScrollTop speichern."""
        if not self.viewport_id:
            return None
        js = (
            "(function(){"
            f"const w=document.getElementById('{self.wrapper_id}');"
            "const vp=w?.querySelector('[data-radix-scroll-area-viewport]')||"
            "document.getElementById('"
            f"{self.viewport_id}"
            "');"
            "if(!vp)return 0;"
            "const y=vp.scrollTop;"
            "const key=w?.dataset?.mnkScrollPersistKey;"
            "if(key){try{localStorage.setItem(key,String(y));}catch(e){};}"
            "return y;"
            "})()"
        )
        return rx.call_script(js, callback=self.save_scroll)

    @rx.event
    def restore_scroll(self) -> EventSpec:
        """ScrollTop nach Mount/Theme-Wechsel wiederherstellen."""
        if not self.viewport_id:
            return None
        y = int(self.scroll_y)
        js = (
            "(function(){"
            f"const w=document.getElementById('{self.wrapper_id}');"
            "const vp=w?.querySelector('[data-radix-scroll-area-viewport]')||document.getElementById('"
            f"{self.viewport_id}"
            "');"
            "if(!vp)return;"
            f"const y={y};"
            "if(y>0){"
            "requestAnimationFrame(()=>requestAnimationFrame(()=>{"
            "vp.scrollTo({ top:y, behavior:'auto' });"
            "}));"
            "}"
            "})();"
        )
        return rx.call_script(js)

    @rx.event
    def setup_controls(
        self,
        viewport_id: str,
        wrapper_id: str,
        top_buf: int,
        bottom_buf: int,
        persist_key: str | None = None,
    ) -> list[EventSpec]:
        """IDs setzen, IO für Buttons aktivieren und anschließend Scroll wiederherstellen."""
        self.viewport_id = viewport_id
        self.wrapper_id = wrapper_id

        # Persist key: if provided, expose it on the wrapper for other handlers
        persist_assignment = (
            f"wrapper.dataset.mnkScrollPersistKey='{persist_key}';"
            if persist_key
            else ""
        )

        io_js = (
            "(function(){"
            f"const wrapper=document.getElementById('{wrapper_id}');"
            "if(!wrapper||wrapper.dataset.mnkScrollInit==='1')return;"
            "wrapper.dataset.mnkScrollInit='1';"
            f"{persist_assignment}"
            "const vp=wrapper.querySelector('[data-radix-scroll-area-viewport]')||document.getElementById('"
            f"{viewport_id}"
            "');"
            "if(!vp)return;"
            f"const btnTop=document.getElementById('{viewport_id}-btn-top');"
            f"const btnBottom=document.getElementById('{viewport_id}-btn-bottom');"
            "const content=vp.firstElementChild||vp;"
            "function sentinel(id,pos){"
            "let s=content.querySelector('#'+id);"
            "if(!s){s=document.createElement('div');s.id=id;"
            "s.style.cssText='width:1px;height:1px;pointer-events:none;';"
            "(pos==='top')?content.prepend(s):content.append(s);}"
            "return s;"
            "}"
            f"const sTop=sentinel('{viewport_id}-sentinel-top','top');"
            f"const sBot=sentinel('{viewport_id}-sentinel-bottom','bottom');"
            "function setVis(el,show){if(!el)return;el.style.opacity=show?'1':'0';el.style.visibility=show?'visible':'hidden';}"
            "if(btnTop){"
            "new IntersectionObserver(([e])=>setVis(btnTop,!e.isIntersecting),"
            "{ root:vp, rootMargin:'-"
            f"{top_buf}"
            "px 0px 0px 0px', threshold:0 }).observe(sTop);}"
            "if(btnBottom){"
            "new IntersectionObserver(([e])=>setVis(btnBottom,!e.isIntersecting),"
            "{ root:vp, rootMargin:'0px 0px -"
            f"{bottom_buf}"
            "px 0px', threshold:0 }).observe(sBot);}"
            # Attach scroll listener to persist position client-side
            "(function(){const key=wrapper?.dataset?.mnkScrollPersistKey; if(!key) return;"
            "vp.addEventListener('scroll', function(){ try{ localStorage.setItem(key, String(vp.scrollTop)); }catch(e){} });"
            "window.addEventListener('beforeunload', function(){ try{ localStorage.setItem(key, String(vp.scrollTop)); }catch(e){} });"
            # Try to restore from localStorage immediately on mount
            "(function(){ try{ const key=wrapper?.dataset?.mnkScrollPersistKey; if(!key) return; const v=localStorage.getItem(key); const yy=v?parseInt(v,10):0; if(yy>0){ requestAnimationFrame(()=>requestAnimationFrame(()=>{ vp.scrollTo({ top:yy, behavior:'auto' }); })); } }catch(e){} })();"
            "})();"
            "})();"
        )
        # Mehrere Aktionen aus einem Handler zurückgeben (Event-Chaining). :contentReference[oaicite:1]{index=1}
        return [rx.call_script(io_js), self.restore_scroll()]

    # ---------- Factory: UI ----------

    @classmethod
    def get_component(
        cls,
        *children,
        top_buffer: int = 0,
        bottom_buffer: int = 0,
        show_controls: bool = True,
        controls: Literal["top", "bottom", "top-bottom", "both"] = "top-bottom",
        top_button_text: str = "↑ Top",
        bottom_button_text: str = "↓ Bottom",
        button_props: dict | None = None,
        height: str = "300px",
        viewport_id: str | None = None,
        persist_key: str | None = None,
        # ScrollArea-Props
        type: Literal["auto", "scroll", "always", "hover", "never"] = "auto",  # noqa: A002
        scrollbars: Literal[False, "x", "y", "xy"] = "xy",
        offset_scrollbars: bool | Literal["x", "y", "present"] = True,
        overscroll_behavior: Literal["contain", "auto", "none"] | None = None,
        scroll_hide_delay: int = 300,
        scrollbar_size: str | int = "0.75rem",
        viewport_props: dict | None = None,
        button_align: Literal["center", "left", "right"] = "center",
        on_top_reached: EventHandler[rx.event.no_args_event_spec] = None,
        on_bottom_reached: EventHandler[rx.event.no_args_event_spec] = None,
        **props,
    ) -> rx.Component:
        if viewport_id is None:
            viewport_id = f"scroll-vp-{secrets.token_hex(4)}"
        wrapper_id = f"{viewport_id}-wrapper"
        btn_top_id = f"{viewport_id}-btn-top"
        btn_bottom_id = f"{viewport_id}-btn-bottom"

        vp_props = {
            "id": viewport_id,
            "style": {"overscrollBehavior": "auto"},  # CSS-Property
        }

        if viewport_props is not None:
            vp_props.update(viewport_props)

        # Basis ScrollArea (Viewport-ID + Scroll-Tracking -> State)
        sa = ScrollArea.create(
            *children,
            height=height,
            type=type,
            scrollbars=scrollbars,
            scrollbar_size=scrollbar_size,
            offset_scrollbars=offset_scrollbars,
            overscroll_behavior=overscroll_behavior,
            scroll_hide_delay=scroll_hide_delay,
            on_scroll_position_change=cls.on_position,
            viewport_props=vp_props,
            on_top_reached=on_top_reached,
            on_bottom_reached=on_bottom_reached,
        )

        # Ohne Controls: nur State-Init + Restore
        if not show_controls:
            return rx.box(
                sa,
                id=wrapper_id,
                style={"position": "relative", "width": "100%"},
                on_mount=cls.setup_controls(
                    viewport_id, wrapper_id, top_buffer, bottom_buffer, persist_key
                ),
                on_unmount=cls.capture_scroll_from_dom,
                data_scroll_y=cls.scroll_y,
                data_mnk_scroll_persist_key=persist_key,
                **props,
            )

        show_top = controls in ("top", "top-bottom", "both")
        show_bottom = controls in ("bottom", "top-bottom", "both")

        base_style = {
            "transition": "opacity 0.2s ease, visibility 0.2s ease",
            "opacity": "0",
            "visibility": "hidden",
            "color": rx.color("gray", 9),
            "background_color": rx.color("gray", 1),
            "border_radius": "9999px",
            "box_shadow": rx.color_mode_cond(
                light="0 1px 10px -0.5px rgba(0,0,0,0.1)",
                dark="0 1px 10px -0.5px rgba(204,204,204,0.1)",
            ),
            "border": f"1px solid {rx.color('gray', 5)}",
            "padding": "6px",
            "min_width": "40px",
            "height": "40px",
            "display": "inline-flex",
            "align_items": "center",
            "justify_content": "center",
        }

        extra = {}
        user_style = {}
        user_class = ""
        if button_props:
            extra = {
                k: v
                for k, v in button_props.items()
                if k not in ("style", "class_name", "className")
            }
            user_style = button_props.get("style") or {}
            user_class = (
                button_props.get("class_name") or button_props.get("className") or ""
            )

        def make_btn(label: str, elem_id: str, to_top: bool) -> rx.Component:
            style = {**base_style, **user_style}
            cls_name = (user_class + " manakit-scroll-btn").strip()
            js = (
                "(function(){"
                f"const w=document.getElementById('{wrapper_id}');"
                "const vp=w?.querySelector('[data-radix-scroll-area-viewport]')||document.getElementById('"
                f"{viewport_id}"
                "');"
                "if(!vp)return;"
                "vp.scrollTo({ top:"
                f"{0 if to_top else 'vp.scrollHeight'}"
                ", behavior:'smooth' });"
                "})();"
            )
            return rx.button(
                label,
                id=elem_id,
                on_click=[rx.call_script(js), cls.capture_scroll_from_dom()],
                size="2",
                style=style,
                class_name=cls_name,
                **extra,
            )

        def hpos(aln: str) -> dict:
            if aln == "left":
                return {"left": "12px"}
            if aln == "right":
                return {"right": "12px"}
            return {"left": "50%", "transform": "translateX(-50%)"}

        overlay_items = []
        if show_top:
            overlay_items.append(
                rx.box(
                    make_btn(top_button_text, btn_top_id, to_top=True),
                    style={
                        "position": "absolute",
                        "top": "8px",
                        "z_index": "20",
                        "pointer_events": "auto",
                        **hpos(button_align),
                    },
                )
            )
        if show_bottom:
            overlay_items.append(
                rx.box(
                    make_btn(bottom_button_text, btn_bottom_id, to_top=False),
                    style={
                        "position": "absolute",
                        "bottom": "8px",
                        "z_index": "20",
                        "pointer_events": "auto",
                        **hpos(button_align),
                    },
                )
            )

        overlay = rx.box(
            *overlay_items,
            style={"position": "absolute", "inset": "0", "pointer_events": "none"},
        )

        return rx.box(
            sa,
            overlay,
            id=wrapper_id,
            style={"position": "relative", "width": "100%"},
            on_mount=cls.setup_controls(
                viewport_id, wrapper_id, top_buffer, bottom_buffer, persist_key
            ),
            on_unmount=cls.capture_scroll_from_dom,
            data_scroll_y=cls.scroll_y,
            data_mnk_scroll_persist_key=persist_key,
            **props,
        )


# ============================================================================
# Convenience Functions
# ============================================================================


class ScrollAreaNamespace(rx.ComponentNamespace):
    """Namespace factory for ScrollArea to match other component patterns."""

    __call__ = staticmethod(ScrollArea.create)
    autosize = staticmethod(ScrollAreaAutosize.create)
    stateful = staticmethod(ScrollAreaWithState.create)


scroll_area = ScrollAreaNamespace()
