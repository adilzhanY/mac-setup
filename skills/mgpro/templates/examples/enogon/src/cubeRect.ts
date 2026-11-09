import { project, threeCamera } from "./camera";
import { CUBE_S, F, camAt } from "./timeline";

/** Where the 3D cube sits on screen at the hand over to the flat logo (its bounding box). */
export function cubeRect() {
  const c = threeCamera(camAt(F.logo));
  const h = CUBE_S / 2;
  const pts = [];
  for (const x of [-h, h]) for (const y of [0, CUBE_S]) for (const z of [-h, h]) pts.push(project(c, [x, y, z]));
  const xs = pts.map((p) => p.x);
  const ys = pts.map((p) => p.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
}
