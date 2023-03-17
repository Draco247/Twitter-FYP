const Pagination = ({ tweetsPerPage, totalTweets, paginate })  => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalTweets / tweetsPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <div>
      {pageNumbers.map(number => (
        <button key={number} onClick={() => paginate(number)}>
          {number}
        </button>
      ))}
    </div>
  );
}
