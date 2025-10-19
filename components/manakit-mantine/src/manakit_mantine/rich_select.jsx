/*
 * Mantine-based RichSelect with a single renderer (option) used for both
 * dropdown options and the selected value. Includes text fallback for search.
 */
import React, { Children, isValidElement, useMemo, useState } from "react";
import { Combobox, InputBase, Text, Box, useCombobox } from "@mantine/core";
import '@mantine/core/styles.css';

export const RichSelectItem = () => null;
(RichSelectItem).displayName = "RichSelectItem";

// Extract plain text from any ReactNode (used for default search fallback)
function textFromNode(node) {
  if (node == null || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(textFromNode).join(" ");
  if (isValidElement(node)) return textFromNode(node.props?.children);
  return "";
}

// Parse children and collect items
function collectItems(children) {
  const arr = Children.toArray(children);
  const items = [];

  for (const child of arr) {
    if (!isValidElement(child)) continue;
    if (child.type?.displayName !== "RichSelectItem") continue;

    const { value, disabled, keywords, payload, option } = child.props;
    if (!option) {
      console.warn("RichSelect.Item requires 'option' prop:", value);
      continue;
    }

    const kw = (keywords ?? []).join(" ");
    const pl = payload ? JSON.stringify(payload) : "";
    const optTxt = textFromNode(option);
    const searchText = `${kw} ${pl} ${optTxt}`.trim().toLowerCase();

    items.push({ value, disabled, keywords, payload, option, searchText });
  }
  return items;
}

export const RichSelect = ({
  value: controlled,
  onChange,
  placeholder = "Pick value",
  searchable = true,
  clearable = false,
  nothingFound = <Text c="dimmed">Nothing found</Text>,
  maxDropdownHeight = 280,
  filter,
  children,
}) => {
  const [uncontrolled, setUncontrolled] = useState(null);
  const isControlled = controlled !== undefined;
  const value = (isControlled ? controlled : uncontrolled) ?? null;

  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });

  const [query, setQuery] = useState("");
  const items = useMemo(() => collectItems(children), [children]);

  const defaultFilter = (q, it) => it.searchText.includes(q);

  const filtered = useMemo(() => {
    if (!searchable || !query) return items;
    const q = query.trim().toLowerCase();
    const fn = filter ?? defaultFilter;
    return items.filter((it) => fn(q, it));
  }, [query, items, searchable, filter]);

  const selected = value ? items.find((i) => i.value === value) ?? null : null;

  const commit = (v) => {
    if (!isControlled) setUncontrolled(v);
    onChange?.(v);
  };

  return (
    <Combobox
      store={combobox}
      withinPortal
      onOptionSubmit={(val) => {
        commit(val);
        combobox.closeDropdown();
      }}
    >
      <Combobox.Target>
        <InputBase
          component="button"
          type="button"
          onClick={() => combobox.toggleDropdown()}
          rightSection={<Combobox.Chevron />}
          rightSectionPointerEvents="none"
          multiline
        >
          {selected ? selected.option : placeholder}
        </InputBase>
      </Combobox.Target>

      <Combobox.Dropdown mah={maxDropdownHeight} style={{ overflow: "auto" }}>
        {searchable ? (
          <Combobox.Search
            value={query}
            onChange={(e) => setQuery(e.currentTarget.value)}
            placeholder="Search…"
          />
        ) : null}

        <Combobox.Options>
          {filtered.length ? (
            filtered.map((it) => (
              <Combobox.Option key={it.value} value={it.value} disabled={it.disabled}>
                {it.option}
              </Combobox.Option>
            ))
          ) : (
            <Combobox.Empty>{nothingFound}</Combobox.Empty>
          )}
        </Combobox.Options>

        {clearable && selected ? (
          <Box p="xs">
            <Combobox.ClearButton onClick={() => commit(null)} aria-label="Clear selection" />
          </Box>
        ) : null}
      </Combobox.Dropdown>
    </Combobox>
  );
};

export default RichSelect;
