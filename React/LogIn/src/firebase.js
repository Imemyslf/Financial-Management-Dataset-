// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCcBCQOyqxBV_ZRPcvtd1-GyqepCcpOoTs",
  authDomain: "financezy-7d41d.firebaseapp.com",
  projectId: "financezy-7d41d",
  storageBucket: "financezy-7d41d.firebasestorage.app",
  messagingSenderId: "1062065150544",
  appId: "1:1062065150544:web:e7094d4a91e07a7efc4f55",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, signInWithPopup };
