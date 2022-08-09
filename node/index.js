import 'dotenv/config';
import { fileURLToPath } from 'url';
import path from 'path';
import express from 'express';
import multer from 'multer';
import fetch from 'node-fetch';
import { SpeechClient } from '@google-cloud/speech';
import { readFileSync } from 'fs';
import { createPool } from 'mysql2';
import cors from 'cors';
// TODO: move all route to routes.js file

const storage = multer.diskStorage(
    {
        destination: './sound_files/',
        filename: function (req, file, cb) {
            cb(null, file.originalname);
        }
    }
);

const upload = multer({ storage: storage });

const another_storage = multer.diskStorage(
    {
        destination: './tmp/',
        filename: function (req, file, cb) {
            cb(null, file.originalname);
        }
    }
);

const another_upload = multer({ storage: another_storage });

const app = express();
const port = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors());
app.use(express.static(__dirname + 'public'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.set('view engine', 'hbs');

const pool = createPool({
    connectionLimit: 10,
    host: process.env.dbHost,
    port: process.env.dbPort,
    user: process.env.dbUser,
    password: process.env.dbPass,
    database: process.env.dbName
});

const promisePool = pool.promise();

app.get("/", (req, res) => {
    res.status(200).send("<h3>這裡什麼都沒有喔~</h3>");
});

app.get("/recognize", (req, res) => {
    res.render(__dirname + '/views' + '/recognize.hbs', {
        title: "測試",
    })
});

app.get("/upload", (req, res) => {
    let sql = `
    select 
        count(*) as "全部測資"
    from 
        NER_data
    `;

    pool.query(sql, (error, results, fields) => {
        res.render(__dirname + '/views' + '/upload.hbs', {
            allRecords: results[0].全部測資
        });
    });
});

app.get("/data/output/:mode", async (req, res) => {
    const mode = req.params.mode;
    const sql = "select `測資手動NER` as json from NER_data";
    const sql1 = "select `編號`, `語音辨識文字`, JSON_EXTRACT(`測資手動NER`, '$.tags') as tags from NER_data";

    switch (mode) {
        // 全部
        case '0':
            let resultA = await promisePool.query(sql)
                .then(([rows, fields]) => {
                    return rows.map((_) => { return JSON.parse(_.json) });
                });

            let resultB = await promisePool.query(sql1)
                .then(([rows, fields]) => {
                    return rows.map((_) => {
                        let tokens = _.語音辨識文字.replace(/\s/g, '').split('');
                        if (tokens.length !== _.tags.length) _.編號;
                        return { "tokens": tokens, "tags": JSON.parse(_.tags) };
                    })
                });

            let output = Array.prototype.concat(resultA, resultB);
            res.json(output);

            break;
        // 只有輸入測資
        case '1':
            pool.query(sql, (error, results, fields) => {
                if (error) throw error;
                let result;
                result = results.map((_) => { return JSON.parse(_.json) });
                res.json(result);
            });
            break;
        // 只有語音測資
        case '2':
            pool.query(sql1, (error, results, fields) => {
                if (error) throw error;
                let result;
                result = results.map((_) => {
                    let tokens = _.語音辨識文字.replace(/\s/g, '').split('');
                    if (tokens.length !== _.tags.length) _.編號;
                    return { "tokens": tokens, "tags": JSON.parse(_.tags) };
                })
                res.json(result);
            });
            break;

        default:
            res.sendStatus(404);
            break;
    }

});

app.get("/manualner", (req, res) => {
    let sql = `
    select 
        count(*) as "全部測資"
    from 
        NER_data
    `;

    pool.query(sql, (error, results, fields) => {
        res.render(__dirname + '/views' + '/manualner.hbs', {
            allRecords: results[0].全部測資
        });
    });
});

app.get("/users/:userName", (req, res) => {
    let uname = req.params.userName;
    let sql = `
    select * from (
        select 
            count(*) as "全部測資"
        from 
            NER_data
    ) a, 
    (
        select 
            count(*) as "某人的測資"
        from 
            NER_data
        where
            你是誰 = "${uname}"
    ) b`;
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
        res.json(result[0]);
    });
});

app.get("/ner-data/:no", (req, res) => {
    const no = req.params.no;
    let sql = `
        select 
            * 
        from 
            NER_data 
        where
            編號 = ${no}
    `
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
        res.json(result[0]);
    });
});

app.get("/admin", (req, res) => {
    res.render(__dirname + '/views' + '/admin.hbs')
});

app.post('/ner-data/update', (req, res) => {
    let json = req.body;
    let json_string = JSON.stringify(req.body.json);
    let sql = `UPDATE NER_data SET 測資手動NER = '${json_string}' WHERE 編號 = ${json.no};`
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
    });
    res.sendStatus(200);
})

app.post("/users/:userName", (req, res) => {
    let uname = req.params.userName;
    let results = req.body;
    let sql = `INSERT INTO NER_data (你是誰, 測資文字, 語音辨識文字, 語音辨識注音, 語音檔路徑, 產生時間) VALUES ("${uname}", "${results.text}", "${results.transcript}", "${results.zhuyin}", "${results.filePath}", current_timestamp())`;
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
    const text = { "text": transcription };

    const res_zhuyin = await fetch("http://python:5000/zhuyin", {
        method: 'POST',
        body: JSON.stringify(text),
        headers: { 'Content-Type': 'application/json' }
    });

    const json = await res_zhuyin.json();
    const zhuyin = json['result'].join(' ');

    res.json(JSON.stringify({ "transcript": transcription, "zhuyin": zhuyin }));
    // res.status(200).send(`Transcription: ${transcription} <br> Zhuyin: ${zhuyin}`);
});

app.post("/recognize", another_upload.single("audio_data"), async (req, res) => {
    const client = new SpeechClient();

    const filename = req.file.path;
    const encoding = '7bit';
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

    const res_zhuyin = await fetch("http://python:5000/zhuyin", {
        method: 'POST',
        body: JSON.stringify(text),
        headers: { 'Content-Type': 'application/json' }
    });

    const json = await res_zhuyin.json();
    const zhuyin = json['result'].join(' ');

    res.json(JSON.stringify({ "transcript": transcription, "zhuyin": zhuyin }));
});

app.listen(port, () => {
    console.log(`Express server listening on port: ${port}...`);
});