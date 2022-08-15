import 'dotenv/config';
import { fileURLToPath } from 'url';
import path from 'path';
import express from 'express';
import { pool } from './src/pool.js';
import { router as api } from './routes/api.js';
import { router as recognize_api } from './routes/speech-recognize.js';
import morgan from 'morgan';

const app = express();

// log
app.use(morgan('dev'));

// view engine
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(__dirname + 'public'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.set('view engine', 'hbs');

// 首頁
app.get("/", (req, res) => {
    const html = `
    <ul>
        <li><a href="/recognize">語音辨識</a></li>
        <li><a href="/upload">測資上傳</a></li>
        <li><a href="/manualner">手動 ner</a></li>
        <li><a href="/admin">管理</a></li>
    </ul>
    `;
    res.send(html);
});

// 語音辨識頁面
app.get("/recognize", (req, res) => {
    res.render(__dirname + '/views' + '/recognize.hbs', {
        title: "測試",
    })
});

// 測資上傳頁面
app.get("/upload", (req, res) => {
    let sql = `select count(*) as "全部測資" from NER_data`;

    pool.query(sql, (error, results, fields) => {
        res.render(__dirname + '/views' + '/upload.hbs', {
            allRecords: results[0].全部測資
        });
    });
});

// 手動 ner 頁面
app.get("/manualner", (req, res) => {
    let sql = `select count(*) as "全部測資" from NER_data`;

    pool.query(sql, (error, results, fields) => {
        res.render(__dirname + '/views' + '/manualner.hbs', {
            allRecords: results[0].全部測資
        });
    });
});

// 管理員頁面
app.get("/admin", (req, res) => {
    res.render(__dirname + '/views' + '/admin.hbs')
});

app.use('/api', api);
app.use('/api', recognize_api);

const port = 3000;
app.listen(port, () => {
    console.log(`Express server listening on port: ${port}...`);
});