module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*', // 将请求代理到后端
      },
    ];
  },
};
