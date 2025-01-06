import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import "./fonts.css";

export type Subtitle = {
	start: number;
	end: number;
	word: string;
};

export type BackgroundTrackingCaptionProps = {
	data_subtitles: Subtitle[][];
};

export const BackgroundTrackingCaption = ({ data_subtitles }: BackgroundTrackingCaptionProps) => {
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
							paddingLeft: "10px",
							paddingRight: "10px",
							bottom: "150px",
							color: "white",
							fontSize: "55px",
							fontFamily: "Poppins",
							textShadow: "4px 4px 4px black",
							borderRadius: "10px",
							fontWeight: "bold",
						}}
					>
						{activeSubtitleGroup.map((subtitle) => {
							const isActive = frame >= subtitle.start && frame <= subtitle.end;
							const scale = isActive
								? interpolate(frame, [subtitle.start, subtitle.start + 5], [1, 1.08], {
									extrapolateRight: "clamp",
								})
								: 1;

							return (
								<span style={{ paddingLeft: "20px" }}>
									<span
										style={{
											position: "relative",
											padding: "1px 0px",
											borderRadius: "10px",
										}}
									>
										<span
											style={{
												position: "absolute",
												top: "0",
												left: "-3px",
												right: "-3px",
												bottom: "0",
												backgroundColor: isActive ? "#764dea" : "transparent",
												borderRadius: "10px",
												zIndex: -1, // send the background behind the text
												transform: `scale(${scale})`,
											}}
										/>
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