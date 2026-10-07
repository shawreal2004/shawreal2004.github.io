import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// GitHub Actions supplies GITHUB_REPOSITORY. Custom domains can override SITE_URL.
const repository = process.env.GITHUB_REPOSITORY;
const [owner, repo] = repository?.split('/') ?? [];
const site = process.env.SITE_URL || (owner ? `https://${owner}.github.io` : 'http://localhost:4321');
const base = process.env.BASE_PATH || (owner && repo?.toLowerCase() !== `${owner.toLowerCase()}.github.io` && !process.env.SITE_URL ? `/${repo}` : '/');

export default defineConfig({
  site,
  base,
  output: 'static',
  trailingSlash: 'always',
  integrations: site.startsWith('http://localhost') ? [] : [sitemap()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: { theme: 'github-dark' },
  },
});
