from __future__ import annotations

import secrets
from typing import Literal

import reflex as rx

from manakit_mantine.scroll_area import scroll_area


def scroll_area_with_controls(
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
    # Mantine ScrollArea props
    scroll_type: Literal["auto", "scroll", "always", "hover", "never"] = "auto",
    scrollbars: Literal[False, "x", "y", "xy"] = "xy",
    scrollbar_size: str | int = "0.75rem",
    offset_scrollbars: bool | Literal["x", "y", "present"] = True,
    button_align: Literal["center", "left", "right"] = "center",
    **props,
) -> rx.Component:
    """ScrollArea mit eingebauten Scroll-Controls, deren Sichtbarkeit über
    Pufferzonen (top/bottom) gesteuert wird.

    Args:
        *children: Inhalt der ScrollArea
        top_buffer: Abstand (px) vom oberen Rand, innerhalb dessen der Top-Button *ausgeblendet* bleibt.
        bottom_buffer: Abstand (px) vom unteren Rand, innerhalb dessen der Bottom-Button *ausgeblendet* bleibt.
        show_controls: Ob Buttons gerendert werden sollen.
        controls: "top" | "bottom" | "top-bottom" | "both"
        top_button_text: Beschriftung Top-Button
        bottom_button_text: Beschriftung Bottom-Button
        button_props: Zusätzliche Button-Props (z. B. style, class_name)
        height: Höhe der ScrollArea
        viewport_id: fester ID-Wert für das Viewport-Element (optional)
        scroll_type, scrollbars, scrollbar_size, offset_scrollbars: Mantine-ScrollArea-Props
        button_align: horizontale Ausrichtung der Buttons
        **props: weitere Props für den äußeren Wrapper
    """
    if viewport_id is None:
        viewport_id = f"scroll-vp-{secrets.token_hex(4)}"

    wrapper_id = f"{viewport_id}-wrapper"
    btn_top_id = f"{viewport_id}-btn-top"
    btn_bottom_id = f"{viewport_id}-btn-bottom"

    # Mantine ScrollArea (Radix-basiert), Viewport via id ansprechbar
    # (Mantine stellt u.a. viewportRef/viewportProps bereit; wir nutzen hier id). :contentReference[oaicite:1]{index=1}
    scroll_area_component = scroll_area(
        *children,
        height=height,
        type=scroll_type,
        scrollbars=scrollbars,
        scrollbar_size=scrollbar_size,
        offset_scrollbars=offset_scrollbars,
        viewport_props={"id": viewport_id},
    )

    if not show_controls:
        return scroll_area_component

    show_top = controls in ("top", "top-bottom", "both")
    show_bottom = controls in ("bottom", "top-bottom", "both")

    # Basisstil (überschreibbar via button_props["style"])
    base_button_style = {
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

    extra_button_props: dict = {}
    user_style: dict = {}
    user_class = ""
    if button_props:
        extra_button_props = {
            k: v
            for k, v in button_props.items()
            if k not in ("style", "class_name", "className")
        }
        user_style = button_props.get("style") or {}
        user_class = (
            button_props.get("class_name") or button_props.get("className") or ""
        )

    def make_button(label: str, elem_id: str, on_click_js: str) -> rx.Component:
        style = {**base_button_style, **user_style}
        class_name = (user_class + " manakit-scroll-btn").strip()
        return rx.button(
            label,
            id=elem_id,
            on_click=rx.call_script(on_click_js),
            size="2",
            style=style,
            class_name=class_name,
            **extra_button_props,
        )

    # Click-Scripts (Element.scrollTo ist Standard-API). :contentReference[oaicite:2]{index=2}
    scroll_to_top_js = f"""
(()=>{{
  const w=document.getElementById('{wrapper_id}');
  if(!w) return;
  const vp = w.querySelector('[data-radix-scroll-area-viewport]') || document.getElementById('{viewport_id}');
  if(vp) vp.scrollTo({{top:0, behavior:'smooth'}});
}})();"""

    scroll_to_bottom_js = f"""
(()=>{{
  const w=document.getElementById('{wrapper_id}');
  if(!w) return;
  const vp = w.querySelector('[data-radix-scroll-area-viewport]') || document.getElementById('{viewport_id}');
  if(vp) vp.scrollTo({{top: vp.scrollHeight, behavior:'smooth'}});
}})();"""

    top_button = (
        make_button(top_button_text, btn_top_id, scroll_to_top_js) if show_top else None
    )
    bottom_button = (
        make_button(bottom_button_text, btn_bottom_id, scroll_to_bottom_js)
        if show_bottom
        else None
    )

    def horiz_pos(align: str) -> dict:
        if align == "left":
            return {"left": "12px"}
        if align == "right":
            return {"right": "12px"}
        return {"left": "50%", "transform": "translateX(-50%)"}

    overlay_children: list[rx.Component] = []
    if top_button:
        overlay_children.append(
            rx.box(
                top_button,
                style={
                    "position": "absolute",
                    "top": "8px",
                    "z_index": "20",
                    "pointer_events": "auto",
                    **horiz_pos(button_align),
                },
            )
        )
    if bottom_button:
        overlay_children.append(
            rx.box(
                bottom_button,
                style={
                    "position": "absolute",
                    "bottom": "8px",
                    "z_index": "20",
                    "pointer_events": "auto",
                    **horiz_pos(button_align),
                },
            )
        )

    overlay_layer = rx.box(
        *overlay_children,
        style={"position": "absolute", "inset": "0", "pointer_events": "none"},
    )

    # Vereinfachtes, idempotentes Control-Script mit IntersectionObserver.
    # – nutzt Sentinels innerhalb des Content-Wrappers
    # – steuert Sichtbarkeit über opacity/visibility (oder optional data-visible)
    control_script = (
        """
(()=> {
  const wrapper = document.getElementById('@@WRAPPER_ID@@');
  if (!wrapper) return;

  // Mehrfach-Init verhindern
  if (wrapper.dataset.mnkScrollInit === '1') return;
  wrapper.dataset.mnkScrollInit = '1';

  // Mantine ScrollArea ist Radix ScrollArea-basiert – Viewport so finden: :contentReference[oaicite:3]{index=3}
  const viewport = wrapper.querySelector('[data-radix-scroll-area-viewport]')
                  || document.getElementById('@@VIEWPORT_ID@@');
  if (!viewport) { console.warn('Viewport not found for @@VIEWPORT_ID@@'); return; }

  const content = viewport.firstElementChild || viewport;

  const btnTop = document.getElementById('@@BTN_TOP@@');
  const btnBottom = document.getElementById('@@BTN_BOTTOM@@');

  // Sentinels an Anfang/Ende des Inhalts einfügen (keine absolute Positionierung nötig)
  function ensureSentinel(id, position /* 'top' | 'bottom' */) {
    let s = content.querySelector('#' + id);
    if (!s) {
      s = document.createElement('div');
      s.id = id;
      s.style.cssText = 'width:1px;height:1px;pointer-events:none;';
      if (position === 'top') content.prepend(s); else content.append(s);
    }
    return s;
  }

  const topSentinel = ensureSentinel('@@VIEWPORT_ID@@-sentinel-top','top');
  const bottomSentinel = ensureSentinel('@@VIEWPORT_ID@@-sentinel-bottom','bottom');

  // Helper zum Umschalten (Atoms statt komplexer Zustände)
  function setVisible(el, visible) {
    if (!el) return;
    el.style.opacity   = visible ? '1' : '0';
    el.style.visibility= visible ? 'visible' : 'hidden';
  }

  // Top-Button: sichtbar, wenn oberer Sentinel NICHT im (nach oben verkleinerten) Root liegt
  if (btnTop) {
    const ioTop = new IntersectionObserver(([e]) => {
      setVisible(btnTop, !e.isIntersecting);
    }, { root: viewport, rootMargin: `-@@TOP_BUF@@px 0px 0px 0px`, threshold: 0 });
    ioTop.observe(topSentinel);
  }

  // Bottom-Button: sichtbar, wenn unterer Sentinel NICHT im (nach unten verkleinerten) Root liegt
  if (btnBottom) {
    const ioBottom = new IntersectionObserver(([e]) => {
      // innerhalb der Bottom-Buffer-Zone => verstecken
      setVisible(btnBottom, !e.isIntersecting);
    }, { root: viewport, rootMargin: `0px 0px -@@BOT_BUF@@px 0px`, threshold: 0 });
    ioBottom.observe(bottomSentinel);
  }
})();
""".replace("@@WRAPPER_ID@@", wrapper_id)
        .replace("@@VIEWPORT_ID@@", viewport_id)
        .replace("@@BTN_TOP@@", btn_top_id)
        .replace("@@BTN_BOTTOM@@", btn_bottom_id)
        .replace("@@TOP_BUF@@", str(top_buffer))
        .replace("@@BOT_BUF@@", str(bottom_buffer))
    )

    return rx.box(
        # relative Hülle + Overlay
        scroll_area_component,
        overlay_layer,
        id=wrapper_id,
        style={"position": "relative", "width": "100%"},
        on_mount=rx.call_script(
            control_script
        ),  # korrektes Muster in Reflex :contentReference[oaicite:4]{index=4}
        **props,
    )
