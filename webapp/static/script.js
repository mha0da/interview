var chatSection = document.getElementById("msger");
var loginSection = document.getElementById("login");
var username = document.getElementById("username").innerText;
var room = document.getElementById("room").innerText;
chatSection.style.visibility = "hidden";
if (username) {
  var websocket = new WebSocket(
    "ws://localhost:8000/ws/" + room + "/" + username
  );
  websocket.onmessage = function (event) {
    var data = JSON.parse(event.data);
    if (data.room == room) {
      if (data.type == "message") {
        var direct = data.user == username ? "right-msg" : "left-msg";
        createBubble(direct, data);
      } else {
        createNotification(data);
      }
    }
  };

  websocket.onopen = function (event) {
    var msg = {
      content: "New Member " + username + " Join.",
      user: username,
      room: room,
      type: "info",
    };
    websocket.send(JSON.stringify(msg));
    event.preventDefault();
  };

  websocket.onclose = function (event) {
    var msgerSection = document.getElementById("msger");
    msgerSection.style.display = "none";
    var closeDiv = document.getElementById("close");
    closeDiv.removeAttribute("hidden");
  };

  websocket.onerror = function (event) {
    var msgerSection = document.getElementById("msger");
    msgerSection.style.display = "none";
    var closeDiv = document.getElementById("error");
    closeDiv.removeAttribute("hidden");
  };

  loginSection.setAttribute("hidden", "true");
  chatSection.style.visibility = "visible";
}

function login(event) {
  var username = document.getElementById("usernameInput");
  var room = document.getElementById("roomInput");
  if (username.value) {
    window.location.assign(
      "http://localhost:8000/" + room.value + "/" + username.value
    );
  }
  event.preventDefault();
}

function sendMessage(event) {
  var input = document.getElementById("msger-input");
  if (input.value) {
    var msg = {
      content: input.value,
      user: username,
      room: room,
      type: "message",
    };
    websocket.send(JSON.stringify(msg));
    input.value = "";
  }
  event.preventDefault();
}

function quitRoom() {
  fetch("http://localhost:8000/disconnect/" + room + "/" + username).catch(
    (error) => console.error("Error:", error)
  );
}

function formatDate() {
  var date = new Date();
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function createBubble(direct, data) {
  var bubble = document.getElementById("msger-chat");
  var time = formatDate();
  bubble.innerHTML +=
    '<div class="msg ' +
    direct +
    '">\
 <div class="msg-bubble">\
   <div class="msg-info">\
     <div class="msg-info-name">' +
    data.user +
    '</div>\
     <div class="msg-info-time">' +
    time +
    '</div>\
   </div>\
  <div class="msg-text">\
      ' +
    data.content +
    "\
  </div>\
</div>\
</div>";
}

function createNotification(data) {
  var bubble = document.getElementById("msger-chat");
  bubble.innerHTML +=
    '<div class="msger-notification">' + data.content + "</div>";
}
