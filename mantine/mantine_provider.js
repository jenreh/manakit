import { createElement, useContext, useEffect, useState, useRef } from "react";
import { MantineProvider as MantineCoreProvider } from "@mantine/core";

import { ColorModeContext } from "$/utils/context";

export default function MantineProvider({ children }) {
  const { resolvedColorMode } = useContext(ColorModeContext);
  const [stableColorMode, setStableColorMode] = useState(null);
  const timerRef = useRef(null);

  useEffect(() => {
    setStableColorMode(resolvedColorMode);
  }, [resolvedColorMode]);

  if (!stableColorMode) {
    return children;
  }

  return createElement(
    MantineCoreProvider,
    {
      key: stableColorMode,
      forceColorScheme: stableColorMode,
    },
    children
  );
}
