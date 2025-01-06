import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import { Caption } from "./Caption";
import { BackgroundTrackingCaption } from "./BackgroundTrackingCaption";
import { ColorTrackCaption } from "./ColorTrackCaption";
import { TypingCaption } from "./TypingCaption";

export type CaptionedVideoProps = {
  data_subtitles:  any[];
  video_file: string;
  fps: number;
  durationInFrames: number;
  subtitle_type: string;
};

export const CaptionedVideo = ({ data_subtitles, video_file, subtitle_type }: CaptionedVideoProps) => {
  return (
    <AbsoluteFill>
      <OffthreadVideo src={staticFile(video_file)} />
      {subtitle_type === 'glowing' && <Caption data_subtitles={data_subtitles} />}
      {subtitle_type === 'background_tracking' && <BackgroundTrackingCaption data_subtitles={data_subtitles}/>}
      {subtitle_type === 'color_tracking' && <ColorTrackCaption data_subtitles={data_subtitles} />}
      {subtitle_type === 'typing_background' && <TypingCaption data_subtitles={data_subtitles}/>}
    </AbsoluteFill>
  );
};
