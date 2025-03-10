import React, { useState, useEffect } from 'react'
import MarkdownRenderer from './MarkdownRenderer'
import styles from '../styles/ResultsPage.module.css'

const ResultsPage = () => {
  const [sidebarVisible, setSidebarVisible] = useState(true)
  const [activeTab, setActiveTab] = useState('dork')
  const [markdownContent, setMarkdownContent] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  // 模拟数据
  const sampleData = {
    dork: `
# Dork 搜索结果

## 相关链接
- [示例链接1](https://example.com/dork1)
- [示例链接2](https://example.com/dork2)

## 统计信息
- 总结果数：2
- 相关度：0.85
    `,
    arp: {
      title: 'ARP 扫描结果',
      devices: [
        '192.168.1.1 - Device A',
        '192.168.1.2 - Device B',
        '192.168.1.3 - Device C'
      ]
    },
    db: `
# 数据库查询结果

## 数据表
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |

## 统计摘要
- 总计: 100
- 平均值: 33.3
- 最大值: 50
    `,
    integrated: `
# 整合结果

## 综合信息
- 综合了 Dork、ARP 和 DB 的结果
- 提供统一的视图

## 代码示例
\`\`\`python
def integrate_results():
    print("整合完成")
\`\`\`
    `,
    web: `
# 普通网页搜索结果

## 相关链接
- [示例链接1](https://example.com/web1)
- [示例链接2](https://example.com/web2)
    `
  }

  // 动态生成Markdown内容
  const generateMarkdown = (tab) => {
    if (tab === 'arp') return '' // ARP保持原样
    return sampleData[tab]
  }

  useEffect(() => {
    setMarkdownContent(generateMarkdown(activeTab))
  }, [activeTab])

  const handleRegenerate = () => {
    // 模拟重新生成Markdown
    const newContent = `
# 重新生成的内容

- 生成时间：${new Date().toLocaleTimeString()}
- 随机值：${Math.random().toFixed(4)}

\`\`\`javascript
console.log("重新生成内容")
\`\`\`
    `
    setMarkdownContent(newContent)
  }

  const renderTabContent = () => {
    if (activeTab === 'arp') {
      return (
        <div className={styles.terminal}>
          <pre>
            {sampleData.arp.devices.join('\n')}
          </pre>
          <div className={styles.terminalControls}>
            <button>⬆️</button>
            <button>⬇️</button>
          </div>
        </div>
      )
    }

    return (
      <div className={styles.markdownSection}>
        <MarkdownRenderer content={markdownContent} />
      </div>
    )
  }

  return (
    <div className={styles.resultsContainer}>
      {/* 侧边栏 */}
      <div className={`${styles.sidebar} ${sidebarVisible ? '' : styles.collapsed}`}>
        <button className={styles.toggleButton} onClick={() => setSidebarVisible(!sidebarVisible)}>
          {sidebarVisible ? '◀' : '▶'}
        </button>
        <nav>
          {['dork', 'arp', 'db', 'integrated', 'web'].map(tab => (
            <button
              key={tab}
              className={`${styles.sidebarButton} ${activeTab === tab ? styles.active : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab.toUpperCase()}
            </button>
          ))}
        </nav>
      </div>

      {/* 主内容区 */}
      <main className={styles.mainContent}>
        <header className={styles.resultsHeader}>
          <div className={styles.headerTop}>
            <h1>{activeTab.toUpperCase()} 结果</h1>
          </div>
          <div className={styles.metaInfo}>
            <span>相关度: 0.85</span>
            <span>更新时间: 刚刚</span>
            <span>来源: 综合数据库</span>
          </div>
          <form className={styles.searchForm} onSubmit={(e) => e.preventDefault()}>
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
          {/* 图表占位符 */}
          <div style={{ height: '200px', background: '#000' }} />
        </div>
      </main>
    </div>
  )
}

export default ResultsPage
