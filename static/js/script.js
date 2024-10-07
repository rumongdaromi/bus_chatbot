document.addEventListener('DOMContentLoaded', function() {
    // 페이지가 로드될 때 초기 메시지 추가
    addMessage("안녕하세요! 용인터미널 시간표 챗봇입니다. 버스 번호를 입력해주세요.", 'other');
});

document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const input = document.getElementById('messageInput');
    const messageText = input.value;
    input.value = '';

    // 메시지 추가
    addMessage(messageText, 'user');

    // 서버에 요청 보내기
    fetch('/your-api-endpoint/', {  // 실제 API 엔드포인트로 수정하세요
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message: messageText
        })
    })
    .then(response => response.json())
    .then(data => {
        // 서버 응답 처리
        addMessage(data.reply, 'other');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('서버에 요청하는 중 오류가 발생했습니다.', 'other');
    });
});

function addMessage(text, type) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.innerHTML = `<p>${text}</p>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // 스크롤을 아래로
}
