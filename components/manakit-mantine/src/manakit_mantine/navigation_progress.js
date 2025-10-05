/**
 * Wrapper for @mantine/nprogress that exposes nprogress API globally
 * This allows Reflex to control the progress bar via rx.call_script()
 */
import { NavigationProgress, nprogress } from "@mantine/nprogress";

// Expose nprogress API globally so it can be accessed via rx.call_script()
if (typeof window !== "undefined") {
    window.nprogress = nprogress;
}

export default NavigationProgress;
