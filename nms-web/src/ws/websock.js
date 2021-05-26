import store from '../store/index'


function onOpen(evt) {
    console.log('websocket open')
}

function onClose(evt) {
    console.log('websocket close')
}

export { onMessage, onOpen, onClose }