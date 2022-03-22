import { fileURLToPath } from 'url';
import path from 'path';
import express from 'express';
import multer from 'multer';
import fetch from 'node-fetch';
import { SpeechClient } from '@google-cloud/speech';
import { readFileSync } from 'fs';

const storage = multer.diskStorage(
    {
        destination: './sound_files/',
        filename: function (req, file, cb) {
            cb(null, file.originalname);
        }
    }
);

const upload = multer({ storage: storage });

const app = express();
const port = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(__dirname + 'public'));

app.get("/", (req, res) => {
    res.status(200).sendFile("index.html", { root: __dirname + '/public' });
});

app.post("/notes", upload.single("audio_data"), async function (req, res) {
    // google speech-to-text API
    // Imports the Google Cloud client library

    // Creates a client
    const client = new SpeechClient();

    /**
     * TODO(developer): Uncomment the following lines before running the sample.
     */
    const filename = req.file.path;
    const encoding = '7bit';
    const sampleRateHertz = 48000;
    const languageCode = 'zh-TW';

    const config = {
        encoding: encoding,
        sampleRateHertz: sampleRateHertz,
        languageCode: languageCode
        // enableAutomaticPunctuation: true
    };

    /**
     * Note that transcription is limited to 60 seconds audio.
     * Use a GCS file for audio longer than 1 minute.
     */
    const audio = {
        content: readFileSync(filename).toString('base64'),
    };

    const conf = {
        config: config,
        audio: audio,
    };

    // Detects speech in the audio file. This creates a recognition job that you
    // can wait for now, or get its result later.
    const [operation] = await client.longRunningRecognize(conf);

    // Get a Promise representation of the final result of the job
    const [response] = await operation.promise();
    const transcription = response.results
        .map(result => result.alternatives[0].transcript)
        .join('\n');
    const text = { "text" : transcription };

    const res_zhuyin = await fetch("http://127.0.0.1:5000/zhuyin", {
        method: 'POST',
        body: JSON.stringify(text),
        headers: { 'Content-Type': 'application/json' }
    });

    const json = await res_zhuyin.json();
    const zhuyin = json['result'].join(' ');

    res.status(200).send(`Transcription: ${transcription} <br> Zhuyin: ${zhuyin}`);
});

app.listen(port, () => {
    console.log(`Express server listening on port: ${port}...`);
});