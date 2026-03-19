---
title: GitHub Pages + VitePress 搭建个人博客踩坑总结
description: 记录一次从零搭建博客过程中遇到的各种问题，总结正确配置方式
date: 2026-03-19
---

# GitHub Pages + VitePress 搭建个人博客踩坑总结

今天从零开始搭建了一个基于 VitePress + GitHub Pages 的个人博客，中间踩了不少坑，这里总结一下给大家参考。

## 最终成功的项目结构

```
your-blog/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 自动部署
├── docs/
│   ├── index.md                # 首页
│   ├── archive.md              # 文章归档（按日期分组）
│   ├── about.md                # 关于我
│   ├── .vitepress/
│   │   └── config.mjs          # VitePress 配置
│   └── posts/                 # 所有文章放在这，命名格式 YYYY-MM-DD-title.md
│       ├── 2026-03-18-hello-world.md
│       └── ...
├── .gitignore
├── package.json
└── package-lock.json
```

## 坑点总结 & 解决方案

### 1. 相对路径问题 - `outDir` 配置

**错误做法：** 误以为 `outDir` 是相对于 `config.mjs` 所在目录，各种算错路径，导致GitHub Actions找不到构建输出。

**正确配置：**
当你执行 `vitepress build docs` 时，这个命令是在**项目根目录**执行的，所以 `outDir` 是相对于**项目根目录**，不是相对于 `config.mjs`。

实际开发中，最简单的做法就是**不配置 `outDir`**，直接使用默认输出 `docs/.vitepress/dist`，然后GitHub Actions上传这个路径。

```javascript
// docs/.vitepress/config.mjs
import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/',  // 如果你放在根域名（username.github.io），就写 '/'
  // ... 其他配置
  cleanUrls: true
  // 不要瞎折腾 outDir，默认就好
})
```

GitHub Actions 配置：
```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: ./docs/.vitepress/dist  # 默认输出路径，直接用这个
```

### 2. 文章链接 末尾斜杠问题

开启 `cleanUrls: true` 后：

- VitePress 生成文章：`posts/xxx.md` → `posts/xxx/index.html`
- GitHub Pages 访问：`yoursite.com/posts/xxx` **不需要末尾斜杠**就能正确访问
- 如果我们代码里生成链接是 `/posts/xxx/` 带斜杠，反而会出问题

**归档页面正确生成链接方式：**
```javascript
let postPath = path.replace(/^\.\/|\.md$/g, '') // → posts/xxx
postPath = '/' + postPath          // → /posts/xxx
// ❌ 不要画蛇添足加 postPath += '/'
```

### 3. 正确的链接生成代码（归档页）

```javascript
async function loadPosts() {
  const modules = import.meta.glob('./posts/*.md')
  
  const postList = []
  for (const path in modules) {
    const info = extractDateFromPath(path)
    if (info) {
      const module = await modules[path]()
      const frontmatter = module.frontmatter || {}
      
      // 正确生成路径：
      let postPath = path.replace(/^\.\/|\.md$/g, '')
      postPath = '/' + postPath
      
      postList.push({
        date: info.date,
        title: frontmatter.title || info.title,
        excerpt: frontmatter.description || '',
        path: postPath
      })
    }
  }
}
```

### 4. GitHub Pages 部署权限问题

使用 GitHub Actions 部署：
1. 仓库 → Settings → Pages → Source → 选择 **GitHub Actions**（不要选择 Deploy from a branch）
2. 仓库 → Settings → Actions → General → Workflow permissions → 选择 **Read and write permissions**
3. 如果用官方 `actions/deploy-pages@v4` 部署，不需要额外配置token，默认权限就够了

### 5. 项目目录git版本控制问题

- 你的GitHub仓库就是博客项目，所有源码都放在这个仓库
- GitHub Actions 自动帮你构建部署，不需要把构建结果提交上去
- `.gitignore` 正确写法：
```gitignore
# Dependencies
node_modules/

# Build output
docs/.vitepress/dist/

# IDE
.vscode
.idea
.DS_Store
```

### 6. 文章命名规范

我们要实现自动按日期归档，所以文章命名必须遵守：
```
YYYY-MM-DD-文章标题.md
```
比如：
- ✅ `2026-03-19-hello-world.md`
- ✅ `2026-03-19-machine-learning-model-optimization.md`

代码自动从文件名提取日期和标题，标题自动把横杠转成空格，非常方便。

### 最终工作流

1. 在本地 `D:\workspace\blog` 开发（符合要求：项目在子文件夹，git版本控制在这里）
2. 新建文章：在 `docs/posts` 新建 `YYYY-MM-DD-article-title.md`，写好markdown
3. `git add` + `git commit` + `git push origin blog`
4. GitHub Actions 自动构建部署，几分钟就能在网上看到了
5. 访问：`https://yourname.github.io/posts/YYYY-MM-DD-article-title` （不需要末尾斜杠，直接访问就好）

## 总结

折腾了这么久，大部分问题都是因为：
1. 对VitePress的相对路径规则理解错了
2. 对GitHub Pages的cleanUrls访问规则理解错了
3. 一开始git提交漏了文件，后来又误打误撞传了不该传的东西

现在终于全部搞定了，这个方案可以：
- ✅ 完全自动，push完就部署
- ✅ 文章自动按日期分组归档
- ✅ 自带搜索、代码高亮、响应式
- ✅ 完全免费，不用买服务器

希望这篇总结能帮助到下次再搭博客的时候少踩坑😊
