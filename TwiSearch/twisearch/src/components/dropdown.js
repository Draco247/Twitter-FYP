import React from 'react';
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

const options = [
  { value: 'normal', label: 'Normal' },
  { value: 'relevance', label: 'Relevance' },
  { value: 'frequency', label: 'Frequency' },
];

const DropdownButton = ({ onSelectOption }) => {
  const handleSelect = (option) => {
    onSelectOption(option.value);
  };

  return (
    <Dropdown options={options} placeholder="Ranking Option" onChange={handleSelect} />
  );
};

export default DropdownButton;
