import React, { useState, useMemo } from 'react';
import { Combobox, Group, Input, InputBase, Text, useCombobox, Tooltip } from '@mantine/core';

export function RichSelect({
  value = null,
  on_change,
  on_option_submit,
  on_search_change,
  placeholder = 'Pick value',
  searchable = true,
  clearable = false,
  nothing_found = 'Nothing found',
  max_dropdown_height = 280,
  children,
}) {
  const [search, setSearch] = useState('');
  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });

  // Normalize children to array
  const items = React.Children.toArray(children).filter(Boolean);

  console.log('RichSelect - items:', items.length);
  console.log('RichSelect - current value:', value);

  // Filter items based on search + keywords
  const filteredItems = useMemo(() => {
    if (!searchable || !search.trim()) return items;

    const searchLower = search.toLowerCase();
    return items.filter((item) => {
      const itemValue = item.props.value?.toLowerCase() || '';
      const keywords = item.props.keywords || [];
      const keywordMatch = Array.isArray(keywords)
        ? keywords.some((kw) => String(kw).toLowerCase().includes(searchLower))
        : false;
      return itemValue.includes(searchLower) || keywordMatch;
    });
  }, [search, items, searchable]);

  const selectedItem = items.find((item) => item.props.value === value);

  const handleSelect = (val) => {
    console.log('handleSelect called with:', val);
    console.log('on_change exists:', !!on_change);
    console.log('on_option_submit exists:', !!on_option_submit);

    if (on_change) {
      console.log('Calling on_change with:', val);
      on_change(val);
    }
    if (on_option_submit) {
      console.log('Calling on_option_submit with:', val);
      on_option_submit(val);
    }
    combobox.closeDropdown();
  };

  const handleSearchChange = (val) => {
    setSearch(val);
    combobox.resetSelectedOption();
    if (on_search_change) {
      on_search_change(val);
    }
  };

  const handleClear = (e) => {
    e.stopPropagation();
    if (on_change) {
      on_change(null);
    }
    setSearch('');
  };

  const options = filteredItems.map((item, index) => {
    console.log(`Option ${index}:`, item.props.value, 'disabled:', item.props.disabled);
    return (
      <Combobox.Option
        value={item.props.value}
        key={item.key || `option-${index}`}
        disabled={item.props.disabled || false}
      >
        {item.props.option}
      </Combobox.Option>
    );
  });

  return (
    <Combobox
      store={combobox}
      withinPortal={false}
      onOptionSubmit={handleSelect}
    >
      <Combobox.Target>
        <InputBase
          component="button"
          type="button"
          pointer
          rightSection={
            clearable && value ? (
              <CloseButton
                size="sm"
                onMouseDown={(event) => event.preventDefault()}
                onClick={handleClear}
                aria-label="Clear value"
              />
            ) : (
              <Combobox.Chevron />
            )
          }
          onClick={() => combobox.toggleDropdown()}
          rightSectionPointerEvents={clearable && value ? "auto" : "none"}
          multiline
        >
          {selectedItem ? (
            selectedItem.props.option
          ) : (
            <Input.Placeholder>{placeholder}</Input.Placeholder>
          )}
        </InputBase>
      </Combobox.Target>
      <Combobox.Dropdown>
        {searchable && (
          <Combobox.Search
            value={search}
            onChange={(e) => handleSearchChange(e.currentTarget.value)}
            placeholder="Search..."
            rightSection={null}
          />
        )}
        <Combobox.Options
          style={{ maxHeight: max_dropdown_height, overflowY: 'auto' }}
        >
          {options.length > 0 ? options : <Text p="xs">{nothing_found}</Text>}
        </Combobox.Options>
      </Combobox.Dropdown>
    </Combobox>
  );
}

export function RichSelectItem({ value, option, disabled = false, keywords, payload }) {
  return <div>{option}</div>;
}
