const Pagination = ({ nPages, currentPage, setCurrentPage }) => {

    let startPage = 1;
    let endPage = Math.min(nPages, 5);

    if (currentPage > 3) {
        startPage = currentPage - 2;
        endPage = Math.min(currentPage + 2, nPages);
    }

    const pageNumbers = [...Array(endPage - startPage + 1).keys()].map(i => startPage + i);

    const nextPage = () => {
        if(currentPage !== nPages) setCurrentPage(currentPage + 1)
    }
    
    const prevPage = () => {
        if(currentPage !== 1) setCurrentPage(currentPage - 1)
    }
    
    return (
        <nav>
            <ul className='pagination justify-content-center'>
                <li className="page-item mr-1">
                    <a className="page-link text-sm"
                        onClick={prevPage}
                        href='#'>
                        Previous
                    </a>
                </li>
                {pageNumbers.map(pgNumber => (
                    <li key={pgNumber}
                        className={`page-item ${currentPage == pgNumber ? 'active' : ''} `}>
                        <a onClick={() => setCurrentPage(pgNumber)}
                            className='page-link text-sm'
                            href='#'>
                            {pgNumber}
                        </a>
                    </li>
                ))}
                <li className="page-item">
                    <a className="page-link text-sm"
                        onClick={nextPage}
                        href='#'>
                        Next
                    </a>
                </li>
            </ul>
        </nav>
    )
}

export default Pagination
