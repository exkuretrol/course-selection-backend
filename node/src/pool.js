import { createPool } from "mysql2";

const pool = createPool({
    connectionLimit: 10,
    host: process.env.dbHost,
    port: process.env.dbPort,
    user: process.env.dbUser,
    password: process.env.dbPass,
    database: process.env.dbName
});

export { pool };