import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/',
  title: "rockycao0's Blog",
  description: "算法工程师的个人博客",
  lang: 'zh-CN',
  
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3eaf7c' }]
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '归档', link: '/archive/' },
      { text: '关于我', link: '/about/' }
    ],

    sidebar: false,

    socialLinks: [
      { icon: 'github', link: 'https://github.com/rockycao0' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      message: '基于 MIT 许可开源',
      copyright: 'Copyright © 2026-present rockycao0'
    },

    outline: {
      level: [2, 3],
      label: '本文目录'
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    returnToTopLabel: '回到顶部',
  },

  cleanUrls: true
})
