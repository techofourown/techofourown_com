export type NavItem = {
  href: string;
  label: string;
  external?: boolean;
  action?: boolean;
};

export const navItems: NavItem[] = [
  { href: "/", label: "Home" },
  { href: "/ourbox/", label: "OurBox" },
  { href: "/journal/", label: "Journal" },
  { href: "https://github.com/techofourown/", label: "GitHub", external: true, action: true },
];
