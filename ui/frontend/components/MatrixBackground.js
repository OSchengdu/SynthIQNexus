import React, { useEffect, useRef } from 'react';
import styles from '../styles/MatrixBackground.module.css';

const MatrixBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // 设置 canvas 大小
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // 定义字符集
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+{}:"<>?[];\',./`~';
    const charactersArray = characters.split('');

    // 定义字体大小和列宽
    const fontSize = 14;
    const columns = canvas.width / fontSize;

    // 创建一个数组来存储每一列的下落位置
    const drops = [];
    for (let i = 0; i < columns; i++) {
      drops[i] = Math.floor(Math.random() * canvas.height); // 随机初始化下落位置
    }

    // 绘制函数
    const draw = () => {
      // 设置背景为半透明黑色，以产生拖尾效果
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // 设置字体颜色和样式
      ctx.fillStyle = '#00FF00';
      ctx.font = `${fontSize}px monospace`;

      // 为每一列绘制字符
      for (let i = 0; i < drops.length; i++) {
        const text = charactersArray[Math.floor(Math.random() * charactersArray.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        // 如果字符超出画布底部，则重置到顶部
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }

        // 增加下落位置
        drops[i]++;
      }
    };

    // 设置动画循环
    const interval = setInterval(draw, 33);

    // 清理函数
    return () => clearInterval(interval);
  }, []);

  return <canvas ref={canvasRef} className={styles.matrixCanvas} />;
};

export default MatrixBackground;
