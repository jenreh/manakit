// components/manakit-mantine/src/manakit_mantine/rich_select.jsx
// RichSelect – Combobox-basierter Select mit "reichhaltigen" Optionen.
// Verhält sich wie die Mantine-Demos: Dropdown rendert jede Option in <Combobox.Option key=...>,
// die Anzeige im Feld rendert *eine neue Instanz* derselben UI (kein Node-Re-Use).
// Quelle/Idee: Combobox/Select-Beispiele & Autocomplete-Implementierung in Mantine.

import '@mantine/core/styles.css';
import React, { Children, cloneElement, isValidElement, useMemo, useState } from 'react';
import { Combobox, InputBase, Text, CloseButton, useCombobox } from '@mantine/core';

// Virtuelles Kind, das Reflex von Python aus erzeugt: <rich_select.item .../>
export const RichSelectItem = () => null;
RichSelectItem.displayName = 'RichSelectItem';

// -------- Hilfen ---------------------------------------------------------

// Beliebiges ReactNode -> Plain-Text (für Suche)
function textFromNode(node) {
  if (node == null || typeof node === 'boolean') return '';
  if (typeof node === 'string' || typeof node === 'number') return String(node);
  if (Array.isArray(node)) return node.map(textFromNode).join(' ');
  if (isValidElement(node)) return textFromNode(node.props?.children);
  return '';
}

// Aus einer ReactNode eine *Fabrik* machen, die je Verwendung einen frischen Clone erzeugt
function makeFactory(node) {
  if (!isValidElement(node)) {
    // Primitive Nodes (string/number) werden "as is" zurückgegeben:
    return () => node;
  }
  return (keySalt) => cloneElement(node, { key: keySalt });
}

// Children -> interne Item-Struktur
function collectItems(children) {
  const items = [];
  for (const child of Children.toArray(children)) {
    if (!isValidElement(child)) continue;
    const isItem =
      (child.type?.displayName || child.type?.name) === 'RichSelectItem';
    if (!isItem) continue;

    const { value, disabled, keywords, payload, option } = child.props;
    if (!value) {
      console.warn('RichSelectItem requires a non-empty "value" prop.');
      continue;
    }
    if (option == null) {
      console.warn('RichSelectItem requires "option" prop for value:', value);
      continue;
    }

    const kw = Array.isArray(keywords) ? keywords.join(' ') : '';
    let pl = '';
    if (payload) {
      try {
        pl = JSON.stringify(payload);
      } catch {
        pl = '';
      }
    }
    const plain = textFromNode(option);
    const searchText = `${kw} ${pl} ${plain}`.trim().toLowerCase();

    items.push({
      value: String(value),
      disabled: !!disabled,
      searchText,
      makeOption: makeFactory(option), // <- jedes Mal frische Instanz
    });
  }
  return items;
}

// -------- Komponente -----------------------------------------------------

export const RichSelect = ({
  value: controlled,
  onChange,
  placeholder = 'Pick value',
  searchable = true,
  clearable = false,
  nothingFound = <Text c="dimmed">Nothing found</Text>,
  maxDropdownHeight = 280,
  filter, // optional: (query, { value, searchText }) => boolean
  children,
}) => {
  // simple local state for value
  const [value, setValue] = useState(null);
  const combobox = useCombobox();
  const [query, setQuery] = useState('');
  const items = useMemo(() => collectItems(children), [children]);

  const defaultFilter = (q, it) => it.searchText.includes(q);
  const filtered = useMemo(() => {
    if (!searchable || !query) return items;
    const q = String(query).trim().toLowerCase();
    const fn = filter ?? defaultFilter;
    return items.filter((it) => fn(q, { value: it.value, searchText: it.searchText }));
  }, [query, items, searchable, filter]);

  const selected = value ? items.find((i) => i.value === value) ?? null : null;

  return (
    <Combobox
      store={combobox}
      withinPortal={false}
      onOptionSubmit={(val) => {
        setValue(val);
        onChange?.(val);
        combobox.closeDropdown();
      }}
    >
      <Combobox.Target>
        <InputBase
          component="button"
          type="button"
          pointer
          rightSection={
            value !== null && clearable ? (
              <CloseButton
                size="sm"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => { setValue(null); onChange?.(null); }}
                aria-label="Clear value"
              />
            ) : (
              <Combobox.Chevron />
            )
          }
          rightSectionPointerEvents={value === null ? 'none' : 'all'}
          onClick={() => combobox.toggleDropdown()}
          multiline
          portal={false}
        >
          {selected
            // Anzeige im Feld – *neue Instanz* mit eigenem Key (wie im Mantine-Demo erneut rendern)
            ? selected.makeOption(`selected-${selected.value}`)
            : placeholder}
        </InputBase>
      </Combobox.Target>

      <Combobox.Dropdown
        mah={maxDropdownHeight}
        style={{ overflow: 'auto' }}
      >
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
              <Combobox.Option
                key={`opt-${it.value}`}
                value={it.value}
                disabled={it.disabled}
              >
                {/* Dropdown-Zeile – *neue Instanz* mit eigenem Key */}
                {it.makeOption(`list-${it.value}`)}
              </Combobox.Option>
            ))
          ) : (
            <Combobox.Empty>{nothingFound}</Combobox.Empty>
          )}
        </Combobox.Options>
      </Combobox.Dropdown>
    </Combobox>
  );
};

export default RichSelect;
