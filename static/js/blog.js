

// ############# Typeahead #############


// configure typeahead

$(document).ready(function(){

    $('.typeahead').val(function(){
        $(this).val($(this).attr('placeholder'));
    });

      $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
      },
      {
        display: function(suggestion){return null;},
        source: ajax_request,
        templates: {
            suggestion: Handlebars.compile(
                "<a href='/article/{{slug}}'><div class='row typeahead_template'>" +
                "<img class='col-lg-4 typeahead_thumbnail' src='/static/img/{{img}}'/>" +
                "<div class='col-lg-8'><h3>{{title}}</h3><div class='typeahead_text'>{{body}}</div></div>" +
                "</div></a>"
            )
        }
      });
  });



var ajax_request = function(query, syncResults, asyncResults){

                      let request = $.ajax({
                           url: "/autocomplete",
                           type: 'POST',
                           contentType: 'application/json',
                           data: JSON.stringify({query:query}),
                           dataType: "JSON"

                        }).done(function(data){

                          return asyncResults(data)
                        });
                    }


// reset searchfield after usage

const button = document.body.querySelector('#searchbutton');

button.addEventListener('click', function(){

        field.submit();
        field.reset();

      });

//Display searchfield

const showSearch = document.querySelector('#show-search');

showSearch.addEventListener('click', toggleSearchfield)

function toggleSearchfield (event){
  const searchfield = document.querySelector('.formcontainer')
  const close = document.querySelector('.close_searchfield')
  close.addEventListener('click', toggleSearchfield)

  $(searchfield).slideToggle('fast')
  $(close).toggle()


}


// Navigation for blog-maincategories. make clicked item active
(function(){
    if (document.querySelectorAll(".cat-nav")){
      items = document.querySelectorAll(".cat-nav")
      var lastitem;
      items.forEach(item => {
        if(window.location.href === item.href){
            item.classList.add('active')
        }
        item.addEventListener('click', (event) =>{
          lastitem = event.target
          lastitem.classList.add('active')
          items.forEach(item => {
            if(item !== lastitem){
              item.classList.remove('active')
            }
          })
        })
      })
    }
})()

//Parse post preview content to display tinymce formatting

const parseCont = function(){

  //If there are post_preview elements on the page -> Select all posts
  if(document.querySelector('.post-preview-text')){
    let content = document.getElementsByClassName('post-preview-text');

    for(var i = 0; i < content.length; i++){
      let str = content[i].textContent;
      content[i].innerHTML = str + " ...";
      }

    // Remove all html elements from preview content
      for (var i = 0; i < content.length; i++){
        var childs = content[i].childNodes;
        var newContent = "";
        for( var j = 0; j < childs.length; j++){
            if(childs[j].nodeName === "#text" || childs[j].nodeType === Node.ELEMENT_NODE || childs[j].nodeType === Node.TEXT_NODE){
              if(childs[j].nodeValue){
                newContent  +=  " " + childs[j].nodeValue;
              }
              else{
                newContent += " " + childs[j].innerText;
              }
            }
        };
          content[i].innerHTML = newContent;
          newContent = "";
      };
  };
};

//parse Article content to display tinymce formatting
const parseArticle = function(){
// if there are article elements on the page
    if(document.querySelector('.post_body')){
      let article = document.querySelector('.post_body');
      let cont = article.textContent;
      article.innerHTML = cont;
    };
};

function init(){
  parseCont();
  parseArticle();
};
// if document ready init content parsing
$(document).ready(init);


// ###############  Reply function for Comments ##################

