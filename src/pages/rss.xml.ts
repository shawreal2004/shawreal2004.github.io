import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPosts, articleUrl } from '../lib/blog';
import { site } from '../data/site';
export async function GET(context: APIContext) {
  const posts = await getPosts();
  return rss({ title: site.title, description: site.description, site: context.site!, items: posts.map(post => ({ title: `${post.data.demo ? '[示例] ' : ''}${post.data.title}`, description: post.data.description, pubDate: post.data.pubDate, link: articleUrl(post.id) })), customData: '<language>zh-cn</language>' });
}
