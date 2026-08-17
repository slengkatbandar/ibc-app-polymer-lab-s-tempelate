import "./index.css";
import { Composition } from "remotion";
import { GiiasInfographic } from "./giias/GiiasInfographic";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="GiiasInfographic"
        component={GiiasInfographic}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1080}
      />
    </>
  );
};
