import * as THREE from "three";

export const W = 1920;
export const H = 1080;

/** An orbit camera: what it looks at, how far, from which side (degrees) and its lens. */
export interface Cam {
  target: [number, number, number];
  dist: number;
  /** 0 = from the south (+z), 90 = from the east (+x). */
  az: number;
  /** Degrees above the horizon; 90 looks straight down. */
  el: number;
  fov: number;
}

export function eyeOf(c: Cam): [number, number, number] {
  const az = (c.az * Math.PI) / 180;
  const el = (Math.min(c.el, 89.9) * Math.PI) / 180;
  return [
    c.target[0] + c.dist * Math.cos(el) * Math.sin(az),
    c.target[1] + c.dist * Math.sin(el),
    c.target[2] + c.dist * Math.cos(el) * Math.cos(az),
  ];
}

export function clipOf(c: Cam) {
  return { near: Math.max(0.3, c.dist * 0.02), far: c.dist * 4 + 2500 };
}

/** The same camera the canvas uses, for projecting points onto the screen from the DOM. Pass the
 * frame size for formats other than 1920x1080 (useVideoConfig()), and the Rig's offset if it has one. */
export function threeCamera(c: Cam, w = W, h = H, offset: [number, number] = [0, 0]) {
  const { near, far } = clipOf(c);
  const cam = new THREE.PerspectiveCamera(c.fov, w / h, near, far);
  cam.position.set(...eyeOf(c));
  cam.lookAt(...c.target);
  if (offset[0] || offset[1]) cam.setViewOffset(w, h, offset[0], offset[1], w, h);
  cam.updateMatrixWorld();
  cam.updateProjectionMatrix();
  return cam;
}

const v = new THREE.Vector3();
/** A world point on the screen, in pixels of a w by h frame. */
export function project(cam: THREE.PerspectiveCamera, p: [number, number, number], w = W, h = H) {
  v.set(p[0], p[1], p[2]).project(cam);
  return { x: ((v.x + 1) / 2) * w, y: ((1 - v.y) / 2) * h, z: v.z };
}

/** Metres per pixel at a world point: how big a 1 m thing looks there. */
export function pxPerMetre(cam: THREE.PerspectiveCamera, p: [number, number, number]) {
  const a = project(cam, p);
  const right = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 0);
  const b = project(cam, [p[0] + right.x, p[1] + right.y, p[2] + right.z]);
  return Math.hypot(b.x - a.x, b.y - a.y);
}

/**
 * Corner pin, as in After Effects: the CSS matrix3d that maps a flat layer's four corners
 * (its own pixels) onto four points on the screen. A plane seen through a perspective camera is
 * exactly such a projective map, so a 2D layer drawn this way sits on the 3D ground.
 */
export function cornerPin(src: [number, number][], dst: { x: number; y: number }[]) {
  // Solve the 8 unknowns of the homography h (h33 = 1) from four point pairs.
  const A: number[][] = [];
  const b: number[] = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = src[i]!;
    const { x: u, y: w } = dst[i]!;
    A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]);
    b.push(u);
    A.push([0, 0, 0, x, y, 1, -w * x, -w * y]);
    b.push(w);
  }
  const h = solve(A, b);
  const [a, bb, c, d, e, f, g, k] = h;
  // Row-major H = [[a b c] [d e f] [g k 1]] as a column-major CSS matrix3d.
  return `matrix3d(${a},${d},0,${g},${bb},${e},0,${k},0,0,1,0,${c},${f},0,1)`;
}

function solve(A: number[][], b: number[]) {
  const n = b.length;
  const M = A.map((row, i) => [...row, b[i]!]);
  for (let col = 0; col < n; col++) {
    let pivot = col;
    for (let r = col + 1; r < n; r++) if (Math.abs(M[r]![col]!) > Math.abs(M[pivot]![col]!)) pivot = r;
    [M[col], M[pivot]] = [M[pivot]!, M[col]!];
    const p = M[col]![col]!;
    for (let r = 0; r < n; r++) {
      if (r === col) continue;
      const f = M[r]![col]! / p;
      const row = M[r]!;
      for (let k = col; k <= n; k++) row[k] = row[k]! - f * M[col]![k]!;
    }
  }
  return M.map((row, i) => row[n]! / row[i]!);
}
