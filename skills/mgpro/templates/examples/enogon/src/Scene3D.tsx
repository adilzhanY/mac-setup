import { useMemo } from "react";
import * as THREE from "three";
import { ThreeCanvas } from "@remotion/three";
import { LineMaterial } from "three/examples/jsm/lines/LineMaterial.js";
import { LineSegments2 } from "three/examples/jsm/lines/LineSegments2.js";
import { LineSegmentsGeometry } from "three/examples/jsm/lines/LineSegmentsGeometry.js";
import { C } from "./brand";
import type { Cam } from "./camera";
import { buildDG, buildRoof, buildSlab, buildWall, outerQuad, toGeometry, W3, WAVE, waveDelay } from "./geo";
import { EASE, clamp, mix, prog, sp } from "./lib";
import { cubeRect } from "./cubeRect";
import { FOOTPRINT, LEVEL, OPENINGS, OUTER_WALLS, STOREY_H, wallById, wallLength, wallPieces } from "./plan";
import { Rig } from "./three";
import { CUBE_S, F } from "./timeline";

const W = 1920;
const H = 1080;

function Ink({ positions, width = 1.6, color = C.ink, opacity = 1 }: { positions: number[]; width?: number; color?: string; opacity?: number }) {
  const obj = useMemo(() => {
    const g = new LineSegmentsGeometry();
    g.setPositions(positions);
    const m = new LineMaterial({ color, linewidth: width, transparent: true, depthTest: true });
    m.resolution.set(W, H);
    return new LineSegments2(g, m);
  }, [positions, color, width]);
  obj.material.opacity = opacity;
  obj.material.linewidth = width;
  obj.visible = opacity > 0.002;
  return <primitive object={obj} />;
}

function Solid({ built, opacity = 1, color }: { built: { pos: number[]; col: number[] }; opacity?: number; color?: string }) {
  const geo = useMemo(() => toGeometry({ ...built, lines: [] }), [built]);
  const mat = useMemo(
    () =>
      new THREE.MeshBasicMaterial({
        vertexColors: !color,
        color: color ?? "#ffffff",
        side: THREE.DoubleSide,
        polygonOffset: true,
        polygonOffsetFactor: 1.2,
        polygonOffsetUnits: 1.2,
        transparent: true,
      }),
    [color],
  );
  mat.opacity = opacity;
  mat.depthWrite = opacity > 0.98;
  return <mesh geometry={geo} material={mat} visible={opacity > 0.002} />;
}

/** One full storey (EG, 1.OG, 2.OG): its walls, each with its own rise, and the slab under it. */
function Storey({ index, frame, rise }: { index: number; frame: number; rise: (id: string) => number }) {
  const walls = useMemo(() => WAVE.map((w) => ({ w, b: buildWall(w, index) })), [index]);
  const slab = useMemo(() => buildSlab(), []);
  return (
    <group>
      {index > 0 && (
        <>
          <Solid built={slab} />
          <Ink positions={slab.lines} />
        </>
      )}
      {walls.map(({ w, b }) => {
        const r = rise(w.id);
        return (
          <group key={w.id} scale={[1, Math.max(r, 0.0005), 1]}>
            <Solid built={b} opacity={r > 0 ? 1 : 0} />
            <Ink positions={b.lines} opacity={clamp(r * 8)} width={1.6} />
          </group>
        );
      })}
    </group>
  );
  void frame;
}

/** The selected wall AW 008 in the ground floor: filled with the selection colour, and, when its
 * thickness is raised, a new outer layer that grows out of the face with the windows kept open. */
