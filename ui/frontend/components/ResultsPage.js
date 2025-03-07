import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import styles from '../styles/ResultsPage.module.css';

const ResultsPage = () => {
  const [activeSections, setActiveSections] = useState({
    audio: false,
    chart: false,
    media: false
  });

  const toggleSection = (section) => {
    setActiveSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const renderContent = () => {
    const activeCount = Object.values(activeSections).filter(Boolean).length;
    const layoutClass = activeCount === 0 ? styles.fullWidth : 
                       activeCount === 1 ? styles.threeQuarter : 
                       activeCount === 2 ? styles.halfWidth : 
                       styles.quarterWidth;

    return (
      <div className={styles.contentContainer}>
        <div className={`${styles.section} ${styles.audioSection} ${!activeSections.audio ? styles.collapsed : ''}`}>
          <h3>音频内容</h3>
          <div className={styles.scrollContent}>
            {/* 音频内容 */}
            <audio controls>
              <source src="/audio/sample.mp3" type="audio/mpeg" />
              您的浏览器不支持 audio 元素。
            </audio>
          </div>
        </div>

        <div className={`${styles.section} ${styles.chartSection} ${!activeSections.chart ? styles.collapsed : ''}`}>
          <h3>图表内容</h3>
          <div className={styles.scrollContent}>
            {/* 图表内容 */}
            <img src="/images/sample-chart.png" alt="示例图表" />
          </div>
        </div>

        <div className={`${styles.section} ${styles.mediaSection} ${!activeSections.media ? styles.collapsed : ''}`}>
          <h3>媒体内容</h3>
          <div className={styles.scrollContent}>
            {/* 媒体内容 */}
            <video controls width="100%">
              <source src="/videos/sample.mp4" type="video/mp4" />
              您的浏览器不支持 video 标签。
            </video>
          </div>
        </div>

        <div className={`${styles.section} ${styles.markdownSection} ${layoutClass}`}>
          <h3>Markdown 结果</h3>
          <div className={styles.scrollContent}>
            <ReactMarkdown>
              {`
              # 示例 Markdown 内容

              ## 二级标题

              - 列表项 1
              - 列表项 2
              - 列表项 3

              **加粗文本**

              *斜体文本*

              [链接示例](https://example.com)
              `}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={styles.resultsContainer}>
      <aside className={styles.sidebar}>
        <button 
          className={`${styles.sidebarButton} ${activeSections.audio ? styles.active : ''}`}
          onClick={() => toggleSection('audio')}
        >
          音频
        </button>
        <button 
          className={`${styles.sidebarButton} ${activeSections.chart ? styles.active : ''}`}
          onClick={() => toggleSection('chart')}
        >
          图表
        </button>
        <button 
          className={`${styles.sidebarButton} ${activeSections.media ? styles.active : ''}`}
          onClick={() => toggleSection('media')}
        >
          媒体
        </button>
      </aside>

      <main className={styles.mainContent}>
        {renderContent()}
      </main>
    </div>
  );
};

export default ResultsPage;
