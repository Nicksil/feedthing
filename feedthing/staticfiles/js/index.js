var webSocketBridge = new channels.WebSocketBridge();
var feedsList = document.getElementById('feeds-list');
var feedURLInput = document.getElementById('feed-url-id');
var feedURLBtn = document.getElementById('feed-url-btn');
var ws_path = '/';

webSocketBridge.connect(ws_path);

webSocketBridge.listen(function (data) {
    var _listItem = createListItem(data.feed_title);
    feedsList.appendChild(_listItem);
});

feedURLBtn.addEventListener('click', function () {
    webSocketBridge.send({
        'feedURL': feedURLInput.value
    });
});

function createListItem(text) {
    var listItem = document.createElement('li');
    listItem.innerText = text;

    return listItem;
}

// webSocketBridge.socket.onopen = function () {
//     console.log('Connected to chat socket');
// };
// webSocketBridge.socket.onclose = function () {
//     console.log('Disconnected from chat socket');
// }
