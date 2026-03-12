export type NavItem = {
  href: string;
  label: string;
  external?: boolean;
  action?: boolean;
};

export const navItems: NavItem[] = [
  { href: "/", label: "Home" },
  { href: "/ourbox/", label: "OurBox" },
  { href: "/matchbox/", label: "Matchbox" },
  { href: "/woodbox/", label: "Woodbox" },
  { href: "https://github.com/techofourown/", label: "GitHub", external: true, action: true },
];
