import { MongoClient } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

let db;
const client = new MongoClient(process.env.MONGO_URI);

async function connectToDb(cb) {
  await client.connect();
  db = client.db("Financezy"); // or any other DB name
  cb();
}

function getDb() {
  return db;
}

export { connectToDb, getDb };
