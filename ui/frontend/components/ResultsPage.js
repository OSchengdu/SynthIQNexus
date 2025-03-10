import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import styles from '../styles/ResultsPage.module.css';

const ResultsPage = () => {
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [activeTab, setActiveTab] = useState('dork');
  const [chartData, setChartData] = useState(null);
  const [regenerateCount, setRegenerateCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');

  const sampleData = {
    dork: {
      title: 'Dork 搜索结果',
      urls: [
        'https://example.com/dork1',
        'https://example.com/dork2'
      ]
    },
    arp: {
      title: 'ARP 扫描结果',
      devices: [
        '192.168.1.1 - Device A',
        '192.168.1.2 - Device B',
        '192.168.1.3 - Device C'
      ]
    },
    db: {
      title: '数据库查询结果',
      table: `
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
      `,
      summary: `
- 总计: 100
- 平均值: 33.3
- 最大值: 50
      `
    },
    integrated: {
      title: '整合结果',
      content: `
# 整合结果

- 综合了 Dork、ARP 和 DB 的结果
- 提供统一的视图
      `
    },
    web: {
      title: '普通网页搜索结果',
      urls: [
        'https://example.com/web1',
        'https://example.com/web2'
      ]
    }
  };

  const handleRegenerate = () => {
    setRegenerateCount(prev => prev + 1);
    setChartData(`/images/chart-${regenerateCount % 3}.png`);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    console.log('Search:', searchQuery);
  };

  const renderTabContent = () => {
    const data = sampleData[activeTab];
    
    return (
      <div className={styles.tabContent}>
        <div className={styles.resultsSection}>
          <h2>{data.title}</h2>
          
          {activeTab === 'dork' && (
            <ul className={styles.urlList}>
              {data.urls.map((url, index) => (
                <li key={index}>
                  <a href={url} target="_blank" rel="noopener noreferrer">
                    {url}
                  </a>
                </li>
              ))}
            </ul>
          )}

          {activeTab === 'arp' && (
            <div className={styles.terminal}>
              <pre>
                {data.devices.join('\n')}
              </pre>
              <div className={styles.terminalControls}>
                <button>⬆️</button>
                <button>⬇️</button>
              </div>
            </div>
          )}

          {activeTab === 'db' && (
            <div className={styles.dbResults}>
              <div className={styles.dbTable}>
                <ReactMarkdown>{data.table}</ReactMarkdown>
              </div>
              <div className={styles.dbSummary}>
                <ReactMarkdown>{data.summary}</ReactMarkdown>
              </div>
            </div>
          )}

          {activeTab === 'integrated' && (
            <div className={styles.integratedResults}>
              <ReactMarkdown>{data.content}</ReactMarkdown>
            </div>
          )}

          {activeTab === 'web' && (
            <ul className={styles.urlList}>
              {data.urls.map((url, index) => (
                <li key={index}>
                  <a href={url} target="_blank" rel="noopener noreferrer">
                    {url}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className={styles.chartSection}>
          <div className={styles.chartHeader}>
            <h3>生成图表</h3>
            <button 
              className={styles.regenerateButton}
              onClick={handleRegenerate}
            >
              🔄 重新生成
            </button>
          </div>
          {chartData && (
            <img src={chartData} alt="生成的图表" />
          )}
        </div>
      </div>
    );
  };

  return (
    <div className={styles.resultsContainer}>
      <div className={`${styles.sidebar} ${sidebarVisible ? '' : styles.collapsed}`}>
        <button className={styles.toggleButton} onClick={() => setSidebarVisible(!sidebarVisible)}>
          {sidebarVisible ? '◀' : '▶'}
        </button>
        <nav>
          <button 
            className={`${styles.sidebarButton} ${activeTab === 'dork' ? styles.active : ''}`}
            onClick={() => setActiveTab('dork')}
          >
            Dork
          </button>
          <button 
            className={`${styles.sidebarButton} ${activeTab === 'arp' ? styles.active : ''}`}
            onClick={() => setActiveTab('arp')}
          >
            ARP
          </button>
          <button 
            className={`${styles.sidebarButton} ${activeTab === 'db' ? styles.active : ''}`}
            onClick={() => setActiveTab('db')}
          >
            DB
          </button>
          <button 
            className={`${styles.sidebarButton} ${activeTab === 'integrated' ? styles.active : ''}`}
            onClick={() => setActiveTab('integrated')}
          >
            整合结果
          </button>
          <button 
            className={`${styles.sidebarButton} ${activeTab === 'web' ? styles.active : ''}`}
            onClick={() => setActiveTab('web')}
          >
            网页结果
          </button>
        </nav>
      </div>

      <main className={styles.mainContent}>
        <header className={styles.resultsHeader}>
          <div className={styles.headerTop}>
            <h1>搜索结果标题</h1>
          </div>
          <div className={styles.metaInfo}>
            <span>相关度: 0.85</span>
            <span>更新时间: 刚刚</span>
            <span>来源: 综合数据库</span>
          </div>
          <form className={styles.searchForm} onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="输入搜索内容..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit">搜索</button>
          </form>
        </header>

        {renderTabContent()}
      </main>
    </div>
  );
};

export default ResultsPage;
