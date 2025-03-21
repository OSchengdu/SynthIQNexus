import React, { useState, useEffect } from 'react';
import MarkdownRenderer from './MarkdownRenderer';
import styles from '../styles/ResultsPage.module.css';

const ResultsPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);

  // 模拟 neofetch 输出
  const neofetchArt = `
                 competition@po
                 .o+                    --------------
                \`ooo/                   OS: Arch Linux x86_64
               \`+oooo:                  Host: 82RC (Legion Y7000P IAH7)
              \`+oooooo:                 Kernel: Linux 6.13.7-arch1-1
              -+oooooo+:                Uptime: 7 hours, 12 mins
            \`/:-:++oooo+:               Packages: 1964 (pacman), 36 (flatpak)
           \`/++++/+++++++:              Shell: bash 5.2.37
          \`/++++++++++++++:             Display (BOE0A2D): 2560x1440 @ 165 Hz (as 1602x901) in 15" [Built-in]
         \`/+++ooooooooooooo/\`           WM: Hyprland 0.47.2 (Wayland)
        ./ooosssso++osssssso+           Cursor: Adwaita
       .oossssso-\`\`\`\`/ossssss+          Terminal: alacritty 0.15.1
      -osssssso.      :ssssssso.         Terminal Font: alacritty (7.0pt)
     :osssssss/        osssso+++.        CPU: 12th Gen Intel(R) Core(TM) i5-12500H (16) @ 4.50 GHz
    /ossssssss/        +ssssooo/-        GPU 1: NVIDIA GeForce RTX 3050 Ti Mobile [Discrete]
  \`/ossssso+/:-        -:/+osssso+-      GPU 2: Intel Iris Xe Graphics @ 1.30 GHz [Integrated]
 \`+sso+:-                 \`.-/+oso:     Memory: 7.16 GiB / 23.20 GiB (31%)
\`++:.                           \`-/+/    Swap: 0 B / 12.50 GiB (0%)
.\`                                 \`/    Disk (/): 136.39 GiB / 195.80 GiB (70%) - ext4
                                         Disk (/home): 133.76 GiB / 195.80 GiB (68%) - ext4
                                         Local IP (wlan0): 192.168.23.193/24
                                         Battery (L21B4PC0): 98% [AC Connected]
                                         Locale: en_US.UTF-8
  `;

  // 从 API 获取数据
  const fetchSearchResults = async (query, trigger) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/search?query=${query}&trigger=${trigger}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Failed to fetch search results:', error);
    }
  };

  // 提交智能体输出
  const submitAgentOutput = async (content) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/agent-output', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Agent output submitted:', data);
    } catch (error) {
      console.error('Failed to submit agent output:', error);
    }
  };

  useEffect(() => {
    fetchSearchResults('', '');
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchSearchResults(searchQuery, '');
  };

  return (
    <div className={styles.resultsContainer}>
      {/* 背景层：neofetch 输出 */}
      <div className={styles.backgroundArt}>
        <pre>{neofetchArt}</pre>
      </div>

      {/* 中间结果块 */}
      <main className={styles.mainContent}>
        <header className={styles.resultsHeader}>
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

        <div className={styles.resultsList}>
          {results.map((result, index) => (
            <div key={index} className={styles.resultItem}>
              <div className={styles.resultMeta}>
                <span className={styles.resultTrigger}>{result.trigger.toUpperCase()}</span>
              </div>
              <div className={styles.markdownSection}>
                <h2 className={styles.resultTitle}>{result.title}</h2>
                <MarkdownRenderer content={result.description} />
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default ResultsPage;
