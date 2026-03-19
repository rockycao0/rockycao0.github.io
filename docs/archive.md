# 文章归档

按日期倒序排列，最新文章在最前面。

<script setup>
import { onMounted, ref } from 'vue'

const groupedPosts = ref({})

function extractDateFromPath(path) {
  // path example: ./posts/2026-03-18-hello-world.md
  const fileName = path.split('/').pop()
  const match = fileName.match(/^(\d{4}-\d{2}-\d{2})-(.*)\.md$/)
  if (match) {
    return {
      date: match[1],
      title: match[2].replace(/-/g, ' ')
    }
  }
  return null
}

async function loadPosts() {
  // Vite glob import
  const modules = import.meta.glob('./posts/*.md')
  
  const postList = []
  for (const path in modules) {
    const info = extractDateFromPath(path)
    if (info) {
      const module = await modules[path]()
      const frontmatter = module.frontmatter || {}
      
      // 正确生成路径：
      // path = ./posts/xxx.md → /posts/xxx/ 
      let postPath = path.replace(/^\.\/|\.md$/g, '') // → posts/xxx
      postPath = '/' + postPath
      // GitHub Pages cleanUrls 模式下，不需要末尾斜杠，不带斜杠反而正确
      
      postList.push({
        date: info.date,
        title: frontmatter.title || info.title,
        excerpt: frontmatter.description || '',
        path: postPath
      })
    }
  }
  
  // 按日期倒序
  postList.sort((a, b) => b.date.localeCompare(a.date))
  
  // 按年份分组
  const grouped = {}
  postList.forEach(post => {
    const year = post.date.slice(0, 4)
    if (!grouped[year]) {
      grouped[year] = []
    }
    grouped[year].push(post)
  })
  
  groupedPosts.value = grouped
}

onMounted(() => {
  loadPosts()
})
</script>

<div v-for="(yearPosts, year) in groupedPosts" :key="year" class="year-group">
  <h2 class="year-title">{{ year }}</h2>
  <ul class="post-list">
    <li v-for="post in yearPosts" :key="post.path" class="post-item">
      <span class="post-date">{{ post.date }}</span>
      <a :href="post.path" class="post-title">{{ post.title }}</a>
      <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>
    </li>
  </ul>
</div>

<style>
.year-group {
  margin-bottom: 2rem;
}

.year-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  margin-bottom: 1rem;
  border-bottom: 2px solid var(--vp-c-divider);
  padding-bottom: 0.5rem;
}

.post-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-item {
  padding: 0.8rem 0;
  border-bottom: 1px dashed var(--vp-c-divider-light);
}

.post-item:last-child {
  border-bottom: none;
}

.post-date {
  display: inline-block;
  min-width: 110px;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}

.post-title {
  color: var(--vp-c-text-1);
  text-decoration: none;
  font-weight: 500;
  margin-left: 0.5rem;
}

.post-title:hover {
  color: var(--vp-c-brand-1);
  text-decoration: underline;
}

.post-excerpt {
  margin: 0.3rem 0 0 115px;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}

@media (max-width: 640px) {
  .post-date {
    display: block;
    margin-bottom: 0.3rem;
  }
  
  .post-excerpt {
    margin-left: 0;
  }
}
</style>
