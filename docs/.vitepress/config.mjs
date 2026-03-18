import { defineConfig } from 'vitepress'

export default defineConfig({
  // 博客基本信息
  title: "rockycao0's Blog",
  description: "算法工程师的个人博客",
  lang: 'zh-CN',
  
  // 站点URL，用于生成 sitemap 和 SEO
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3eaf7c' }]
  ],

  // 主题配置
  themeConfig: {
    // 导航栏
    nav: [
      { text: '首页', link: '/' },
      { text: '归档', link: '/archive' },
      { text: '关于我', link: '/about' }
    ],

    // 侧边栏 - 这里我们不需要，因为博客是独立页面
    sidebar: false,

    // 右侧导航
    socialLinks: [
      { icon: 'github', link: 'https://github.com/rockycao0' }
    ],

    // 开启搜索
    search: {
      provider: 'local'
    },

    // 页脚信息
    footer: {
      message: '基于 MIT 许可开源',
      copyright: 'Copyright © 2026-present rockycao0'
    },

    // 文章阅读提示
    outline: {
      level: [2, 3],
      label: '本文目录'
    },

    // 上一篇/下一篇导航
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    // 回到顶部按钮文字
    returnToTopLabel: '回到顶部',
  },

  // 配置永久链接，我们按日期组织文章
  cleanUrls: true,

  // 构建输出目录
  outDir: '../dist'
})
