import { useState } from 'react';
import { useNavigate,  createSearchParams,
} from 'react-router-dom';
import './searchbar.css'
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';

function SearchBar() {
  // const [searchQuery, setSearchQuery] = useState('');
  // const navigate = useNavigate();

  // // const handleFormSubmit = (event) => {
  // //   event.preventDefault();
  // //   navigate(`/results?q=${searchQuery}`);
  // // };
  // function handleSearchSubmit(event) {
  //   event.preventDefault();
  //   const formData = new FormData(event.target);
  //   const searchQuery = formData.get('searchQuery');
  //   // setSearchQuery = formData.get('searchQuery');
  //   console.log(searchQuery);
  //   fetch('http://127.0.0.1:5000/search?query=' + encodeURIComponent(searchQuery))
  //     .then(response => response.json())
  //     .then(data => {
  //       // Process the search results here
  //     })
  //     .catch(error => {
  //       console.error('Error searching:', error);
  //     });
  // }

  // const handleInputChange = (event) => {
  //   setSearchQuery(event.target.value);
  // };

  // return (
  //   <form onSubmit={handleSearchSubmit}>
  //     <input type="text" value={searchQuery} onChange={handleInputChange} />
  //     <button type="submit">Search</button>
  //   </form>
  // );
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    // console.log(query)
    // const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
    // const data = await response.json();
    // console.log(data);
    // do something with the search results
    
    navigate({
      pathname: '/results',
      search: `?${createSearchParams({query})}`
      // state:{ result: data },
    });
    // ?q=${query}
  };
    // navigate(`/results?q=${query}`);

  return (
    <form onSubmit={handleSubmit} class="mb-3">
      <div class="mb-6">
        <input
          type="text"
          class="appearance-none bg-transparent border-none w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none"
          placeholder="Enter search query"
          aria-label="Search Query"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <button
          class="bg-gray-200 text-gray-700 font-bold py-2 px-4 border border-gray-300 rounded-md ml-1 hover:bg-gray-300 focus:outline-none focus:shadow-outline-gray active:bg-gray-400 transition duration-150 ease-in-out"
          type="submit"
        >
          Search
        </button>
      </div>
    </form>
  
  );
}

export default SearchBar;