function Selection({ on, grow }: { on: number; grow: number }) {
  const w = wallById("AW 008");
  const i = OUTER_WALLS.indexOf(w);
  const pieces = useMemo(() => {
    const out: { x0: number; x1: number; y0: number; y1: number }[] = [];
    const band = (y0: number, y1: number, kinds: ("door" | "window")[]) => {
      for (const [s0, s1] of wallPieces(w, kinds, 0)) {
        const q = outerQuad(i, s0, s1);
        out.push({ x0: W3(q[0]!).x, x1: W3(q[1]!).x, y0, y1 });
      }
    };
    band(0, 0.9, ["door"]);
    band(0.9, 2.2, ["door", "window"]);
    band(2.2, STOREY_H, []);
    return out;
  }, [w, i]);
  const zFace = W3({ x: 0, y: 0 }).z;
  const skin = useMemo(() => {
    const pos: number[] = [];
    for (const p of pieces) {
      const v = [
        [p.x0, p.y0], [p.x1, p.y0], [p.x1, p.y1],
        [p.x0, p.y0], [p.x1, p.y1], [p.x0, p.y1],
      ];
      for (const [x, y] of v) pos.push(x!, y!, 0);
    }
    return { pos, col: pos.map(() => 1) };
  }, [pieces]);
  // Outline of the new face: the wall's rectangle and its window openings.
  const outline = useMemo(() => {
    const L = wallLength(w);
    const q = outerQuad(i, 0, L);
    const x0 = W3(q[0]!).x, x1 = W3(q[1]!).x;
    const seg: number[] = [];
    const rect = (a: number, b: number, c: number, d: number) => seg.push(a, c, 0, b, c, 0, b, c, 0, b, d, 0, b, d, 0, a, d, 0, a, d, 0, a, c, 0);
    rect(x0, x1, 0, STOREY_H);
    for (const op of OPENINGS_AW8) {
      const qq = outerQuad(i, op.at - op.width / 2, op.at + op.width / 2);
      rect(W3(qq[0]!).x, W3(qq[1]!).x, 0.9, 2.2);
    }
    return seg;
  }, [w, i]);
  const depth = 0.12 * grow;
  const layerMat = useMemo(() => new THREE.MeshBasicMaterial({ color: C.apricot100, transparent: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }), []);
  layerMat.opacity = on;
  if (on <= 0.001) return null;
  return (
    <group position={[0, 0, zFace + 0.004 + depth]}>
      <Solid built={skin} color={C.apricot300} opacity={on} />
      <Ink positions={outline} opacity={on} width={2} />
      {depth > 0.002 &&
        pieces.map((p, k) => (
          <mesh key={k} material={layerMat} position={[(p.x0 + p.x1) / 2, (p.y0 + p.y1) / 2, -depth / 2 - 0.004]}>
            <boxGeometry args={[p.x1 - p.x0, p.y1 - p.y0, depth]} />
          </mesh>
        ))}
    </group>
  );
}

const OPENINGS_AW8 = OPENINGS.filter((o) => o.wall === "AW 008");

/** The model: storeys landing, the roof, and at the end its simplification into the Enogon cube. */
export function Scene3D({ frame, cam }: { frame: number; cam: Cam }) {
  const roof = useMemo(() => buildRoof(), []);
  const dg = useMemo(() => buildDG(), []);
  const dgSlab = useMemo(() => buildSlab(FOOTPRINT), []);

  // Ground floor walls rise in a wave around the house (back out: about 6 percent overshoot).
  const rise = (id: string) => {
    const w = WAVE.find((v) => v.id === id)!;
    const s = F.egRise + waveDelay(w) * F.egRiseLen * 0.55;
    const t = clamp((frame - s) / 34);
    const k = t - 1;
    return t <= 0 ? 0 : 1 + 2.3 * k * k * k + 1.3 * k * k;
  };
  // Upper storeys drop in with weight and settle (only results overshoot).
  const land = (start: number) => {
    const t = sp(frame, start - 22, "settle");
    return { y: (1 - t) * 3.2, on: frame >= start - 22 ? 1 : 0 };
  };
  const s1 = land(F.land1);
  const s2 = land(F.land2);
  const s3 = land(F.land3);
  // The roof falls in one move and lands with the storeys' weight: no hover.
  const roof3 = land(F.roofLand);

  const selOn = prog(frame, F.click, F.click + 8) * (1 - prog(frame, F.title5Out, F.title5Out + 20));
  const grow = prog(frame, F.type + 6, F.type + 40, EASE.out) * (1 - prog(frame, F.title5Out, F.title5Out + 20));

  // End: a box folds up around the model and closes; the house stays solid inside it.
  const houseOn = frame < F.lid + 30 ? 1 : 0;

  return (
    <ThreeCanvas flat width={W} height={H} gl={{ antialias: true, alpha: true }} style={{ position: "absolute", inset: 0 }}>
      <Rig cam={cam} />
      {houseOn > 0.001 && (
        <group>
          {frame >= F.egRise && <Storey index={0} frame={frame} rise={rise} />}
          {s1.on > 0 && (
            <group position={[0, LEVEL + s1.y, 0]}>
              <Storey index={1} frame={frame} rise={() => 1} />
            </group>
          )}
          {s2.on > 0 && (
            <group position={[0, 2 * LEVEL + s2.y, 0]}>
              <Storey index={2} frame={frame} rise={() => 1} />
            </group>
          )}
          {s3.on > 0 && (
            <group position={[0, 3 * LEVEL + s3.y, 0]}>
              <Solid built={dgSlab} />
              <Ink positions={dgSlab.lines} />
              <Solid built={dg} />
              <Ink positions={dg.lines} />
            </group>
          )}
          {roof3.on > 0 && (
            <group position={[0, 3 * LEVEL + roof3.y, 0]}>
              <Solid built={roof.solid} />
              <Ink positions={roof.solid.lines} />
              <Ink positions={roof.hatch} color={C.apricot600} width={1.2} />
            </group>
          )}
          <Selection on={selOn} grow={grow} />
        </group>
      )}
      <PackBox frame={frame} inkAtSwap={(4.01 / 123) * cubeRect().h} />
    </ThreeCanvas>
  );
}

