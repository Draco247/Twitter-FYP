import { useState } from 'react';
import { useNavigate,  createSearchParams,
} from 'react-router-dom';
import './searchbar.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid, regular, brands, icon } from '@fortawesome/fontawesome-svg-core/import.macro' // <-- import styles to be used

import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';

function SearchBar() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) {
      // If the query is empty or contains only whitespace, return from the function without navigating
      return;
    }
    
    navigate({
      pathname: '/results',
      search: `?${createSearchParams({query})}`
    });
  };

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
          <FontAwesomeIcon icon={solid("magnifying-glass")} />
        </button>
      </div>
    </form>
  
  );
}

export default SearchBar;
