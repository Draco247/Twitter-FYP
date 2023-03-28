import React from 'react';
import './tweets.css'
// import { TwitterTweetEmbed } from 'react-twitter-embed';


const Tweets = ({ tweet }) => {
  return (
     <div className="bg-slate-100 border border-slate-300 rounded-2xl duration-300 my-8 p-5 max-w-xl mx-auto">
      <div className="flex justify-between">
          <div className="flex flex-col leading-snug">
            <span className="text-sm opacity-80 group-hover:opacity-100 duration-300">{tweet.date}</span>
          </div>

      </div>
      <div className="flex my-3">
          <a className="flex items-center gap-3 group cursor-pointer hover:bg-slate-200" href={tweet.url} target="_blank" rel="noreferrer">
            <div className="text-lg leading-normal">{tweet.tweet}</div>
          </a>
          <div className="text-5xl">
              {tweet.sentiment.compound < 0 ? (
                  <span role="img" aria-label="sentiment">😠</span>
              ) : tweet.sentiment.compound === 0 ? (
                  <span role="img" aria-label="sentiment">😐</span>
              ) : (
                  <span role="img" aria-label="sentiment">🙂</span>
              )}
          </div>
      </div>
      <div className="flex mt-2 gap-8 text-sm font-medium tracking-wider">
        <span>{tweet.retweets} Retweets</span>
        <span>{tweet.impressions} Views</span>
      </div>
    </div>

  )
}


export default Tweets;