(function(){

//renders reply field

  let renderReplyField = (event) => {

    let comment_id = event.target.dataset.commentid

    var container = document.querySelector('#reply_input'+ event.target.dataset.commentid)

    container.innerHTML = ""

    if(event.target.dataset.id){
      var reply_id = event.target.dataset.id
    }else{
      var reply_id = 0
    }

    let field = `<form id='form${comment_id}' class='form-group'>` +
                    `<label for='name${comment_id}'>Name</label>`+
                    `<input id='name${comment_id}' class='form-control' type='text' name='name' placeholder='Name'/>`+
                    `<small id='hint' class='form-text text-muted'>We'll never share your email with anyone else.</small>`+
                    `<label for='mail${comment_id}'>Email address</label>`+
                    `<input id='mail${comment_id}' class='form-control' type='email' name='email' placeholder='Email' />`+
                    `<label for='body${comment_id}'>Comments</label>`+
                    `<textarea id='body${comment_id}' class='form-control' type='text' rows='6' cols='40' wrap='hard' name='body' placeholder='Your Comment...'></textarea>`+
                    `<input type='checkbox' class='check-input' id='check${comment_id}' name='check'>`+
                    `<label class='form-check-label' for='check${comment_id}'>Save my mail-address and send me updates.</label>`+


                    `<div><button class='btn btn-dark reply_submit_button' data-replyid = '${reply_id}' data-commentid='${comment_id}' type='submit'>Submit</button>`+
                      "<button class='btn btn-dark cancel_request_button ml-2'>Cancel</div>"+
                "</form>"



    if(event.target.dataset.id){
      var render_div = document.querySelector(`#reply_input${event.target.dataset.id}`)
    }else{
      var render_div = document.querySelector(`#reply_input${comment_id}`)
    }

    $(render_div).slideToggle("fast")

    render_div.innerHTML = field

    linkReplySubmitButtons()
    linkCancelRequestButtons()

    //render_div.innerHTML = ""
  }

  // renders new reply

  let renderReply = function (objectarray, container){

    let heading = "<h1> Replies: </h1>"
    container.style.display = 'none'
    container.innerHTML = heading

    for(let i = 0; i < objectarray.length; i++){
      var innerdiv = document.createElement('div')
      let p = document.createElement('p')
      let formdiv = document.createElement('div')
      let cont  = `<h3>Reply from : ${objectarray[i].name}</h3>`+
                      `<p> ${objectarray[i].body}`+
                      `<p><small> ${objectarray[i].date}</small></p>`+
                      "<hr>"

      let button = `<button class='btn btn-dark reply_button' data-commentid = '${objectarray[i].comment_id}' data-id='${objectarray[i].id}' data-parentid='${objectarray[i].parent_id}'>Reply</button>`
      formdiv.innerHTML = `<div id='reply_input${objectarray[i].id}' class='replyformdiv'></div>`
      innerdiv.innerHTML = cont
      innerdiv.classList.add('replyitem')
      p.innerHTML = button
      innerdiv.appendChild(p)
      innerdiv.appendChild(formdiv)
      container.classList.add('replycontainer')
      container.appendChild(innerdiv)

    }
    $(container).slideToggle("fast")
    container.parentElement.parentElement.scrollIntoView(true)
    linkReplyButtons()
  }

  // REnders a new message

  let renderMessage = function (json, container){

    let content = "<div class='alert alert-success' role='alert'>"+
                  "<i class='fa fa-check'></i>"+
                  `${json.message}`+
                  "<p class='text-muted'> It will be added after moderation!</p>"+
                  "</div>"

    container.innerHTML = content
    container.style.display = 'block'
    container.scrollIntoView(false)

  }

//

let removeContent = function(event){
  event.preventDefault()
  element = event.target.parentElement.parentElement
  $(element).slideToggle("fast")
  element.innerHTML = ""
}

let removeReplyContent = function(event){
  container = document.getElementById('reply_div' + event.target.dataset.commentid)
  $(container).slideToggle("fast")
}
// ajax request to add reply to database

let addReplyToDatabase = function (event){
  //event.target.parentElement.parentElement.innerHTML = ""
  event.preventDefault()
  //check if there are any replies allready
  var childs = $(`#reply_div${event.target.dataset.commentid}`).children()
  if(childs.length >= 1){
    var parent_id = event.target.dataset.replyid
  }
  var comment_id = event.target.dataset.commentid
  // set up ajax request
  let form = document.getElementById(`form${comment_id}`)
  let replyJson = {}
  let ajax = new XMLHttpRequest()
  ajax.open('POST', `/newreply`)
  let data = new FormData(form)
  if(parent_id){
    data.append('parent_id', parent_id)
  }
  data.append('comment_id', comment_id)
  ajax.onreadystatechange = function(){
    if(this.readyState === 4 && this.status == 200){

      replyJson = JSON.parse(ajax.responseText);
      let container = document.getElementById(`reply_input${comment_id}`)
      renderMessage(replyJson, container)
    }
  }
  ajax.send(data)
}

//Retrieve comment replies from database
let getReplies = function(event){
  event.preventDefault()
  let comment_id = event.target.dataset.commentid
  var data = {"comment_id" : comment_id}
  let container = document.getElementById(`reply_div${comment_id}`)
  let replies = {}
  let ajax = new XMLHttpRequest
  ajax.overrideMimeType('application/json')
  ajax.open('POST', `/getreplies`)
  ajax.onreadystatechange = function(){
    if(this.readyState === 4 && this.status == 200){
      replies = JSON.parse(ajax.responseText)
      renderReply(replies, container)
    }
  }
  ajax.send(JSON.stringify(data))


}


let toggleShowMoreButton = function (event){
    if(event.target.classList.contains("show_more_button") || event.target.classList.contains("hide_replies_button")){

      $(event.target).toggle()
      if(event.target.classList.contains("show_more_button")){
        $('#hide_replies_button' + event.target.dataset.commentid).toggle()
      }else{
        $('#show_replies_button' + event.target.dataset.commentid).toggle()
      }
      linkHideRepliesButtons()
    }
}
// add eventlisteners to reply buttons

let linkReplyButtons = function (){
  if(document.querySelector('.reply_button')){
    var reply_button = document.querySelectorAll('.reply_button')

    for(let i = 0; i < reply_button.length;i++){
      reply_button[i].addEventListener('click', renderReplyField)
    }
  }
}

let linkReplySubmitButtons = function(){
  if(document.querySelector('.reply_submit_button')){
    var reply_submit_button = document.querySelectorAll('.reply_submit_button')

    for(let i = 0; i < reply_submit_button.length;i++){
      reply_submit_button[i].addEventListener('click', addReplyToDatabase)
    }

  }
}

let linkShowMoreButtons = function(){
  if(document.querySelector('.show_more_button')){
    var showMoreButton = document.querySelectorAll('.show_more_button')
    for(let i = 0; i < showMoreButton.length; i++){
      showMoreButton[i].addEventListener('click', getReplies)
      showMoreButton[i].addEventListener('click', toggleShowMoreButton)
    }
  }
}

let linkHideRepliesButtons = function(){
  if(document.querySelector('.hide_replies_button')){
    var hideRepliesButton = document.querySelectorAll('.hide_replies_button')
    for(let i = 0; i < hideRepliesButton.length; i++){
      hideRepliesButton[i].addEventListener('click', toggleShowMoreButton)
      hideRepliesButton[i].addEventListener('click', removeReplyContent)

    }
  }
}
let linkCancelRequestButtons = function(){
  if(document.querySelector('.cancel_request_button')){
    var cancelRequestButton = document.querySelectorAll('.cancel_request_button')
    for(let i = 0; i < cancelRequestButton.length; i++){
      cancelRequestButton[i].addEventListener('click', removeContent)
    }
  }
}

linkReplyButtons()
linkShowMoreButtons()


})()
