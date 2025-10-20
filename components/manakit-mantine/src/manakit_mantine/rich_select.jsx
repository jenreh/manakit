import React, { useState, useMemo, useEffect } from 'react';
import { Combobox, Input, InputBase, Text, useCombobox, CloseButton } from '@mantine/core';

export function RichSelect({
  value = null,
  onChange,
  onOptionSubmit,
  onSearchChange,
  onClear,
  onDropdownOpen,
  onDropdownClose,
  placeholder = 'Pick value',
  searchable = true,
  clearable = false,
  nothing_found = 'Nothing found',
  max_dropdown_height = 280,

  // Combobox props
  position,
  middlewares,
  hidden,

  // Size and style props
  width,
  min_height,
  max_height,
  height,
  size,
  radius,
  className,
  classNames,
  styles,
  unstyled,

  // Additional props
  id,
  name,
  aria_label,
  disabled,

  children,
  ...rest  // Catch any other props
}) {
  const [search, setSearch] = useState('');
  const [internalValue, setInternalValue] = useState(value);
  useEffect(() => { setInternalValue(value); }, [value]);

  const combobox = useCombobox({
    onDropdownOpen: () => { if (onDropdownOpen) onDropdownOpen(); },
    onDropdownClose: () => {
      if (onDropdownClose) onDropdownClose();
      combobox.resetSelectedOption();
    },
  });

  const items = React.Children.toArray(children).filter(Boolean);

  const filteredItems = useMemo(() => {
    if (!searchable || !search.trim()) return items;
    const q = search.toLowerCase();
    return items.filter((item) => {
      const v = String(item.props.value ?? '').toLowerCase();
      const kws = Array.isArray(item.props.keywords) ? item.props.keywords : [];
      return v.includes(q) || kws.some((kw) => String(kw).toLowerCase().includes(q));
    });
  }, [search, items, searchable]);

  const selectedValue = internalValue;
  const selectedItem = items.find((i) => i.props.value === selectedValue);

  const handleSelect = (val) => {
    if (onChange) onChange(val); else setInternalValue(val);
    if (onOptionSubmit) onOptionSubmit(val);
    combobox.closeDropdown();
  };

  const handleSearch = (val) => {
    setSearch(val);
    combobox.resetSelectedOption();
    if (onSearchChange) onSearchChange(val);
  };

  const handleClear = (e) => {
    e.stopPropagation();
    const prev = selectedValue;
    if (onChange) onChange(null); else setInternalValue(null);
    setSearch('');
    if (onClear) onClear(prev);
  };

  const options = filteredItems.map((item, index) => (
    <Combobox.Option
      key={item.key ?? `option-${index}`}
      value={String(item.props.value)}
      disabled={!!item.props.disabled}
      onClick={() => handleSelect(item.props.value)}
    >
      {item.props.option}
    </Combobox.Option>
  ));

  // Build style object for InputBase
  const inputBaseStyle = {
    minHeight: min_height,
    maxHeight: max_height,
    height: height,
  };

  // Build style object for Combobox wrapper
  const comboboxStyle = {
    width: width,
  };

  return (
    <Combobox
      store={combobox}
      onOptionSubmit={handleSelect}
      position={position}
      middlewares={middlewares}
      hidden={hidden}
      classNames={classNames}
      styles={styles}
      unstyled={unstyled}
      style={comboboxStyle}
      disabled={disabled}
      {...rest}
    >
      <Combobox.Target>
        <InputBase
          component="button"
          type="button"
          pointer
          id={id}
          name={name}
          aria-label={aria_label}
          disabled={disabled}
          size={size}
          radius={radius}
          style={inputBaseStyle}
          className={className}
          rightSection={
            clearable && selectedValue ? (
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
          rightSectionPointerEvents={clearable && selectedValue ? 'auto' : 'none'}
          multiline
        >
          {selectedItem ? selectedItem.props.option : (
            <Input.Placeholder>{placeholder}</Input.Placeholder>
          )}
        </InputBase>
      </Combobox.Target>

      <Combobox.Dropdown>
        {searchable && (
          <Combobox.Search
            value={search}
            onChange={(e) => handleSearch(e.currentTarget.value)}
            placeholder="Search..."
            rightSection={null}
          />
        )}
        <Combobox.Options style={{ maxHeight: max_dropdown_height, overflowY: 'auto' }}>
          {options.length > 0 ? options : <Text p="xs">{nothing_found}</Text>}
        </Combobox.Options>
      </Combobox.Dropdown>
    </Combobox>
  );
}

export function RichSelectItem({ value, option, disabled = false, keywords, payload }) {
  return <div style={{ display: 'contents' }}>{option}</div>;
}
