interface PaginationProps {
  currentPage: number;
  onPageChange: (page: number) => void;
  hasMore: boolean;
}

const Pagination = ({ currentPage, onPageChange, hasMore }: PaginationProps) => {
  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (hasMore) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div className="pagination">
      <button 
        onClick={handlePrevious}
        disabled={currentPage === 1}
        className="btn btn-secondary"
      >
        ← Previous
      </button>
      
      <span className="page-info">
        Page {currentPage}
      </span>
      
      <button 
        onClick={handleNext}
        disabled={!hasMore}
        className="btn btn-secondary"
      >
        Next →
      </button>
    </div>
  );
};

export default Pagination;