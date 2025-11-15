import '@mantine/core/styles.css';
import '@uiw/react-markdown-preview/markdown.css';

import {
    Fragment,
    createElement,
    memo,
    useCallback,
    useContext,
    useEffect,
    useMemo,
    useRef,
    useState,
} from 'react';
import MarkdownPreview from '@uiw/react-markdown-preview';
import { getCodeString } from 'rehype-rewrite';
import rehypeSanitize from 'rehype-sanitize';
import { ColorModeContext } from '$/utils/context';

let mermaidLibPromise = null;
let katexLibPromise = null;
let katexStylesLoaded = false;

async function loadMermaid() {
    if (!mermaidLibPromise) {
        mermaidLibPromise = import('mermaid')
            .then((module) => {
                const mermaid = module.default || module;
                if (mermaid && typeof mermaid.initialize === 'function') {
                    mermaid.initialize({ startOnLoad: false });
                }
                return mermaid;
            })
            .catch((error) => {
                console.warn('[MarkdownPreview] Mermaid not available:', error);
                return null;
            });
    }
    return mermaidLibPromise;
}

async function loadKatex() {
    if (!katexLibPromise) {
        katexLibPromise = import('katex')
            .then((module) => module.default || module)
            .catch((error) => {
                console.warn('[MarkdownPreview] KaTeX not available:', error);
                return null;
            });
    }

    const katex = await katexLibPromise;
    if (katex && !katexStylesLoaded) {
        try {
            await import('katex/dist/katex.css');
        } catch (error) {
            console.warn('[MarkdownPreview] Failed to load KaTeX styles:', error);
        }
        katexStylesLoaded = true;
    }
    return katex;
}

function generateRandomId() {
    return Math.random().toString(36).slice(2);
}

const MermaidCode = memo(function MermaidCode({ children = [], className, node }) {
    const demoId = useRef(`mermaid-${generateRandomId()}`);
    const containerRef = useRef(null);
    const [renderError, setRenderError] = useState(null);

    const code = useMemo(() => {
        if (node && node.children) {
            return getCodeString(node.children) || '';
        }
        if (Array.isArray(children)) {
            return children.join('');
        }
        return children || '';
    }, [children, node]);

    const isMermaid =
        typeof className === 'string' && /^language-mermaid/.test(className.toLowerCase());

    const renderDiagram = useCallback(async () => {
        if (!containerRef.current || !isMermaid || !code) {
            return;
        }
        const mermaid = await loadMermaid();
        if (!mermaid) {
            setRenderError('Mermaid library is unavailable.');
            return;
        }
        try {
            const { svg, bindFunctions } = await mermaid.render(demoId.current, code);
            containerRef.current.innerHTML = svg;
            if (typeof bindFunctions === 'function') {
                bindFunctions(containerRef.current);
            }
            setRenderError(null);
        } catch (error) {
            console.error('[MarkdownPreview] Mermaid render failed:', error);
            setRenderError(error.message || 'Mermaid render failed.');
            containerRef.current.innerHTML = '';
        }
    }, [code, isMermaid]);

    useEffect(() => {
        renderDiagram();
    }, [renderDiagram]);

    if (!isMermaid) {
        return createElement('code', { className }, children);
    }

    if (renderError) {
        return createElement(
            'code',
            { className: `${className || ''} mermaid-error` },
            `Mermaid error: ${renderError}`
        );
    }

    return createElement(
        Fragment,
        null,
        createElement('code', { id: demoId.current, style: { display: 'none' } }),
        createElement('code', {
            ref: (nodeElement) => {
                containerRef.current = nodeElement;
            },
            'data-name': 'mermaid',
        })
    );
});

