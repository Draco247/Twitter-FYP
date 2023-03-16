// SearchPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../searchbar/searchbar';
import './search.css'
import { TwitterTweetEmbed } from 'react-twitter-embed';

function SearchPage() {

  return (
    <div className="container">
      <h1>TwiSearch</h1>
      <SearchBar />
      {/* <TwitterTweetEmbed
        tweetId={'1621961127017201664'}
      />
      <TwitterTweetEmbed
        tweetId={'1622315647060566016'}
      /> */}
    </div>
  );
}

export default SearchPage;
