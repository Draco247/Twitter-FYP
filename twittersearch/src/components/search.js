import React, { useEffect, useState } from 'react';


function Search(props) {

    const { 
        onSearch 
      } = props;

    const [term, setTerm] = useState('');

    const handleInput = (e) => {
        const text = e.target.value
        setTerm(text)
      }
    
      const handleEnterKeyPressed = (e) => {
        if(e.key=== 'Enter') {
          console.log(term)
          onSearch(term)
        }
      }

      return (
        <div>
          <div className="control"> 
            <input
              className="input"
              onChange={handleInput}
              onKeyPress={handleEnterKeyPressed}
              type="text"
              value={term}
              placeholder="Search"
            />
          </div>
        </div>
      );

}

export default Search;
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