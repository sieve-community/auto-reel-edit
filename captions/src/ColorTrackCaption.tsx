import { AbsoluteFill, useCurrentFrame } from "remotion";
import "./fonts.css";

export type Subtitle = {
  start: number;
  end: number;
  word: string;
  index: number;
};

export type ColorTrackCaptionProps = {
  data_subtitles: Subtitle[][];
};

export const ColorTrackCaption = ({ data_subtitles }: ColorTrackCaptionProps) => {
  const frame = useCurrentFrame();

  const activeSubtitleGroup = data_subtitles.find((group) => {
    const groupStart = group[0]?.start;
    const groupEnd = group[group.length - 1]?.end;
    return frame >= groupStart && frame <= groupEnd;
  });
  //#FFFF00 Yellow
  //#00FF00 Green
  const getColor = (index: number) => {
    if (index === 0) {
      return "#FFFF00"; // Default color for index 0
    }
    return "#FFFF00" // Same color yellow
    // return index % 5 === 0 ? "#00FF00" : "#FFFF00"; // Change color based on index
  };

  return (
    <AbsoluteFill style={{ zIndex: 1 }}>
      <div
        style={{
          justifyContent: "center",
          alignItems: "center",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {activeSubtitleGroup && (
          <span
            style={{
              position: "fixed",
              paddingLeft: "10px",
              paddingRight: "10px",
              bottom: "150px",
              color: "white",
              fontSize: "90px",
              fontFamily: "Bebas Neue",
              textShadow: "4px 4px 4px black",
              borderRadius: "10px",
            }}
          >
            {activeSubtitleGroup.map((subtitle) => {
              const isActive = frame >= subtitle.start && frame <= subtitle.end;
              const color = getColor(subtitle.index); // Get the color based on the index

              return (
                <span style={{ paddingLeft: "20px" }}>
                  <span
                    style={{
                      color: isActive ? color : "white",
                      textShadow: isActive
                        ? `4px 4px 4px black,0 0 60px ${color}`
                        : ``,
                      padding: "1px 5px",
                      borderRadius: "10px",
                    }}
                  >
                    {subtitle.word.toUpperCase()}
                  </span>
                </span>
              );
            })}
          </span>
        )}
      </div>
    </AbsoluteFill>
  );
};
