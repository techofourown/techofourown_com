export type OurBoxPath = {
  key: "matchbox" | "woodbox";
  title: string;
  href: string;
  summary: string;
  platform: string;
  status: string;
  docsUrl?: string;
  videoUrl?: string;
  discussionUrl?: string;
};

export const ourBoxPaths: OurBoxPath[] = [
  {
    key: "matchbox",
    title: "Matchbox",
    href: "/matchbox/",
    summary: "A compact Raspberry Pi path for a quiet, always-on personal server.",
    platform: "Raspberry Pi",
    status: "Foundational page",
    docsUrl: "https://github.com/techofourown/pf-ourbox/tree/main/hw/matchbox",
  },
  {
    key: "woodbox",
    title: "Woodbox",
    href: "/woodbox/",
    summary: "An x86 path for more headroom, more storage, and wider services.",
    platform: "x86",
    status: "Foundational page",
    docsUrl: "https://github.com/techofourown/pf-ourbox/tree/main/hw/woodbox",
  },
];
