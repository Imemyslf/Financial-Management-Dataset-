// firebaseAdmin.js
import admin from "firebase-admin";
import fs from "fs";

const serviceAccount = JSON.parse(
  fs.readFileSync(new URL('../firebaseServiceAccountKey.json', import.meta.url))
);


admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

export default admin;
