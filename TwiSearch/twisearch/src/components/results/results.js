// ResultsPage.js
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import SearchBar from '../searchbar/searchbar';
import './results.css'
import Pagination from '../pagination/Pagination'
import DropdownButton from '../dropdown';
import Sidebar from "../sidebar/sidebar";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro' // <-- import styles to be used


function ResultsPage() {
  

  const { search } = useLocation();
  const [results, setResults] = useState([]);
  const [searchquery, setSearchQuery] = useState('normal');
  const [option, setOption] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [currenttweets, setCurrenttweets] = useState([]);
  const [currenttopics, setCurrenttopics] = useState([]);
  const [currenthashtags, setCurrentHashtags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resultsPerPage] = useState(10);
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

   // Calculate the total number of pages
  const totalResults = results.length;
  const totalPages = Math.ceil(totalResults / resultsPerPage);

  // Get the current results
  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  

  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);


  

async function handleViewClick(id){
  // Send a request to the backend with the ID of the clicked result
  let obj;
  const res = await fetch(`http://127.0.0.1:5000/tweets?id=${id}&query=${searchquery}`)
  obj = await res.json()
  setCurrenttopics(obj[0])
  setCurrenttweets(obj[1])
  setCurrentHashtags(obj[3])
  handleShow();
  
};

useEffect(() => {
}, [currenttweets]);



async function fetchResults() {
      const query = new URLSearchParams(search).get('query');
      setSearchQuery(query);
      handleClose()
      setCurrenttweets([])
      setCurrenttopics([])
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
        const data = await response.json();
        setResults(data);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }

    }

  useEffect(() => {
    fetchResults();
  }, [search]);

  useEffect(() => {
    console.log(results)
  }, [results]);

  
  
  const onSelectOption = (optionValue) => {
    setOption(optionValue);
  };

  useEffect(() => {
    sortResults();
  }, [option]);

  const sortResults = () => {
    let sortedResults = [...results];
    console.log(option)
    if (option === 'normal') {
      sortedResults.sort((a, b) => b.score - a.score); // sort by score in descending order
    } else if (option === 'relevance') {
      sortedResults.sort((a, b) => b.cosine_similarity - a.cosine_similarity); // sort by cosine similarity in descending order
    } else if (option === 'frequency') {
      sortedResults.sort((a, b) => b.frequency - a.frequency); // sort by frequency in descending order
    }
    console.log(sortedResults);

    // update searchResults state
    setResults(sortedResults);
    };
  

  return (
    <React.Fragment>
      <div className="flex flex-col">
        <div class="flex items-center mt-4">
            <a href = "/">
              <h1 className="mr-4">TwiSearch</h1>
            </a>

            <div class="flex w-full md:w-1/2">
              <div class="flex-1">
                <SearchBar />
              </div>
              <div class="ml-2">
                <DropdownButton onSelectOption={onSelectOption} />
              </div>
            </div>
        </div>

        {loading && (       
            <div role="status">
                <svg aria-hidden="true" class="w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
              )}
        {!loading && (
        
        <div className="flex flex-wrap">
          {currentResults?.length > 0 ? (
            <div className="w-2/3 p-4">
              {currentResults.map(result => (
                <div key={result.id} className="bg-white rounded-lg mb-4 p-4">
                  <a href={result.url} className="text-blue-600 font-bold hover:underline" target="_blank" rel="noreferrer">{result.url}</a>
                  <p>{new Date(result.date).toDateString()}</p>
                  <div className="flex justify-between items-center">
                    <h2 className="text-lg font-bold mb-2"><a href={result.url} target="_blank" rel="noreferrer">{result.title}</a></h2>
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full mt-4" onClick={() => handleViewClick(result.id)}>
                      Show Tweets
                      <FontAwesomeIcon icon={solid("arrow-right")} size="xl" />
                    </button>
                  </div>
                  <p className="text-gray-700 text-base">{result.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="w-2/3 p-4">
              <h1>No results found</h1>
            </div>
          )}
          
            
              <div className="w-1/3 p-4">
                {show && (
                    <div className="flex flex-col items-center justify-center min-h-screen py-2">
                      <Sidebar currenthashtags = {currenthashtags} setShow = {setShow} show={show} currenttweets={currenttweets} currenttopics={currenttopics} />
                  </div>
                )}
              </div>
        </div>
        )}
        <Pagination
            nPages={totalPages}
            currentPage={currentPage}
            setCurrentPage={setCurrentPage}
        />
      </div>
      
    </React.Fragment>
  );
}

export default ResultsPage;
