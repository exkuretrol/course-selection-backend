import express from 'express';
import multer from 'multer';
import fetch from 'node-fetch';
import { SpeechClient } from '@google-cloud/speech';
import { readFileSync } from 'fs';

const router = express.Router();

const storage = multer.diskStorage(
    {
        destination: './sound_files/',
        filename: function (req, file, cb) {
            cb(null, file.originalname);
        }
    }
);
const upload = multer({ storage: storage });

router.post("/recognize", upload.single("audio_data"), async function (req, res) {
    const client = new SpeechClient();

    const filename = req.file.path;
    const encoding = 'OGG_OPUS';
    const sampleRateHertz = 48000;
    const languageCode = 'zh-TW';

    const config = {
        encoding: encoding,
        sampleRateHertz: sampleRateHertz,
        languageCode: languageCode
    };

    const audio = {
        content: readFileSync(filename).toString('base64'),
    };

    const conf = {
        config: config,
        audio: audio,
    };

    const [operation] = await client.longRunningRecognize(conf);

    const [response] = await operation.promise();
    const transcription = response.results
        .map(result => result.alternatives[0].transcript)
        .join('\n');
    const text = { "text": transcription };

    const json = await fetch(`http://${process.env.pythonHost}/api/zhuyin`, {
        method: 'POST',
        body: JSON.stringify(text),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(_ => _.json());

    const zhuyin = json['result'].join(' ');

    res.json(JSON.stringify({ "transcript": transcription, "zhuyin": zhuyin }));
    // res.json(JSON.stringify(text));
});

export { router };