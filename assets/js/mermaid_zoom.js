/**
 * Mermaid SVG Zoom - Click-to-zoom functionality for Mermaid diagrams
 *
 * Provides modal overlay zoom for SVG diagrams rendered by Mermaid in markdown content.
 * Mimics behavior of react-medium-image-zoom library.
 */

(function () {
    'use strict';

    let activeModal = null;
    let originalBodyOverflow = null;

    /**
     * Initialize zoom functionality when DOM is ready
     */
    function init() {
        console.log('[Mermaid Zoom] Initializing...');
        // Use event delegation for better performance with dynamic content
        document.addEventListener('click', handleClick);
        document.addEventListener('keydown', handleKeydown);

        // Log available mermaid diagrams
        setTimeout(() => {
            const diagrams = document.querySelectorAll('code[data-name="mermaid"] svg, .wmde-markdown svg[id^="mermaid-"], .markdown svg[id^="mermaid-"]');
            console.log('[Mermaid Zoom] Found diagrams:', diagrams.length);
        }, 1000);
    }

    /**
     * Handle click events on Mermaid SVGs
     */
    function handleClick(event) {
        const target = event.target;

        // Check if click is on a Mermaid SVG (or child element of SVG)
        // Try multiple selectors to match different Mermaid rendering structures
        let svg = target.closest('code[data-name="mermaid"] svg');

        // Fallback: check if it's an SVG with mermaid ID in markdown container
        if (!svg) {
            svg = target.closest('.wmde-markdown svg[id^="mermaid-"], .markdown svg[id^="mermaid-"]');
        }

        if (svg && !activeModal) {
            // Click on unzoomed SVG - open zoom
            console.log('[Mermaid Zoom] Opening zoom for:', svg);
            event.preventDefault();
            event.stopPropagation();
            openZoom(svg);
        } else if (activeModal && (target === activeModal || target.closest('[data-mermaid-zoom-modal]'))) {
            // Click on modal or zoomed content - close zoom
            console.log('[Mermaid Zoom] Closing zoom');
            event.preventDefault();
            event.stopPropagation();
            closeZoom();
        }
    }

    /**
     * Handle keyboard events (Escape key closes zoom)
     */
    function handleKeydown(event) {
        if (event.key === 'Escape' && activeModal) {
            event.preventDefault();
            closeZoom();
        }
    }

    /**
     * Open zoom modal with cloned SVG
     */
    function openZoom(originalSvg) {
        if (activeModal) return;

        // Clone the SVG
        const svgClone = originalSvg.cloneNode(true);

        // Create modal container
        const modal = document.createElement('div');
        modal.setAttribute('data-mermaid-zoom-modal', 'opening');
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-label', 'Zoomed diagram');

        // Create content wrapper
        const content = document.createElement('div');
        content.setAttribute('data-mermaid-zoom-content', '');
        content.appendChild(svgClone);
        modal.appendChild(content);

        // Lock body scroll
        originalBodyOverflow = document.body.style.overflow;
        document.body.style.overflow = 'hidden';

        // Add to DOM
        document.body.appendChild(modal);
        activeModal = modal;

        // Trigger animation by changing attribute after paint
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                modal.setAttribute('data-mermaid-zoom-modal', 'visible');
            });
        });
    }

    /**
     * Close zoom modal
     */
    function closeZoom() {
        if (!activeModal) return;

        const modal = activeModal;

        // Start closing animation
        modal.setAttribute('data-mermaid-zoom-modal', 'closing');

        // Wait for animation to complete
        const duration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 10 : 300;

        setTimeout(() => {
            // Remove modal from DOM
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }

            // Restore body scroll
            if (originalBodyOverflow !== null) {
                document.body.style.overflow = originalBodyOverflow;
                originalBodyOverflow = null;
            }

            activeModal = null;
        }, duration);
    }

    /**
     * Cleanup on page unload
     */
    function cleanup() {
        if (activeModal) {
            closeZoom();
        }
        document.removeEventListener('click', handleClick);
        document.removeEventListener('keydown', handleKeydown);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-initialize when new content is added (for dynamic Mermaid rendering)
    // Use MutationObserver to detect when Mermaid diagrams are added
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.addedNodes.length > 0) {
                const hasMermaid = Array.from(mutation.addedNodes).some(node => {
                    if (node.nodeType === 1) {
                        return node.querySelector && (
                            node.querySelector('svg[id^="mermaid-"]') ||
                            node.querySelector('code[data-name="mermaid"] svg')
                        );
                    }
                    return false;
                });
                if (hasMermaid) {
                    console.log('[Mermaid Zoom] New Mermaid diagram detected');
                }
            }
        }
    });

    // Start observing after init
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        cleanup();
        observer.disconnect();
    });

})();
