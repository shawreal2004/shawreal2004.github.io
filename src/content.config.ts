import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { categories } from './data/site';

const blog = defineCollection({
  loader: glob({ pattern: ['**/*.md', '!**/~$*.md'], base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.enum(categories),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    demo: z.boolean().default(false),
  }),
});

export const collections = { blog };
