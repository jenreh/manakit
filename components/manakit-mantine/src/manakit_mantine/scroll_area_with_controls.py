# components/manakit-mantine/src/manakit_mantine/scroll_area_with_controls.py
from __future__ import annotations

import secrets
from typing import Literal

import reflex as rx

from manakit_mantine.scroll_area import scroll_area


class ScrollAreaWithControlsState(rx.ComponentState):
    """ScrollArea + Controls mit State-basiertem Scroll-Resume und IO-basierten Buttons."""

    # letzter bekannter Scroll-Y (px)
    scroll_y: int = 0

    # DOM-IDs (bei Mount gesetzt)
    viewport_id: str = ""
    wrapper_id: str = ""

    # ---------- Events (müssen öffentlich sein!) ----------

    @rx.event
    def on_position(self, position: dict):
        """Mantine onScrollPositionChange -> {x, y}"""
        try:
            self.scroll_y = int(position.get("y", 0))
        except Exception:
            self.scroll_y = 0

    @rx.event
    def save_scroll(self, y: int):
        """Scrollwert aus dem Browser übernehmen."""
        self.scroll_y = int(y)

    @rx.event
    def capture_scroll_from_dom(self):
        """ScrollTop einmalig aus dem DOM lesen (z. B. vor Unmount)."""
        if not self.viewport_id:
            return None
        js = (
            "(function(){"
            f"const w=document.getElementById('{self.wrapper_id}');"
            "const vp=w?.querySelector('[data-radix-scroll-area-viewport]')||document.getElementById('"
            f"{self.viewport_id}"
            "');"
            "return vp?vp.scrollTop:0;"
            "})()"
        )
        return rx.call_script(js, callback=self.save_scroll)

    @rx.event
    def track_scroll(self):
        """Bei Scroll-Ereignissen den aktuellen ScrollTop speichern."""
        if not self.viewport_id:
            return None
        js = (
            "(function(){"
            f"const w=document.getElementById('{self.wrapper_id}');"
            "const vp=w?.querySelector('[data-radix-scroll-area-viewport]')||document.getElementById('"
            f"{self.viewport_id}"
            "');"
            "return vp?vp.scrollTop:0;"
            "})()"
        )
        return rx.call_script(js, callback=self.save_scroll)

    @rx.event
    def restore_scroll(self):
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
        self, viewport_id: str, wrapper_id: str, top_buf: int, bottom_buf: int
    ):
        """IDs setzen, IO für Buttons aktivieren und anschließend Scroll wiederherstellen."""
        self.viewport_id = viewport_id
        self.wrapper_id = wrapper_id

        io_js = (
            "(function(){"
            f"const wrapper=document.getElementById('{wrapper_id}');"
            "if(!wrapper||wrapper.dataset.mnkScrollInit==='1')return;"
            "wrapper.dataset.mnkScrollInit='1';"
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
        # ScrollArea-Props
        scroll_type: Literal["auto", "scroll", "always", "hover", "never"] = "auto",
        scrollbars: Literal[False, "x", "y", "xy"] = "xy",
        scrollbar_size: str | int = "9px",
        offset_scrollbars: bool | Literal["x", "y", "present"] = True,
        button_align: Literal["center", "left", "right"] = "center",
        **props,
    ) -> rx.Component:
        if viewport_id is None:
            viewport_id = f"scroll-vp-{secrets.token_hex(4)}"
        wrapper_id = f"{viewport_id}-wrapper"
        btn_top_id = f"{viewport_id}-btn-top"
        btn_bottom_id = f"{viewport_id}-btn-bottom"

        # Basis ScrollArea (Viewport-ID + Scroll-Tracking -> State)
        sa = scroll_area(
            *children,
            height=height,
            type=scroll_type,
            scrollbars=scrollbars,
            scrollbar_size=scrollbar_size,
            offset_scrollbars=offset_scrollbars,
            on_scroll_position_change=cls.on_position,
            viewport_props={
                "id": viewport_id,
                "style": {"overscrollBehavior": "auto"},  # CSS-Property
            },
        )

        # Ohne Controls: nur State-Init + Restore
        if not show_controls:
            return rx.box(
                sa,
                id=wrapper_id,
                style={"position": "relative", "width": "100%"},
                on_mount=cls.setup_controls(
                    viewport_id, wrapper_id, top_buffer, bottom_buffer
                ),
                on_unmount=cls.capture_scroll_from_dom,
                data_scroll_y=cls.scroll_y,
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
                viewport_id, wrapper_id, top_buffer, bottom_buffer
            ),
            on_unmount=cls.capture_scroll_from_dom,
            data_scroll_y=cls.scroll_y,
            **props,
        )


# API-kompatibel zur bisherigen Nutzung:
def scroll_area_with_controls(*args, **kwargs) -> rx.Component:
    return ScrollAreaWithControlsState.create(*args, **kwargs)
