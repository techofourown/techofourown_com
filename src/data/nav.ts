import { site } from "./site";

export type NavItem = {
  href: string;
  label: string;
  external?: boolean;
  matchPrefixes?: string[];
};

export type NavSection = {
  title: string;
  items: NavItem[];
};

// Permanent desktop nav should stay reserved for true top-level rooms.
// Product paths, publishing surfaces, and external destinations belong in the menu panel.
export const primaryNavItems: NavItem[] = [
  {
    href: "/drumbeat/",
    label: "Drumbeat",
    matchPrefixes: ["/drumbeat/"],
  },
  {
    href: "/ourbox/",
    label: "OurBox",
    matchPrefixes: ["/ourbox/", "/matchbox/", "/woodbox/"],
  },
  {
    href: "/why/",
    label: "Why",
    matchPrefixes: ["/why/"],
  },
];

export const menuSections: NavSection[] = [
  {
    title: "Explore",
    items: [
      { href: "/", label: "Home", matchPrefixes: ["/"] },
      { href: "/drumbeat/", label: "Drumbeat", matchPrefixes: ["/drumbeat/"] },
      {
        href: "/ourbox/",
        label: "OurBox",
        matchPrefixes: ["/ourbox/", "/matchbox/", "/woodbox/"],
      },
      { href: "/why/", label: "Why", matchPrefixes: ["/why/"] },
    ],
  },
  {
    title: "OurBox paths",
    items: [
      { href: "/matchbox/", label: "Matchbox", matchPrefixes: ["/matchbox/"] },
      { href: "/woodbox/", label: "Woodbox", matchPrefixes: ["/woodbox/"] },
      { href: "/learn/", label: "Learn", matchPrefixes: ["/learn/"] },
      { href: "/build/", label: "Build", matchPrefixes: ["/build/"] },
    ],
  },
  {
    title: "Publishing",
    items: [
      { href: "/journal/", label: "Journal", matchPrefixes: ["/journal/"] },
      { href: "/library/", label: "Library", matchPrefixes: ["/library/"] },
    ],
  },
  {
    title: "Elsewhere",
    items: [{ href: site.githubOrgUrl, label: "GitHub", external: true }],
  },
];
