import { useLayoutEffect, useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { clipOf, eyeOf } from "./camera";
import type { Cam } from "./camera";

/** Puts the canvas camera where the frame wants it, with an optional roll and shake. */
export function Rig({ cam, roll = 0, shake = [0, 0], offset = [0, 0] }: { cam: Cam; roll?: number; shake?: [number, number]; offset?: [number, number] }) {
  const { camera, size } = useThree();
  const eye = eyeOf(cam);
  const { near, far } = clipOf(cam);
  useLayoutEffect(() => {
    const c = camera as THREE.PerspectiveCamera;
    c.position.set(...eye);
    c.up.set(0, 1, 0);
    c.lookAt(...cam.target);
    c.fov = cam.fov;
    c.near = Math.min(near, 0.05);
    c.far = far;
    if (roll) c.rotateZ((roll * Math.PI) / 180);
    // Shake is a film offset of the lens, so it reads as a handheld jolt, not a move. offset moves
    // the picture by whole pixels the same way (positive x moves it left), for placing the subject
    // inside a safe box without moving the camera. Pass the same offset to threeCamera().
    c.setViewOffset(size.width, size.height, shake[0] + offset[0], shake[1] + offset[1], size.width, size.height);
    c.updateProjectionMatrix();
    c.updateMatrixWorld();
  });
  return null;
}

/** A soft studio room as the reflection map, so metal reads as metal on a black stage. */
export function Studio({ intensity = 1 }: { intensity?: number }) {
  const { gl, scene } = useThree();
  const env = useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    const tex = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    pm.dispose();
    return tex;
  }, [gl]);
  useLayoutEffect(() => {
    scene.environment = env;
    scene.environmentIntensity = intensity;
  });
  return null;
}
