import { useMemo } from "react";
import * as THREE from "three";
import { SVGLoader } from "three/examples/jsm/loaders/SVGLoader.js";

/** torq's vortex mark (src/components/Logo.tsx), potrace output in a 1024 box. */
export const VORTEX_PATH =
  "M3601 8405 c3 -2 63 -26 134 -54 814 -310 1529 -776 1942 -1266 365 -434 583 -993 583 -1497 l0 -100 -59 114 c-119 234 -259 409 -432 541 -50 38 -53 34 -24 -23 189 -374 243 -748 165 -1150 -10 -52 -16 -97 -14 -99 2 -2 47 28 101 66 54 38 112 79 130 91 l31 22 21 -68 c11 -37 45 -161 76 -277 70 -265 74 -277 87 -269 16 10 132 256 172 365 160 435 176 945 46 1453 -82 324 -208 589 -425 895 -44 61 -87 122 -95 134 -9 13 16 0 64 -33 500 -348 923 -866 1161 -1422 16 -37 31 -66 33 -64 7 8 -67 273 -111 396 -448 1262 -1752 2136 -3342 2240 -164 11 -251 13 -244 5z M3695 8292 c6 -5 66 -56 135 -113 220 -182 476 -455 633 -675 l37 -52 -57 -7 c-1027 -123 -2067 -848 -2580 -1795 -87 -161 -257 -560 -239 -560 2 0 23 33 47 73 557 942 1495 1630 2500 1832 371 74 799 78 1127 10 34 -7 62 -10 62 -6 0 13 -183 233 -293 352 -258 280 -571 525 -937 733 -202 115 -471 244 -435 208z M7086 8034 c408 -866 512 -1934 277 -2849 -115 -448 -310 -856 -583 -1216 -103 -137 -108 -131 72 -93 572 121 1160 427 1575 820 l78 74 -160 -78 c-181 -87 -327 -147 -495 -202 -137 -44 -339 -95 -346 -87 -4 3 13 53 35 111 287 735 335 1549 137 2317 -109 421 -307 853 -551 1205 -92 132 -102 131 -39 -2z M3525 6574 c-520 -431 -881 -1084 -1010 -1827 -66 -382 -60 -896 16 -1302 67 -363 198 -742 371 -1075 77 -148 210 -381 215 -377 1 2 -20 92 -47 201 -108 426 -144 720 -145 1176 0 367 10 479 66 765 150 773 542 1351 1137 1678 45 25 82 43 82 40 0 -3 -17 -26 -38 -52 -152 -185 -255 -394 -306 -621 -14 -62 -24 -115 -22 -117 1 -1 25 30 53 70 226 323 553 553 920 648 48 12 92 26 97 30 5 4 -38 31 -94 59 -57 29 -121 63 -143 77 l-40 25 219 220 219 220 -170 -5 c-498 -15 -974 -210 -1388 -567 -250 -216 -427 -446 -606 -790 -45 -85 -79 -141 -76 -125 2 17 12 79 21 139 78 533 335 1083 701 1503 80 90 71 92 -32 7z M8440 4618 c-1088 -1046 -2270 -1376 -3235 -904 -112 55 -313 175 -293 176 3 0 59 -9 125 -21 228 -40 467 -25 693 44 l74 23 -134 23 c-408 70 -717 224 -997 494 l-94 91 5 -49 c11 -107 17 -275 8 -275 -4 0 -143 38 -307 85 -164 47 -300 83 -302 82 -7 -7 105 -184 181 -285 103 -138 342 -377 476 -476 424 -315 901 -478 1440 -493 l205 -6 -55 -19 c-559 -195 -1190 -191 -1821 12 -141 45 -141 41 1 -34 670 -353 1441 -409 2171 -157 740 255 1449 852 1890 1590 141 235 134 257 -31 99z M3261 4206 c-230 -606 -277 -1237 -144 -1936 l18 -95 7 100 c30 383 61 595 118 811 31 116 87 284 99 297 4 4 47 -41 96 -100 670 -812 1696 -1350 2725 -1432 198 -16 360 -22 360 -13 0 4 -51 18 -112 31 -62 12 -197 47 -300 76 -1284 368 -2343 1241 -2754 2273 -27 67 -52 122 -55 122 -4 0 -30 -60 -58 -134z";

/** The six blades of the mark, one path each, in the 1024 box with y pointing down. */
export const BLADES = VORTEX_PATH.split(/(?=M)/).map((d) => d.trim());

export const HEX_R = 1;
export const TRACK_R = 1.24;

/** Pointy-top hexagon corners, clockwise from the top (seen from the front, y up). */
export function hexPts(r: number) {
  return Array.from({ length: 6 }, (_, i) => {
    const a = Math.PI / 2 - (i * Math.PI) / 3;
    return new THREE.Vector2(r * Math.cos(a), r * Math.sin(a));
  });
}

/** A hexagon with rounded corners as a path, so the bevel catches light on every corner. */
function roundedHex(r: number, round: number, target: THREE.Shape | THREE.Path) {
  const pts = hexPts(r);
  for (let i = 0; i < 6; i++) {
    const p = pts[i]!;
    const prev = pts[(i + 5) % 6]!;
    const next = pts[(i + 1) % 6]!;
    const a = p.clone().add(prev.clone().sub(p).setLength(round));
    const b = p.clone().add(next.clone().sub(p).setLength(round));
    if (i === 0) target.moveTo(a.x, a.y);
    else target.lineTo(a.x, a.y);
    target.quadraticCurveTo(p.x, p.y, b.x, b.y);
  }
  target.closePath();
}