const KatexCode = memo(function KatexCode({ children = [], className, node }) {
    const [html, setHtml] = useState(null);
    const [error, setError] = useState(null);

    const isInlineKatex = useMemo(() => {
        return typeof children === 'string' && /^\$\$(.*)\$\$/.test(children);
    }, [children]);

    const isBlockKatex = useMemo(() => {
        return (
            typeof className === 'string' &&
            /^language-katex/.test(className.toLowerCase())
        );
    }, [className]);

    const code = useMemo(() => {
        if (node && node.children) {
            return getCodeString(node.children) || '';
        }
        if (Array.isArray(children)) {
            return children.join('');
        }
        return typeof children === 'string' ? children : '';
    }, [children, node]);

    useEffect(() => {
        if (!(isInlineKatex || isBlockKatex)) {
            return;
        }

        let cancelled = false;

        async function renderKatex() {
            const katex = await loadKatex();
            if (!katex) {
                setError('KaTeX library is unavailable.');
                return;
            }

            try {
                const mathContent = isInlineKatex ? code.replace(/^\$\$(.*)\$\$/, '$1') : code;
                const rendered = katex.renderToString(mathContent, {
                    throwOnError: false,
                });
                if (!cancelled) {
                    setHtml(rendered);
                    setError(null);
                }
            } catch (renderError) {
                console.error('[MarkdownPreview] KaTeX render failed:', renderError);
                if (!cancelled) {
                    setError(renderError.message || 'KaTeX render failed.');
                    setHtml(null);
                }
            }
        }

        renderKatex();

        return () => {
            cancelled = true;
        };
    }, [code, isBlockKatex, isInlineKatex]);

    if (!(isInlineKatex || isBlockKatex)) {
        return createElement('code', { className }, children);
    }

    if (error) {
        return createElement('code', { className }, `KaTeX error: ${error}`);
    }

    if (html) {
        const style = isBlockKatex
            ? { display: 'block', fontSize: '150%' }
            : { background: 'transparent' };
        return createElement('code', {
            className,
            style,
            dangerouslySetInnerHTML: { __html: html },
        });
    }

    return createElement('code', { className }, children);
});

function buildCustomCodeRenderer(enableMermaid, enableKatex, baseRenderer) {
    if (!enableMermaid && !enableKatex) {
        return baseRenderer;
    }

    return function CustomCodeComponent(props) {
        const { className } = props;
        if (enableMermaid && typeof className === 'string' && className.includes('mermaid')) {
            return createElement(MermaidCode, props);
        }
        if (enableKatex) {
            const inlineCandidate = props.children;
            const isInline =
                typeof inlineCandidate === 'string' && /^\$\$(.*)\$\$/.test(inlineCandidate);
            const isBlock =
                typeof className === 'string' && /^language-katex/.test(className.toLowerCase());
            if (isInline || isBlock) {
                return createElement(KatexCode, props);
            }
        }
        if (baseRenderer) {
            return baseRenderer(props);
        }
        return createElement('code', { className }, props.children);
    };
}

const SECURITY_PRESETS = {
    strict: {
        skipHtml: true,
        rehypePlugins: [rehypeSanitize],
    },
    standard: {
        skipHtml: true,
        rehypePlugins: [
            [rehypeSanitize, {
                attributes: {
                    '*': ['className', 'style'],
                    a: ['href', 'target', 'rel'],
                    img: ['src', 'alt', 'width', 'height'],
                },
            }],
        ],
    },
    none: {
        skipHtml: false,
        rehypePlugins: [],
    },
};

