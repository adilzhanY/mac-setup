import type { CSSProperties, ReactNode } from "react";
import { AbsoluteFill } from "remotion";
import { AI_GRADIENT, COLOR, EASE, clamp, prog } from "./lib";

/**
 * Kinetic type: word by word, each rising out of a blur with an expo out (22 frames, 4 apart),
 * and leaving upward into a blur, faster than it came. Lines are arrays of words; a word that
 * starts with "*" is drawn in the accent colour.
 */
export function Words({
  lines,
  frame,
  start,
  end,
  size = 88,
  color = COLOR.ink,
  accent = COLOR.accent,
  weight = 600,
  align = "left",
  stagger = 4,
  colors,
  style,
}: {
  lines: string[];
  frame: number;
  start: number;
  end?: number;
  size?: number;
  color?: string;
  accent?: string;
  weight?: number;
  align?: "left" | "center";
  stagger?: number;
  /** Colours for single words (without their "*"), over the accent. */
  colors?: Record<string, string>;
  style?: CSSProperties;
}) {
  let n = 0;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: align === "center" ? "center" : "flex-start", ...style }}>
      {lines.map((line, li) => (
        <div key={li} style={{ display: "flex", gap: `0 ${size * 0.26}px`, flexWrap: "nowrap", lineHeight: 1.04 }}>
          {line.split(" ").map((raw, wi) => {
            const i = n++;
            const word = raw.startsWith("*") ? raw.slice(1) : raw;
            const t = prog(frame, start + i * stagger, start + i * stagger + 24, EASE.out);
            const o = end === undefined ? 0 : prog(frame, end + i * 2, end + i * 2 + 12, EASE.in);
            const blur = 14 * (1 - t) + 10 * o;
            return (
              <span
                key={wi}
                style={{
                  display: "inline-block",
                  fontSize: size,
                  fontWeight: weight,
                  letterSpacing: "-0.035em",
                  color: colors?.[word] ?? (raw.startsWith("*") ? accent : color),
                  opacity: clamp(t * 1.4) * (1 - o),
                  transform: `translateY(${(1 - t) * size * 0.5 - o * size * 0.32}px) scale(${0.94 + 0.06 * t})`,
                  transformOrigin: "50% 100%",
                  filter: blur > 0.1 ? `blur(${blur}px)` : undefined,
                  whiteSpace: "nowrap",
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
}

/** Liquid glass: a frosted, saturated pane with a bright rim, a specular top light and a deep soft shadow. */
export function Glass({
  children,
  radius = 28,
  dark = false,
  style,
}: {
  children?: ReactNode;
  radius?: number;
  dark?: boolean;
  style?: CSSProperties;
}) {
  return (
    <div
      style={{
        position: "relative",
        borderRadius: radius,
        background: dark
          ? "linear-gradient(180deg, rgba(40,52,70,.62), rgba(22,30,44,.58))"
          : "linear-gradient(180deg, rgba(255,255,255,.78), rgba(255,255,255,.58))",
        backdropFilter: "blur(28px) saturate(170%)",
        boxShadow: dark
          ? "inset 0 1px 0 rgba(255,255,255,.18), inset 0 0 0 1px rgba(255,255,255,.08), 0 30px 70px -18px rgba(0,0,0,.6)"
          : "inset 0 1px 0 rgba(255,255,255,.95), inset 0 0 0 1px rgba(255,255,255,.6), 0 1px 2px rgba(13,33,55,.06), 0 28px 64px -18px rgba(13,33,55,.32)",
        ...style,
      }}
    >
      {/* The specular light across the top of the pane. */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: radius,
          background: dark
            ? "radial-gradient(120% 60% at 20% 0%, rgba(255,255,255,.12), transparent 60%)"
            : "radial-gradient(120% 70% at 18% 0%, rgba(255,255,255,.7), transparent 55%)",
          pointerEvents: "none",
        }}
      />
      <div style={{ position: "relative" }}>{children}</div>
    </div>
  );
}

/**
 * The AI at work, Apple Intelligence style: a conic gradient (blue, violet, coral, amber) turning
 * around the shape's edge, once as a sharp rim and once as a wide blurred glow behind it.
 */
export function AiGlow({ frame, radius = 24, strength = 1, rim = 3, spread = 36, turn = 110 }: { frame: number; radius?: number; strength?: number; rim?: number; spread?: number; turn?: number }) {
  if (strength <= 0.001) return null;
  const angle = (frame / turn) * 360;
  const conic = `conic-gradient(from ${angle}deg, ${AI_GRADIENT.join(", ")})`;
  return (
    <>
      <div
        style={{
          position: "absolute",
          inset: -spread * 0.35,
          borderRadius: radius + spread * 0.35,
          background: conic,
          filter: `blur(${spread}px)`,
          opacity: 0.85 * strength,
          zIndex: -1,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: -rim,
          borderRadius: radius + rim,
          padding: rim,
          background: conic,
          WebkitMask: "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)",
          WebkitMaskComposite: "xor",
          maskComposite: "exclude",
          opacity: strength,
        }}
      />
    </>
  );
}

/** Film grain: animated noise, a few percent, so gradients never band and the frame feels shot. */
export function Grain({ frame, opacity = 0.05 }: { frame: number; opacity?: number }) {
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "overlay", opacity }}>
      <svg width="100%" height="100%">
        <filter id={`g${frame % 8}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={frame % 97} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${frame % 8})`} />
      </svg>
    </AbsoluteFill>
  );
}

/** A soft vignette that keeps the eye in the middle. */
export function Vignette({ strength = 0.12, color = "13,33,55" }: { strength?: number; color?: string }) {
  return <AbsoluteFill style={{ pointerEvents: "none", background: `radial-gradient(120% 90% at 50% 45%, transparent 55%, rgba(${color},${strength}) 100%)` }} />;
}
