// SearchPage.js
import React, { useState } from 'react';
import SearchBar from '../searchbar/searchbar';
import './search.css'

function SearchPage() {

  return (
    <div className="container">
      <h1>TwiSearch</h1>
      <SearchBar />
    </div>
  );
}

export default SearchPage;
