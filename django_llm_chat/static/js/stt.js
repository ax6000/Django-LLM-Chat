let socket;
let mediaRecorder;
let audioChunks = [];

// WebSocketの接続を開始する関数
function startWebSocket() {
    socket = new WebSocket('ws://localhost:8000/ws/');
    
    socket.onopen = function(e) {
        console.log("WebSocket接続が確立されました");
    };

    socket.onmessage = function(event) {
        console.log("サーバーからの応答:", event.data);
        // ここで受信したテキストを画面に表示する処理を追加
        document.getElementById('transcription').textContent = event.data;
    };

    socket.onclose = function(event) {
        console.log("WebSocket接続が閉じられました");
    };

    socket.onerror = function(error) {
        console.log("WebSocketエラー: ", error);
    };
}

// 音声のキャプチャを開始する関数
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
                if (socket.readyState === WebSocket.OPEN) {
                    socket.send(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                // 必要に応じて、ここでaudioBlobを処理する
            };

            mediaRecorder.start(1000); // 1秒ごとにデータを送信
        })
        .catch(error => console.error('マイクへのアクセスエラー:', error));
}

// 音声のキャプチャを停止する関数
function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}

// ページ読み込み時にWebSocket接続を開始
window.onload = function() {
    startWebSocket();
};