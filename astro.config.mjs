// @ts-check
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://techofourown.com",
  output: "static",
  trailingSlash: "always",
  build: {
    format: "directory",
  },
});
