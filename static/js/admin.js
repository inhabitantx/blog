(function(){


  function renderStatus(event, confirmation){

    container = event.target.parentElement.parentElement
    if(confirmation.action === "delete"){
      var cont = "<div class='alert alert-danger' role='alert'>"+
                  `<i class='fa fa-ban'></i>${confirmation.message}`+
                  "</div>"

    }else{
    var cont = "<div class='alert alert-success' role='alert'>"+
                `<i class='fa fa-check'></i>${confirmation.message}`+
                "</div>"
    }

    container.innerHTML = cont

  }

  function handleModeration (event){
    event.preventDefault()

    let data = {"value" : event.target.value, "id" : event.target.dataset.id}

    let confirmation = {}

    let ajax = new XMLHttpRequest
    ajax.overrideMimeType('application/json')
    ajax.open('POST', `/moderatecomments`)
    ajax.onreadystatechange = function(){
      if(this.readyState === 4 && this.status == 200){
        confirmation = JSON.parse(ajax.responseText)
        renderStatus(event, confirmation)

      }
    }
    ajax.send(JSON.stringify(data))
  }

  //add Eventlisteners to comment-moderation linkReplyButtons
  if(document.querySelector('.approve_comment_button')){
    let approvecomment = document.querySelectorAll('.approve_comment_button')
    let deletecomment = document.querySelectorAll('.delete_comment_button')

    for(let i = 0; i < approvecomment.length; i++){
      approvecomment[i].addEventListener('click', handleModeration)
      deletecomment[i].addEventListener('click', handleModeration)
    }
  }

  if(document.querySelector('.approve_reply_button')){
    let approvereply = document.querySelectorAll('.approve_reply_button')
    let deletereply = document.querySelectorAll('.delete_reply_button')

    for(let i = 0; i < approvereply.length; i++){
      approvereply[i].addEventListener('click', handleModeration)
      deletereply[i].addEventListener('click', handleModeration)
    }
  }
})()
