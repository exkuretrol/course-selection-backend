
import fetch from 'node-fetch';
const text = { "text": "測試" };
const data = JSON.stringify(text);

const res_zhuyin = await fetch("http://127.0.0.1:5000/zhuyin", {
  method: 'POST',
  body: data,
	headers: {'Content-Type': 'application/json'}
});
console.log(res_zhuyin);

const dt = await res_zhuyin.json();
console.log(dt['result'].join(' '));