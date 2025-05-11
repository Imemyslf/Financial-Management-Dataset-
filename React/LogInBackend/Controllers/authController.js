import bcrypt from "bcryptjs";
import { getDb } from "../src/database.js";
import admin from "../src/firebaseAdmin.js";

const login = async (req, res) => {
  try {
    const db = getDb();
    const { username, password, authMethod = "local" } = req.body;

    const user = await db.collection("User").findOne({ username, authMethod });
    if (!user) {
      return res.status(400).json({ error: "User not found for this method" });
    }

    if (authMethod === "local") {
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res.status(400).json({ error: "Invalid credentials" });
      }
    }

    res.status(200).json({ message: "Login successful" });
  } catch (err) {
    console.error("Login error:", err);
    res.status(500).json({ error: "Login failed" });
  }
};

const signup = async (req, res) => {
  try {
    const db = getDb();
    const { username, password, authMethod = "local" } = req.body;

    const existingUser = await db.collection("User").findOne({ username, authMethod });
    if (existingUser) {
      return res.status(409).json({ error: "User already exists with this method" });
    }

    const hashedPassword = authMethod === "local" ? await bcrypt.hash(password, 10) : null;

    await db.collection("User").insertOne({
      username,
      password: hashedPassword,
      authMethod,
    });

    res.status(201).json({ message: "User registered successfully" });
  } catch (err) {
    console.error("Signup error:", err);
    res.status(500).json({ error: "Signup failed" });
  }
};

const googleAuth = async (req, res) => {
  try {
    const { idToken, displayName } = req.body;

    const decodedToken = await admin.auth().verifyIdToken(idToken);
    const { email } = decodedToken;

    const db = getDb();

    const existingUser = await db.collection("User").findOne({
      username: email,
      authMethod: "google",
    });

    if (existingUser) {
      return res.status(200).json({
        message: "Logged in successfully",
        name: existingUser.displayName || displayName,
      });
    } else {
      await db.collection("User").insertOne({
        username: email,
        password: null,
        authMethod: "google",
        displayName: displayName || email.split("@")[0],
      });

      return res.status(200).json({
        message: "User signed up successfully",
        name: displayName || email.split("@")[0],
      });
    }
  } catch (err) {
    console.error("Google auth error:", err);
    return res.status(401).json({ error: "Google auth failed" });
  }
};


export { login, signup, googleAuth };