const threads = document.querySelector(".threads")
const message_form = document.querySelector("#message_form")

var replied_msg_id;

function getCookies(){
    cookies = document.cookie.split(";")

    cookie_map = { }

    for(cookie of cookies){
        split = cookie.indexOf("=")
        cookie_name = cookie.substring(0, split)
        cookie_value = cookie.substring(split + 1,)
        
        cookie_map[cookie_name] = cookie_value
    }

    return cookie_map
}


function addThreadEvent (){
    const thread_item_list = document.querySelectorAll("div.thread")
 
     for(let item of thread_item_list){
         item.addEventListener("dblclick", (e) => {
             replied_msg_id = item.getAttribute("id")
             console.log("🚀 ~ file: message.js ~ line 127 ~ item.addEventListener ~ replied_msg_id", replied_msg_id)
         })
     }
 }


function sendMessage(userId, roomId, messageContent, replied_msg_id){
    let csrftoken = getCookies()["csrftoken"]
    let request_body = {
        "user":userId,
        "room":roomId,
        "body": messageContent,
        "replied_msg_id":replied_msg_id || null
    }
    
    fetch("http://127.0.0.1:8000/base/api/create-room-message/", {
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken":csrftoken,
        },
        method:"post",
        body:JSON.stringify(request_body),        
    })
    .then(res => {
        if (res.ok) return res.json()
        console.error("something went wrong")
    })
    .then(data => {
        displayData(data)
    })
    .catch( err => console.error(err))
}


function displayData(data){
    let threads = document.querySelector("div.threads")
    let participants = document.querySelector("div.participants__list")
    let {body, message_id, username, user_url, timesince, replied_msg, replied_user, delete_url, participants_list} = data
    console.dir(data)

    let thread = document.createElement("div")
    thread.classList.add("thread")
    thread.setAttribute("id", message_id)

    thread.innerHTML = `
    <div class="thread__top">
      <div class="thread__author">
        <a href="${user_url}" class="thread__authorInfo">
          <div class="avatar avatar--small">
            <img src="https://randomuser.me/api/portraits/men/37.jpg" />
          </div>
          <span>@${username}</span>
        </a>
        <span class="thread__date">${timesince} </span>
      </div>
      <div class="thread__delete">
          <a href="${delete_url}">
              <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                  <title>remove</title>
                  <path
                  d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"
                  ></path>
              </svg>
          </a>
      </div>
    </div>
    <div class="thread__details">
      <div class="replied__message">
        replied to ${replied_user || ""}: "${replied_msg || ""}"
      </div>
      ${body}
    </div>`

  threads.appendChild(thread)
  addThreadEvent()

  let participant = document.createElement("a")
  participant.classList.add("participant")
  participant.href = user_url

  participant.innerHTML = `
  <div class="avatar avatar--medium">
      <img src="https://randomuser.me/api/portraits/men/37.jpg" />
  </div>
  <p>
      ${username}
      <span>@${username}</span>
  </p>
 `

    let participant_names = participants_list.map((item) => {
        return item.username
    })

    
    if(!participant_names.includes(username)){
        participants.appendChild(participant)
        console.log(participant_names)
    }

    let thread_bottom =threads.lastElementChild.getBoundingClientRect().bottom

    threads.scrollBy(0, thread_bottom)
}

//Event Listeners

addThreadEvent()


message_form.addEventListener("submit", (e) => {
    e.preventDefault()
    
    let messageBody = document.querySelector("#message_form>input[name='body']")

    sendMessage(userId, roomId, messageBody.value,replied_msg_id)
    replied_msg_id = undefined

    messageBody.value = ""
})







