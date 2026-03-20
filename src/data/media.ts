export const videoAspectValues = ["landscape", "portrait", "square"] as const;

export type VideoAspect = (typeof videoAspectValues)[number];

export const defaultVideoAspect: VideoAspect = "landscape";
