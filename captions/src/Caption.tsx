import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import "./fonts.css";

export type CaptionProps = {
    data_subtitles: Record<string, unknown>[];
};

export const Caption = ({ data_subtitles }: CaptionProps) => {
	const frame = useCurrentFrame();
	const typed_data_subtitles: any[] = data_subtitles;

	let subtitle = "";
	let startFrame = 0;
	let subtitleIndex = -1;

	for (let i = 0; i < typed_data_subtitles.length; i++) {
		const data_subtitle = typed_data_subtitles[i];
		if (frame >= data_subtitle["start"] && frame <= data_subtitle["end"]) {
			subtitle = data_subtitle["word"];
			startFrame = data_subtitle["start"];
			subtitleIndex = i;
			break;
		}
	}

	const scalingFrequency = 4;
	const shouldScale = subtitleIndex % scalingFrequency === 0;

	const scale = shouldScale
		? interpolate(
			frame,
			[startFrame, startFrame + 3],
			[0.5, 1],
			{
				extrapolateLeft: "clamp",
				extrapolateRight: "clamp",
			}
		  )
		: 1;

	const colors = [
		"#b6e243", // Conifer
		"#43d2e2", // Picton Blue
		"#00FF00", // Green
		"#FFFF00", // Yellow
		"#FFFFFF", // White
	];
	const color = colors[subtitleIndex % colors.length];

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
				<span
					style={{
						position: "fixed",
						paddingLeft: "10px",
						paddingRight: "10px",
						bottom: "150px",
						color: color,
						fontSize: "120px",
						fontFamily: "Crimson Text",
						textShadow: `
							4px 4px 4px black,
							0 0 40px ${color}, 
							0 0 50px ${color}, 
							0 0 60px ${color}
						`,
						transform: `scale(${scale})`, // Apply the conditional scale
					}}
				>
					<i>{subtitle}</i>
				</span>
			</div>
		</AbsoluteFill>
	);
};