export function MarkdownPreviewWrapper(props) {
    const {
        source = '',
        security_level,
        securityLevel,
        enable_mermaid,
        enableMermaid,
        enable_katex,
        enableKatex,
        style,
        class_name,
        className,
        prefix_cls,
        prefixCls,
        disable_copy,
        disableCopy,
        remark_plugins,
        remarkPlugins,
        rehype_plugins,
        rehypePlugins,
        rehype_rewrite,
        rehypeRewrite,
        components,
        wrapper_element,
        wrapperElement,
        ...rest
    } = props;

    const resolvedSecurityLevel = (typeof securityLevel !== 'undefined' ? securityLevel : security_level) || 'standard';
    const mermaidEnabled = (typeof enableMermaid !== 'undefined' ? enableMermaid : enable_mermaid) || false;
    const katexEnabled = (typeof enableKatex !== 'undefined' ? enableKatex : enable_katex) || false;
    const resolvedClassName = typeof className !== 'undefined' ? className : class_name;
    const resolvedPrefixCls = typeof prefixCls !== 'undefined' ? prefixCls : prefix_cls;
    const resolvedDisableCopy = typeof disableCopy !== 'undefined' ? disableCopy : disable_copy;
    const resolvedRemarkPlugins = typeof remarkPlugins !== 'undefined' ? remarkPlugins : remark_plugins;
    const resolvedRehypePlugins = typeof rehypePlugins !== 'undefined' ? rehypePlugins : rehype_plugins;
    const resolvedRehypeRewrite = typeof rehypeRewrite !== 'undefined' ? rehypeRewrite : rehype_rewrite;
    const resolvedWrapperElement = typeof wrapperElement !== 'undefined' ? wrapperElement : wrapper_element;

    const securityConfig = SECURITY_PRESETS[resolvedSecurityLevel] || SECURITY_PRESETS.standard;

    const finalRehypePlugins = useMemo(() => {
        const extraPlugins = Array.isArray(resolvedRehypePlugins) ? resolvedRehypePlugins : [];
        return [...securityConfig.rehypePlugins, ...extraPlugins];
    }, [resolvedRehypePlugins, securityConfig]);

    const finalRemarkPlugins = useMemo(() => {
        if (Array.isArray(resolvedRemarkPlugins)) {
            return resolvedRemarkPlugins;
        }
        return resolvedRemarkPlugins ? [resolvedRemarkPlugins] : [];
    }, [resolvedRemarkPlugins]);

    const colorModeContext = useContext(ColorModeContext);
    const resolvedColorMode = colorModeContext?.resolvedColorMode;
    const contextColorMode = typeof resolvedColorMode === 'string'
        ? resolvedColorMode
        : resolvedColorMode?.valueOf?.();

    const [colorMode, setColorMode] = useState(() => {
        if (contextColorMode === 'dark' || contextColorMode === 'light') {
            return contextColorMode;
        }
        if (typeof document !== 'undefined') {
            const attr =
                document.documentElement.getAttribute('data-theme') ||
                document.documentElement.getAttribute('data-color-mode');
            return attr === 'dark' ? 'dark' : 'light';
        }
        return 'light';
    });

    useEffect(() => {
        if (contextColorMode === 'dark' || contextColorMode === 'light') {
            setColorMode(contextColorMode);
            return;
        }

        if (typeof document === 'undefined' || typeof MutationObserver === 'undefined') {
            return;
        }

        const detectColorMode = () => {
            const attr =
                document.documentElement.getAttribute('data-theme') ||
                document.documentElement.getAttribute('data-color-mode');
            setColorMode(attr === 'dark' ? 'dark' : 'light');
        };

        detectColorMode();

        const observer = new MutationObserver(detectColorMode);
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme', 'data-color-mode'],
        });

        return () => observer.disconnect();
    }, [contextColorMode]);

    const resolvedComponents = useMemo(() => {
        const baseComponents = components && typeof components === 'object' ? { ...components } : {};
        const mergedRenderer = buildCustomCodeRenderer(
            mermaidEnabled,
            katexEnabled,
            baseComponents.code
        );
        if (mermaidEnabled || katexEnabled) {
            baseComponents.code = mergedRenderer;
        }
        return Object.keys(baseComponents).length ? baseComponents : undefined;
    }, [components, katexEnabled, mermaidEnabled]);

    const wrapperProps = useMemo(() => {
        const base = resolvedWrapperElement && typeof resolvedWrapperElement === 'object'
            ? { ...resolvedWrapperElement }
            : {};
        if (!('data-color-mode' in base)) {
            base['data-color-mode'] = colorMode;
        }
        return base;
    }, [colorMode, resolvedWrapperElement]);

    return createElement(MarkdownPreview, {
        source,
        skipHtml: securityConfig.skipHtml,
        remarkPlugins: finalRemarkPlugins,
        rehypePlugins: finalRehypePlugins,
        rehypeRewrite: resolvedRehypeRewrite,
        components: resolvedComponents,
        style,
        className: resolvedClassName,
        prefixCls: resolvedPrefixCls,
        disableCopy: resolvedDisableCopy,
        wrapperElement: wrapperProps,
        ...rest,
    });
}
