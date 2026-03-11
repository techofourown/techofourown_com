import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const learn = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/learn" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date().optional(),
    runtime: z.string().optional(),
    videoUrl: z.url().optional(),
    noindex: z.boolean().default(false),
    referrer: z.string().optional(),
  }),
});

const build = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/build" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date().optional(),
    difficulty: z.enum(["easy", "medium", "hard"]).default("medium"),
    estimatedTime: z.string().optional(),
    videoUrl: z.url().optional(),
    noindex: z.boolean().default(false),
    referrer: z.string().optional(),
  }),
});

const philosophy = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/philosophy" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date().optional(),
  }),
});

const journal = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/journal" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date(),
  }),
});

const decisions = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/decisions" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date().optional(),
    status: z.enum(["proposed", "accepted", "superseded", "archived"]).default("accepted"),
  }),
});

const rfcs = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date().optional(),
    status: z.enum(["draft", "review", "accepted", "rejected", "archived"]).default("draft"),
  }),
});

const apps = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
    order: z.number().optional(),
    publishedAt: z.coerce.date().optional(),
    status: z.enum(["planned", "prototype", "alpha", "beta", "stable"]).default("planned"),
    sourceUrl: z.url().optional(),
    demoUrl: z.url().optional(),
  }),
});

export const collections = {
  learn,
  build,
  philosophy,
  journal,
  decisions,
  rfcs,
  apps,
};