/** A point at fraction t of the track's perimeter, clockwise from the top. */
export function trackPoint(t: number, r = TRACK_R) {
  const pts = hexPts(r);
  const s = ((t % 1) + 1) % 1 * 6;
  const i = Math.floor(s);
  return pts[i]!.clone().lerp(pts[(i + 1) % 6]!, s - i);
}

function useGeometry() {
  return useMemo(() => {
    const frame = new THREE.Shape();
    roundedHex(HEX_R, 0.16, frame);
    const hole = new THREE.Path();
    roundedHex(HEX_R * 0.8, 0.12, hole);
    frame.holes.push(hole);
    const frameGeo = new THREE.ExtrudeGeometry(frame, { depth: 0.16, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.045, bevelSegments: 8, curveSegments: 10 });
    frameGeo.translate(0, 0, -0.08);

    const field = new THREE.Shape();
    roundedHex(HEX_R * 0.84, 0.12, field);
    const fieldGeo = new THREE.ExtrudeGeometry(field, { depth: 0.08, bevelEnabled: false, curveSegments: 10 });
    fieldGeo.translate(0, 0, -0.04);

    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><g transform="translate(0,1024) scale(0.1,-0.1)"><path d="${VORTEX_PATH}"/></g></svg>`;
    const data = new SVGLoader().parse(svg);
    const shapes = data.paths.flatMap((p) => SVGLoader.createShapes(p));
    const emblemGeo = new THREE.ExtrudeGeometry(shapes, { depth: 40, bevelEnabled: true, bevelThickness: 8, bevelSize: 5, bevelSegments: 3, curveSegments: 8 });
    // From the 1024 box (y down) to medal units (y up), centred on the field.
    emblemGeo.translate(-512, -512, 0);
    const k = (HEX_R * 1.25) / 1024;
    // Flip y (SVG is y down) and z together, so the winding and the normals stay outward.
    emblemGeo.scale(k, -k, -k);
    emblemGeo.computeBoundingBox();
    const bb = emblemGeo.boundingBox!;
    emblemGeo.translate(-(bb.min.x + bb.max.x) / 2, -(bb.min.y + bb.max.y) / 2, 0.04 - bb.min.z);
    emblemGeo.computeVertexNormals();

    const trackPts = Array.from({ length: 6 }, (_, i) => hexPts(TRACK_R)[i]!).map((p) => new THREE.Vector3(p.x, p.y, 0));
    const trackCurve = new THREE.CatmullRomCurve3(trackPts, true, "catmullrom", 0.02);
    const trackGeo = new THREE.TubeGeometry(trackCurve, 240, 0.014, 8, true);
    return { frameGeo, fieldGeo, emblemGeo, trackGeo };
  }, []);
}

/** The lit part of the track, rebuilt each frame from the top clockwise to fraction t. */
function LitTrack({ t, color }: { t: number; color: string }) {
  const geo = useMemo(() => {
    if (t <= 0.002) return null;
    const n = Math.max(2, Math.ceil(t * 240));
    const pts = Array.from({ length: n + 1 }, (_, i) => {
      const p = trackPoint((i / n) * t);
      return new THREE.Vector3(p.x, p.y, 0.01);
    });
    return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, false, "catmullrom", 0), n * 2, 0.026, 10, false);
  }, [t]);
  if (!geo) return null;
  const tip = trackPoint(t);
  return (
    <>
      <mesh geometry={geo}>
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={1.6} roughness={0.3} toneMapped={false} />
      </mesh>
      <mesh position={[tip.x, tip.y, 0.02]}>
        <sphereGeometry args={[0.06, 24, 16]} />
        <meshStandardMaterial color="#ffffff" emissive={color} emissiveIntensity={2.5} toneMapped={false} />
      </mesh>
    </>
  );
}

export interface MedalLook {
  base: string;
  light: string;
  dark: string;
  /** 0 to 1: the white heat of a tier change. */
  flash: number;
  /** 0 to 1 of the track lit. */
  track: number;
  trackColor: string;
}

/** The 3D rank medal: a bevelled metal hex frame, a dark field and the vortex standing out of it. */
export function Medal({ look, rotation }: { look: MedalLook; rotation: [number, number, number] }) {
  const { frameGeo, fieldGeo, emblemGeo, trackGeo } = useGeometry();
  const heat = look.flash;
  return (
    <group rotation={rotation}>
      <mesh geometry={frameGeo}>
        <meshPhysicalMaterial color={look.base} metalness={1} roughness={0.24} clearcoat={0.6} clearcoatRoughness={0.15} emissive={look.light} emissiveIntensity={heat * 1.4} />
      </mesh>
      <mesh geometry={fieldGeo}>
        <meshStandardMaterial color="#131510" metalness={0.4} roughness={0.55} emissive={look.dark} emissiveIntensity={0.12 + heat * 0.5} />
      </mesh>
      {/* The mark stands out of both faces, so the medal never shows an empty back while it spins. */}
      {[0, Math.PI].map((r) => (
        <mesh key={r} geometry={emblemGeo} rotation={[0, r, 0]}>
          <meshPhysicalMaterial color={look.light} metalness={0.9} roughness={0.2} clearcoat={0.8} emissive={look.light} emissiveIntensity={0.35 + heat * 1.6} />
        </mesh>
      ))}
      <mesh geometry={trackGeo}>
        <meshStandardMaterial color="#2a2e27" roughness={0.5} metalness={0.3} />
      </mesh>
      <LitTrack t={look.track} color={look.trackColor} />
    </group>
  );
}
