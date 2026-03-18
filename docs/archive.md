# 文章归档

按日期倒序排列，最新文章在最前面。

<!-- @vitepress-plugin-script-setup -->
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()
const posts = ref([])
const groupedPosts = ref({})

function extractDateFromPath(path) {
  // 从文件名提取日期，格式我们约定为 YYYY-MM-DD-title.md
  const fileName = path.split('/').pop()
  const match = fileName.match(/^(\d{4}-\d{2}-\d{2})-(.*)\.md$/)
  if (match) {
    return {
      date: match[1],
      title: match[2].replace(/-/g, ' '),
      path: path.replace(/^\/docs|\.md$/g, '')
    }
  }
  return null
}

async function loadPosts() {
  // 使用 Vite 的 glob 导入功能获取所有文章
  const modules = import.meta.glob('./posts/*.md')
  
  const postList = []
  for (const path in modules) {
    const info = extractDateFromPath(path)
    if (info) {
      // 获取文章元数据
      const module = await modules[path]()
      const frontmatter = module.frontmatter || {}
      postList.push({
        date: info.date,
        title: frontmatter.title || info.title,
        excerpt: frontmatter.description || '',
        path: '/' + path.replace(/^\.\/|md$/g, '')
      })
    }
  }
  
  // 按日期倒序排列
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
  
  posts.value = postList
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
