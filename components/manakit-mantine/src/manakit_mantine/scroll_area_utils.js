/**
 * Scroll Area with Controls - Utility Functions
 * Handles scroll position management and control visibility
 */

/**
 * Get current scroll position from viewport
 * @param {string} viewportId - ID of the viewport element
 * @param {string} wrapperId - ID of the wrapper element
 * @returns {number} Current scroll top position
 */
window.mnkScrollArea = window.mnkScrollArea || {};

window.mnkScrollArea.getScrollTop = function(viewportId, wrapperId) {
  const wrapper = document.getElementById(wrapperId);
  const viewport = wrapper?.querySelector('[data-radix-scroll-area-viewport]') ||
                   document.getElementById(viewportId);
  return viewport ? viewport.scrollTop : 0;
};

/**
 * Restore scroll position to viewport
 * @param {string} viewportId - ID of the viewport element
 * @param {string} wrapperId - ID of the wrapper element
 * @param {number} scrollY - Target scroll position
 */
window.mnkScrollArea.restoreScroll = function(viewportId, wrapperId, scrollY) {
  const wrapper = document.getElementById(wrapperId);
  const viewport = wrapper?.querySelector('[data-radix-scroll-area-viewport]') ||
                   document.getElementById(viewportId);

  if (!viewport) return;

  const y = parseInt(scrollY);
  if (y > 0) {
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        viewport.scrollTo({ top: y, behavior: 'auto' });
      })
    );
  }
};

/**
 * Scroll viewport to specific position
 * @param {string} viewportId - ID of the viewport element
 * @param {string} wrapperId - ID of the wrapper element
 * @param {number} scrollTarget - 0 to scroll to top, 1 to scroll to bottom
 * @param {string} behavior - Scroll behavior ('smooth', 'auto')
 */
window.mnkScrollArea.scrollToPosition = function(viewportId, wrapperId, scrollTarget, behavior = 'smooth') {
  const wrapper = document.getElementById(wrapperId);
  const viewport = wrapper?.querySelector('[data-radix-scroll-area-viewport]') ||
                   document.getElementById(viewportId);

  if (!viewport) return;

  const scrollTop = scrollTarget === 0 ? 0 : viewport.scrollHeight;
  viewport.scrollTo({ top: scrollTop, behavior });
};

/**
 * Setup scroll controls with Intersection Observer
 * Creates sentinel elements and observes visibility
 * @param {string} viewportId - ID of the viewport element
 * @param {string} wrapperId - ID of the wrapper element
 * @param {number} topBuffer - Top buffer in pixels for sentinel
 * @param {number} bottomBuffer - Bottom buffer in pixels for sentinel
 */
window.mnkScrollArea.setupControls = function(viewportId, wrapperId, topBuffer, bottomBuffer) {
  const wrapper = document.getElementById(wrapperId);
  if (!wrapper || wrapper.dataset.mnkScrollInit === '1') return;

  wrapper.dataset.mnkScrollInit = '1';

  const viewport = wrapper.querySelector('[data-radix-scroll-area-viewport]') ||
                   document.getElementById(viewportId);

  if (!viewport) return;

  const btnTop = document.getElementById(viewportId + '-btn-top');
  const btnBottom = document.getElementById(viewportId + '-btn-bottom');
  const content = viewport.firstElementChild || viewport;

  /**
   * Create or get sentinel element at specified position
   */
  function sentinel(id, pos) {
    let s = content.querySelector('#' + id);
    if (!s) {
      s = document.createElement('div');
      s.id = id;
      s.style.cssText = 'width:1px;height:1px;pointer-events:none;';
      pos === 'top' ? content.prepend(s) : content.append(s);
    }
    return s;
  }

  /**
   * Set visibility of button
   */
  function setVis(el, show) {
    if (!el) return;
    el.style.opacity = show ? '1' : '0';
    el.style.visibility = show ? 'visible' : 'hidden';
  }

  const sentinelTop = sentinel(viewportId + '-sentinel-top', 'top');
  const sentinelBottom = sentinel(viewportId + '-sentinel-bottom', 'bottom');

  // Observe top sentinel
  if (btnTop) {
    new IntersectionObserver(
      ([entry]) => setVis(btnTop, !entry.isIntersecting),
      { root: viewport, rootMargin: `-${topBuffer}px 0px 0px 0px`, threshold: 0 }
    ).observe(sentinelTop);
  }

  // Observe bottom sentinel
  if (btnBottom) {
    new IntersectionObserver(
      ([entry]) => setVis(btnBottom, !entry.isIntersecting),
      { root: viewport, rootMargin: `0px 0px -${bottomBuffer}px 0px`, threshold: 0 }
    ).observe(sentinelBottom);
  }
};
