import React, { useState } from 'react';
import '../styles/globals.css'; // 引入全局 CSS 文件
import ResultsPage from '../components/ResultsPage';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;
