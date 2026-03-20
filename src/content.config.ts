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
    runtime: z.string().optional(),
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

const drumbeat = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/drumbeat" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      summary: z.string().optional(),
      draft: z.boolean().default(false),
      publishedAt: z.coerce.date(),
      format: z.enum(["text", "image", "video", "audio", "mixed"]).default("text"),
      runtime: z.string().optional(),
      series: z.string().optional(),
      coverImage: image(),
      coverImageAlt: z.string(),
      cardImage: image().optional(),
      cardImageAlt: z.string().optional(),
      cardImageFit: z.enum(["cover", "contain"]).default("cover"),
      cardImagePosition: z.string().optional(),
      shareImage: image().optional(),
      shareImageAlt: z.string().optional(),
      videoUrl: z.url().optional(),
      audioUrl: z.url().optional(),
      videoAspect: z.enum(["landscape", "portrait"]).optional(),
      mirrors: z
        .array(
          z.object({
            label: z.string(),
            href: z.url(),
          }),
        )
        .default([]),
      links: z
        .array(
          z.object({
            label: z.string(),
            href: z.url(),
            title: z.string(),
            description: z.string(),
            source: z.string().optional(),
          }),
        )
        .default([]),
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
  drumbeat,
};
