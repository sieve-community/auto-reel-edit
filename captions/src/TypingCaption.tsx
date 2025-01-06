import { AbsoluteFill, useCurrentFrame } from "remotion";
import "./fonts.css";

export type Subtitle = {
	start: number;
	end: number;
	word: string;
};

export type TypingCaptionProps = {
	data_subtitles: Subtitle[][];
};

export const TypingCaption = ({ data_subtitles }: TypingCaptionProps) => {
	const frame = useCurrentFrame();

	const activeSubtitleGroup = data_subtitles.find((group) => {
		const groupStart = group[0]?.start;
		const groupEnd = group[group.length - 1]?.end;
		return frame >= groupStart && frame <= groupEnd;
	});

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
							bottom: "150px",
							color: "white",
							fontSize: "43px",
							fontFamily: "Poppins",
							borderRadius: "10px",
							backgroundColor: "white",
							paddingTop: "1px",
							paddingLeft: "0px",
							paddingRight: "10px",
						}}
					>
						{activeSubtitleGroup.map((subtitle) => {
							const progress = (frame - subtitle.start) / (subtitle.end - subtitle.start);
							const opacity = Math.min(Math.max(progress, 0.2), 1); // Ensure opacity starts at 0.5 and goes up to 1

							const color = "black";

							return (
								<span style={{ paddingLeft: "10px" }}>
									<span
										style={{
											color: color,
											opacity: opacity,
											padding: "1px 2px",
											fontWeight: 420
										}}
									>
										{subtitle.word.toLowerCase()}
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