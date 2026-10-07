import { getCollection, type CollectionEntry } from 'astro:content';

export const withBase = (path: string) => `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
export const articleUrl = (id: string) => withBase(`/blog/${id}/`);
export const tagUrl = (tag: string) => withBase(`/tags/${encodeURIComponent(tag)}/`);
export const dateText = (date: Date) => date.toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit' }).replaceAll('/', '.');
export const readingTime = (post: CollectionEntry<'blog'>) => Math.max(1, Math.ceil((post.body?.length ?? 0) / 450));

export async function getPosts() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}
