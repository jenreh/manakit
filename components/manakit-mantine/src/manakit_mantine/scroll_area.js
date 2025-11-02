import '@mantine/core/styles.css';
import React from 'react';
import { ScrollArea as MantineScrollArea } from '@mantine/core';

export const WrappedScrollArea = React.forwardRef((props, ref) => {
    const {
        onScrollPositionChange,
        viewportProps,
        reportScrollMetrics = false,
        bottomBuffer = 0,
        children,
        ...rest
    } = props || {};

    const viewportRef = React.useRef(null);

    const mergedViewportProps = {
        ...viewportProps,
        ref: (el) => {
            viewportRef.current = el;
            if (typeof viewportProps?.ref === 'function') {
                try {
                    viewportProps.ref(el);
                } catch (e) {
                    // ignore
                }
            } else if (viewportProps?.ref && typeof viewportProps.ref === 'object') {
                viewportProps.ref.current = el;
            }
        },
    };

    const handleScrollPositionChange = (pos) => {
        try {
            if (reportScrollMetrics && viewportRef.current && pos) {
                const vp = viewportRef.current;
                const scrollHeight = vp.scrollHeight;
                const clientHeight = vp.clientHeight;
                const distanceToBottom = scrollHeight - clientHeight - (pos.y ?? 0);
                onScrollPositionChange && onScrollPositionChange({
                    ...pos,
                    scrollHeight,
                    clientHeight,
                    distanceToBottom,
                });
                return;
            }
        } catch (e) {
            // Fall through to forwarding original payload
        }
        onScrollPositionChange && onScrollPositionChange(pos);
    };

    return (
        <MantineScrollArea
            {...rest}
            ref={ref}
            onScrollPositionChange={handleScrollPositionChange}
            viewportProps={mergedViewportProps}
        >
            {children}
        </MantineScrollArea>
    );
});

export default WrappedScrollArea;
