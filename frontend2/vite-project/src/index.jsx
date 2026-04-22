body {
  margin: 0;
  background: #0f172a;
  color: white;
  font-family: "Segoe UI";
}

.navbar {
  display: flex;
  justify-content: space-between;
  padding: 15px 30px;
  background: #020617;
}

.main {
  display: flex;
  height: calc(100vh - 60px);
}

.panel {
  padding: 20px;
  border-radius: 15px;
}

.left {
  width: 20%;
  background: #1e293b;
}

.center {
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.right {
  width: 20%;
  background: #1e293b;
}

.result-img {
  max-width: 90%;
  border-radius: 15px;
}

.preview {
  width: 100%;
}

.map-bar {
  height: 10px;
  background: #334155;
  border-radius: 5px;
  margin-top: 10px;
}

.map-bar div {
  height: 100%;
  background: linear-gradient(to right, red, orange, green);
}