/**
 * Export packs the model: the box's net is drawn flat on the ground around the house, its four
 * sides fold up one after the other, the lid closes, and the closed box is the Enogon cube (top
 * apricot, east Türkis, south white). Everything stays opaque: no crossfade, no see-through.
 */
function PackBox({ frame, inkAtSwap }: { frame: number; inkAtSwap: number }) {
  const S = CUBE_S;
  const mats = useMemo(() => {
    const m = (c: string) => new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1.5, polygonOffsetUnits: 1.5 });
    return { south: m(C.paper), east: m(C.tuerkis500), north: m(C.tuerkis300), west: m(C.tuerkis300), lid: m(C.apricot500), floor: m(C.tuerkis100) };
  }, []);
  const side = useMemo(() => new THREE.PlaneGeometry(S, S).translate(0, S / 2, 0), [S]);
  const lid = useMemo(() => new THREE.PlaneGeometry(S, S).rotateX(-Math.PI / 2).translate(0, 0, S / 2), [S]);
  const floor = useMemo(() => new THREE.PlaneGeometry(S, S).rotateX(-Math.PI / 2).translate(0, 0.02, 0), [S]);
  const sideEdge = useMemo(() => [-S / 2, 0, 0, S / 2, 0, 0, S / 2, 0, 0, S / 2, S, 0, S / 2, S, 0, -S / 2, S, 0, -S / 2, S, 0, -S / 2, 0, 0], [S]);
  const lidEdge = useMemo(() => [-S / 2, 0, 0, S / 2, 0, 0, S / 2, 0, 0, S / 2, 0, S, S / 2, 0, S, -S / 2, 0, S, -S / 2, 0, S, -S / 2, 0, 0], [S]);
  if (frame < F.net || frame >= F.logo + 2) return null;
  // The net is drawn flat: each panel grows out from its hinge.
  const grow = prog(frame, F.net, F.net + 14, EASE.out);
  const ink = mix(2.2, inkAtSwap, prog(frame, F.lid, F.logo, EASE.inOut));
  const sides: { key: keyof typeof mats; yaw: number; order: number }[] = [
    { key: "south", yaw: 0, order: 0 },
    { key: "east", yaw: Math.PI / 2, order: 1 },
    { key: "north", yaw: Math.PI, order: 2 },
    { key: "west", yaw: -Math.PI / 2, order: 3 },
  ];
  // Each side folds up with a spring that settles (a closing box is a result).
  const angle = (order: number) => (Math.PI / 2) * (1 - sp(frame, F.fold + order * 7, "settle"));
  const lidAngle = -(Math.PI / 2) * (1 - sp(frame, F.lid, "settle"));
  return (
    <group>
      <mesh geometry={floor} material={mats.floor} scale={[grow, 1, grow]} />
      {sides.map(({ key, yaw, order }) => (
        <group key={key} rotation={[0, yaw, 0]}>
          <group position={[0, 0, S / 2]} rotation={[angle(order), 0, 0]} scale={[1, grow, 1]}>
            <mesh geometry={side} material={mats[key]} />
            <Ink positions={sideEdge} width={ink} />
          </group>
        </group>
      ))}
      {frame >= F.fold + 20 && (
        <group position={[0, S, -S / 2]} rotation={[lidAngle, 0, 0]}>
          <mesh geometry={lid} material={mats.lid} />
          <Ink positions={lidEdge} width={ink} />
        </group>
      )}
    </group>
  );
}
