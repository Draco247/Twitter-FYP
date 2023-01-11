import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([])

  const handleChange = event => {
    setQuery(event.target.value);
  };

  // const onSearch = async term => {
  //     const res = await axios.get(`http://127.0.0.1:5000/search?query=${term}`);
  //     const arr = await res.data;
  //     console.log(arr); 
  //     setresults(arr);
  //   };

  const handleSubmit = event => {
    event.preventDefault();
    // Send query to backend using fetch or axios
    fetch('http://127.0.0.1:5000/search?query=' + query)
      .then(response => response.json())
      .then(data => {
        // Update component's state with results
        setResults(data.results);
        onSearchResults(data.results);
        console.log(data);
      });
  };


  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="Search..."
      />
      <button type="submit">Search</button>
    </form>
  );
};

export default SearchBar;


// import React, { useEffect, useState } from 'react';


// function Search(props) {

//     const { 
//         onSearch 
//       } = props;

//     const [term, setTerm] = useState('');

//     const handleInput = (e) => {
//         const text = e.target.value
//         setTerm(text)
//       }
    
//       const handleEnterKeyPressed = (e) => {
//         if(e.key=== 'Enter') {
//           console.log(term)
//           onSearch(term)
//         }
//       }

//       return (
//         <div>
//           <div className="control"> 
//             <input
//               className="input"
//               onChange={handleInput}
//               onKeyPress={handleEnterKeyPressed}
//               type="text"
//               value={term}
//               placeholder="Search"
//             />
//           </div>
//         </div>
//       );

// }

// export default Search;
// function search(props) {
    
//     }

// export default search;

// // function Searchbar(props) {
// //   const { 
// //     onSearch 
// //   } = props;

//   const [searchText, setSearchText] = useState('')

//   const handleInput = (e) => {
//     const text = e.target.value
//     setSearchText(text)
//   }

//   const handleEnterKeyPressed = (e) => {
//     if(e.key=== 'Enter') {
//       onSearch(searchText)
//     }
//   }

//   return (
//     <div>
//       <div className="control"> 
//         <input
//           className="input"
//           onChange={handleInput}
//           onKeyPress={handleEnterKeyPressed}
//           type="text"
//           value={searchText}
//           placeholder="Search your movies"
//         />
//       </div>
//     </div>
//   );
// }