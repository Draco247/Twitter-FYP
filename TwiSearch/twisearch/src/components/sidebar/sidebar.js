// import { useState } from "react";
import './sidebar.css'
import ReactWordcloud from 'react-wordcloud';
import Tweets from '../tweets/tweets'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro'
import React from "react";


const Sidebar = ({currenthashtags, setShow,show,currenttweets,currenttopics,currentsentiment, numtweets}) => {

    return(
        <>
          {show && (
            <button
              className="flex text-4xl text-white items-center cursor-pointer fixed right-10 top-2 z-50"
              onClick={() => setShow(!show)}
            >
             <FontAwesomeIcon icon={solid("xmark")} />
            </button>
          )}
          <div
            className={`top-0 right-0 w-[35vw] bg-blue-300  p-5  fixed h-full z-40  ease-in-out duration-300 ${
              show ? "translate-x-0 " : "translate-x-full"
            }`}
          >
                {show && (
                    <div className="topics bg-white mb-4 border-2 border-sky-500 rounded-full flex justify-center">
                        {currenttopics && currenttopics.length > 0 &&(
                          <div style={{ height: 200, width: 300 }}>
                            <ReactWordcloud
                              words={currenttopics}
                              options={{
                                fontSizes: [20, 90],
                                rotations: 0,
                                enableOptimizations: true
                              }}
                            />
                          </div>
                        )}
                      </div>
                )}
                  {show && (
                      <div className="hashtags">
                       <ul className="flex flex-wrap">
                        {currenthashtags && currenthashtags.length > 0 && currenthashtags.map((item) => (
                          <li className="mr-2">
                              <button className="bg-blue-500 hover:bg-blue-700 text-purple-600 font-bold rounded-full border-2 border-sky-500 mb-4 p-2" onClick={() => window.open(`https://twitter.com/hashtag/${item.substring(1)}`, '_blank')}>
                                    {item}
                              </button>
                          </li>
                        ))}
                       </ul>
                      </div>

                    )}

                  {show && (
                  <div className="bg-white rounded-lg shadow-lg mb-4 p-4" style={{height: "800px", overflowY: "scroll"}}>
                      <div className="text-4xl">
                          Overall Sentiment:
                          {currentsentiment < 0 ? (
                              <span role="img" aria-label="sentiment">😠</span>
                          ) : currentsentiment === 0 ? (
                              <span role="img" aria-label="sentiment">😐</span>
                          ) : (
                              <span role="img" aria-label="sentiment">🙂</span>
                          )}
                      </div>
                      <div className="text-2xl">
                          Total tweets:
                          {numtweets}
                      </div>
                      <ul className="divide-y divide-gray-300">
                          {currenttweets && currenttweets.length > 0 && currenttweets.map(tweet => (
                              <li className="py-4" key={tweet.id}>
                                  <Tweets tweet={tweet}/>
                              </li>
                          ))}
                      </ul>

                  </div>
                )}
          </div>
        </>

    )
}

export default Sidebar;