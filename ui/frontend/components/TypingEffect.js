import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { Back, Power1, Power2, Power3 } from 'gsap';

const TypingEffect = () => {
  const textareaRef = useRef(null); // 将 inputRef 改为 textareaRef
  return (
    <div className="google-style-container">
      <h1 className="nexus-title">SynthIQ NexuS</h1>
      
      <div className="input-container">
        <textarea
          ref={textareaRef}
          className="search-textarea"
          placeholder=""
        />
        <div className="button-container">

          <button className="search-button">📊Diagram</button>
          <button className="search-button">🎞️Media</button>
          <button className="search-button">🧪Audio</button>          
        </div>
      </div>
  <div class="stealth-description">
  <div class="description-trigger">🔍 功能说明</div>
  <div class="description-content">
    <h3>基于数据库的ai搜索引擎</h3>
    <p>支持搜索功能，包括：</p>
    <p>· 基于地理坐标的<span class="highlight">实时地图检索</span></p>
    <p>· 结合气象数据的<span class="highlight">智能天气预测</span></p>
    <p>· 动态生成的<span class="highlight">可视化数据图表</span></p>
    <p>· 多媒体资源的<span class="highlight">智能关联推荐</span></p>
    <p>· 开放式的<span class="highlight">数据接口服务</span></p>
  </div>
</div>

    </div>
  );
};

export default TypingEffect;


