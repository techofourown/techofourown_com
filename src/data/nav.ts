export type NavItem = {
  href: string;
  label: string;
  external?: boolean;
  action?: boolean;
};

export const navItems: NavItem[] = [
  { href: "/", label: "Home" },
  { href: "/ourbox", label: "OurBox" },
  { href: "/build", label: "Build" },
  { href: "/learn", label: "Learn" },
  { href: "/why", label: "Why" },
  { href: "/library", label: "Library" },
  { href: "https://github.com/techofourown/", label: "GitHub", external: true, action: true },
];
