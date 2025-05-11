import express from "express";
import { connectToDb } from "./database.js";
import cors from "cors";
import dotenv from "dotenv";
import authRoutes from "../routes/auth.js";

dotenv.config();
const port = process.env.PORT || 5000;
const app = express();

app.use(cors());
app.use(express.json());
app.use("/api/auth", authRoutes);

connectToDb(() => {
  console.log("Successfully connected to Database");
  app.listen(port, "localhost", () => {
    console.log(`listening on port ${port}`);
  });
});
