import logo from './logo.svg';
import './App.css';
import Search from './components/search';
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [results, setresults] = useState([]);


//   const headers = {
//     "Access-Control-Allow-Headers": "*",
//     "Access-Control-Allow-Origin": "*",
//     "Access-Control-Allow-Methods": "*"      
// }
  const onSearch = async term => {
    const res = await axios.get(`http://127.0.0.1:5000/search?query=${term}`);
    const arr = await res.data;
    console.log(arr); 
    setresults(arr);
  };

  return (
    <div className='app'>
    <h1 className='title'>Realtime Search Bar</h1>
    <Search onSearch={onSearch} />
    {/* <Search onSearchSubmit={onSearch}/ */}
    <div className='main-content'>
      {results.map(data => (
        <p> - {data}</p>
      ))}
    </div>
  </div>    );
}

export default App;
