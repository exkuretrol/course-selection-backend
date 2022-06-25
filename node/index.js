import 'dotenv/config';
import { fileURLToPath } from 'url';
import path from 'path';
import express from 'express';
import multer from 'multer';
import fetch from 'node-fetch';
import { SpeechClient } from '@google-cloud/speech';
import { readFileSync } from 'fs';
import { createPool } from 'mysql';

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
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
console.log(__dirname);
app.set('view engine', 'ejs');

const pool = createPool({
    connectionLimit: 10,
    host: process.env.dbHost,
    port: process.env.dbPort,
    user: process.env.dbUser,
    password: process.env.dbPass,
    database: process.env.dbName
});

app.get("/", (req, res) => {
    res.status(200).send("<h3>這裡什麼都沒有喔~</h3>");
});

app.get("/upload", (req, res) => {
    let sql = `
    select 
        count(*) as "全部測資"
    from 
        NER測資
    `;

    pool.query(sql, (error, results, fields) => {
        res.render(__dirname + '/views' + '/upload.ejs', {allRecords: results[0].全部測資});
    });
});

app.get("/testdta", (req, res) => {
    pool.query("select * from NER測資", (error, results, fields) => {
        if (error) throw error;
        res.send("number of rows is: " + results[0]);
    });
});

app.get("/users/:userName", (req, res) => {
    let uname = req.params.userName;
    let sql = `
    select * from (
        select 
            count(*) as "全部測資"
        from 
            NER測資
    ) a, 
    (
        select 
            count(*) as "某人的測資"
        from 
            NER測資
        where
            你是誰 = "${uname}"
    ) b`;
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
        res.json(result[0]);
    });
});

app.post("/users/:userName", (req, res) => {
    let uname = req.params.userName;
    let results = req.body;
    let sql = `INSERT INTO NER測資 (你是誰, 測資文字, 語音辨識文字, 語音辨識注音, 語音檔路徑, 產生時間) VALUES ("${uname}", "${results.text}", "${results.transcript}", "${results.zhuyin}", "${results.filePath}", current_timestamp())`;
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
    });
    res.sendStatus(200);
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

    res.json(JSON.stringify({ "transcript" : transcription, "zhuyin" : zhuyin }));
    // res.status(200).send(`Transcription: ${transcription} <br> Zhuyin: ${zhuyin}`);
});


app.listen(port, () => {
    console.log(`Express server listening on port: ${port}...`);
});