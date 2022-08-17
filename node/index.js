import 'dotenv/config';
import { fileURLToPath } from 'url';
import path from 'path';
import express from 'express';
import { pool } from './src/pool.js';
import { router as apiRouter } from './routes/api.js';
import { router as recogApiRouter } from './routes/speech-recognize.js';
import morgan from 'morgan';

const app = express();

// log
app.use(morgan('dev'));

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// static files
app.use('/static', express.static(path.join(__dirname, 'public')));

// view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'twig');

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

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
    res.render('recognize', {
        title: "測試",
    })
});

// 測資上傳頁面
app.get("/upload", (req, res) => {
    let sql = `select count(*) as "全部測資" from NER_data`;

    pool.query(sql, (error, results, fields) => {
        res.render('upload.hbs', {
            allRecords: results[0].全部測資
        });
    });
});

// 手動 ner 頁面
app.get("/manualner",async (req, res) => {
    res.render('manualner.hbs');
});

// 管理員頁面
app.get("/admin", (req, res) => {
    res.render('admin.hbs')
});

app.use('/api', apiRouter);
app.use('/api', recogApiRouter);

const port = 3000;
app.listen(port, () => {
    console.log(`Express server listening on port: ${port}...`);
});