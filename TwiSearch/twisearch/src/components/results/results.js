// ResultsPage.js
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import SearchBar from '../searchbar/searchbar';
import VideosTab from '../videos/videos';
import './results.css'
import { TwitterTweetEmbed } from 'react-twitter-embed';
import Tweets from '../tweets/tweets'
import { ListGroup, Card } from 'react-bootstrap';
import Pagination from '../Pagination'
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import ReactWordcloud from 'react-wordcloud';
// import Pagination from 'react-bootstrap/Pagination';


function ResultsPage(...props) {
  // const [searchResults, setSearchResults] = useState([]);
  // const { state } = useLocation();
  // console.log(state);
  // const searchQuery = new URLSearchParams(location.search).get('q');
  // const tempsearchResults = [
  //   {
  //     title: 'Example Result 1',
  //     description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies urna at magna ullamcorper, a semper quam blandit. Integer luctus turpis ac nisi suscipit fringilla.',
  //     url: 'https://www.example.com/result1'
  //   },
  //   {
  //     title: 'Example Result 2',
  //     description: 'Sed ullamcorper lorem sed dolor maximus, at lacinia velit rutrum. Sed malesuada quam sit amet lectus suscipit, vel hendrerit ipsum lacinia. In pharetra felis vel lectus eleifend hendrerit.',
  //     url: 'https://www.example.com/result2'
  //   },
  //   {
  //     title: 'Example Result 3',
  //     description: 'Morbi consectetur lorem quis ipsum gravida rhoncus. Nulla in nunc id mi ornare mattis. Nullam a risus bibendum, vehicula massa ac, luctus libero.',
  //     url: 'https://www.example.com/result3'
  //   }
  // ];

  // const videos = [
  //   {
  //     id: 1,
  //     title: "Placeholder Video 1",
  //     url: "#",
  //     thumbnail: "https://via.placeholder.com/150",
  //   },
  //   {
  //     id: 2,
  //     title: "Placeholder Video 2",
  //     url: "#",
  //     thumbnail: "https://via.placeholder.com/150",
  //   },
  //   {
  //     id: 3,
  //     title: "Placeholder Video 3",
  //     url: "#",
  //     thumbnail: "https://via.placeholder.com/150",
  //   },
  // ];
  

  // useEffect(() => {
  //   // Fetch data from API or database using searchQuery
  //   // and set searchResults state with the fetched data
  // }, [searchQuery]);
  // const words = [
  //   {
  //     text: 'told'
  //   },
  //   {
  //     text: 'mistake',
  //     value: 11,
  //   },
  //   {
  //     text: 'thought',
  //     value: 16,
  //   },
  //   {
  //     text: 'bad',
  //     value: 17,
  //   },
  // ]

  const { search } = useLocation();
  const [results, setResults] = useState([]);
  const [searchquery, setSearchQuery] = useState('');
  const [showResults, setShowResults] = useState(false)
  const [currenturl, setCurrentUrl] = useState('')
  const [currentPage, setCurrentPage] = useState(1);
  const [currenttweets, setCurrenttweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState("All");
  // let [tweets, setTweets] = useState([]);
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
 
   // Change the current page
  //  const handlePageChange = (pageNumber) => {
  //    setCurrentPage(pageNumber);
  //  };

  const handleTabClick = (tab) => {
    setCurrentTab(tab);
  };
  
  async function handleViewClick(id){
    // Send a request to the backend with the ID of the clicked result
    let obj;
    const res = await fetch(`http://127.0.0.1:5000/tweets?id=${id}&query=${searchquery}`)
    obj = await res.json()
    // console.log(obj)
    // setTweets(obj)
    
    setCurrenttweets(obj)
    handleShow();
    
  };

  useEffect(() => {
    // fetchData();
    console.log(currenttweets)
    console.log(show)
    // handleShow();
  }, [currenttweets]);

  // const close = () => {
  //   setShowResults(false);
  // };
async function fetchResults() {
      const query = new URLSearchParams(search).get('query');
      // console.log(query);
      setSearchQuery(query);
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
      const data = await response.json();
      setLoading(false);
      // console.log(loading)
      setResults(data);
    }
  useEffect(() => {
    
      // console.log(results)
    fetchResults();
  }, [search]);

  useEffect(() => {
    // fetchData();
    console.log(results)
    // handleShow();
  }, [results]);
  

  

  return (
    <React.Fragment>
          {/* <h1>Search results for "{searchQuery}"</h1> */}
      <div className="flex flex-col">
        <div class="flex items-center mt-4">
          <h1 class="mr-4">TwiSearch</h1>
          <div class="w-full md:w-1/2">
            <SearchBar />
          </div>
        </div>
        <div className="mt-8">
          <div className="border-b border-gray-300">
            <nav className="flex justify-between">
              <button
                className={`${
                  currentTab === "All"
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-700"
                } py-2 px-4 font-semibold`}
                onClick={() => handleTabClick("All")}
              >
                All
              </button>
              <button
                className={`${
                  currentTab === "Videos"
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-700"
                } py-2 px-4 font-semibold`}
                onClick={() => handleTabClick("Videos")}
              >
                Videos
              </button>
            </nav>
          </div>
        </div>
        {loading && (       
            <div role="status">
              {/* <ReactWordcloud words={words} /> */}
                <svg aria-hidden="true" class="w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
              )}
        {!loading && (
        
        <div className="flex flex-wrap">
          {currentTab === "All" && (
            <div className="w-2/3 p-4">
              
              {currentResults?.map(result => (
                <div key={result.id} className="bg-white rounded-lg shadow-lg mb-4 p-4">
                  <a href={result.url} className="text-blue-600 font-bold hover:underline">{result.url}</a>
                  <div className="flex justify-between items-center">
                    <h2 className="text-lg font-bold mb-2"><a href={result.url}>{result.title}</a></h2>
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4" onClick={() => handleViewClick(result.id)}>
                        Show Tweets
                    </button>
                  </div>
                  <p className="text-gray-700 text-base">{result.description}</p>
                </div>
              ))}
            </div>
            )}
            {currentTab === "Videos" && <VideosTab />}
            <div className="w-1/3 p-4">
              {show && (
                <div className="bg-white rounded-lg shadow-lg mb-4 p-4">
                  <ul className="list-disc list-inside">
                    {currenttweets?.map(tweet => (
                      <li key={tweet.id}>
                        <Tweets tweet={tweet}/>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
        </div>
        )}
      </div>
      <Pagination
            nPages={totalPages}
            currentPage={currentPage}
            setCurrentPage={setCurrentPage}
        />
    </React.Fragment>
  );
}

export default ResultsPage;
