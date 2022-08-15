import express from 'express';
import { pool } from '../src/pool.js';

const promisePool = pool.promise();
const router = express.Router();

/**
 * 輸出訓練模型用測資
 */
router.get("/output/:mode", async (req, res) => {
    const mode = req.params.mode;
    const sql = "select `測資手動NER` as json from NER_data";
    const sql1 = "select `編號`, `語音辨識文字`, JSON_EXTRACT(`測資手動NER`, '$.tags') as tags from NER_data";
    let resultA = await promisePool.query(sql)
        .then(([rows, fields]) => {
            return rows.map((_) => { return JSON.parse(_.json) });
        })

    let resultB = await promisePool.query(sql1)
        .then(([rows, fields]) => {
            return rows.map((_) => {
                let tokens = _.語音辨識文字.replace(/\s/g, '').split('');
                let tags = JSON.parse(_.tags);
                if (_.tags == null) return null;
                if (tokens.length !== tags.length) return null;
                return { "tokens": tokens, "tags": tags };
            })
        })
    resultA = resultA.filter(_ => _ !== null);
    resultB = resultB.filter(_ => _ !== null);

    switch (mode) {
        // 全部
        case '0':
            let output = Array.prototype.concat(resultA, resultB);
            res.json(output);
            break;

        // 只有輸入測資
        case '1':
            res.json(resultA);
            break;
        // 只有語音測資

        case '2':
            res.json(resultB);
            break;

        default:
            res.sendStatus(404);
            break;
    }

});

/**
 * 使用者測資數目
 */
router.get("/users/:userName", (req, res) => {
    let uname = req.params.userName;
    let sql = `select * from ( select count(*) as "全部測資" from NER_data) a, ( select count(*) as "某人的測資" from NER_data where 你是誰 = "${uname}") b`;
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
        res.json(result[0]);
    });
});

/**
 * 使用者新增測資
 */
router.post("/users/:userName", (req, res) => {
    let uname = req.params.userName;
    let results = req.body;
    let sql = `INSERT INTO NER_data (你是誰, 測資文字, 語音辨識文字, 語音辨識注音, 語音檔路徑, 產生時間) VALUES ("${uname}", "${results.text}", "${results.transcript}", "${results.zhuyin}", "${results.filePath}", current_timestamp())`;
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
    });
    res.sendStatus(200);
});

/**
 * 取回測資
 */
router.get("/data/:no", (req, res) => {
    const no = req.params.no;
    let sql = `select * from NER_data where 編號 = ${no}`
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
        res.json(result[0]);
    });
});

/**
 * 更新測資
 */
router.put('/data', (req, res) => {
    let json = req.body;
    let json_string = JSON.stringify(json.json);
    let sql = `UPDATE NER_data SET 測資手動NER = '${json_string}' WHERE 編號 = ${json.no};`
    pool.query(sql, (error, result, fields) => {
        if (error) throw error;
    });
    res.sendStatus(200);
})

export { router };