const WebSocket = require('ws');

// WebSocket 서버 생성 (포트 8080)
const wss = new WebSocket.Server({ port: 8080 });

console.log('WebSocket 서버가 8080 포트에서 실행 중입니다.');


const Response = {
    MESSAGE_NOT_VALID : "MESSAGE_NOT_VALID",
    MOVIE_NOT_EXIST : "MOVIE_NOT_EXIST",
    MOVIE_EXIST : "MOVIE_EXIST",
    INTERNAL_SERVER_ERROR : "INTERNAL_SERVER_ERROR",
}

const Request = {
    GET : "GET",
    POST : "POST",
    GET_ALL : "GET_ALL"
}

let movie_review_map = {
    "마션":{
        "헬로 마션?":["우주","우주선"],
        "마션입니까?":["현직 군인","우주"]
    },
    "인터스텔라":{
        "굿 인터스텔라":["공군","우주"],
    }
}

// 연결된 모든 클라이언트에게 메시지 전송하는 broadcast 함수
function broadcast(message, ws) {
  wss.clients.forEach(client => {
    if(client != ws){
        if (client.readyState === WebSocket.OPEN) {
            client.send(message);
          }
    }
  });
}

class ReviewPatcher{
    constructor(){}

    addMovie(moviename, review_list){

        review_list.forEach((key)=>{

        })

    }

    getMovie(moviename){
        if(movie_review_map[moviename] == null){
            return JSON.stringify({"msg":Response.MOVIE_NOT_EXIST})
        }

        return JSON.stringify({"msg":Response.MOVIE_EXIST,"moviedata":movie_review_map[moviename]});
    }
}

const reviewpatcher = new ReviewPatcher();

// 클라이언트와의 연결 이벤트 처리
wss.on('connection', (ws) => {
  console.log('새 클라이언트가 연결되었습니다.');

  // 클라이언트로부터 메시지 수신
  ws.on('message', (message) => {
    console.log(`수신한 메시지: ${message}`);
    // 받은 메시지를 모든 클라이언트에 전송
    broadcast(`Broadcast: ${message}`, ws);

    try{
        json_message = JSON.parse(message);

        response_message = undefined;
        switch(json_message["reqType"]){
            case Request.GET:{
                response_message = reviewpatcher.getMovie(json_message["moviename"]);
                break;
            }
            default:{
                break;
            }
        }

        if(response_message != undefined){
            ws.send(response_message);
        }else{
            ws.send(JSON.stringify({"msg":Response.INTERNAL_SERVER_ERROR}));
        }
    }catch(error){
        console.error(error)
        ws.send(JSON.stringify({"msg":Response.MESSAGE_NOT_VALID,"err":error}));
    }
  });

  // 클라이언트가 연결을 끊었을 때 처리
  ws.on('close', () => {
    console.log('클라이언트 연결이 종료되었습니다.');
  });
});
