import path from "node:path";
import { Config } from "@remotion/cli/config";
import { enableTailwind } from "@remotion/tailwind-v4";

const here = process.cwd();
const app = path.resolve(here, "../bauwerk/src");
const mine = (name: string) => path.resolve(here, "node_modules", name);

Config.setVideoImageFormat("png");
Config.setConcurrency(6);
Config.overrideWebpackConfig((config) => {
  const withTailwind = enableTailwind(config);
  return {
    ...withTailwind,
    resolve: {
      ...withTailwind.resolve,
      alias: {
        ...(withTailwind.resolve?.alias ?? {}),
        // Bauwerk's own components, icons and tokens, imported as the app imports them.
        "@": app,
        // One React for the video and the app's components, or hooks break.
        react: mine("react"),
        "react-dom": mine("react-dom"),
        "lucide-react": mine("lucide-react"),
        // One three.js and one React Three Fiber for the app's 3D components and the video.
        three: path.resolve(app, "../node_modules/three"),
        "@react-three/fiber": path.resolve(app, "../node_modules/@react-three/fiber"),
        "@react-three/drei": path.resolve(app, "../node_modules/@react-three/drei"),
      },
      modules: [path.resolve(here, "node_modules"), path.resolve(app, "../node_modules"), "node_modules"],
    },
  };
});
