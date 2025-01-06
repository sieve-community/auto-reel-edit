const { bundle } = require("@remotion/bundler");
const { renderMedia, selectComposition } = require("@remotion/renderer");
const path = require("path");
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json({ limit: '50mb' }));
app.use(cors())


app.post('/caption-video', async (req, res) => {
  try {
    const { video_file, data_subtitles, fps, durationInFrames, subtitle_type} = req.body;

    if (!video_file || !data_subtitles || !fps || !durationInFrames) {
      return res.status(400).send({ error: 'Missing required input properties' });
    }

    const compositionId = 'CaptionedVideo';

    const bundleLocation = await bundle({
      entryPoint: path.resolve('./src/index.ts'),
      webpackOverride: (config) => config,
    });

    const inputProps = { video_file, data_subtitles, fps, durationInFrames, subtitle_type};

    console.log(`Rendering a video at ${fps}fps of length ${durationInFrames}frames`)
    const composition = await selectComposition({
      serveUrl: bundleLocation,
      id: compositionId,
      inputProps,
    });

    const outputLocation = `out/${video_file}`;
    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation,
      inputProps,
    });
    console.log(`Rendering done!`);

    res.send({ message: 'Render done!', outputLocation });
  } catch (error) {
    console.error('Error rendering video:', error);
    res.status(500).send({ error: 'Failed to render video', details: error.message });
  }
});

const PORT = 4505;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
