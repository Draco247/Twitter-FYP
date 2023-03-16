import React , { useEffect, useState } from 'react';

function VideosTab() {
    const [videos, setVideos] = useState([
      { id: 1, title: "Video 1" },
      { id: 2, title: "Video 2" },
      { id: 3, title: "Video 3" },
    ]);
  
    return (
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {videos.map((video) => (
          <div key={video.id} className="flex items-center p-4 bg-white rounded-lg shadow-lg">
            <div className="flex-shrink-0 h-20 w-32 bg-gray-400"></div>
            <div className="ml-4">
              <div className="text-lg font-medium text-gray-900">{video.title}</div>
              <div className="text-sm text-gray-500">Placeholder description</div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  export default VideosTab;