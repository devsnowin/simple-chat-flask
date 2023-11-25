var socket = io();

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("chat-form")

    socket.on('message', (data) => {
        createMessage(data.name, data.message)
    })

    form.addEventListener('submit', handleSubmit);
})

function handleSubmit(e) {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const msg = formData.get('message')
    console.log("msg", msg)
    if (msg.trim() === "") return

    socket.emit("message", {message: msg})
    e.currentTarget.reset()
}

function createMessage(name, msg) {

    const parsedName = String(name);
    const parsedMsg = String(msg)

    const currentUser = document.getElementById("username").textContent.toLowerCase();
    const messages = document.getElementById("chat-messages")
    const messageDiv = document.createElement('div')
    messageDiv.classList.add('message')

    if (parsedMsg.toLowerCase().includes(currentUser)) return

    if (currentUser === name.toLowerCase()) {
        messageDiv.classList.add('my-message')
    }

    const nameTag = document.createElement('h5')
    nameTag.textContent = parsedName

    const msgTag = document.createElement('p')
    msgTag.textContent = parsedMsg

    const timeTag = document.createElement('time')
    timeTag.textContent = new Date().toLocaleString()

    messageDiv.appendChild(nameTag)
    messageDiv.appendChild(msgTag)
    messageDiv.appendChild(timeTag)

    messages.appendChild(messageDiv)
}
