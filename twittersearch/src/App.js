import './App.css';
import Search from './components/search';
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [results, setresults] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  const handleSearchResults = (results) => {
    setSearchResults(results);
  }
  const data = {
  "name": "John Doe",
  "age": 32,
  "city": "New York"
};

  return (
    <div className='app'>
      <h1 className='title'>Realtime Search Bar</h1>
      <Search onSearchResults={handleSearchResults}/>
      <div>
      {/* {searchResults?.map(function(object, i){
        return <li key={i}>{object}</li>
        })} */}
      <div>
      {searchResults.map((d) => (
        <div key={d.id}>
          <p>ID: {d.id}</p>
          <p>Product Name: {d.productName}</p>
          <p>Price: {d.price}</p>
          <p>Description: {d.description}</p>
          <p>Category: {d.category}</p>
          <p>
             Image: <img src={d.image} width="100" />
          </p>
          <br />
          <br />
        </div>
  ))}
   </div>
      </div>
    </div>    
  );
}

export default App;
