// Firebase integration for TrustGuard UI — realtime Firestore sync
// Loads Firebase modular SDK from CDN and wires a simple scans collection
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js';
import { getFirestore, collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy } from 'https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js';

// Configuration (from user)
const firebaseConfig = {
  apiKey: "AIzaSyCCGv9pq9QHhcIrBAwvXE4Yfebcv3a6D9A",
  authDomain: "trustguard-9cff9.firebaseapp.com",
  projectId: "trustguard-9cff9",
  storageBucket: "trustguard-9cff9.firebasestorage.app",
  messagingSenderId: "515477057525",
  appId: "1:515477057525:web:d717fcfea0a292604bbabc",
  measurementId: "G-1C9L7KH0QR"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Keep Firebase optional for the scan workflow: the FastAPI backend remains authoritative.
window.firebaseReady = Promise.resolve({ app, db });

function showFirebaseToast(message, detail, type) {
  if (typeof window.toast === 'function') window.toast(message, detail, type);
}

// Expose a saveScan function used by the main UI to persist local entries.
window.saveScan = async function(entry){
  try{
    // Ensure a timestamp exists
    const payload = Object.assign({}, entry);
    if(!payload.date) payload.date = Date.now();
    const saved = await addDoc(collection(db, 'scans'), payload);
    // Note: onSnapshot will update the UI when the doc appears.
    return saved.id;
  }catch(e){ console.error('saveScan error', e); showFirebaseToast('Firestore save failed','See console for details','danger'); }
};

window.deleteRemoteScan = async function(id){
  try{
    await deleteDoc(doc(db, 'scans', id));
    toast && toast('Remote entry deleted','', 'info');
  }catch(e){ console.error('deleteRemoteScan error', e); showFirebaseToast('Delete failed','See console for details','danger'); }
};

// Realtime listener: keep the UI in sync with the 'scans' collection.
const scansQ = query(collection(db,'scans'), orderBy('date','desc'));
onSnapshot(scansQ, snapshot=>{
  const arr = snapshot.docs.map(d=>({ id: d.id, ...d.data() }));
  window.firebaseScanHistory = arr;
}, error => {
  console.error('Firestore scans listener error', error);
  showFirebaseToast('Firebase sync unavailable', 'FastAPI history remains active', 'warn');
});

console.log('Firebase realtime listener initialized');
