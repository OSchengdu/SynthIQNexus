import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import styles from './ResultsPage.module.css';

const ResultsPage = () => {
  const [markdownContent, setMarkdownContent] = useState('');
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const containerRef = useRef(null);

  const loadMoreResults = async () => {
    if (!hasMore || isLoading) return;

    setIsLoading(true);
    try {
      const response = await fetch(`/api/generate?page=${page}`);
      const data = await response.json();

      setMarkdownContent((prev) => prev + "\n" + data.markdown);
      setHasMore(data.has_more);
      setPage(page + 1);
    } catch (error) {
      console.error("加载失败：", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadMoreResults();
  }, []);

  useEffect(() => {
    const container = containerRef.current;
    const handleScroll = () => {
      if (
        container.scrollTop + container.clientHeight >= container.scrollHeight - 100 &&
        hasMore &&
        !isLoading
      ) {
        loadMoreResults();
      }
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [hasMore, isLoading]);

  return (
    <div className={styles.resultsContainer} ref={containerRef}>
      <ReactMarkdown>{markdownContent}</ReactMarkdown>
      {isLoading && <div className={styles.loading}>加载中...</div>}
      {!hasMore && <div className={styles.noMore}>没有更多结果了</div>}
    </div>
  );
};

export default ResultsPage;
